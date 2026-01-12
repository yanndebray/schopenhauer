"""
Tests for the WordDocument core class.
"""

import os
import tempfile

import pytest

from will.core import WordDocument


class TestWordDocumentCreation:
    """Tests for creating WordDocument instances."""

    def test_create_empty_document(self):
        """Test creating an empty document."""
        doc = WordDocument()
        assert doc.doc is not None

    def test_create_document_with_title(self):
        """Test creating a document with title."""
        doc = WordDocument(title="Test Title")
        assert doc.doc.core_properties.title == "Test Title"

    def test_create_document_with_author(self):
        """Test creating a document with author."""
        doc = WordDocument(author="Test Author")
        assert doc.doc.core_properties.author == "Test Author"

    def test_create_document_with_nonexistent_template(self):
        """Test that creating with nonexistent template raises error."""
        with pytest.raises(FileNotFoundError):
            WordDocument(template="nonexistent.docx")


class TestHeadings:
    """Tests for heading functionality."""

    def test_add_heading_level_1(self):
        """Test adding a level 1 heading."""
        doc = WordDocument()
        heading = doc.add_heading("Test Heading", level=1)
        assert heading is not None
        assert "Test Heading" in heading.text

    def test_add_heading_level_2(self):
        """Test adding a level 2 heading."""
        doc = WordDocument()
        heading = doc.add_heading("Subheading", level=2)
        assert "Subheading" in heading.text

    def test_add_title(self):
        """Test adding title with subtitle."""
        doc = WordDocument()
        title, subtitle = doc.add_title("Main Title", "Subtitle Text")
        assert "Main Title" in title.text
        assert subtitle is not None
        assert "Subtitle Text" in subtitle.text

    def test_add_title_without_subtitle(self):
        """Test adding title without subtitle."""
        doc = WordDocument()
        title, subtitle = doc.add_title("Main Title")
        assert "Main Title" in title.text
        assert subtitle is None


class TestParagraphs:
    """Tests for paragraph functionality."""

    def test_add_simple_paragraph(self):
        """Test adding a simple paragraph."""
        doc = WordDocument()
        para = doc.add_paragraph("Hello, World!")
        assert para is not None
        assert "Hello, World!" in para.text

    def test_add_bold_paragraph(self):
        """Test adding a bold paragraph."""
        doc = WordDocument()
        para = doc.add_paragraph("Bold text", bold=True)
        assert para.runs[0].bold is True

    def test_add_italic_paragraph(self):
        """Test adding an italic paragraph."""
        doc = WordDocument()
        para = doc.add_paragraph("Italic text", italic=True)
        assert para.runs[0].italic is True


class TestLists:
    """Tests for list functionality."""

    def test_add_bullets(self):
        """Test adding bullet list."""
        doc = WordDocument()
        paragraphs = doc.add_bullets(["Item 1", "Item 2", "Item 3"])
        assert len(paragraphs) == 3
        assert "Item 1" in paragraphs[0].text

    def test_add_numbered_list(self):
        """Test adding numbered list."""
        doc = WordDocument()
        paragraphs = doc.add_numbered_list(["Step 1", "Step 2"])
        assert len(paragraphs) == 2


class TestTables:
    """Tests for table functionality."""

    def test_add_simple_table(self):
        """Test adding a simple table."""
        doc = WordDocument()
        table = doc.add_table(
            data=[["A", "B"], ["C", "D"]],
            headers=["Col1", "Col2"]
        )
        assert table is not None
        assert len(table.rows) == 3  # Header + 2 data rows

    def test_add_table_without_headers(self):
        """Test adding a table without headers."""
        doc = WordDocument()
        table = doc.add_table(data=[["A", "B"], ["C", "D"]])
        assert len(table.rows) == 2


class TestSpecialContent:
    """Tests for special content types."""

    def test_add_quote(self):
        """Test adding a blockquote."""
        doc = WordDocument()
        paragraphs = doc.add_quote("Test quote", author="Author Name")
        assert len(paragraphs) == 2
        assert "Test quote" in paragraphs[0].text

    def test_add_quote_without_author(self):
        """Test adding a quote without attribution."""
        doc = WordDocument()
        paragraphs = doc.add_quote("Test quote")
        assert len(paragraphs) == 1

    def test_add_code_block(self):
        """Test adding a code block."""
        doc = WordDocument()
        para = doc.add_code_block("print('hello')")
        assert "print('hello')" in para.text

    def test_add_page_break(self):
        """Test adding a page break."""
        doc = WordDocument()
        doc.add_page_break()
        # No exception means success

    def test_add_horizontal_line(self):
        """Test adding a horizontal line."""
        doc = WordDocument()
        para = doc.add_horizontal_line()
        assert para is not None


