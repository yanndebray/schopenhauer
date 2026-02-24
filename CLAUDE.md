# CLAUDE.md — Schopenhauer

> This file guides Claude Code when working on the Schopenhauer project.
> It describes the current state, the target architecture, and the migration path.

## Project Identity

**Schopenhauer** — "The Will to Document"
A CLI tool and Python library for generating professional documents from Markdown sources.
Part of the philosopher-named tools ecosystem (nietzsche.cc, montaigne.cc, ricoeur.cc).

- **Package name:** `schopenhauer`
- **CLI command:** `will`
- **Website:** schopenhauer.cc
- **PyPI:** `pip install schopenhauer`
- **License:** MIT

## Architecture Transition

### Where we are (v0.1.x — Legacy)

The current implementation uses python-docx to render YAML/JSON specs into .docx files.
This approach is being **retired**. Do not add features to the python-docx backend.

```
YAML spec → python-docx → .docx only
```

Key legacy files (to be replaced):
- `src/will/` — current python-docx based engine
- YAML spec format with `sections:` array defining document structure
- `WordDocument` class and `DocumentBuilder` fluent API
- Direct style manipulation via python-docx

### Where we're going (v0.2+ — Pandoc Backend)

Markdown becomes the source of truth. Schopenhauer becomes an orchestration layer
on top of Pandoc (via pypandoc_binary), similar to how Quarto wraps Pandoc for
scientific publishing — but optimized for programmatic and AI-agent use cases.

```
Markdown + YAML frontmatter
        ↓
  Schopenhauer (preprocessing: data binding, template resolution, includes)
        ↓
  Pandoc (via pypandoc_binary)
        ↓
  .docx / .pdf / .html / .pptx / .epub / .latex
```

### Core Principle

**Schopenhauer does not render documents. Pandoc renders documents.**
Schopenhauer owns: the spec format, preprocessing, templates, data binding, CLI, API, and MCP server.
Pandoc owns: parsing Markdown, applying styles, producing output files.

---

## Target Architecture (v0.2)

### Source Format: Markdown with YAML Frontmatter

The canonical input is a `.md` file with YAML frontmatter. This is the source of truth.

```markdown
---
title: "Quarterly Report"
subtitle: "Q4 2024 Results"
author: "Analytics Team"
date: "2024-12-15"
will:
  template: report
  output:
    - docx
    - pdf
  data:
    metrics: data/q4_metrics.csv
  variables:
    quarter: Q4
    year: 2024
---

# Executive Summary

This report covers **{{quarter}} {{year}}** performance across all divisions.

# Key Metrics

{{table:metrics, columns=[Metric, Value, Change]}}

# Team Updates

{{for member in team}}
## {{member.name}} — {{member.role}}

{{member.summary}}
{{endfor}}
```

**Design decisions:**
- Standard YAML frontmatter for Pandoc-native fields (title, author, date, etc.)
- `will:` namespace in frontmatter for Schopenhauer-specific config (template, output formats, data sources, variables)
- `{{variable}}` syntax for simple variable substitution (preprocessed before Pandoc)
- `{{table:source}}`, `{{for}}`, `{{if}}` for data binding directives (preprocessed before Pandoc)
- Raw Markdown passes through to Pandoc unchanged — any valid Pandoc Markdown works

### YAML Spec Compatibility Layer

The legacy YAML spec format is still accepted but compiled to Markdown internally.
This is important for backward compatibility and for AI agents that emit structured JSON/YAML.

```bash
# These are equivalent:
will render report.md -o report.docx
will render spec.yaml -o report.docx       # compiled to markdown first
echo '{"title":"Report",...}' | will render --stdin -o report.docx
```

A JSON Schema is published for both the YAML spec format and the frontmatter schema
so LLMs can validate specs before submission.

### Directory Structure (Target)

