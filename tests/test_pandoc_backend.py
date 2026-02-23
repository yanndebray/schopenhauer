"""Tests for the Pandoc backend wrapper."""

import os
import tempfile

import pytest

from will.pandoc_backend import (
    PandocBackendError,
    convert,
    convert_to_bytes,
    get_pandoc_version,
    get_supported_formats,
)


class TestGetPandocVersion:
    def test_returns_string(self):
        version = get_pandoc_version()
        assert isinstance(version, str)
        assert len(version) > 0


class TestGetSupportedFormats:
    def test_returns_dict(self):
        fmts = get_supported_formats()
        assert "input" in fmts
        assert "output" in fmts
        assert "markdown" in fmts["input"]
        assert "docx" in fmts["output"]


class TestConvert:
    def test_markdown_to_docx(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            out = os.path.join(tmpdir, "test.docx")
            result = convert("# Hello\n\nWorld", out, output_format="docx")
            assert result.exists()
            assert result.stat().st_size > 0

    def test_markdown_to_html(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            out = os.path.join(tmpdir, "test.html")
            result = convert("# Hello\n\nWorld", out, output_format="html")
            assert result.exists()
            content = result.read_text(encoding="utf-8")
            assert "Hello" in content

    def test_with_metadata(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            out = os.path.join(tmpdir, "test.html")
            convert(
                "# Doc\n\nBody",
                out,
                output_format="html",
                metadata={"title": "My Title"},
            )
            content = open(out, encoding="utf-8").read()
            assert "My Title" in content

    def test_invalid_format(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            out = os.path.join(tmpdir, "test.xyz")
            with pytest.raises(PandocBackendError):
                convert("# Hello", out, output_format="not_a_format_xyz")


class TestConvertToBytes:
    def test_returns_bytes(self):
        data = convert_to_bytes("# Hello\n\nWorld", output_format="docx")
        assert isinstance(data, bytes)
        assert len(data) > 0

    def test_html_bytes(self):
        data = convert_to_bytes("# Hello", output_format="html")
        assert b"Hello" in data
