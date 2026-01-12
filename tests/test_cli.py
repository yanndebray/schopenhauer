"""
Tests for the CLI commands.
"""

import os
import tempfile

import pytest
from click.testing import CliRunner

from will.cli import main


@pytest.fixture
def runner():
    """Create a CLI runner."""
    return CliRunner()


@pytest.fixture
def temp_dir():
    """Create a temporary directory."""
    with tempfile.TemporaryDirectory() as tmpdir:
        yield tmpdir


class TestMainCommand:
    """Tests for the main CLI command."""

    def test_version(self, runner):
        """Test --version flag."""
        result = runner.invoke(main, ["--version"])
        assert result.exit_code == 0
        assert "Schopenhauer" in result.output
        assert "version" in result.output

    def test_help(self, runner):
        """Test --help flag."""
        result = runner.invoke(main, ["--help"])
        assert result.exit_code == 0
        assert "Schopenhauer" in result.output
        assert "create" in result.output
        assert "generate" in result.output


class TestCreateCommand:
    """Tests for the create command."""

    def test_create_basic(self, runner, temp_dir):
        """Test basic document creation."""
        output = os.path.join(temp_dir, "test.docx")
        result = runner.invoke(main, ["create", "-o", output, "--title", "Test Document"])
        assert result.exit_code == 0
        assert os.path.exists(output)

    def test_create_with_all_options(self, runner, temp_dir):
        """Test document creation with all options."""
        output = os.path.join(temp_dir, "test.docx")
        result = runner.invoke(
            main,
            [
                "create",
                "-o",
                output,
                "--title",
                "Test Title",
                "--subtitle",
                "Test Subtitle",
                "--author",
                "Test Author",
                "--page-size",
                "a4",
                "--margins",
                "narrow",
            ],
        )
        assert result.exit_code == 0
        assert os.path.exists(output)

    def test_create_missing_output(self, runner):
        """Test create without output flag."""
        result = runner.invoke(main, ["create", "--title", "Test"])
        assert result.exit_code != 0


class TestGenerateCommand:
    """Tests for the generate command."""

    def test_generate_from_yaml(self, runner, temp_dir):
        """Test generating from YAML file."""
        # Create YAML file
        yaml_path = os.path.join(temp_dir, "spec.yaml")
        with open(yaml_path, "w") as f:
            f.write(
                """
title: Generated Document
sections:
  - type: heading
    title: Hello
    level: 1
  - type: content
    text: World
"""
            )

        output = os.path.join(temp_dir, "output.docx")
        result = runner.invoke(main, ["generate", yaml_path, "-o", output])
        assert result.exit_code == 0
        assert os.path.exists(output)

    def test_generate_with_variables(self, runner, temp_dir):
        """Test generating with variable substitution."""
        yaml_path = os.path.join(temp_dir, "spec.yaml")
        with open(yaml_path, "w") as f:
            f.write(
                """
title: "{{TITLE}}"
sections:
  - type: content
    text: "Hello {{NAME}}"
"""
            )

        output = os.path.join(temp_dir, "output.docx")
        result = runner.invoke(
            main,
            ["generate", yaml_path, "-o", output, "-V", "TITLE=My Document", "-V", "NAME=World"],
        )
        assert result.exit_code == 0

    def test_generate_missing_spec(self, runner, temp_dir):
        """Test generate with missing spec file."""
        output = os.path.join(temp_dir, "output.docx")
        result = runner.invoke(main, ["generate", "nonexistent.yaml", "-o", output])
        assert result.exit_code != 0