```
schopenhauer/
├── CLAUDE.md                    # This file
├── README.md
├── pyproject.toml
├── LICENSE
├── Dockerfile
├── deploy.sh
├── mkdocs.yml
│
├── src/will/
│   ├── __init__.py              # Public API: render(), convert(), Document class
│   ├── cli.py                   # Click CLI (will command)
│   ├── render.py                # Core render pipeline: preprocess → pandoc → output
│   ├── preprocess.py            # Data binding, variable substitution, includes, loops
│   ├── pandoc_backend.py        # pypandoc wrapper, filter management, format options
│   ├── templates.py             # Template registry: resolve names → reference docs
│   ├── spec_compiler.py         # YAML/JSON spec → Markdown compiler (compat layer)
│   ├── schema.py                # JSON Schema definitions for spec + frontmatter
│   ├── api.py                   # FastAPI REST API (format-agnostic)
│   ├── mcp.py                   # MCP server (generate, inspect, list_templates, convert)
│   └── filters/                 # Lua filters for Pandoc
│       ├── callouts.lua
│       └── branded.lua
│
├── templates/                   # Pandoc reference documents and templates
│   ├── reference-docs/          # .docx reference templates for Pandoc
│   │   ├── default.docx
│   │   ├── report.docx
│   │   ├── memo.docx
│   │   ├── letter.docx
│   │   ├── academic.docx
│   │   ├── proposal.docx
│   │   └── contract.docx
│   ├── latex/                   # LaTeX templates for PDF output
│   │   └── report.tex
│   ├── html/                    # HTML templates/themes
│   │   └── default.html
│   └── defaults/                # Pandoc defaults YAML files
│       ├── docx.yaml
│       ├── pdf.yaml
│       └── html.yaml
│
├── schemas/                     # Published JSON Schemas
│   ├── frontmatter.schema.json  # Schema for YAML frontmatter
│   └── spec.schema.json         # Schema for YAML/JSON spec (compat)
│
├── examples/
│   ├── report.md                # Example: Markdown source document
│   ├── report-spec.yaml         # Example: Legacy YAML spec
│   ├── data/                    # Example data files
│   └── multi-format/            # Example: one source → multiple outputs
│
├── tests/
│   ├── test_render.py
│   ├── test_preprocess.py
│   ├── test_spec_compiler.py
│   ├── test_templates.py
│   ├── test_cli.py
│   ├── test_api.py
│   └── fixtures/
│
├── docs/                        # MkDocs documentation
│   ├── index.md
│   ├── getting-started.md
│   ├── markdown-format.md
│   ├── templates.md
│   ├── data-binding.md
│   ├── multi-format.md
│   ├── api-reference.md
│   ├── mcp-server.md
│   └── migration-from-v01.md
│
└── website/                     # Landing page (schopenhauer.cc)
```

---

## Migration Path

### Phase 1: Pandoc Backend (v0.2.0)

**Goal:** Add pypandoc as a rendering backend. Markdown in, multi-format out. Keep legacy working.

1. Add `pypandoc_binary` to dependencies in pyproject.toml
2. Create `src/will/pandoc_backend.py`:
   - Thin wrapper around pypandoc
   - Accepts a Markdown string + frontmatter dict → renders to target format
   - Manages reference doc paths, Pandoc options, filters
3. Create `src/will/render.py`:
   - `render(source: str | Path, output: str | Path, format: str = "docx")`
   - Detects input type (.md vs .yaml/.json)
   - For .md: extract frontmatter, preprocess, pass to pandoc_backend
   - For .yaml/.json: compile to markdown first (spec_compiler), then same pipeline
4. Create `src/will/preprocess.py`:
   - Variable substitution: `{{var}}` → resolved value
   - Start simple, expand later
5. Create initial reference docs in `templates/reference-docs/`:
   - Start with `default.docx` — create a clean Word template with heading styles, etc.
   - Can use pandoc itself to generate a starter: `pandoc -o default.docx --print-default-data-file reference.docx`
