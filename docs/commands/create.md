# will create

Create a new Word document with optional title, subtitle, and author.

## Synopsis

```bash
will create -o OUTPUT [OPTIONS]
```

## Description

The `create` command creates a new Word document with a title page. This is the simplest way to start a new document from the command line.

## Options

| Option | Short | Required | Description |
|--------|-------|----------|-------------|
| `--output` | `-o` | Yes | Output file path (.docx) |
| `--title` | `-t` | No | Document title |
| `--subtitle` | `-s` | No | Document subtitle |
| `--author` | `-a` | No | Document author |
| `--template` | | No | Template file or built-in name |
| `--page-size` | | No | Page size (letter, legal, a4, a5) |
| `--margins` | | No | Margins preset (normal, narrow, moderate, wide) |
| `--header` | | No | Header text |
| `--footer` | | No | Footer text |
| `--page-numbers` | | No | Include page numbers (default: true) |
| `--no-page-numbers` | | No | Exclude page numbers |

## Examples

### Basic Document

```bash
will create -o report.docx --title "My Report"
```

### Complete Document

```bash
will create -o report.docx \
    --title "Annual Report" \
    --subtitle "Fiscal Year 2024" \
    --author "Jane Doe" \
    --page-size letter \
    --margins moderate \
    --header "Acme Corp" \
    --footer "Confidential"
```

### Using a Template

```bash
# Built-in template
will create -o memo.docx --template memo --title "Project Update"

# Custom template file
will create -o doc.docx --template /path/to/template.docx --title "Report"
```

### A4 Page Size

```bash
will create -o report.docx --title "Report" --page-size a4
```

### No Page Numbers

```bash
will create -o doc.docx --title "Letter" --no-page-numbers
```

## Output

On success, displays:
- Confirmation message
- Document properties (title, author, page size, margins)

```
Created document: report.docx
Property        Value
────────────────────────────
Title           Annual Report
Author          Jane Doe
Page Size       letter
Margins         moderate
```

## See Also

- [will generate](generate.md) - Generate from YAML/JSON spec
- `will new` - Interactive document creation
- `will template` - Template management
