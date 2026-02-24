"""Data loading utilities for Schopenhauer.

Handles loading data from various formats (CSV, YAML, JSON) for use in
document templates.
"""

import csv
import json
from pathlib import Path
from typing import Any

import yaml


class DataLoaderError(Exception):
    """Raised when data loading fails."""


def load_data(path_str: str, base_dir: Path | None = None) -> Any:
    """Load data from a file path.

    Supported formats:
    - .csv: List of dictionaries (one per row)
    - .yaml / .yml: Dictionary or list
    - .json: Dictionary or list

    Args:
        path_str: Path to the data file.
        base_dir: Base directory for resolving relative paths.

    Returns:
        Loaded data as Python objects.

    Raises:
        DataLoaderError: If the file is not found or format is unsupported.
    """
    path = Path(path_str)
    if not path.is_absolute() and base_dir:
        path = base_dir / path

    if not path.is_file():
        raise DataLoaderError(f"Data file not found: {path}")

    suffix = path.suffix.lower()

    try:
        if suffix == ".csv":
            with open(path, encoding="utf-8-sig") as f:
                return list(csv.DictReader(f))
        elif suffix in (".yaml", ".yml"):
            with open(path, encoding="utf-8") as f:
                return yaml.safe_load(f)
        elif suffix == ".json":
            with open(path, encoding="utf-8") as f:
                return json.load(f)
        else:
            raise DataLoaderError(f"Unsupported data format: {suffix}")
    except Exception as exc:
        raise DataLoaderError(f"Failed to load data from {path}: {exc}") from exc


def load_data_map(data_spec: dict[str, str], base_dir: Path | None = None) -> dict[str, Any]:
    """Load multiple data sources into a mapping.

    Args:
        data_spec: Dictionary mapping variable names to file paths.
        base_dir: Base directory for resolving relative paths.

    Returns:
        Dictionary mapping variable names to loaded data objects.
    """
    results = {}
    for key, path in data_spec.items():
        results[key] = load_data(path, base_dir)
    return results
