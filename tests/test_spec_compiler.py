"""Tests for the spec compiler (legacy YAML/JSON → Markdown)."""

import json
import os
import tempfile

import pytest

from will.spec_compiler import SpecCompileError, compile_spec, compile_spec_file


class TestCompileSpec:
    """Tests for compile_spec()."""

    def test_minimal_spec(self):
        md = compile_spec({"title": "Hello"})
        assert "title: Hello" in md

    def test_frontmatter_fields(self):
        md = compile_spec({
            "title": "Title",
            "subtitle": "Sub",
            "author": "Author",
        })
        assert "title:" in md
        assert "subtitle:" in md
        assert "author:" in md

    def test_will_metadata(self):
        md = compile_spec({
            "title": "T",
            "page_size": "a4",
            "margins": "narrow",
            "template": "report",
        })
        assert "will:" in md
        assert "page_size: a4" in md

    def test_heading_section(self):
        md = compile_spec({
            "sections": [
                {"type": "heading", "title": "My Heading", "level": 2},
            ],
        })
        assert "## My Heading" in md

    def test_section_with_page_break(self):
        md = compile_spec({
            "sections": [
                {"type": "section", "title": "Chapter", "page_break": True},
            ],
        })
        assert "\\newpage" in md
        assert "# Chapter" in md

    def test_section_with_subtitle(self):
        md = compile_spec({
            "sections": [
                {"type": "section", "title": "Ch", "subtitle": "Sub"},
            ],
        })
        assert "*Sub*" in md

    def test_content_with_text(self):
        md = compile_spec({
            "sections": [
                {"type": "content", "text": "Hello world"},
            ],
        })
        assert "Hello world" in md

    def test_content_with_bullets(self):
        md = compile_spec({
            "sections": [
                {"type": "content", "bullets": ["A", "B", "C"]},
            ],
        })
        assert "- A" in md
        assert "- B" in md
        assert "- C" in md

    def test_content_with_numbered(self):
        md = compile_spec({
            "sections": [
                {"type": "content", "numbered": ["First", "Second"]},
            ],
        })
        assert "1. First" in md
        assert "2. Second" in md

    def test_table(self):
        md = compile_spec({
            "sections": [
                {
                    "type": "table",
                    "title": "Data",
                    "headers": ["Col1", "Col2"],
                    "data": [["a", "b"], ["c", "d"]],
                },
            ],
        })
        assert "| Col1 | Col2 |" in md
        assert "| a | b |" in md

    def test_image(self):
        md = compile_spec({
            "sections": [
                {"type": "image", "path": "fig.png", "caption": "Figure 1", "width": 5},
            ],
        })
        assert "![Figure 1](fig.png)" in md
        assert "width=5in" in md

    def test_quote(self):
        md = compile_spec({
            "sections": [
                {"type": "quote", "text": "To be", "author": "Shakespeare"},
            ],
        })
        assert '> "To be"' in md
        assert "Shakespeare" in md

    def test_code(self):
        md = compile_spec({
            "sections": [
                {"type": "code", "code": "print('hi')", "language": "python"},
            ],
        })
        assert "```python" in md
        assert "print('hi')" in md

    def test_page_break(self):
        md = compile_spec({
            "sections": [{"type": "page_break"}],
        })
        assert "\\newpage" in md

    def test_horizontal_line(self):
        md = compile_spec({
            "sections": [{"type": "horizontal_line"}],
        })
        assert "---" in md

    def test_empty_sections(self):
        md = compile_spec({"sections": []})
        assert md.strip() == ""


class TestCompileSpecFile:
    """Tests for compile_spec_file()."""

    def test_yaml_file(self):
        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".yaml", delete=False, encoding="utf-8"
        ) as f:
            f.write("title: Test\nsections:\n  - type: heading\n    title: Hello\n    level: 1\n")
            f.flush()
            md = compile_spec_file(f.name)
        os.unlink(f.name)
        assert "# Hello" in md

    def test_json_file(self):
        spec = {"title": "JSON Test", "sections": [{"type": "content", "text": "body"}]}
        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".json", delete=False, encoding="utf-8"
        ) as f:
            json.dump(spec, f)
            f.flush()
            md = compile_spec_file(f.name)
        os.unlink(f.name)
        assert "body" in md

    def test_nonexistent_file(self):
        with pytest.raises(SpecCompileError):
            compile_spec_file("/nonexistent/file.yaml")
