# Schopenhauer's Will

<p align="center">
  <img src="docs/assets/logo.png" alt="Schopenhauer Logo" width="200" />
</p>

<p align="center">
  <strong>The Will to Document</strong><br>
  A powerful CLI tool and Python library for generating Word documents from YAML/JSON specifications
</p>

<p align="center">
  <a href="https://pypi.org/project/schopenhauer/"><img src="https://img.shields.io/pypi/v/schopenhauer.svg?style=flat-square&color=722F37" alt="PyPI"></a>
  <a href="https://pypi.org/project/schopenhauer/"><img src="https://img.shields.io/pypi/pyversions/schopenhauer.svg?style=flat-square" alt="Python Versions"></a>
  <a href="https://github.com/yanndebray/schopenhauer/blob/main/LICENSE"><img src="https://img.shields.io/github/license/yanndebray/schopenhauer.svg?style=flat-square" alt="License"></a>
  <a href="https://github.com/yanndebray/schopenhauer/actions"><img src="https://img.shields.io/github/actions/workflow/status/yanndebray/schopenhauer/test.yml?style=flat-square" alt="Build Status"></a>
</p>

<p align="center">
  <a href="https://yanndebray.github.io/schopenhauer">Documentation</a> •
  <a href="#installation">Installation</a> •
  <a href="#quick-start">Quick Start</a> •
  <a href="#features">Features</a> •
  <a href="#api">API</a>
</p>

---

## Overview

**Schopenhauer** transforms YAML or JSON specifications into professional Word documents (.docx). Named after the philosopher Arthur Schopenhauer and his work "The World as Will and Representation," this tool embodies the *will* to create beautiful documents programmatically.

### Why Schopenhauer?

- **Version Control Friendly**: Document specs are plain text (YAML/JSON)
- **Reproducible**: Same spec always produces the same output
- **Automatable**: Perfect for CI/CD pipelines and batch processing
- **Customizable**: Full control over styling, templates, and content
- **Cloud Ready**: REST API for microservices and cloud deployment

## Installation

```bash
pip install schopenhauer
```

### Optional Dependencies

```bash
# With REST API server
pip install schopenhauer[api]

# With documentation tools
pip install schopenhauer[docs]

# Everything
pip install schopenhauer[all]
```

## Quick Start

### CLI Usage

```bash
# Create a simple document
will create -o report.docx --title "Annual Report" --author "Jane Doe"

# Generate from YAML specification
will generate spec.yaml -o output.docx

# Initialize a YAML template
will template init report -o my-report.yaml

# Interactive document creation
will new -o document.docx
```

### YAML Specification

Create a file `report.yaml`:

```yaml
title: Quarterly Report
subtitle: Q4 2024 Results
author: Analytics Team

page_size: letter
margins: moderate
table_of_contents: true

sections:
  - type: section
    title: Executive Summary

  - type: content
    text: |
      This report summarizes the key achievements
      and metrics for the fourth quarter.

  - type: content
    title: Key Highlights
    bullets:
      - Revenue increased by 25%
      - Customer satisfaction at all-time high
      - New product launch successful

  - type: table
    title: Performance Metrics
    headers: [Metric, Q3, Q4, Change]
    data:
      - [Revenue, "$1.2M", "$1.5M", "+25%"]
      - [Users, "10K", "15K", "+50%"]
```

Generate the document:

```bash
will generate report.yaml -o quarterly-report.docx
```

### Python API

```python
from will import WordDocument, DocumentBuilder

# Simple approach
doc = WordDocument()
doc.add_title("My Report", subtitle="2024 Edition")
doc.add_heading("Introduction", level=1)
doc.add_paragraph("Welcome to the report.")
doc.add_bullets(["Point 1", "Point 2", "Point 3"])
doc.add_table(
    data=[["Alice", "Engineering"], ["Bob", "Sales"]],
    headers=["Name", "Department"]
)
doc.save("report.docx")

# Fluent builder approach
(DocumentBuilder()
    .set_title("My Report")
    .add_heading("Introduction")
    .add_paragraph("Welcome to the report.")
    .add_bullets(["Point 1", "Point 2"])
    .save("report.docx"))
```

## Features

### Content Types

