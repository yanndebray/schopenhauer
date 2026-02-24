"""Render pipeline — the main entry point for document generation.

Orchestrates: input detection → spec compilation → frontmatter extraction →
variable preprocessing → Pandoc conversion.
"""

import logging
import re
from pathlib import Path

import yaml

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
    source: str | Path,
    output: str | Path | None = None,
    format: str | None = None,
    template: str | None = None,
    variables: dict | None = None,
    backend: str = "pandoc",
) -> Path | bytes:
    """Render a document from Markdown or a legacy spec file.

    Args:
        source: Path to a ``.md``, ``.yaml``, ``.yml``, or ``.json`` file,
            or a raw Markdown string (detected by the absence of a file
            extension on disk).
        output: Destination file path.  When *None*, raw bytes are returned.
        format: Output format (``docx``, ``pdf``, ``html``, …).
            Inferred from *output* extension when omitted.
        template: Template name (resolved to ``templates/reference-docs/<name>.docx``)
            or an absolute/relative path to a ``.docx`` reference doc.
        variables: Extra variables for ``{{var}}`` substitution.
        backend: ``"pandoc"`` (default) or ``"legacy"`` (python-docx).

    Returns:
        The output ``Path`` when *output* is given, otherwise ``bytes``.

    Raises:
        RenderError: On any failure in the pipeline.
    """
    variables = dict(variables or {})

    # --- Legacy backend shortcut ---------------------------------------------
    if backend == "legacy":
        return _render_legacy(source, output, variables)

    # --- Determine Markdown content ------------------------------------------
    source_path = Path(source) if not isinstance(source, Path) else source

    if source_path.is_file():
        suffix = source_path.suffix.lower()
        if suffix in (".yaml", ".yml", ".json"):
            markdown = compile_spec_file(source_path)
        else:
            markdown = source_path.read_text(encoding="utf-8")
    elif source_path.suffix and not source_path.is_file():
        # Looks like a file path (has extension) but doesn't exist
        raise RenderError(f"Source not found: {source}")
    elif isinstance(source, str):
        # Treat as raw Markdown string
        markdown = source
    else:
        raise RenderError(f"Source not found: {source}")

    # --- Extract frontmatter -------------------------------------------------
    frontmatter, body = _extract_frontmatter(markdown)

    # --- Merge variables -----------------------------------------------------
    will_meta = frontmatter.get("will", {}) or {}
    fm_vars = will_meta.get("variables", {}) or {}
    merged_vars = {**fm_vars, **variables}

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
            )
        else:
            return pandoc_convert_to_bytes(
                final_md,
                output_format=format,
                reference_doc=reference_doc,
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
