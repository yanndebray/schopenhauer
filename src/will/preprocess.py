"""Preprocessing engine for Schopenhauer.

Handles variable substitution and template directives in Markdown content
before passing to Pandoc. Uses Jinja2 under the hood with permissive
undefined handling so unresolved variables pass through unchanged.
"""

import logging

from jinja2 import BaseLoader, Environment, Undefined

logger = logging.getLogger(__name__)


class PreprocessError(Exception):
    """Raised when preprocessing fails."""


class _PassthroughUndefined(Undefined):
    """Jinja2 Undefined subclass that renders back to ``{{name}}``."""

    def __str__(self) -> str:
        return "{{" + self._undefined_name + "}}"

    def __iter__(self):
        return iter([])

    def __bool__(self) -> bool:
        return False


def preprocess(content: str, variables: dict | None = None) -> str:
    """Preprocess Markdown content with variable substitution.

    Replaces ``{{var}}`` tokens in *content* with values from *variables*.
    Unresolved tokens are left as-is (passthrough) for backward compatibility.

    Args:
        content: Raw Markdown string (may contain ``{{var}}`` tokens).
        variables: Mapping of variable names to replacement values.

    Returns:
        The processed Markdown string.

    Raises:
        PreprocessError: If Jinja2 rendering fails for a reason other than
            missing variables (e.g. syntax error in a directive).
    """
    if variables is None:
        variables = {}

    # Use Jinja2 with {{ }} delimiters (the default) and passthrough undefined
    env = Environment(
        loader=BaseLoader(),
        undefined=_PassthroughUndefined,
        keep_trailing_newline=True,
    )

    try:
        template = env.from_string(content)
        return template.render(**variables)
    except Exception as exc:
        raise PreprocessError(f"Preprocessing failed: {exc}") from exc
