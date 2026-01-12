# CLI Commands

The `will` command-line interface provides powerful tools for creating and manipulating Word documents.

## Overview

```bash
will [OPTIONS] COMMAND [ARGS]...
```

### Global Options

| Option | Description |
|--------|-------------|
| `--version`, `-v` | Show version and exit |
| `--help` | Show help message |

## Commands

| Command | Description |
|---------|-------------|
| [`create`](create.md) | Create a new Word document |
| [`generate`](generate.md) | Generate document from YAML/JSON spec |
| [`inspect`](inspect.md) | Inspect document or template |
| [`new`](new.md) | Interactive document creation |
| [`add`](add.md) | Add content to existing document |
| [`replace`](replace.md) | Replace placeholders in document |
| [`template`](template.md) | Template management commands |
| [`cloud`](cloud.md) | Cloud API commands |

## Quick Reference

### Create Documents

```bash
# Simple document
will create -o report.docx --title "My Report"

# With all options
will create -o report.docx \
    --title "Annual Report" \
    --subtitle "2024" \
    --author "Jane Doe" \
    --template report \
    --page-size letter \
    --margins moderate \
    --header "Company Name" \
    --footer "Confidential"
```

### Generate from Spec

```bash
# From YAML
will generate report.yaml -o output.docx

# With variable substitution
will generate template.yaml -o invoice.docx \
    -V CLIENT="Acme Corp" \
    -V DATE="2024-01-15"

# With template file
will generate spec.yaml -o doc.docx --template base.docx
```

### Inspect Documents

```bash
# Full inspection
will inspect document.docx

# Show placeholders only
will inspect template.docx --placeholders

# JSON output
will inspect document.docx --json
```

### Manage Templates

```bash
# List templates
will template list

# Show template info
will template info report

# Create YAML from template
will template init proposal -o my-proposal.yaml
```

### Add Content

```bash
# Add heading
will add report.docx --heading "New Section" --level 1

# Add paragraph
will add report.docx --paragraph "Additional text"

# Add bullets
will add report.docx -b "Point 1" -b "Point 2"

# Add image
will add report.docx --image chart.png --caption "Figure 1"
```

### Replace Placeholders

```bash
# Replace in document
will replace template.docx NAME="John" DATE="2024-01-15"

# List placeholders
will replace template.docx --list

# Save to new file
will replace template.docx NAME="John" -o filled.docx
```

### Cloud API

```bash
# Check API health
will cloud health --url http://api.example.com

# Generate via API
will cloud generate spec.yaml -o doc.docx --url http://api.example.com
```

## Exit Codes

| Code | Meaning |
|------|---------|
| 0 | Success |
| 1 | General error |
| 2 | Invalid usage/options |

## Environment Variables

| Variable | Description |
|----------|-------------|
| `WILL_API_URL` | Default cloud API URL |
| `WILL_DEFAULT_TEMPLATE` | Default template name |

## Getting Help

Each command has built-in help:

```bash
# General help
will --help

# Command-specific help
will create --help
will generate --help
will template --help
```
