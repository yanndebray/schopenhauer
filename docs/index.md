# Schopenhauer's Will

<div class="hero-banner">
  <h1>The Will to Document</h1>
  <p>A powerful CLI tool and Python library for generating Word documents from YAML/JSON specifications</p>
  <span class="version-badge">v0.1.0</span>
</div>

<div class="quick-links">
  <a href="install/">Installation</a>
  <a href="quickstart/">Quick Start</a>
  <a href="commands/">CLI Commands</a>
  <a href="api/">Python API</a>
  <a href="https://github.com/schopenhauer/schopenhauer">GitHub</a>
</div>

## What is Schopenhauer?

**Schopenhauer** is a modern document generation tool that transforms YAML or JSON specifications into professional Word documents (.docx). Named after the philosopher Arthur Schopenhauer and his seminal work "The World as Will and Representation," this tool embodies the *will* to create beautiful documents programmatically.

<div class="feature-grid">
  <div class="feature-card">
    <h3>YAML/JSON Specs</h3>
    <p>Define your document structure in human-readable YAML or JSON format. No need to manually format Word documents.</p>
  </div>
  <div class="feature-card">
    <h3>Powerful CLI</h3>
    <p>The <code>will</code> command provides intuitive commands for creating, generating, and manipulating documents.</p>
  </div>
  <div class="feature-card">
    <h3>Python Library</h3>
    <p>Full Python API for programmatic document creation with fluent builder patterns.</p>
  </div>
  <div class="feature-card">
    <h3>Templates</h3>
    <p>Built-in templates for reports, memos, proposals, and more. Support for custom templates.</p>
  </div>
  <div class="feature-card">
    <h3>REST API</h3>
    <p>FastAPI-powered REST API for cloud-based document generation and microservices integration.</p>
  </div>
  <div class="feature-card">
    <h3>Cloud Ready</h3>
    <p>Docker and GCP Cloud Run deployment support for scalable document generation services.</p>
  </div>
</div>

## Quick Example

### CLI Usage

```bash
# Create a simple document
will create -o report.docx --title "Annual Report" --author "Jane Doe"

# Generate from YAML specification
will generate spec.yaml -o output.docx

# Initialize a YAML template
will template init report -o my-report.yaml
```

### YAML Specification

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

### Python API

```python
from will import WordDocument, DocumentBuilder

# Simple approach
doc = WordDocument()
doc.add_title("My Report", subtitle="2024 Edition")
doc.add_heading("Introduction", level=1)
doc.add_paragraph("Welcome to the report.")
doc.add_bullets(["Point 1", "Point 2", "Point 3"])
doc.save("report.docx")

# Fluent builder approach
(DocumentBuilder()
    .set_title("My Report")
    .add_heading("Introduction")
    .add_paragraph("Welcome to the report.")
    .add_bullets(["Point 1", "Point 2"])
    .save("report.docx"))
```

## Installation

```bash
pip install schopenhauer
```

For additional features:

```bash
# With API server support
pip install schopenhauer[api]

# With documentation tools
pip install schopenhauer[docs]

# Everything
pip install schopenhauer[all]
```

## Why "Schopenhauer"?

The name pays homage to Arthur Schopenhauer (1788-1860), the German philosopher best known for "The World as Will and Representation" (*Die Welt als Wille und Vorstellung*).

In Schopenhauer's philosophy, the **Will** (*Wille*) is the fundamental driving force behind all existence. Similarly, this tool represents the *will* to transform ideas into documents - the driving force that converts your specifications into tangible Word documents.

The CLI command `will` reflects this philosophical foundation, making document generation as natural as willing something into existence.

## Features

- **Multiple Input Formats**: YAML, JSON, or Python dictionaries
- **Rich Content Support**: Headings, paragraphs, lists, tables, images, quotes, code blocks
- **Placeholder System**: `{{PLACEHOLDERS}}` for template-based generation
- **Built-in Templates**: Professional templates for common document types
- **Custom Styling**: Full control over fonts, colors, margins, and layouts
- **Table of Contents**: Automatic TOC generation
- **Headers & Footers**: Configurable with page numbers
- **REST API**: Full-featured API for cloud deployments
- **Batch Processing**: Generate multiple documents in one request

## Getting Started

1. [Install Schopenhauer](install.md)
2. [Follow the Quick Start guide](quickstart.md)
3. [Learn the YAML format](yaml-format.md)
4. [Explore CLI commands](commands/index.md)

## Support

- **GitHub Issues**: [Report bugs and request features](https://github.com/schopenhauer/schopenhauer/issues)
- **Documentation**: You're reading it!
- **Examples**: Check the `examples/` directory in the repository
