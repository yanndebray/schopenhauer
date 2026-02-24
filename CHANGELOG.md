# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.3.0] - 2026-02-23

### Added
- **Data Binding**: Robust data loading from CSV, YAML, and JSON files via `will.data` in frontmatter.
- **MCP Server**: Model Context Protocol server implementation in `src/will/mcp.py` for AI agent integration.
- **Multi-file Input**: Support for rendering multiple files at once (e.g., `will render chapters/*.md`).
- **Pandoc Pass-through**: Support for passing arbitrary arguments directly to Pandoc using the `--` separator.
- **JSON Schema**: Formal specification schema at `schemas/will-spec.schema.json`.
- **Reference Doc Inspector**: `will template inspect` command to debug template styling and font inheritance.
- **Standardized Templates**: 7 built-in reference document templates (default, report, memo, academic, book, manual, proposal).
- **MATLAB Integration**: Example script showing document generation from MATLAB workflows.
- **Pandoc backend**: Markdown as the source of truth, enabling multi-format output (docx, pdf, html, epub, pptx).
- `will render` CLI command with multi-format and template support.
- Jinja2-based preprocessing with passthrough for unresolved variables.

### Changed
- Bumped version to 0.3.0.
- `requires-python` raised to `>=3.10`.
- Added `pypandoc-binary`, `jinja2`, and `fastmcp` to dependencies.

### Backward Compatibility
- Legacy `will generate` command and python-docx backend remain functional.
- Legacy YAML/JSON spec format automatically compiled to Markdown internally.

## [0.1.1] - 2026-01-12

### Added
- Landing page website for schopenhauer.cc
- Burgundy-themed design with scroll animations

### Fixed
- Windows console encoding issues with Rich progress spinners
- YAML parsing for special characters (% symbol)

## [0.1.0] - 2026-01-12

### Added
- Initial release
- `will` CLI tool with commands: create, generate, inspect, add, replace, template
- WordDocument class for programmatic document generation
- DocumentBuilder fluent API
- 15+ built-in templates (report, memo, letter, academic, proposal, etc.)
- YAML/JSON specification support
- Variable substitution with {{PLACEHOLDER}} syntax
- Rich text formatting (bold, italic, underline, code)
- Tables with headers and custom column widths
- Image embedding from local files and URLs
- Block quotes and code blocks
- FastAPI REST API for document generation
- Docker support and GCP Cloud Run deployment
- MkDocs documentation with Material theme

[0.3.0]: https://github.com/yanndebray/schopenhauer/compare/v0.1.1...v0.3.0
[0.1.1]: https://github.com/yanndebray/schopenhauer/compare/v0.1.0...v0.1.1
[0.1.0]: https://github.com/yanndebray/schopenhauer/releases/tag/v0.1.0
