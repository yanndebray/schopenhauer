# Installation

## Requirements

- Python 3.9 or higher
- pip (Python package manager)

## Quick Install

The simplest way to install Schopenhauer is via pip:

```bash
pip install schopenhauer
```

This installs the core package with all essential dependencies for document generation.

## Installation Options

### Core Installation

Basic installation with document generation capabilities:

```bash
pip install schopenhauer
```

**Includes:**

- `python-docx` - Word document manipulation
- `click` - CLI framework
- `rich` - Beautiful terminal output
- `pyyaml` - YAML parsing
- `pillow` - Image handling
- `httpx` - HTTP client
- `jinja2` - Template engine

### With API Server

Install with FastAPI server support for cloud deployment:

```bash
pip install schopenhauer[api]
```

**Additional packages:**

- `fastapi` - Web framework
- `uvicorn` - ASGI server
- `python-multipart` - File upload handling

### With Documentation Tools

Install with documentation generation tools:

```bash
pip install schopenhauer[docs]
```

**Additional packages:**

- `mkdocs` - Documentation generator
- `mkdocs-material` - Material theme
- `mkdocstrings` - API documentation

### Development Installation

Install with all development dependencies:

```bash
pip install schopenhauer[dev]
```

**Additional packages:**

- `pytest` - Testing framework
- `pytest-cov` - Coverage reporting
- `black` - Code formatter
- `ruff` - Linter
- `mypy` - Type checking
- `pre-commit` - Git hooks

### Full Installation

Install everything:

```bash
pip install schopenhauer[all]
```

## Verify Installation

After installation, verify that the `will` command is available:

```bash
will --version
```

Expected output:

```
Schopenhauer's Will version 0.1.0
Primary color: Burgundy
```

## Installing from Source

For the latest development version:

```bash
# Clone the repository
git clone https://github.com/schopenhauer/schopenhauer.git
cd schopenhauer

# Install in development mode
pip install -e ".[dev]"
```

## Virtual Environment (Recommended)

We recommend using a virtual environment to avoid conflicts with other packages:

=== "venv"

    ```bash
    # Create virtual environment
    python -m venv .venv

    # Activate (Linux/macOS)
    source .venv/bin/activate

    # Activate (Windows)
    .venv\Scripts\activate

    # Install
    pip install schopenhauer
    ```

=== "conda"

    ```bash
    # Create conda environment
    conda create -n schopenhauer python=3.11

    # Activate
    conda activate schopenhauer

    # Install
    pip install schopenhauer
    ```

=== "uv"

    ```bash
    # Create and install with uv
    uv venv
    source .venv/bin/activate  # or .venv\Scripts\activate on Windows
    uv pip install schopenhauer
    ```

## Upgrading

To upgrade to the latest version:

```bash
pip install --upgrade schopenhauer
```

## Uninstalling

To remove Schopenhauer:

```bash
pip uninstall schopenhauer
```

## Troubleshooting

### Command not found

If `will` is not found after installation, ensure your Python scripts directory is in your PATH:

```bash
# Find where pip installs scripts
python -m site --user-base
```

Add the `bin` (Linux/macOS) or `Scripts` (Windows) subdirectory to your PATH.

### Import errors

If you encounter import errors, try reinstalling with all dependencies:

```bash
pip uninstall schopenhauer
pip install schopenhauer --no-cache-dir
```

### Permission errors

On Linux/macOS, if you get permission errors:

```bash
pip install --user schopenhauer
```

Or use a virtual environment (recommended).

## Next Steps

- [Quick Start Guide](quickstart.md) - Create your first document
- [CLI Commands](commands/index.md) - Learn all available commands
- [YAML Format](yaml-format.md) - Master the specification format
