#!/bin/bash
# =============================================================================
# Schopenhauer's Will - GCP Cloud Run Deployment Script
# =============================================================================
#
# This script deploys the Schopenhauer API to Google Cloud Run.
#
# Prerequisites:
#   - Google Cloud SDK (gcloud) installed and configured
#   - Docker installed (for local builds)
#   - A GCP project with billing enabled
#   - Cloud Run and Artifact Registry APIs enabled
#
# Usage:
#   ./deploy.sh                    # Deploy with defaults
#   ./deploy.sh --region us-west1  # Deploy to specific region
#   ./deploy.sh --build-only       # Only build, don't deploy
#   ./deploy.sh --help             # Show help
#
# =============================================================================

set -e  # Exit on error

# =============================================================================
# Configuration
# =============================================================================

# Default values (can be overridden via environment or arguments)
PROJECT_ID="${GCP_PROJECT_ID:-}"
REGION="${GCP_REGION:-us-central1}"
SERVICE_NAME="${SERVICE_NAME:-schopenhauer-api}"
IMAGE_NAME="${IMAGE_NAME:-schopenhauer}"
MEMORY="${MEMORY:-512Mi}"
CPU="${CPU:-1}"
MIN_INSTANCES="${MIN_INSTANCES:-0}"
MAX_INSTANCES="${MAX_INSTANCES:-10}"
CONCURRENCY="${CONCURRENCY:-80}"
TIMEOUT="${TIMEOUT:-300}"

# Artifact Registry
REGISTRY="${REGISTRY:-gcr.io}"
REPOSITORY="${REPOSITORY:-schopenhauer}"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# =============================================================================
# Helper Functions
# =============================================================================

print_header() {
    echo -e "\n${BLUE}==============================================================================${NC}"
    echo -e "${BLUE}$1${NC}"
    echo -e "${BLUE}==============================================================================${NC}\n"
}

print_success() {
    echo -e "${GREEN}✓ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠ $1${NC}"
}

print_error() {
    echo -e "${RED}✗ $1${NC}"
}

show_help() {
    cat << EOF
Schopenhauer's Will - GCP Cloud Run Deployment

Usage: ./deploy.sh [OPTIONS]

Options:
    --project ID        GCP project ID (required if not set via GCP_PROJECT_ID)
    --region REGION     GCP region (default: us-central1)
    --service NAME      Cloud Run service name (default: schopenhauer-api)
    --memory SIZE       Memory allocation (default: 512Mi)
    --cpu COUNT         CPU allocation (default: 1)
    --min-instances N   Minimum instances (default: 0)
    --max-instances N   Maximum instances (default: 10)
    --build-only        Only build the image, don't deploy
    --deploy-only       Only deploy (image must exist)
    --local             Build for local testing only
    --help              Show this help message

Environment Variables:
    GCP_PROJECT_ID      GCP project ID
    GCP_REGION          GCP region
    SERVICE_NAME        Cloud Run service name

Examples:
    ./deploy.sh --project my-project
    ./deploy.sh --project my-project --region us-west1
    ./deploy.sh --project my-project --memory 1Gi --max-instances 20
    ./deploy.sh --build-only --local

EOF
}

# =============================================================================
# Parse Arguments
# =============================================================================

BUILD_ONLY=false
DEPLOY_ONLY=false
LOCAL_BUILD=false

while [[ $# -gt 0 ]]; do
    case $1 in
        --project)
            PROJECT_ID="$2"
            shift 2
            ;;
        --region)
            REGION="$2"
            shift 2
            ;;
        --service)
            SERVICE_NAME="$2"
            shift 2
            ;;
        --memory)
            MEMORY="$2"
            shift 2
            ;;
        --cpu)
            CPU="$2"
            shift 2
            ;;
        --min-instances)
            MIN_INSTANCES="$2"
            shift 2
            ;;
        --max-instances)
            MAX_INSTANCES="$2"
            shift 2
            ;;
        --build-only)
            BUILD_ONLY=true
            shift
            ;;
        --deploy-only)
            DEPLOY_ONLY=true
            shift
            ;;
        --local)
            LOCAL_BUILD=true
            shift
            ;;
        --help)
            show_help
            exit 0
            ;;
        *)
            print_error "Unknown option: $1"
            show_help
            exit 1
            ;;
    esac
