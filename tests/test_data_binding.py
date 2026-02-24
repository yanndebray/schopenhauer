import pytest
from pathlib import Path
from will.render import render

def test_data_binding_csv_yaml(tmp_path):
    # Setup data files
    data_dir = tmp_path / "data"
    data_dir.mkdir()
    
    runs_csv = data_dir / "runs.csv"
    runs_csv.write_text("name,f1\nmodel_a,0.95\nmodel_b,0.92", encoding="utf-8")
    
    best_yaml = data_dir / "best.yaml"
    best_yaml.write_text("model_name: best_model\nf1: 0.98", encoding="utf-8")
    
    # Setup markdown with frontmatter
    md_content = """---
will:
  data:
    runs: data/runs.csv
    best: data/best.yaml
---
# Report
Best model: {{best.model_name}} ({{best.f1}})

# Runs
{% for run in runs -%}
- {{run.name}}: {{run.f1}}
{% endfor %}
"""
    md_file = tmp_path / "report.md"
    md_file.write_text(md_content, encoding="utf-8")
    
    # Render to HTML (fastest to check)
    output_html = tmp_path / "report.html"
    render(md_file, output=output_html, format="html")
    
    result = output_html.read_text(encoding="utf-8")
    
    assert "Best model: best_model (0.98)" in result
    assert "model_a: 0.95" in result
    assert "model_b: 0.92" in result

def test_data_binding_missing_file(tmp_path):
    md_content = """---
will:
  data:
    missing: data/notfound.csv
---
# Report
"""
    md_file = tmp_path / "report.md"
    md_file.write_text(md_content, encoding="utf-8")
    
    from will.render import RenderError
    with pytest.raises(RenderError) as exc:
        render(md_file, format="html")
    assert "Data file not found" in str(exc.value)
