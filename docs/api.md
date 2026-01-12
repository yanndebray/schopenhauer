# Python API

Schopenhauer provides a comprehensive Python API for programmatic document creation.

## Quick Start

```python
from will import WordDocument, DocumentBuilder

# Simple approach
doc = WordDocument()
doc.add_heading("My Document", level=1)
doc.add_paragraph("Hello, World!")
doc.save("document.docx")

# Fluent builder approach
(DocumentBuilder()
    .set_title("My Document")
    .add_paragraph("Hello, World!")
    .save("document.docx"))
```

## Core Classes

### WordDocument

The main class for creating and manipulating Word documents.

```python
from will import WordDocument

# Create new document
doc = WordDocument()

# Create from template
doc = WordDocument(template="template.docx")

# Create with metadata
doc = WordDocument(
    title="Report Title",
    author="Author Name"
)
```

<!-- Full API reference available in docstrings -->

### DocumentBuilder

Fluent interface for document construction.

```python
from will import DocumentBuilder

builder = DocumentBuilder()
(builder
    .set_title("Report")
    .add_heading("Introduction")
    .add_paragraph("Content here.")
    .add_bullets(["Point 1", "Point 2"])
    .save("report.docx"))
```

<!-- Full API reference available in docstrings -->

## Common Operations

### Adding Headings

```python
doc = WordDocument()

# Title (level 0)
doc.add_heading("Document Title", level=0)

# Section headings
doc.add_heading("Chapter 1", level=1)
doc.add_heading("Section 1.1", level=2)
doc.add_heading("Subsection 1.1.1", level=3)

# With custom color
doc.add_heading("Colored Heading", level=1, color="722F37")
```

### Adding Paragraphs

```python
# Simple paragraph
doc.add_paragraph("This is a paragraph.")

# Formatted paragraph
doc.add_paragraph(
    "Important text",
    bold=True,
    font_size=14,
    color="722F37"
)

# With alignment
from docx.enum.text import WD_ALIGN_PARAGRAPH
doc.add_paragraph(
    "Centered text",
    alignment=WD_ALIGN_PARAGRAPH.CENTER
)
```

### Adding Lists

```python
# Bullet list
doc.add_bullets([
    "First item",
    "Second item",
    "Third item"
])

# Numbered list
doc.add_numbered_list([
    "Step one",
    "Step two",
    "Step three"
])

# Nested lists (with level)
doc.add_bullets(["Main point"], level=0)
doc.add_bullets(["Sub point 1", "Sub point 2"], level=1)
```

### Adding Tables

```python
# Simple table
doc.add_table(
    data=[
        ["Alice", "Engineering", "Senior"],
        ["Bob", "Sales", "Manager"],
    ],
    headers=["Name", "Department", "Title"]
)

# With custom styling
doc.add_table(
    data=data,
    headers=headers,
    header_color="722F37",        # Burgundy header
    alternating_rows=True,         # Zebra striping
    column_widths=[2, 3, 2]       # Inches
)
```

### Adding Images

```python
# Basic image
doc.add_image("chart.png")

# With dimensions and caption
doc.add_image(
    "chart.png",
    width=5,              # inches
    height=3,             # inches (optional, maintains ratio)
    caption="Figure 1: Sales Chart"
)

# Centered
from docx.enum.text import WD_ALIGN_PARAGRAPH
doc.add_image(
    "logo.png",
    width=2,
    alignment=WD_ALIGN_PARAGRAPH.CENTER
)
```

### Special Content

```python
# Blockquote
doc.add_quote(
    "The only thing we have to fear is fear itself.",
    author="Franklin D. Roosevelt"
)

# Code block
doc.add_code_block("""
def hello():
    print("Hello, World!")
""")

# Horizontal line
doc.add_horizontal_line()

# Page break
doc.add_page_break()
```

### Document Structure

```python
# Title with subtitle
doc.add_title("Annual Report", subtitle="2024 Edition")

# Table of contents
doc.add_table_of_contents(
    title="Contents",
    levels=3  # Include H1-H3
)

# Headers and footers
doc.set_header("Company Name - Confidential")
doc.set_footer("", include_page_numbers=True)
```

