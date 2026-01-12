"""
Tests for the templates module.
"""

import pytest
import tempfile
import os

from will.templates import (
    get_template,
    list_templates,
    get_template_names,
    list_yaml_templates,
    get_yaml_template,
    save_yaml_template,
    BUILTIN_TEMPLATES,
)


class TestBuiltinTemplates:
    """Tests for built-in templates."""

    def test_builtin_templates_exist(self):
        """Test that built-in templates exist."""
        assert len(BUILTIN_TEMPLATES) > 0
        assert 'default' in BUILTIN_TEMPLATES
        assert 'report' in BUILTIN_TEMPLATES

    def test_get_template(self):
        """Test getting a template by name."""
        template = get_template('default')
        assert template is not None
        assert template.name == 'default'

    def test_get_template_case_insensitive(self):
        """Test that template lookup is case insensitive."""
        template1 = get_template('DEFAULT')
        template2 = get_template('default')
        assert template1 is not None
        assert template1.name == template2.name

    def test_get_nonexistent_template(self):
        """Test getting a nonexistent template."""
        template = get_template('nonexistent')
        assert template is None

    def test_list_templates(self):
        """Test listing templates."""
        templates = list_templates()
        assert len(templates) > 0
        assert all('name' in t for t in templates)
        assert all('description' in t for t in templates)
        assert all('page_size' in t for t in templates)

    def test_get_template_names(self):
        """Test getting template names."""
        names = get_template_names()
        assert 'default' in names
        assert 'report' in names
        assert 'memo' in names


class TestTemplateConfig:
    """Tests for TemplateConfig properties."""

    def test_default_template_config(self):
        """Test default template configuration."""
        template = get_template('default')
        assert template.page_size == 'letter'
        assert template.margins == 'normal'
        assert template.include_footer is True

    def test_report_template_config(self):
        """Test report template configuration."""
        template = get_template('report')
        assert template.page_size == 'letter'
        assert template.margins == 'moderate'
        assert template.include_header is True
        assert template.include_footer is True

    def test_academic_template_config(self):
        """Test academic template configuration."""
        template = get_template('academic')
        assert template.line_spacing == 2.0
        assert template.first_line_indent == 0.5
        assert template.font_body == 'Times New Roman'


class TestYamlTemplates:
    """Tests for YAML templates."""

    def test_list_yaml_templates(self):
        """Test listing YAML templates."""
        templates = list_yaml_templates()
        assert len(templates) > 0
        assert 'blank' in templates
        assert 'report' in templates

    def test_get_yaml_template(self):
        """Test getting a YAML template."""
        template = get_yaml_template('blank')
        assert template is not None
        assert 'title' in template
        assert 'sections' in template

    def test_get_yaml_template_case_insensitive(self):
        """Test that YAML template lookup is case insensitive."""
        template1 = get_yaml_template('REPORT')
        template2 = get_yaml_template('report')
        assert template1 is not None
        assert template1 == template2

    def test_get_nonexistent_yaml_template(self):
        """Test getting a nonexistent YAML template."""
        template = get_yaml_template('nonexistent')
        assert template is None

    def test_save_yaml_template(self):
        """Test saving a YAML template to file."""
        with tempfile.TemporaryDirectory() as tmpdir:
            path = os.path.join(tmpdir, 'template.yaml')
            result = save_yaml_template('blank', path)
            assert result is True
            assert os.path.exists(path)

            with open(path) as f:
                content = f.read()
            assert 'title' in content

    def test_save_nonexistent_yaml_template(self):
        """Test saving a nonexistent template."""
        with tempfile.TemporaryDirectory() as tmpdir:
            path = os.path.join(tmpdir, 'template.yaml')
            result = save_yaml_template('nonexistent', path)
            assert result is False
            assert not os.path.exists(path)


class TestYamlTemplateContent:
    """Tests for YAML template content."""

    def test_blank_template_structure(self):
        """Test blank template has required structure."""
        template = get_yaml_template('blank')
        assert 'title' in template
        assert 'page_size' in template
        assert 'sections' in template

    def test_report_template_structure(self):
        """Test report template has sections."""
        template = get_yaml_template('report')
        assert 'title' in template
        assert 'sections' in template
        assert 'table_of_contents' in template

    def test_proposal_template_structure(self):
        """Test proposal template has required sections."""
        template = get_yaml_template('proposal')
        assert 'title' in template
        assert 'sections' in template
