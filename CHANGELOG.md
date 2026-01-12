# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

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

[0.1.1]: https://github.com/yanndebray/schopenhauer/compare/v0.1.0...v0.1.1
[0.1.0]: https://github.com/yanndebray/schopenhauer/releases/tag/v0.1.0
