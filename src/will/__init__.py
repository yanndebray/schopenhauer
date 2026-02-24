"""
Schopenhauer - The Will to Document

A CLI tool and Python library for generating professional documents
from Markdown sources.  Uses Pandoc as the rendering engine for
multi-format output (docx, pdf, html, pptx, epub, …).

Example:
    >>> from will import render
    >>> render("report.md", output="report.docx")
    >>> render("report.md", output="report.pdf", format="pdf")

Legacy (python-docx) usage still works:
    >>> from will import WordDocument
    >>> doc = WordDocument()
    >>> doc.add_heading("My Report", level=1)
    >>> doc.save("report.docx")

CLI Usage:
    $ will render report.md -o report.docx
    $ will render report.md -o report.pdf -f pdf
    $ will generate spec.yaml -o report.docx        # legacy
"""

__version__ = "0.2.0"
__author__ = "Schopenhauer Contributors"

from will.core import WordDocument
from will.document import DocumentBuilder
from will.render import render
from will.styles import (
    BRAND,
    COLORS,
    FONTS,
    MARGINS,
    PAGE_SIZES,
    STYLES,
)
from will.templates import (
    BUILTIN_TEMPLATES,
    get_template,
    list_templates,
)

__all__ = [
    # Version
    "__version__",
    # Render pipeline (v0.2+)
    "render",
    # Core classes (legacy)
    "WordDocument",
    "DocumentBuilder",
    # Styles and configuration
    "BRAND",
    "FONTS",
    "COLORS",
    "STYLES",
    "MARGINS",
    "PAGE_SIZES",
    # Templates
    "get_template",
    "list_templates",
    "BUILTIN_TEMPLATES",
]