done

# =============================================================================
# Validation
# =============================================================================

print_header "Validating Configuration"

if [ "$LOCAL_BUILD" = false ] && [ -z "$PROJECT_ID" ]; then
    print_error "GCP Project ID is required. Set GCP_PROJECT_ID or use --project"
    exit 1
fi

# Check for required tools
if ! command -v docker &> /dev/null; then
    print_error "Docker is not installed"
    exit 1
fi
print_success "Docker is installed"

if [ "$LOCAL_BUILD" = false ]; then
    if ! command -v gcloud &> /dev/null; then
        print_error "Google Cloud SDK is not installed"
        exit 1
    fi
    print_success "Google Cloud SDK is installed"

    # Set project
    gcloud config set project "$PROJECT_ID" 2>/dev/null
    print_success "Project set to: $PROJECT_ID"
fi

# =============================================================================
# Build Image
# =============================================================================

if [ "$DEPLOY_ONLY" = false ]; then
    print_header "Building Docker Image"

    if [ "$LOCAL_BUILD" = true ]; then
        IMAGE_TAG="${IMAGE_NAME}:latest"
        echo "Building local image: $IMAGE_TAG"
        docker build -t "$IMAGE_TAG" .
    else
        IMAGE_TAG="${REGISTRY}/${PROJECT_ID}/${IMAGE_NAME}:latest"
        echo "Building image: $IMAGE_TAG"

        # Use Cloud Build for remote builds (faster, no local Docker needed)
        if [ -f "cloudbuild.yaml" ]; then
            gcloud builds submit --tag "$IMAGE_TAG"
        else
            # Fall back to local build and push
            docker build -t "$IMAGE_TAG" .
            docker push "$IMAGE_TAG"
        fi
    fi

    print_success "Image built successfully"
fi

# =============================================================================
# Deploy to Cloud Run
# =============================================================================

if [ "$BUILD_ONLY" = false ] && [ "$LOCAL_BUILD" = false ]; then
    print_header "Deploying to Cloud Run"

    IMAGE_TAG="${REGISTRY}/${PROJECT_ID}/${IMAGE_NAME}:latest"

    echo "Deploying to Cloud Run..."
    echo "  Service: $SERVICE_NAME"
    echo "  Region: $REGION"
    echo "  Image: $IMAGE_TAG"
    echo "  Memory: $MEMORY"
    echo "  CPU: $CPU"
    echo "  Min instances: $MIN_INSTANCES"
    echo "  Max instances: $MAX_INSTANCES"

    gcloud run deploy "$SERVICE_NAME" \
        --image "$IMAGE_TAG" \
        --region "$REGION" \
        --platform managed \
        --memory "$MEMORY" \
        --cpu "$CPU" \
        --min-instances "$MIN_INSTANCES" \
        --max-instances "$MAX_INSTANCES" \
        --concurrency "$CONCURRENCY" \
        --timeout "${TIMEOUT}s" \
        --allow-unauthenticated \
        --set-env-vars "ENVIRONMENT=production"

    print_success "Deployment complete"

    # Get service URL
    SERVICE_URL=$(gcloud run services describe "$SERVICE_NAME" \
        --region "$REGION" \
        --format 'value(status.url)')

    print_header "Deployment Summary"
    echo -e "Service URL: ${GREEN}$SERVICE_URL${NC}"
    echo -e "Health check: ${GREEN}${SERVICE_URL}/health${NC}"
    echo -e "API docs: ${GREEN}${SERVICE_URL}/docs${NC}"
    echo ""
    echo "Test the API:"
    echo "  curl ${SERVICE_URL}/health"
fi

# =============================================================================
# Local Testing Instructions
# =============================================================================

if [ "$LOCAL_BUILD" = true ]; then
    print_header "Local Testing"
    echo "To run the container locally:"
    echo ""
    echo "  docker run -p 8000:8000 ${IMAGE_NAME}:latest"
    echo ""
    echo "Then access:"
    echo "  Health: http://localhost:8000/health"
    echo "  API docs: http://localhost:8000/docs"
fi

print_success "Done!"