- **Headings**: Multiple levels (H1-H5) with custom styling
- **Paragraphs**: Rich text with formatting options
- **Lists**: Bullet and numbered lists with nesting
- **Tables**: Data tables with headers and styling
- **Images**: Inline images with captions
- **Quotes**: Blockquotes with attribution
- **Code Blocks**: Formatted code snippets
- **Page Breaks**: Manual page control
- **Table of Contents**: Automatic TOC generation

### Document Features

- **Templates**: Built-in templates for reports, memos, proposals, etc.
- **Placeholders**: `{{PLACEHOLDER}}` syntax for dynamic content
- **Headers/Footers**: Configurable with page numbers
- **Page Setup**: Custom sizes, margins, orientation
- **Styling**: Brand colors, fonts, and formatting

### Deployment Options

- **CLI Tool**: `will` command for terminal usage
- **Python Library**: Full API for programmatic use
- **REST API**: FastAPI server for cloud deployment
- **Docker**: Containerized deployment
- **GCP Cloud Run**: One-click deployment script

## CLI Commands

| Command | Description |
|---------|-------------|
| `will create` | Create a new document |
| `will generate` | Generate from YAML/JSON spec |
| `will inspect` | Inspect document or template |
| `will new` | Interactive document creation |
| `will add` | Add content to existing document |
| `will replace` | Replace placeholders |
| `will template` | Template management |
| `will cloud` | Cloud API commands |

## Templates

Built-in templates for common document types:

- `default` - Clean, professional default
- `report` - Business report with header/footer
- `memo` - Internal memo format
- `letter` - Formal business letter
- `academic` - Academic paper (APA-style)
- `proposal` - Project proposal
- `manual` - Technical documentation
- `contract` - Legal contract format
- And more...

```bash
# List templates
will template list

# Use a template
will create -o doc.docx --template report --title "Report"

# Initialize YAML from template
will template init proposal -o my-proposal.yaml
```

## REST API

Deploy as a REST API for cloud-based document generation:

```bash
# Start the server
uvicorn will.api:app --host 0.0.0.0 --port 8000

# Or with Docker
docker build -t schopenhauer .
docker run -p 8000:8000 schopenhauer
```

### Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/health` | GET | Health check |
| `/templates` | GET | List templates |
| `/generate` | POST | Generate document |
| `/inspect` | POST | Inspect template |
| `/replace` | POST | Replace placeholders |
| `/batch/generate` | POST | Batch generation |

### Example Request

```bash
curl -X POST "http://localhost:8000/generate" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "My Report",
    "sections": [
      {"type": "heading", "title": "Introduction", "level": 1},
      {"type": "content", "text": "Hello, World!"}
    ]
  }' \
  --output report.docx
```

## Cloud Deployment

### GCP Cloud Run

```bash
# Deploy to Cloud Run
./deploy.sh --project my-project --region us-central1

# Build only
./deploy.sh --build-only --local
```

### Docker

```bash
# Build image
docker build -t schopenhauer .

# Run container
docker run -p 8000:8000 schopenhauer

# Access API
curl http://localhost:8000/health
```

## Documentation

Full documentation is available at [schopenhauer.github.io/schopenhauer](https://schopenhauer.github.io/schopenhauer).

### Building Docs Locally

```bash
pip install schopenhauer[docs]
mkdocs serve
```

## Development

### Setup

```bash
# Clone repository
git clone https://github.com/schopenhauer/schopenhauer.git
cd schopenhauer

# Install in development mode
pip install -e ".[dev]"

# Run tests
pytest

# Run linters
black src tests
ruff check src tests
mypy src
```

### Running Tests

```bash
# All tests
pytest

# With coverage
pytest --cov=will --cov-report=html

# Specific test file
pytest tests/test_core.py
```

## Contributing

Contributions are welcome! Please read our [Contributing Guide](CONTRIBUTING.md) for details.

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Named after **Arthur Schopenhauer** (1788-1860), German philosopher
- Built with [python-docx](https://python-docx.readthedocs.io/)
- CLI powered by [Click](https://click.palletsprojects.com/)
- API built with [FastAPI](https://fastapi.tiangolo.com/)

---

<p align="center">
  <sub>The Will to Document</sub><br>
  <sub>Made with ♥ by the Schopenhauer Contributors</sub>
</p>
