# YAML Format Reference

This page documents the complete YAML specification format for generating Word documents with Schopenhauer.

## Basic Structure

```yaml
# Document metadata
title: Document Title
subtitle: Optional Subtitle
author: Author Name

# Page setup
page_size: letter      # letter, legal, a4, a5
margins: normal        # normal, narrow, moderate, wide
template: null         # Path to .docx template file

# Header/Footer
header: "Header Text"
footer: "Footer Text"

# Options
table_of_contents: false
title_page_break: true

# Content sections
sections:
  - type: section
    title: Section Title
  # ... more sections
```

## Document Properties

| Property | Type | Default | Description |
|----------|------|---------|-------------|
| `title` | string | null | Document title |
| `subtitle` | string | null | Document subtitle |
| `author` | string | null | Document author |
| `template` | string | null | Path to .docx template |
| `page_size` | string | "letter" | Page size preset |
| `margins` | string | "normal" | Margin preset |
| `header` | string | null | Header text |
| `footer` | string | null | Footer text |
| `table_of_contents` | boolean | false | Include TOC |
| `title_page_break` | boolean | true | Page break after title |

### Page Sizes

- `letter` - 8.5" x 11" (US Letter)
- `legal` - 8.5" x 14" (US Legal)
- `a4` - 210mm x 297mm (ISO A4)
- `a5` - 148mm x 210mm (ISO A5)

### Margin Presets

- `normal` - 1" all sides
- `narrow` - 0.5" all sides
- `moderate` - 1" top/bottom, 0.75" left/right
- `wide` - 1" top/bottom, 1.5" left/right

## Section Types

### Section Header

Creates a new section with a title:

```yaml
- type: section
  title: Section Title
  subtitle: Optional subtitle
  page_break: false    # Add page break before
```

### Heading

Adds a heading at any level:

```yaml
- type: heading
  title: Heading Text
  level: 1             # 1-5 (default: 1)
```

### Content

General content with optional elements:

```yaml
- type: content
  title: Optional Heading     # Creates heading before content
  level: 2                    # Heading level if title provided
  text: |
    Paragraph text here.
    Can be multiple lines.
  bullets:                    # Bullet list
    - Point 1
    - Point 2
  numbered:                   # Numbered list
    - Step 1
    - Step 2
```

### Table

Data table with headers:

```yaml
- type: table
  title: Table Title          # Optional
  headers:
    - Column 1
    - Column 2
    - Column 3
  data:
    - [Row 1 Col 1, Row 1 Col 2, Row 1 Col 3]
    - [Row 2 Col 1, Row 2 Col 2, Row 2 Col 3]
  column_widths:              # Optional, in inches
    - 2
    - 3
    - 2
```

### Image

Insert an image:

```yaml
- type: image
  path: path/to/image.png     # or use 'image' key
  title: Image Caption        # Optional, shows as caption
  caption: Figure caption     # Alternative to title
  width: 5                    # Width in inches
  height: 3                   # Height in inches (optional)
```

### Quote

Blockquote with optional attribution:

```yaml
- type: quote
  text: The quote text here
  author: Quote Author        # Optional
```

### Code Block

Code or preformatted text:

```yaml
- type: code
  title: Code Example         # Optional
  code: |
    def hello():
        print("Hello, World!")
  language: python            # Optional, for documentation
```

Alternative with `text` key:

```yaml
- type: code
  text: |
    function hello() {
        console.log("Hello!");
    }
```

### Page Break

Insert a page break:

```yaml
- type: page_break
```

### Horizontal Line

Insert a horizontal rule:

```yaml
- type: horizontal_line
```

## Complete Example