class TestInspectCommand:
    """Tests for the inspect command."""

    def test_inspect_document(self, runner, temp_dir):
        """Test inspecting a document."""
        # Create a document first
        from will.core import WordDocument

        doc_path = os.path.join(temp_dir, "test.docx")
        doc = WordDocument(title="Test")
        doc.add_paragraph("Hello {{NAME}}")
        doc.save(doc_path)

        result = runner.invoke(main, ["inspect", doc_path])
        assert result.exit_code == 0
        assert "Test" in result.output

    def test_inspect_placeholders(self, runner, temp_dir):
        """Test inspecting placeholders."""
        from will.core import WordDocument

        doc_path = os.path.join(temp_dir, "test.docx")
        doc = WordDocument()
        doc.add_paragraph("Hello {{NAME}}, date is {{DATE}}")
        doc.save(doc_path)

        result = runner.invoke(main, ["inspect", doc_path, "--placeholders"])
        assert result.exit_code == 0
        assert "NAME" in result.output
        assert "DATE" in result.output

    def test_inspect_json(self, runner, temp_dir):
        """Test inspecting with JSON output."""
        from will.core import WordDocument

        doc_path = os.path.join(temp_dir, "test.docx")
        doc = WordDocument(title="Test", author="Author")
        doc.save(doc_path)

        result = runner.invoke(main, ["inspect", doc_path, "--json"])
        assert result.exit_code == 0
        assert '"title"' in result.output


class TestAddCommand:
    """Tests for the add command."""

    def test_add_heading(self, runner, temp_dir):
        """Test adding a heading."""
        from will.core import WordDocument

        doc_path = os.path.join(temp_dir, "test.docx")
        doc = WordDocument()
        doc.save(doc_path)

        result = runner.invoke(main, ["add", doc_path, "--heading", "New Section", "--level", "1"])
        assert result.exit_code == 0

    def test_add_paragraph(self, runner, temp_dir):
        """Test adding a paragraph."""
        from will.core import WordDocument

        doc_path = os.path.join(temp_dir, "test.docx")
        doc = WordDocument()
        doc.save(doc_path)

        result = runner.invoke(main, ["add", doc_path, "--paragraph", "New paragraph text"])
        assert result.exit_code == 0

    def test_add_bullets(self, runner, temp_dir):
        """Test adding bullet points."""
        from will.core import WordDocument

        doc_path = os.path.join(temp_dir, "test.docx")
        doc = WordDocument()
        doc.save(doc_path)

        result = runner.invoke(main, ["add", doc_path, "-b", "Point 1", "-b", "Point 2"])
        assert result.exit_code == 0


class TestReplaceCommand:
    """Tests for the replace command."""

    def test_replace_placeholders(self, runner, temp_dir):
        """Test replacing placeholders."""
        from will.core import WordDocument

        doc_path = os.path.join(temp_dir, "test.docx")
        doc = WordDocument()
        doc.add_paragraph("Hello {{NAME}}")
        doc.save(doc_path)

        result = runner.invoke(main, ["replace", doc_path, "NAME=World"])
        assert result.exit_code == 0

    def test_replace_list_only(self, runner, temp_dir):
        """Test listing placeholders only."""
        from will.core import WordDocument

        doc_path = os.path.join(temp_dir, "test.docx")
        doc = WordDocument()
        doc.add_paragraph("Hello {{NAME}}, date: {{DATE}}")
        doc.save(doc_path)

        result = runner.invoke(main, ["replace", doc_path, "--list"])
        assert result.exit_code == 0
        assert "NAME" in result.output
        assert "DATE" in result.output


class TestTemplateCommand:
    """Tests for the template command."""

    def test_template_list(self, runner):
        """Test listing templates."""
        result = runner.invoke(main, ["template", "list"])
        assert result.exit_code == 0
        assert "default" in result.output
        assert "report" in result.output

    def test_template_list_yaml(self, runner):
        """Test listing YAML templates."""
        result = runner.invoke(main, ["template", "list", "--yaml"])
        assert result.exit_code == 0
        assert "blank" in result.output
        assert "report" in result.output

    def test_template_info(self, runner):
        """Test getting template info."""
        result = runner.invoke(main, ["template", "info", "report"])
        assert result.exit_code == 0
        assert "report" in result.output.lower()

    def test_template_init(self, runner, temp_dir):
        """Test initializing from template."""
        output = os.path.join(temp_dir, "spec.yaml")
        result = runner.invoke(main, ["template", "init", "report", "-o", output])
        assert result.exit_code == 0
        assert os.path.exists(output)


class TestCloudCommand:
    """Tests for the cloud command."""

    def test_cloud_health_no_server(self, runner):
        """Test cloud health check with no server."""
        result = runner.invoke(main, ["cloud", "health", "--url", "http://localhost:9999"])
        # Should fail since no server is running
        assert result.exit_code != 0