class TestPlaceholders:
    """Tests for placeholder functionality."""

    def test_get_placeholders_empty(self):
        """Test getting placeholders from empty document."""
        doc = WordDocument()
        doc.add_paragraph("No placeholders here")
        placeholders = doc.get_placeholders()
        assert placeholders == []

    def test_get_placeholders(self):
        """Test getting placeholders."""
        doc = WordDocument()
        doc.add_paragraph("Hello {{NAME}}, today is {{DATE}}")
        placeholders = doc.get_placeholders()
        assert "NAME" in placeholders
        assert "DATE" in placeholders

    def test_replace_placeholders(self):
        """Test replacing placeholders."""
        doc = WordDocument()
        doc.add_paragraph("Hello {{NAME}}")
        count = doc.replace_placeholders({"NAME": "World"})
        assert count > 0
        # Verify replacement
        assert doc.get_placeholders() == []


class TestPageSetup:
    """Tests for page setup functionality."""

    def test_set_margins_preset(self):
        """Test setting margins with preset."""
        doc = WordDocument()
        doc.set_margins(preset="narrow")
        # No exception means success

    def test_set_margins_custom(self):
        """Test setting custom margins."""
        doc = WordDocument()
        doc.set_margins(top=1.5, bottom=1.5, left=1, right=1)
        # No exception means success

    def test_set_page_size_preset(self):
        """Test setting page size with preset."""
        doc = WordDocument()
        doc.set_page_size(preset="a4")
        # No exception means success


class TestSaveAndExport:
    """Tests for saving and exporting documents."""

    def test_save_document(self):
        """Test saving document to file."""
        doc = WordDocument()
        doc.add_heading("Test", level=1)

        with tempfile.TemporaryDirectory() as tmpdir:
            path = os.path.join(tmpdir, "test.docx")
            doc.save(path)
            assert os.path.exists(path)

    def test_to_bytes(self):
        """Test exporting document as bytes."""
        doc = WordDocument()
        doc.add_paragraph("Test content")
        doc_bytes = doc.to_bytes()
        assert isinstance(doc_bytes, bytes)
        assert len(doc_bytes) > 0

    def test_get_info(self):
        """Test getting document information."""
        doc = WordDocument(title="Test Doc", author="Test Author")
        doc.add_heading("Heading", level=1)
        doc.add_paragraph("Paragraph")
        doc.add_table(data=[["A"]])

        info = doc.get_info()
        assert info["title"] == "Test Doc"
        assert info["author"] == "Test Author"
        assert info["paragraphs"] > 0
        assert info["tables"] == 1


class TestFromSpec:
    """Tests for creating documents from specifications."""

    def test_from_spec_minimal(self):
        """Test creating document from minimal spec."""
        spec = {
            "title": "Test Document",
            "sections": []
        }
        doc = WordDocument.from_spec(spec)
        assert doc is not None

    def test_from_spec_with_sections(self):
        """Test creating document from spec with sections."""
        spec = {
            "title": "Test Document",
            "sections": [
                {"type": "heading", "title": "Section 1", "level": 1},
                {"type": "content", "text": "Hello World"},
                {"type": "content", "bullets": ["Item 1", "Item 2"]},
            ]
        }
        doc = WordDocument.from_spec(spec)
        info = doc.get_info()
        assert info["paragraphs"] > 0

    def test_from_spec_with_table(self):
        """Test creating document from spec with table."""
        spec = {
            "sections": [
                {
                    "type": "table",
                    "headers": ["A", "B"],
                    "data": [["1", "2"], ["3", "4"]]
                }
            ]
        }
        doc = WordDocument.from_spec(spec)
        assert len(doc.doc.tables) == 1


class TestFromYaml:
    """Tests for creating documents from YAML files."""

    def test_from_yaml(self):
        """Test creating document from YAML file."""
        yaml_content = """
title: Test Document
sections:
  - type: heading
    title: Hello
    level: 1
  - type: content
    text: World
"""
        with tempfile.TemporaryDirectory() as tmpdir:
            yaml_path = os.path.join(tmpdir, "test.yaml")
            with open(yaml_path, 'w') as f:
                f.write(yaml_content)

            doc = WordDocument.from_yaml(yaml_path)
            assert doc is not None
