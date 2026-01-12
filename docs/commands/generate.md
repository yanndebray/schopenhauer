# will generate

Generate a Word document from a YAML or JSON specification file.

## Synopsis

```bash
will generate SPEC_FILE -o OUTPUT [OPTIONS]
```

## Description

The `generate` command creates a Word document based on a YAML or JSON specification file. This is the most powerful way to create complex documents with full control over structure and content.

## Arguments

| Argument | Description |
|----------|-------------|
| `SPEC_FILE` | Path to YAML (.yaml, .yml) or JSON (.json) specification file |

## Options

| Option | Short | Required | Description |
|--------|-------|----------|-------------|
| `--output` | `-o` | Yes | Output file path (.docx) |
| `--template` | `-t` | No | Template file (.docx) to use as base |
| `--var` | `-V` | No | Variable substitution (KEY=VALUE), can be repeated |

## Examples

### Basic Generation

```bash
will generate report.yaml -o report.docx
```

### With Template

```bash
will generate spec.yaml -o doc.docx --template branded-template.docx
```

### With Variables

```bash
will generate invoice-template.yaml -o invoice.docx \
    -V CLIENT="Acme Corp" \
    -V INVOICE_NUM="INV-001" \
    -V DATE="2024-01-15" \
    -V AMOUNT="$1,500.00"
```

### JSON Specification

```bash
will generate spec.json -o output.docx
```

## Specification Format

### YAML Example

```yaml
title: Quarterly Report
subtitle: Q4 2024
author: Analytics Team

page_size: letter
margins: moderate
table_of_contents: true

sections:
  - type: section
    title: Executive Summary

  - type: content
    text: |
      This report summarizes key findings.

  - type: content
    bullets:
      - Revenue up 25%
      - Customer growth 50%

  - type: table
    headers: [Metric, Value]
    data:
      - [Revenue, "$1.5M"]
      - [Users, "15K"]
```

### JSON Example

```json
{
  "title": "Report",
  "sections": [
    {"type": "heading", "title": "Introduction", "level": 1},
    {"type": "content", "text": "Hello, World!"}
  ]
}
```

## Variables (Placeholders)

Use `{{PLACEHOLDER}}` syntax in your spec:

```yaml
title: "Invoice for {{CLIENT}}"
sections:
  - type: content
    text: "Amount due: {{AMOUNT}}"
```

Replace at generation time:

```bash
will generate spec.yaml -o doc.docx -V CLIENT="Acme" -V AMOUNT="$100"
```

## Output

On success, displays:
- Confirmation message
- Document statistics

```
Generated document: report.docx
  Paragraphs: 15
  Tables: 2
  Word count: 450
```

## See Also

- [YAML Format Reference](../yaml-format.md) - Complete specification format
- [will create](create.md) - Simple document creation
- [will replace](replace.md) - Replace placeholders
