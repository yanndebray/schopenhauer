"""Render pipeline — the main entry point for document generation.

Orchestrates: input detection → spec compilation → frontmatter extraction →
variable preprocessing → Pandoc conversion.
"""

import logging
import re
from pathlib import Path

import yaml

from will.data_loader import DataLoaderError, load_data_map
from will.pandoc_backend import convert as pandoc_convert
from will.pandoc_backend import convert_to_bytes as pandoc_convert_to_bytes
from will.preprocess import preprocess
from will.spec_compiler import compile_spec_file

logger = logging.getLogger(__name__)

# Where Pandoc reference docs are located (relative to the package root).
_TEMPLATES_DIR = Path(__file__).resolve().parent.parent.parent / "templates"

# Regex for YAML frontmatter delimiters (leading ``---``)
_FRONTMATTER_RE = re.compile(r"\A---\n(.*?\n)---\n", re.DOTALL)


class RenderError(Exception):
    """Raised when the render pipeline fails."""


def render(
    source: str | Path | list[str | Path],
    output: str | Path | None = None,
    format: str | None = None,
    template: str | None = None,
    variables: dict | None = None,
    backend: str = "pandoc",
    extra_args: list[str] | None = None,
) -> Path | bytes:
    """Render a document from one or more Markdown or legacy spec files.

    Args:
        source: Path to a ``.md``, ``.yaml``, ``.yml``, or ``.json`` file,
            or a raw Markdown string, or a list of any of these.
        output: Destination file path.  When *None*, raw bytes are returned.
        format: Output format (``docx``, ``pdf``, ``html``, …).
            Inferred from *output* extension when omitted.
        template: Template name (resolved to ``templates/reference-docs/<name>.docx``)
            or an absolute/relative path to a ``.docx`` reference doc.
        variables: Extra variables for ``{{var}}`` substitution.
        backend: ``"pandoc"`` (default) or ``"legacy"`` (python-docx).
        extra_args: Extra arguments passed directly to Pandoc.

    Returns:
        The output ``Path`` when *output* is given, otherwise ``bytes``.

    Raises:
        RenderError: On any failure in the pipeline.
    """
    variables = dict(variables or {})
    extra_args = list(extra_args or [])

    # --- Legacy backend shortcut ---------------------------------------------
    if backend == "legacy":
        if isinstance(source, list):
            raise RenderError("Legacy backend does not support multiple input files.")
        if extra_args:
            logger.warning("Legacy backend does not support extra_args, ignoring.")
        return _render_legacy(source, output, variables)

    # --- Normalize sources to a list -----------------------------------------
    sources = source if isinstance(source, list) else [source]
    all_frontmatter = {}
    body_parts = []
    
    # Track the directory of the first file for relative data paths
    first_file_dir = Path.cwd()
    first_file_found = False

    for s in sources:
        source_path = Path(s) if not isinstance(s, Path) else s
        
        # --- Determine Markdown content --------------------------------------
        if source_path.is_file():
            if not first_file_found:
                first_file_dir = source_path.parent
                first_file_found = True
            
            suffix = source_path.suffix.lower()
            if suffix in (".yaml", ".yml", ".json"):
                markdown = compile_spec_file(source_path)
            else:
                markdown = source_path.read_text(encoding="utf-8")
        elif source_path.suffix and not source_path.is_file():
            raise RenderError(f"Source not found: {s}")
        elif isinstance(s, str):
            markdown = s
        else:
            raise RenderError(f"Source not found: {s}")

        # --- Extract frontmatter ---------------------------------------------
        fm, body = _extract_frontmatter(markdown)
        
        # Merge frontmatter: first one wins for top-level keys, 
        # but 'will' sub-sections are deeply merged where it makes sense.
        for k, v in fm.items():
            if k == "will":
                if "will" not in all_frontmatter:
                    all_frontmatter["will"] = {}
                # Merge 'data' and 'variables'
                for subkey in ("data", "variables"):
                    if subkey in v:
                        if subkey not in all_frontmatter["will"]:
                            all_frontmatter["will"][subkey] = {}
                        all_frontmatter["will"][subkey].update(v[subkey])
                # Other will keys (template, page_size, etc.) - first one wins
                for subkey in v:
                    if subkey not in ("data", "variables") and subkey not in all_frontmatter["will"]:
                        all_frontmatter["will"][subkey] = v[subkey]
            elif k not in all_frontmatter:
                all_frontmatter[k] = v
        
        body_parts.append(body)

    # Combine bodies
    body = "\n\n".join(body_parts)
    frontmatter = all_frontmatter

    # --- Load external data --------------------------------------------------
    will_meta = frontmatter.get("will", {}) or {}
    data_spec = will_meta.get("data", {}) or {}
    
    try:
        loaded_data = load_data_map(data_spec, base_dir=first_file_dir)
    except DataLoaderError as exc:
        raise RenderError(f"Data loading failed: {exc}") from exc

    # --- Merge variables -----------------------------------------------------
    fm_vars = will_meta.get("variables", {}) or {}
    merged_vars = {**fm_vars, **loaded_data, **variables}

    # --- Preprocess ----------------------------------------------------------
    body = preprocess(body, merged_vars)

    # --- Resolve output format -----------------------------------------------
    if format is None and output is not None:
        format = Path(output).suffix.lstrip(".")
    if format is None:
        format = "docx"

    # --- Resolve template / reference doc ------------------------------------
    template_name = template or will_meta.get("template")
    reference_doc = _resolve_template(template_name, format)

    # --- Rebuild full Markdown (frontmatter + processed body) ----------------
    final_md = _rebuild_markdown(frontmatter, body)

    # --- Convert via Pandoc --------------------------------------------------
    try:
        if output is not None:
            return pandoc_convert(
                final_md,
                output_path=output,
                output_format=format,
                reference_doc=reference_doc,
                extra_args=extra_args,
            )
        else:
            return pandoc_convert_to_bytes(
                final_md,
                output_format=format,
                reference_doc=reference_doc,
                extra_args=extra_args,
            )
    except Exception as exc:
        raise RenderError(f"Render failed: {exc}") from exc


# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------

def _extract_frontmatter(markdown: str) -> tuple[dict, str]:
    """Split YAML frontmatter from the Markdown body.

    Returns:
        ``(frontmatter_dict, body_string)``
    """
    # Strip UTF-8 BOM if present (common in files created on Windows)
    if markdown.startswith("\ufeff"):
        markdown = markdown[1:]

    match = _FRONTMATTER_RE.match(markdown)
    if not match:
        return {}, markdown

    raw_fm = match.group(1)
    body = markdown[match.end():]

    try:
        fm = yaml.safe_load(raw_fm) or {}
    except yaml.YAMLError:
        logger.warning("Invalid YAML frontmatter, ignoring")
        fm = {}

    return fm, body


def _resolve_template(name: str | None, format: str) -> Path | None:
    """Map a template *name* to a reference-doc path.

    Resolution order:
    1. If *name* is ``None``, return ``None`` (Pandoc defaults).
    2. If *name* is an existing file path, use it directly.
    3. Look up ``templates/reference-docs/<name>.docx`` (for docx format).
    """
    if name is None:
        return None

    # Direct path?
    p = Path(name)
    if p.is_file():
        return p

    # Only docx templates for now
    if format == "docx":
        candidate = _TEMPLATES_DIR / "reference-docs" / f"{name}.docx"
        if candidate.is_file():
            return candidate

    return None


def _rebuild_markdown(frontmatter: dict, body: str) -> str:
    """Reconstruct Markdown with YAML frontmatter for Pandoc.

    Only standard Pandoc fields are forwarded (title, subtitle, author, date,
    lang, …).  The ``will:`` namespace is stripped because Pandoc doesn't
    understand it.
    """
    # Fields that Pandoc understands natively
    pandoc_keys = {"title", "subtitle", "author", "date", "lang", "abstract", "keywords"}
    pandoc_fm = {k: v for k, v in frontmatter.items() if k in pandoc_keys}

    if pandoc_fm:
        header = "---\n" + yaml.dump(pandoc_fm, default_flow_style=False, allow_unicode=True).rstrip() + "\n---\n\n"
    else:
        header = ""

    return header + body


def _render_legacy(
    source: str | Path,
    output: str | Path | None,
    variables: dict,
) -> Path | bytes:
    """Fallback to the python-docx legacy backend."""
    import json as _json

    from will.core import WordDocument

    source_path = Path(source)
    if source_path.suffix.lower() in (".yaml", ".yml"):
        doc = WordDocument.from_yaml(str(source_path))
    elif source_path.suffix.lower() == ".json":
        doc = WordDocument.from_json(str(source_path))
    else:
        raise RenderError(
            "Legacy backend only supports .yaml/.json specs, not Markdown."
        )

    if variables:
        doc.replace_placeholders(variables)

    if output is not None:
        doc.save(output)
        return Path(output)
    return doc.to_bytes()
