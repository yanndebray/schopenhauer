"""Spec compiler — converts legacy YAML/JSON specs to Markdown.

The legacy spec format (v0.1.x) uses a ``sections`` array to describe
document structure.  This module compiles that format into Markdown with
YAML frontmatter so the rest of the pipeline only needs to deal with
Markdown.
"""

import json
import logging
from pathlib import Path

import yaml

logger = logging.getLogger(__name__)


class SpecCompileError(Exception):
    """Raised when a spec cannot be compiled to Markdown."""


def compile_spec(spec: dict) -> str:
    """Compile a legacy spec dictionary to Markdown with YAML frontmatter.

    Args:
        spec: A document specification dict (as loaded from YAML/JSON).

    Returns:
        A Markdown string with YAML frontmatter.
    """
    parts: list[str] = []

    # --- Build frontmatter ---------------------------------------------------
    fm: dict = {}
    for key in ("title", "subtitle", "author", "date"):
        if key in spec:
            fm[key] = spec[key]

    will_meta: dict = {}
    if spec.get("page_size"):
        will_meta["page_size"] = spec["page_size"]
    if spec.get("margins"):
        will_meta["margins"] = spec["margins"]
    if spec.get("header"):
        will_meta["header"] = spec["header"]
    if spec.get("footer"):
        will_meta["footer"] = spec["footer"]
    if spec.get("table_of_contents"):
        will_meta["table_of_contents"] = True
    if spec.get("template"):
        will_meta["template"] = spec["template"]

    # Support 'will' section in legacy spec for advanced features (data binding, etc.)
    if "will" in spec and isinstance(spec["will"], dict):
        will_meta.update(spec["will"])

    if will_meta:
        fm["will"] = will_meta

    if fm:
        parts.append("---")
        parts.append(yaml.dump(fm, default_flow_style=False, allow_unicode=True).rstrip())
        parts.append("---")
        parts.append("")

    # --- Compile sections -----------------------------------------------------
    for section in spec.get("sections", []):
        md = _compile_section(section)
        if md:
            parts.append(md)

    return "\n".join(parts) + "\n"


def compile_spec_file(path: str | Path) -> str:
    """Load a YAML or JSON spec file and compile to Markdown.

    Args:
        path: Path to a ``.yaml``, ``.yml``, or ``.json`` file.

    Returns:
        Compiled Markdown string.

    Raises:
        SpecCompileError: If the file cannot be read or parsed.
    """
    path = Path(path)
    try:
        text = path.read_text(encoding="utf-8")
    except OSError as exc:
        raise SpecCompileError(f"Cannot read spec file: {exc}") from exc

    try:
        if path.suffix.lower() in (".yaml", ".yml"):
            spec = yaml.safe_load(text)
        else:
            spec = json.loads(text)
    except Exception as exc:
        raise SpecCompileError(f"Cannot parse spec file: {exc}") from exc

    if not isinstance(spec, dict):
        raise SpecCompileError("Spec must be a YAML/JSON object (dict)")

    return compile_spec(spec)


# ---------------------------------------------------------------------------
# Section compilers
# ---------------------------------------------------------------------------

def _compile_section(section: dict) -> str:
    """Compile a single spec section dict to Markdown."""
    section_type = section.get("type", "content")
    compiler = _SECTION_COMPILERS.get(section_type)
    if compiler is None:
        logger.warning("Unknown section type '%s', skipping", section_type)
        return ""
    return compiler(section)


def _heading(sec: dict) -> str:
    level = sec.get("level", 1)
    title = sec.get("title", "")
    prefix = "#" * level
    return f"{prefix} {title}\n"


def _section(sec: dict) -> str:
    parts: list[str] = []
    if sec.get("page_break"):
        parts.append("\\newpage\n")
    title = sec.get("title", "")
    parts.append(f"# {title}\n")
    if sec.get("subtitle"):
        parts.append(f"*{sec['subtitle']}*\n")
    return "\n".join(parts)


def _content(sec: dict) -> str:
    parts: list[str] = []
    if sec.get("title"):
        level = sec.get("level", 2)
        prefix = "#" * level
        parts.append(f"{prefix} {sec['title']}\n")
    if sec.get("text"):
        parts.append(sec["text"].rstrip() + "\n")
    if sec.get("bullets"):
        for item in sec["bullets"]:
            parts.append(f"- {item}")
        parts.append("")
    if sec.get("numbered"):
        for i, item in enumerate(sec["numbered"], 1):
            parts.append(f"{i}. {item}")
        parts.append("")
    return "\n".join(parts)


def _table(sec: dict) -> str:
    parts: list[str] = []
    if sec.get("title"):
        level = sec.get("level", 2)
        prefix = "#" * level
        parts.append(f"{prefix} {sec['title']}\n")

    headers: list[str] = sec.get("headers", [])
    data: list[list] = sec.get("data", [])

    if headers:
        parts.append("| " + " | ".join(str(h) for h in headers) + " |")
        parts.append("| " + " | ".join("---" for _ in headers) + " |")

    for row in data:
        parts.append("| " + " | ".join(str(c) for c in row) + " |")

    parts.append("")
    return "\n".join(parts)


def _image(sec: dict) -> str:
    path = sec.get("path", sec.get("image", ""))
    caption = sec.get("caption", sec.get("title", ""))
    width = sec.get("width")
    md = f"![{caption}]({path})"
    if width:
        md += f"{{ width={width}in }}"
    return md + "\n"


def _quote(sec: dict) -> str:
    text = sec.get("text", "")
    author = sec.get("author")
    parts = [f'> "{text}"']
    if author:
        parts.append(f"> --- {author}")
    parts.append("")
    return "\n".join(parts)


def _code(sec: dict) -> str:
    parts: list[str] = []
    if sec.get("title"):
        level = sec.get("level", 3)
        prefix = "#" * level
        parts.append(f"{prefix} {sec['title']}\n")
    language = sec.get("language", "")
    code = sec.get("code", sec.get("text", ""))
    parts.append(f"```{language}")
    parts.append(code.rstrip())
    parts.append("```\n")
    return "\n".join(parts)


def _page_break(_sec: dict) -> str:
    return "\\newpage\n"


def _horizontal_line(_sec: dict) -> str:
    return "---\n"


_SECTION_COMPILERS = {
    "heading": _heading,
    "section": _section,
    "content": _content,
    "table": _table,
    "image": _image,
    "quote": _quote,
    "code": _code,
    "page_break": _page_break,
    "horizontal_line": _horizontal_line,
}
