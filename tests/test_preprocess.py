"""Tests for the preprocessing engine."""

import pytest

from will.preprocess import PreprocessError, preprocess


class TestPreprocess:
    """Tests for variable substitution."""

    def test_no_variables(self):
        assert preprocess("Hello world") == "Hello world"

    def test_simple_substitution(self):
        result = preprocess("Hello {{name}}", {"name": "World"})
        assert result == "Hello World"

    def test_multiple_variables(self):
        result = preprocess(
            "{{greeting}}, {{name}}!",
            {"greeting": "Hi", "name": "Alice"},
        )
        assert result == "Hi, Alice!"

    def test_unresolved_passthrough(self):
        """Unresolved variables should pass through as {{name}}."""
        result = preprocess("Hello {{unknown}}")
        assert result == "Hello {{unknown}}"

    def test_partial_resolution(self):
        """Resolved vars replaced, unresolved vars kept."""
        result = preprocess(
            "{{resolved}} and {{unresolved}}",
            {"resolved": "YES"},
        )
        assert result == "YES and {{unresolved}}"

    def test_empty_content(self):
        assert preprocess("") == ""

    def test_none_variables(self):
        result = preprocess("Hello {{x}}", None)
        assert result == "Hello {{x}}"

    def test_preserves_markdown(self):
        md = "# Title\n\n**bold** and *italic*\n\n- bullet\n"
        assert preprocess(md) == md

    def test_preserves_trailing_newline(self):
        result = preprocess("line\n", {})
        assert result.endswith("\n")

    def test_numeric_value(self):
        result = preprocess("Year: {{year}}", {"year": 2024})
        assert result == "Year: 2024"
