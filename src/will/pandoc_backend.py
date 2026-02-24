"""Pandoc backend — thin wrapper around pypandoc.

All actual document rendering goes through Pandoc.  This module provides
a clean interface for the rest of Schopenhauer to call into Pandoc without
knowing the details of pypandoc's API.
"""

import logging
import tempfile
from pathlib import Path

import pypandoc

logger = logging.getLogger(__name__)


class PandocBackendError(Exception):
    """Raised when a Pandoc conversion fails."""


# Format aliases: map short names to Pandoc format identifiers
_FORMAT_ALIASES: dict[str, str] = {
    "docx": "docx",
    "pdf": "pdf",
    "html": "html",
    "pptx": "pptx",
    "epub": "epub",
    "latex": "latex",
    "tex": "latex",
    "odt": "odt",
    "rtf": "rtf",
    "md": "markdown",
    "markdown": "markdown",
}


def _resolve_format(fmt: str) -> str:
    return _FORMAT_ALIASES.get(fmt.lower(), fmt)


def convert(
    source: str,
    output_path: str | Path,
    output_format: str = "docx",
    reference_doc: str | Path | None = None,
    extra_args: list[str] | None = None,
    metadata: dict | None = None,
) -> Path:
    """Convert a Markdown string to the target format via Pandoc.

    Args:
        source: Markdown content (string).
        output_path: Destination file path.
        output_format: Target format (``docx``, ``pdf``, ``html``, etc.).
        reference_doc: Path to a Pandoc reference doc (``.docx``).
        extra_args: Additional CLI arguments forwarded to Pandoc.
        metadata: Key-value metadata pairs passed via ``-M key=value``.

    Returns:
        The resolved output ``Path``.

    Raises:
        PandocBackendError: If Pandoc returns a non-zero exit code.
    """
    output_path = Path(output_path)
    fmt = _resolve_format(output_format)

    args: list[str] = list(extra_args or [])
    args.append("--standalone")

    # Format-specific defaults
    if fmt == "pdf":
        if not any(a.startswith("--pdf-engine") for a in args):
            args.append("--pdf-engine=xelatex")
    if fmt == "html":
        if not any(a.startswith("--self-contained") or a == "--embed-resources" for a in args):
            args.append("--embed-resources")

    if reference_doc:
        args.extend(["--reference-doc", str(reference_doc)])

    if metadata:
        for key, value in metadata.items():
            args.extend(["-M", f"{key}={value}"])

    try:
        pypandoc.convert_text(
            source,
            fmt,
            format="markdown",
            outputfile=str(output_path),
            extra_args=args,
        )
    except RuntimeError as exc:
        raise PandocBackendError(f"Pandoc conversion failed: {exc}") from exc

    return output_path


def convert_to_bytes(
    source: str,
    output_format: str = "docx",
    reference_doc: str | Path | None = None,
    extra_args: list[str] | None = None,
    metadata: dict | None = None,
) -> bytes:
    """Convert Markdown to the target format and return raw bytes.

    Same parameters as :func:`convert` but returns ``bytes`` instead of
    writing to a file.
    """
    suffix = f".{output_format}" if not output_format.startswith(".") else output_format
    with tempfile.NamedTemporaryFile(suffix=suffix, delete=False) as tmp:
        tmp_path = Path(tmp.name)

    try:
        convert(
            source,
            tmp_path,
            output_format=output_format,
            reference_doc=reference_doc,
            extra_args=extra_args,
            metadata=metadata,
        )
        return tmp_path.read_bytes()
    finally:
        tmp_path.unlink(missing_ok=True)


def get_pandoc_version() -> str:
    """Return the Pandoc version string."""
    return pypandoc.get_pandoc_version()


def get_supported_formats() -> dict[str, list[str]]:
    """Return a dict with ``input`` and ``output`` format lists."""
    return {
        "input": pypandoc.get_pandoc_formats()[0],
        "output": pypandoc.get_pandoc_formats()[1],
    }
