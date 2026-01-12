# Quick Start

This guide will get you creating Word documents with Schopenhauer in minutes.

## Your First Document

### Using the CLI

The quickest way to create a document is with the `create` command:

```bash
will create -o my-document.docx --title "My First Document"
```

This creates a basic document with a title page. Let's add more options:

```bash
will create -o report.docx \
    --title "Quarterly Report" \
    --subtitle "Q4 2024" \
    --author "Jane Doe" \
    --page-size letter \
    --margins moderate
```

### Using YAML

For more complex documents, use a YAML specification file:

1. Create a file called `report.yaml`:

```yaml
title: Quarterly Report
subtitle: Q4 2024 Results
author: Jane Doe

page_size: letter
margins: moderate
table_of_contents: true

sections:
  - type: section
    title: Executive Summary

  - type: content
    text: |
      This quarter showed significant growth across all key metrics.
      We exceeded our targets and are well-positioned for next year.

  - type: section
    title: Key Metrics
    page_break: true

  - type: table
    headers: [Metric, Target, Actual, Status]
    data:
      - [Revenue, "$1M", "$1.2M", "Exceeded"]
      - [New Customers, "100", "150", "Exceeded"]
      - [Retention, "90%", "92%", "Exceeded"]

  - type: section
    title: Highlights
    page_break: true

  - type: content
    bullets:
      - Launched new product line
      - Expanded to 3 new markets
      - Achieved ISO certification
      - Reduced operating costs by 15%

  - type: section
    title: Next Steps

  - type: content
    numbered:
      - Complete annual planning
      - Hire additional team members
      - Launch marketing campaign
```

2. Generate the document:

```bash
will generate report.yaml -o quarterly-report.docx
```

### Using Python

For programmatic control, use the Python API:

```python
from will import WordDocument

# Create a new document
doc = WordDocument(title="My Report", author="Jane Doe")

# Add content
doc.add_title("Quarterly Report", subtitle="Q4 2024")
doc.add_page_break()

doc.add_heading("Executive Summary", level=1)
doc.add_paragraph(
    "This quarter showed significant growth across all metrics."
)

doc.add_heading("Key Highlights", level=2)
doc.add_bullets([
    "Revenue up 25%",
    "Customer satisfaction improved",
    "New product launched successfully"
])

doc.add_heading("Financial Data", level=2)
doc.add_table(
    data=[
        ["Revenue", "$1.2M", "+20%"],
        ["Expenses", "$800K", "-5%"],
        ["Profit", "$400K", "+45%"],
    ],
    headers=["Metric", "Value", "Change"]
)

# Save the document
doc.save("report.docx")
```

## Using Templates

Schopenhauer includes built-in templates for common document types.

### List Available Templates

```bash
will template list
```

Output:

```
Available Document Templates:

Name          Description                    Page Size
────────────────────────────────────────────────────────
default       Clean, professional default    letter
report        Business report with header    letter
memo          Internal memo format           letter
letter        Formal business letter         letter
academic      Academic paper (APA-style)     letter
proposal      Project proposal template      letter
manual        Technical documentation        letter
contract      Legal contract format          letter
...
```

### Use a Template

```bash
# Create document with a template
will create -o memo.docx --template memo --title "Project Update"

# Initialize a YAML spec from a template
will template init report -o my-report.yaml
```

### YAML Templates

Get a pre-filled YAML specification:

```bash
# List YAML templates
will template list --yaml

# Create from template
will template init proposal -o my-proposal.yaml

# Edit the YAML file, then generate
will generate my-proposal.yaml -o proposal.docx
```

## Interactive Mode

For guided document creation:

```bash
will new -o document.docx
```

This launches an interactive session that prompts you for:

- Document title
- Subtitle
- Author
- Template selection
- Content sections

## Placeholder Replacement

Use `{{PLACEHOLDERS}}` in templates for dynamic content:

1. Create a template with placeholders:

```yaml
title: Invoice for {{CLIENT_NAME}}

sections:
  - type: content
    text: |
      Invoice Number: {{INVOICE_NUMBER}}
      Date: {{DATE}}

      Bill To:
      {{CLIENT_NAME}}
      {{CLIENT_ADDRESS}}
```

2. Generate with replacements:

```bash
will generate invoice-template.yaml -o invoice.docx \
    -V CLIENT_NAME="Acme Corp" \
    -V INVOICE_NUMBER="INV-001" \
    -V DATE="2024-01-15" \
    -V CLIENT_ADDRESS="123 Main St, City"
```

Or replace in an existing document:

```bash
will replace template.docx \
    CLIENT_NAME="Acme Corp" \
    DATE="2024-01-15" \
    -o filled-document.docx
```

## Adding Content to Existing Documents

Add content to an existing document:

```bash
# Add a heading
will add report.docx --heading "New Section" --level 1

# Add a paragraph
will add report.docx --paragraph "Additional content here."

# Add bullet points
will add report.docx -b "Point 1" -b "Point 2" -b "Point 3"

# Add an image
will add report.docx --image chart.png --caption "Figure 1: Sales Chart"

# Add a page break
will add report.docx --page-break
```

## Inspect Documents

View information about a document:

```bash
# Full inspection
will inspect document.docx

# Show only placeholders
will inspect template.docx --placeholders

# Show available styles
will inspect document.docx --styles

# JSON output
will inspect document.docx --json
```

## Common Workflows

### Generate Report from Data

```python
from will import WordDocument
import json

# Load your data
with open("data.json") as f:
    data = json.load(f)

# Create document
doc = WordDocument(title=data["report_name"])
doc.add_title(data["report_name"])

for section in data["sections"]:
    doc.add_heading(section["title"], level=1)
    doc.add_paragraph(section["content"])

    if "metrics" in section:
        doc.add_table(
            data=[[m["name"], m["value"]] for m in section["metrics"]],
            headers=["Metric", "Value"]
        )

doc.save("report.docx")
```

### Batch Generate Documents

```python
import yaml
from will import WordDocument

# Load template spec
with open("template.yaml") as f:
    template = yaml.safe_load(f)

# Generate for each client
clients = ["Acme Corp", "Beta Inc", "Gamma LLC"]

for client in clients:
    doc = WordDocument.from_spec(template)
    doc.replace_placeholders({"CLIENT_NAME": client})
    doc.save(f"{client.lower().replace(' ', '-')}-report.docx")
```

## Next Steps

- [YAML Format Reference](yaml-format.md) - Complete specification format
- [CLI Commands](commands/index.md) - All available commands
- [Python API](api.md) - Full API documentation
- [Cookbook](cookbook.md) - Common recipes and examples