6. Add CLI commands:
   - `will render <input> -o <output> -f <format>` (new primary command)
   - Keep `will generate` as alias pointing to render
7. Tests:
   - Test that a simple .md file renders to .docx via pandoc
   - Test that the same .md renders to .pdf, .html
   - Test that a legacy .yaml spec still renders (via compilation to markdown)

**Key dependency change in pyproject.toml:**
```toml
dependencies = [
    "click>=8.0",
    "pyyaml>=6.0",
    "pypandoc-binary>=1.13",    # replaces python-docx
    "jinja2>=3.0",              # for preprocessing
]
```

**Do not remove python-docx yet.** Keep the old backend available via `--backend legacy` flag during this phase.

### Phase 2: Data Binding & Templates (v0.2.x)

**Goal:** The features that differentiate Schopenhauer from raw Pandoc.

1. Expand `preprocess.py` with Jinja2-powered preprocessing:
   - `{{for item in collection}}...{{endfor}}` — loop over data
   - `{{if condition}}...{{endif}}` — conditional sections
   - `{{include "path/to/section.md"}}` — file includes
   - `{{table:data_source, columns=[...]}}` — auto-generate Markdown tables from CSV/JSON
2. Data source loading:
   - CSV files → list of dicts
   - JSON files → parsed objects
   - YAML files → parsed objects
   - Later: URL fetching, database queries
3. Template system overhaul:
   - `will template list` — shows available templates with descriptions
   - `will template init <name> -o doc.md` — scaffolds a .md file with frontmatter
   - `will template create` — creates a new reference doc from an existing .docx
   - Templates resolve by name: `template: report` → finds `templates/reference-docs/report.docx`
4. Pandoc defaults files:
   - Each output format has a defaults YAML file (e.g., `templates/defaults/docx.yaml`)
   - Templates can override defaults
   - User can provide their own defaults

### Phase 3: Remove Legacy Backend (v0.3.0)

**Goal:** Clean break. python-docx is gone.

1. Remove all python-docx code from `src/will/`
2. Remove `python-docx` from dependencies
3. Remove `--backend` flag
4. Update all examples to use Markdown format
5. Publish migration guide in docs (`docs/migration-from-v01.md`)
6. The YAML/JSON spec input still works (via spec_compiler) but is documented as
   "programmatic input format" rather than the primary authoring format

### Phase 4: Agent Interface & MCP (v0.4.0)

**Goal:** Purpose-built for AI agents and automation.

1. MCP Server (`src/will/mcp.py`):
   - `generate_document` — accepts spec or markdown, returns rendered file
   - `list_templates` — returns available templates with schemas
   - `inspect_document` — reads an existing document, returns structure
   - `convert_format` — converts between formats via Pandoc
   - `get_schema` — returns JSON Schema for spec format
2. JSON Schema publication:
   - `schemas/frontmatter.schema.json` — validates YAML frontmatter
   - `schemas/spec.schema.json` — validates YAML/JSON specs
   - Schemas are versioned and published with the package
3. Stdin/stdout pipeline support:
   - `echo "# Hello" | will render -f docx > hello.docx`
   - `cat spec.json | will render --stdin -f pdf > report.pdf`
4. REST API updates:
   - All endpoints become format-agnostic
   - New `/convert` endpoint for format conversion
   - OpenAPI schema auto-generated from Pydantic models

---

## CLI Reference (Target)

```bash
# Primary commands
will render <input> -o <output>          # Render .md or .yaml to output format
will render <input> -f docx -f pdf       # Multi-format output
will render --stdin -f docx > out.docx   # Pipe mode

# Template management
will template list                        # List available templates
will template init <name> -o doc.md       # Scaffold a new document
will template create <name> <file.docx>   # Register a .docx as a reference template
will template info <name>                 # Show template details

# Conversion (Pandoc passthrough)
will convert <input> -f <format> -o <output>

# Inspection
will inspect <file>                       # Show document structure

# Server modes
will serve                                # Start REST API server
will mcp                                  # Start MCP server

# Utilities
will schema                               # Print JSON Schema for spec format
will schema --frontmatter                  # Print JSON Schema for frontmatter
```

