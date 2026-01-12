# GCP Cloud Run Deployment

Deploy Schopenhauer as a serverless API on Google Cloud Run.

## Prerequisites

1. **Google Cloud SDK**: Install and configure [gcloud CLI](https://cloud.google.com/sdk/docs/install)
2. **GCP Project**: A GCP project with billing enabled
3. **APIs Enabled**: Cloud Run API, Artifact Registry API

## Quick Deployment

Use the included deployment script:

```bash
# Basic deployment
./deploy.sh --project your-project-id

# Custom region
./deploy.sh --project your-project-id --region us-west1

# Custom resources
./deploy.sh --project your-project-id \
    --memory 1Gi \
    --cpu 2 \
    --max-instances 20
```

## Manual Deployment

### 1. Build the Container

```bash
# Set your project
gcloud config set project YOUR_PROJECT_ID

# Build and push image
gcloud builds submit --tag gcr.io/YOUR_PROJECT_ID/schopenhauer
```

### 2. Deploy to Cloud Run

```bash
gcloud run deploy schopenhauer-api \
    --image gcr.io/YOUR_PROJECT_ID/schopenhauer \
    --region us-central1 \
    --platform managed \
    --memory 512Mi \
    --cpu 1 \
    --min-instances 0 \
    --max-instances 10 \
    --concurrency 80 \
    --timeout 300s \
    --allow-unauthenticated
```

### 3. Get Service URL

```bash
gcloud run services describe schopenhauer-api \
    --region us-central1 \
    --format 'value(status.url)'
```

## Configuration Options

### Resource Allocation

| Setting | Default | Description |
|---------|---------|-------------|
| `--memory` | 512Mi | Memory allocation |
| `--cpu` | 1 | CPU allocation |
| `--min-instances` | 0 | Minimum instances (0 = scale to zero) |
| `--max-instances` | 10 | Maximum instances |
| `--concurrency` | 80 | Max concurrent requests per instance |
| `--timeout` | 300s | Request timeout |

### Environment Variables

Set environment variables in Cloud Run:

```bash
gcloud run deploy schopenhauer-api \
    --set-env-vars "ENVIRONMENT=production,LOG_LEVEL=info"
```

## Using the Deployed API

### Health Check

```bash
curl https://YOUR-SERVICE-URL/health
```

### Generate Document

```bash
curl -X POST "https://YOUR-SERVICE-URL/generate" \
    -H "Content-Type: application/json" \
    -d '{
      "title": "My Report",
      "sections": [
        {"type": "heading", "title": "Hello", "level": 1}
      ]
    }' \
    --output report.docx
```

### Using CLI

```bash
will cloud health --url https://YOUR-SERVICE-URL
will cloud generate spec.yaml -o doc.docx --url https://YOUR-SERVICE-URL
```

## Authentication

### Public Access

For public APIs (default):

```bash
--allow-unauthenticated
```

### Authenticated Access

For secured APIs:

```bash
--no-allow-unauthenticated
```

Access with authentication:

```bash
# Get identity token
TOKEN=$(gcloud auth print-identity-token)

# Make authenticated request
curl -H "Authorization: Bearer $TOKEN" https://YOUR-SERVICE-URL/health
```

## CI/CD Integration

### GitHub Actions

```yaml
name: Deploy to Cloud Run

on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Authenticate to GCP
        uses: google-github-actions/auth@v2
        with:
          credentials_json: ${{ secrets.GCP_SA_KEY }}

      - name: Set up Cloud SDK
        uses: google-github-actions/setup-gcloud@v2

      - name: Deploy to Cloud Run
        run: |
          gcloud run deploy schopenhauer-api \
            --source . \
            --region us-central1 \
            --allow-unauthenticated
```

## Monitoring

### View Logs

```bash
gcloud run services logs read schopenhauer-api --region us-central1
```

### View Metrics

Visit the Cloud Run console:
```
https://console.cloud.google.com/run?project=YOUR_PROJECT_ID
```

## Cost Optimization

1. **Scale to Zero**: Use `--min-instances 0` for cost savings
2. **Right-size**: Start with 512Mi memory, scale up if needed
3. **Concurrency**: Higher concurrency = fewer instances
4. **Cold Start**: First request after idle period is slower

## Troubleshooting

### Container fails to start

Check logs:
```bash
gcloud run services logs read schopenhauer-api --limit 50
```

### Out of memory

Increase memory allocation:
```bash
gcloud run services update schopenhauer-api --memory 1Gi
```

### Timeout errors

Increase timeout:
```bash
gcloud run services update schopenhauer-api --timeout 600s
```