```yaml
title: Annual Report 2024
subtitle: Year in Review
author: Executive Team

page_size: letter
margins: moderate

header: "Annual Report 2024"
footer: "Confidential"

table_of_contents: true
title_page_break: true

sections:
  # Executive Summary
  - type: section
    title: Executive Summary

  - type: content
    text: |
      This annual report presents a comprehensive overview of our
      company's performance throughout 2024. We are pleased to report
      significant growth across all key metrics.

  - type: content
    title: Key Achievements
    level: 2
    bullets:
      - Revenue growth of 35% year-over-year
      - Expanded operations to 5 new markets
      - Launched 3 new product lines
      - Achieved record customer satisfaction scores

  # Financial Overview
  - type: section
    title: Financial Overview
    page_break: true

  - type: content
    text: |
      Our financial performance exceeded expectations, driven by
      strong demand and operational efficiency improvements.

  - type: table
    title: Financial Summary
    headers:
      - Metric
      - 2023
      - 2024
      - Change
    data:
      - [Revenue, "$10M", "$13.5M", "+35%"]
      - [Gross Profit, "$6M", "$8.5M", "+42%"]
      - [Operating Income, "$2M", "$3.2M", "+60%"]
      - [Net Income, "$1.5M", "$2.5M", "+67%"]

  # Operations
  - type: section
    title: Operations
    page_break: true

  - type: content
    title: Regional Performance
    level: 2

  - type: table
    headers: [Region, Revenue, Growth]
    data:
      - [North America, "$5M", "+25%"]
      - [Europe, "$4M", "+40%"]
      - [Asia Pacific, "$3M", "+55%"]
      - [Other, "$1.5M", "+30%"]

  - type: image
    path: charts/revenue-by-region.png
    caption: "Figure 1: Revenue Distribution by Region"
    width: 6

  # Strategic Initiatives
  - type: section
    title: Strategic Initiatives
    page_break: true

  - type: content
    numbered:
      - Digital transformation program launched
      - Sustainability initiatives implemented
      - Talent development program expanded
      - Technology infrastructure upgraded

  - type: quote
    text: Our commitment to innovation and customer success drives everything we do.
    author: CEO, Jane Smith

  # Looking Ahead
  - type: section
    title: Looking Ahead
    page_break: true

  - type: content
    text: |
      As we move into 2025, we are focused on sustainable growth
      and continued innovation. Our strategic priorities include:

  - type: content
    bullets:
      - Expand market presence in emerging economies
      - Accelerate product development cycle
      - Strengthen customer relationships
      - Invest in employee development

  - type: horizontal_line

  - type: content
    text: |
      We thank our shareholders, customers, employees, and partners
      for their continued support and trust.
```

## Placeholders

Use `{{PLACEHOLDER}}` syntax for dynamic content:

```yaml
title: Invoice #{{INVOICE_NUMBER}}

sections:
  - type: content
    text: |
      Date: {{DATE}}

      Bill To:
      {{CLIENT_NAME}}
      {{CLIENT_ADDRESS}}

      Amount Due: {{AMOUNT}}
```

Replace placeholders when generating:

```bash
will generate invoice.yaml -o invoice.docx \
    -V INVOICE_NUMBER=INV-001 \
    -V DATE="2024-01-15" \
    -V CLIENT_NAME="Acme Corp" \
    -V CLIENT_ADDRESS="123 Main St" \
    -V AMOUNT="$1,500.00"
```

## Tips and Best Practices

### 1. Use YAML Multi-line Strings

For long text, use the `|` character:

```yaml
text: |
  This is a long paragraph that
  spans multiple lines. The line
  breaks are preserved.
```

### 2. Organize with Sections

Use section types with page breaks for clear organization:

```yaml
- type: section
  title: Chapter 1
  page_break: true
```

### 3. Consistent Heading Levels

Maintain hierarchy with proper heading levels:

```yaml
- type: heading
  title: Main Topic      # level: 1
  level: 1

- type: heading
  title: Subtopic        # level: 2
  level: 2
```

### 4. Table Data as Arrays

Tables use nested arrays for data:

```yaml
data:
  - [Cell 1, Cell 2, Cell 3]  # Row 1
  - [Cell 4, Cell 5, Cell 6]  # Row 2
```

### 5. Relative Image Paths

Use paths relative to the YAML file:

```yaml
- type: image
  path: ./images/chart.png
```
