"""
Schopenhauer - The Will to Document

A powerful CLI tool and Python library for generating Word documents
from YAML/JSON specifications.

Example:
    >>> from will import WordDocument, DocumentBuilder
    >>> doc = WordDocument()
    >>> doc.add_heading("My Report", level=1)
    >>> doc.add_paragraph("This is the introduction.")
    >>> doc.save("report.docx")

CLI Usage:
    $ will create -o report.docx --title "My Report"
    $ will generate spec.yaml -o report.docx
"""

__version__ = "0.1.0"
__author__ = "Schopenhauer Contributors"

from will.core import WordDocument
from will.document import DocumentBuilder
from will.styles import (
    BRAND,
    FONTS,
    COLORS,
    STYLES,
    MARGINS,
    PAGE_SIZES,
)
from will.templates import (
    get_template,
    list_templates,
    BUILTIN_TEMPLATES,
)

__all__ = [
    # Version
    "__version__",
    # Core classes
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
