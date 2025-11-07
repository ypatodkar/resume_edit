#!/bin/bash

# Build Lambda zip file - Simple version
# This builds a Linux-compatible package using Docker

set -e

echo "🔨 Building Lambda package..."

# Check Docker
if ! docker info > /dev/null 2>&1; then
    echo "❌ Docker is not running. Please start Docker Desktop."
    exit 1
fi

# Clean previous builds
rm -rf lambda_package lambda_deployment.zip

# Create package directory
mkdir -p lambda_package

echo "📦 Copying files..."
cp -r src lambda_package/
cp app.py lambda_package/
cp lambda_handler.py lambda_package/

echo "🐳 Installing dependencies in Linux container..."
docker run --rm -v "$(pwd):/var/task" \
    -w /var/task \
    public.ecr.aws/lambda/python:3.11 \
    /bin/bash -c "
        pip install -r requirements.txt -t lambda_package/ --upgrade --quiet && \
        find lambda_package -name '*.pyc' -delete && \
        find lambda_package -type d -name '__pycache__' -exec rm -rf {} + 2>/dev/null || true
    "

echo "📦 Creating zip..."
cd lambda_package
zip -r ../lambda_deployment.zip . -q
cd ..

SIZE=$(du -h lambda_deployment.zip | cut -f1)
echo "✅ Done! lambda_deployment.zip ($SIZE) is ready to upload."