## Python API (Target)

```python
from will import render, Document

# Simple render
render("report.md", output="report.docx")
render("report.md", output="report.pdf", format="pdf")

# From string
doc = Document("""
---
title: My Report
will:
  template: report
---
# Introduction
Hello world.
""")
doc.render("report.docx")
doc.render("report.pdf")

# From YAML spec (backward compat)
render("spec.yaml", output="report.docx")

# Programmatic construction
doc = Document()
doc.frontmatter(title="My Report", template="report")
doc.heading("Introduction", level=1)
doc.paragraph("Hello world.")
doc.render("report.docx")
```

---

## Development Commands

```bash
# Setup
pip install -e ".[dev]"

# Tests
pytest                                    # All tests
pytest --cov=will --cov-report=html       # With coverage
pytest tests/test_render.py               # Specific file

# Linting
black src tests
ruff check src tests
mypy src

# Docs
pip install -e ".[docs]"
mkdocs serve                              # Local docs server

# Build
python -m build                           # Build package
```

## Code Style

- Python 3.10+
- Black formatter, Ruff linter, mypy for type checking
- Type hints on all public functions
- Docstrings on all public functions (Google style)
- Tests for every public function
- No print statements — use `logging` or `click.echo` in CLI

## Key Design Decisions

1. **Markdown is the source of truth.** All roads lead to Markdown. YAML specs compile to Markdown.
   Programmatic API builds Markdown. The rendering pipeline always starts with Markdown.

2. **Pandoc does the rendering.** We never write format-specific rendering code.
   If Pandoc can't do it, we add a Lua filter. If a Lua filter can't do it, we preprocess the Markdown.

3. **Preprocessing happens before Pandoc.** Data binding, variable substitution, includes, loops —
   all resolved to plain Markdown before Pandoc sees it. Pandoc receives clean, standard Markdown.

4. **Templates are Pandoc reference documents.** A "template" in Schopenhauer is a combination of:
   a Pandoc reference doc (for docx), a defaults YAML (for Pandoc options), and optionally a
   LaTeX/HTML template. We don't invent our own template format.

5. **pypandoc_binary for zero-config.** Users should not need to install Pandoc separately.
   The `pypandoc_binary` package bundles Pandoc. This is a hard requirement.

6. **Backward compatibility via compilation.** The YAML/JSON spec format is supported indefinitely
   by compiling it to Markdown. No user is left behind, but new docs should be Markdown.

7. **Agent-friendly by design.** JSON Schema for all inputs. Stdin/stdout piping. MCP server.
   REST API. Every interface an AI agent might need.

## What NOT to Do

- **Do not** add python-docx code or direct document manipulation
- **Do not** write format-specific rendering logic (that's Pandoc's job)
- **Do not** invent new Markdown syntax — use standard Pandoc Markdown extensions
- **Do not** require Pandoc to be installed separately (use pypandoc_binary)
- **Do not** break the legacy YAML spec input (compile it to Markdown instead)
- **Do not** add heavy dependencies — keep the core light (pypandoc, jinja2, click, pyyaml)

## Reference

- [Pandoc User's Guide](https://pandoc.org/MANUAL.html)
- [pypandoc](https://github.com/JessicaTegner/pypandoc)
- [Pandoc Reference Docs](https://pandoc.org/MANUAL.html#option--reference-doc)
- [Pandoc Lua Filters](https://pandoc.org/lua-filters.html)
- [Pandoc Defaults Files](https://pandoc.org/MANUAL.html#defaults-files)
- [Quarto](https://quarto.org) — inspiration for the architecture (Pandoc orchestration layer)
- [Jinja2](https://jinja.palletsprojects.com/) — template engine for preprocessing
