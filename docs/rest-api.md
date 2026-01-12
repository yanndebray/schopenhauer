# REST API

Schopenhauer provides a FastAPI-powered REST API for cloud-based document generation.

## Running the Server

### Local Development

```bash
# Install API dependencies
pip install schopenhauer[api]

# Start the server
uvicorn will.api:app --host 0.0.0.0 --port 8000 --reload
```

### Production

```bash
uvicorn will.api:app --host 0.0.0.0 --port 8000 --workers 4
```

### Docker

```bash
docker build -t schopenhauer .
docker run -p 8000:8000 schopenhauer
```

## API Documentation

Interactive documentation is available at:

- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`

## Endpoints

### Health Check

```http
GET /health
```

Returns API health status.

**Response:**

```json
{
  "status": "healthy",
  "version": "0.1.0",
  "timestamp": "2024-01-15T10:30:00Z"
}
```

### List Templates

```http
GET /templates
```

Returns available templates.

**Response:**

```json
{
  "templates": [
    {
      "name": "default",
      "description": "Clean, professional default template",
      "page_size": "letter"
    },
    ...
  ],
  "yaml_templates": ["blank", "report", "proposal", ...]
}
```

### Generate Document

```http
POST /generate
Content-Type: application/json
```

Generate a document from a JSON specification.

**Request Body:**

```json
{
  "title": "My Report",
  "subtitle": "2024 Edition",
  "author": "Jane Doe",
  "page_size": "letter",
  "margins": "normal",
  "table_of_contents": false,
  "sections": [
    {
      "type": "heading",
      "title": "Introduction",
      "level": 1
    },
    {
      "type": "content",
      "text": "Welcome to my report."
    },
    {
      "type": "content",
      "bullets": ["Point 1", "Point 2", "Point 3"]
    },
    {
      "type": "table",
      "headers": ["Name", "Value"],
      "data": [["Metric A", "100"], ["Metric B", "200"]]
    }
  ],
  "placeholders": {
    "DATE": "2024-01-15"
  }
}
```

**Response:**

Binary .docx file

**cURL Example:**

```bash
curl -X POST "http://localhost:8000/generate" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "My Report",
    "sections": [
      {"type": "heading", "title": "Hello", "level": 1},
      {"type": "content", "text": "World!"}
    ]
  }' \
  --output report.docx
```

### Generate with Template

```http
POST /generate-with-template
Content-Type: multipart/form-data
```

Generate using an uploaded template file.

**Request:**

- `template`: Template .docx file
- `spec`: JSON specification string

**cURL Example:**

```bash
curl -X POST "http://localhost:8000/generate-with-template" \
  -F "template=@template.docx" \
  -F 'spec={"title": "Report", "sections": []}' \
  --output output.docx
```

### Inspect Document

```http
POST /inspect
Content-Type: multipart/form-data
```

Inspect an uploaded document or template.

**Request:**

- `template`: Document .docx file

**Response:**

```json
{
  "title": "Document Title",
  "author": "Author Name",
  "created": "2024-01-15T10:00:00",
  "modified": "2024-01-15T12:00:00",
  "paragraphs": 25,
  "tables": 3,
  "sections": 1,
  "word_count": 500,
  "styles": ["Normal", "Heading 1", "Heading 2"],
  "placeholders": ["NAME", "DATE", "COMPANY"]
}
```

### Replace Placeholders

```http
POST /replace
Content-Type: multipart/form-data
```

Replace placeholders in an uploaded document.

**Request:**

- `document`: Document .docx file
- `replacements`: JSON object mapping placeholders to values

**cURL Example:**

```bash
curl -X POST "http://localhost:8000/replace" \
  -F "document=@template.docx" \
  -F 'replacements={"NAME": "John Doe", "DATE": "2024-01-15"}' \
  --output filled.docx
```

### Batch Generate

```http
POST /batch/generate
Content-Type: application/json
```

Generate multiple documents in one request. Returns a ZIP archive.

**Request Body:**

```json
{
  "items": [
    {
      "spec": {
        "title": "Report 1",
        "sections": [{"type": "content", "text": "Content 1"}]
      },
      "filename": "report1.docx"
    },
    {
      "spec": {
        "title": "Report 2",
        "sections": [{"type": "content", "text": "Content 2"}]
      },
      "filename": "report2.docx"
    }
  ]
}
```

**Response:**

ZIP archive containing all generated documents.

## Section Types

Available section types for the `sections` array:

| Type | Description |
|------|-------------|
| `heading` | Heading with title and level |
| `section` | Section header with optional page break |
| `content` | Text, bullets, or numbered list |
| `table` | Data table with headers |
| `image` | Image with path and caption |
| `quote` | Blockquote with attribution |
| `code` | Code block |
| `page_break` | Manual page break |
| `horizontal_line` | Horizontal rule |

## Error Handling

Errors return JSON with error details:

```json
{
  "error": "Error type",
  "detail": "Detailed error message"
}
```

**HTTP Status Codes:**

| Code | Description |
|------|-------------|
| 200 | Success |
| 400 | Bad request (invalid input) |
| 404 | Not found |
| 500 | Internal server error |

## Client Libraries

### Python

```python
import httpx

# Generate document
with httpx.Client() as client:
    response = client.post(
        "http://localhost:8000/generate",
        json={
            "title": "My Report",
            "sections": [
                {"type": "heading", "title": "Hello", "level": 1}
            ]
        }
    )

    with open("report.docx", "wb") as f:
        f.write(response.content)
```

### JavaScript

```javascript
// Using fetch
const response = await fetch('http://localhost:8000/generate', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    title: 'My Report',
    sections: [
      { type: 'heading', title: 'Hello', level: 1 }
    ]
  })
});

const blob = await response.blob();
// Save blob as file
```

### Using CLI

```bash
# Check health
will cloud health --url http://localhost:8000

# Generate via API
will cloud generate spec.yaml -o doc.docx --url http://localhost:8000
```