### Page Setup

```python
# Set page size
doc.set_page_size(preset="a4")
doc.set_page_size(width=8.5, height=11)  # inches

# Set margins
doc.set_margins(preset="narrow")
doc.set_margins(top=1, bottom=1, left=0.75, right=0.75)  # inches
```

### Working with Placeholders

```python
# Find placeholders
placeholders = doc.get_placeholders()
print(placeholders)  # ['NAME', 'DATE', 'AMOUNT']

# Replace placeholders
doc.replace_placeholders({
    "NAME": "John Doe",
    "DATE": "January 15, 2024",
    "AMOUNT": "$1,500.00"
})
```

### Creating from Specifications

```python
# From YAML file
doc = WordDocument.from_yaml("spec.yaml")
doc.save("output.docx")

# From JSON file
doc = WordDocument.from_json("spec.json")

# From dictionary
spec = {
    "title": "My Report",
    "sections": [
        {"type": "heading", "title": "Introduction", "level": 1},
        {"type": "content", "text": "Welcome to the report."}
    ]
}
doc = WordDocument.from_spec(spec)
```

### Document Information

```python
info = doc.get_info()
print(f"Title: {info['title']}")
print(f"Author: {info['author']}")
print(f"Paragraphs: {info['paragraphs']}")
print(f"Tables: {info['tables']}")
print(f"Word count: {info['word_count']}")
print(f"Placeholders: {info['placeholders']}")
```

### Saving Documents

```python
# Save to file
doc.save("document.docx")

# Get as bytes (for web responses, etc.)
doc_bytes = doc.to_bytes()
```

## Styles and Colors

```python
from will import BRAND, COLORS, FONTS

# Access brand colors
print(BRAND['primary'])      # '722F37' (Burgundy)
print(BRAND['accent'])       # 'D4A574' (Gold)

# Use color enum
from will.styles import Colors
color = Colors.PRIMARY.rgb   # RGBColor object

# Font specifications
print(FONTS.HEADING_1.family)  # 'Cambria'
print(FONTS.BODY.size)         # 11 (points)
```

<!-- See will/styles.py for full reference -->

## Templates

```python
from will import list_templates, get_template

# List available templates
for t in list_templates():
    print(f"{t['name']}: {t['description']}")

# Get template configuration
template = get_template("report")
print(template.page_size)   # 'letter'
print(template.margins)     # 'moderate'
```

<!-- See will/templates.py for full reference -->

## Best Practices

### Use Context Manager (Coming Soon)

```python
# Future feature
with WordDocument() as doc:
    doc.add_heading("Title")
    doc.add_paragraph("Content")
# Automatically saves on exit
```

### Chain Operations

```python
# DocumentBuilder allows method chaining
(DocumentBuilder()
    .set_title("Report")
    .set_author("Jane Doe")
    .add_heading("Introduction")
    .add_paragraph("Welcome.")
    .add_bullets(["Point 1", "Point 2"])
    .add_page_break()
    .add_heading("Details")
    .add_paragraph("More content.")
    .save("report.docx"))
```

### Error Handling

```python
from will import WordDocument

try:
    doc = WordDocument(template="nonexistent.docx")
except FileNotFoundError as e:
    print(f"Template not found: {e}")

try:
    doc.add_image("missing.png")
except FileNotFoundError as e:
    print(f"Image not found: {e}")
```

## Advanced Usage

### Access Underlying Document

```python
# Get python-docx Document object
doc = WordDocument()
underlying = doc.doc

# Use python-docx features directly
from docx.shared import Inches
underlying.add_picture("image.png", width=Inches(4))
```

### Custom Styling

```python
from will.styles import Colors, FONTS

# Create heading with custom color
doc.add_heading(
    "Custom Heading",
    level=1,
    color=Colors.ACCENT.value
)

# Access font specifications
font = FONTS.HEADING_1
print(f"Font: {font.family}, Size: {font.size}pt")
```
