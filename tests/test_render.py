"""Tests for the render pipeline."""

import os
import tempfile

import pytest

from will.render import RenderError, render


@pytest.fixture
def temp_dir():
    with tempfile.TemporaryDirectory() as tmpdir:
        yield tmpdir


@pytest.fixture
def sample_md(temp_dir):
    """Create a sample Markdown file."""
    path = os.path.join(temp_dir, "sample.md")
    with open(path, "w", encoding="utf-8") as f:
        f.write(
            "---\n"
            "title: Test Document\n"
            "author: Tester\n"
            "will:\n"
            "  variables:\n"
            "    greeting: Hello\n"
            "---\n\n"
            "# {{greeting}} World\n\n"
            "This is a test document.\n"
        )
    return path


@pytest.fixture
def sample_yaml(temp_dir):
    """Create a sample YAML spec file."""
    path = os.path.join(temp_dir, "sample.yaml")
    with open(path, "w", encoding="utf-8") as f:
        f.write(
            "title: YAML Document\n"
            "sections:\n"
            "  - type: heading\n"
            "    title: Introduction\n"
            "    level: 1\n"
            "  - type: content\n"
            "    text: This is from a YAML spec.\n"
        )
    return path


class TestRenderMarkdownToDocx:
    def test_basic(self, sample_md, temp_dir):
        out = os.path.join(temp_dir, "out.docx")
        result = render(sample_md, output=out)
        assert result.exists()
        assert result.stat().st_size > 0

    def test_returns_bytes_when_no_output(self, sample_md):
        data = render(sample_md)
        assert isinstance(data, bytes)
        assert len(data) > 0


class TestRenderMarkdownToHtml:
    def test_html_output(self, sample_md, temp_dir):
        out = os.path.join(temp_dir, "out.html")
        result = render(sample_md, output=out, format="html")
        assert result.exists()
        content = result.read_text(encoding="utf-8")
        assert "Hello World" in content


class TestRenderYamlSpec:
    def test_yaml_to_docx(self, sample_yaml, temp_dir):
        out = os.path.join(temp_dir, "out.docx")
        result = render(sample_yaml, output=out)
        assert result.exists()
        assert result.stat().st_size > 0


class TestRenderWithVariables:
    def test_cli_variables_override(self, temp_dir):
        """CLI variables should override frontmatter variables."""
        md_path = os.path.join(temp_dir, "vars.md")
        with open(md_path, "w", encoding="utf-8") as f:
            f.write(
                "---\n"
                "title: Vars Test\n"
                "will:\n"
                "  variables:\n"
                "    name: Default\n"
                "---\n\n"
                "Hello {{name}}\n"
            )
        out = os.path.join(temp_dir, "out.html")
        result = render(md_path, output=out, format="html", variables={"name": "Override"})
        content = result.read_text(encoding="utf-8")
        assert "Override" in content
        assert "Default" not in content


class TestRenderLegacyBackend:
    def test_legacy_yaml(self, sample_yaml, temp_dir):
        out = os.path.join(temp_dir, "legacy.docx")
        result = render(sample_yaml, output=out, backend="legacy")
        assert result.exists()
        assert result.stat().st_size > 0

    def test_legacy_rejects_markdown(self, sample_md, temp_dir):
        out = os.path.join(temp_dir, "legacy.docx")
        with pytest.raises(RenderError):
            render(sample_md, output=out, backend="legacy")


class TestRenderErrors:
    def test_nonexistent_source(self, temp_dir):
        out = os.path.join(temp_dir, "out.docx")
        with pytest.raises(RenderError):
            render("/nonexistent/file.md", output=out)
