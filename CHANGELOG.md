# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.2.0] - 2026-02-22

### Added
- **Pandoc backend**: Markdown becomes the source of truth, with multi-format output (docx, pdf, html, epub, pptx) via pypandoc
- `will render` CLI command with options: `-o/--output`, `-f/--format` (multiple), `-t/--template`, `-V/--var` (KEY=VALUE), `--backend` (pandoc/legacy)
- `src/will/render.py` — render pipeline: input detection → spec compilation → frontmatter extraction → variable preprocessing → Pandoc conversion
- `src/will/pandoc_backend.py` — thin pypandoc wrapper with format-specific defaults (pdf-engine, embed-resources, standalone)
- `src/will/preprocess.py` — Jinja2-based `{{var}}` substitution with passthrough undefined (unresolved vars remain as-is)
- `src/will/spec_compiler.py` — compiles legacy YAML/JSON specs to Markdown+frontmatter for backward compatibility
- Pandoc defaults files: `templates/defaults/docx.yaml`, `pdf.yaml`, `html.yaml`
- `examples/report.md` — Markdown equivalent of `examples/report.yaml` with YAML frontmatter
- Test suites: `test_render.py`, `test_preprocess.py`, `test_spec_compiler.py`, `test_pandoc_backend.py`

### Changed
- Bumped version to 0.2.0
- `requires-python` raised to `>=3.10`
- Added `pypandoc-binary>=1.15` and `jinja2>=3.0` to dependencies
- Updated keywords and classifiers for multi-format support

### Backward Compatibility
- Legacy `will generate` command and python-docx backend remain fully functional
- Legacy YAML/JSON spec format accepted and compiled to Markdown internally
- Use `--backend legacy` to force the python-docx backend

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

[0.2.0]: https://github.com/yanndebray/schopenhauer/compare/v0.1.1...v0.2.0
[0.1.1]: https://github.com/yanndebray/schopenhauer/compare/v0.1.0...v0.1.1
[0.1.0]: https://github.com/yanndebray/schopenhauer/releases/tag/v0.1.0
