#!/bin/bash

# Quick deploy script for Lambda
# Usage: ./deploy.sh [function-name] [api-key]

set -e

FUNCTION_NAME=${1:-"resume-optimizer-api"}
API_KEY=${2:-""}

echo "🚀 Deploying Lambda function: $FUNCTION_NAME"
echo ""

# Check if zip exists
if [ ! -f "lambda_deployment.zip" ]; then
    echo "❌ lambda_deployment.zip not found!"
    echo "Building zip file..."
    npm install
    zip -r lambda_deployment.zip . -x "*.git*" "node_modules/.cache/*" "*.log"
    echo "✅ Zip file created"
fi

# Check AWS CLI
if ! command -v aws &> /dev/null; then
    echo "⚠️  AWS CLI not found. Using manual upload method."
    echo ""
    echo "📋 Manual Steps:"
    echo "1. Go to: https://console.aws.amazon.com/lambda"
    echo "2. Upload: lambda_deployment.zip"
    echo "3. Handler: index.handler"
    echo "4. Runtime: Node.js 18.x"
    echo "5. Environment: GEMINI_API_KEY = $API_KEY"
    exit 0
fi

echo "📦 Uploading code..."
aws lambda update-function-code \
    --function-name "$FUNCTION_NAME" \
    --zip-file fileb://lambda_deployment.zip \
    --output json > /dev/null

echo "✅ Code uploaded"

# Update configuration if API key provided
if [ -n "$API_KEY" ]; then
    echo "⚙️  Updating configuration..."
    aws lambda update-function-configuration \
        --function-name "$FUNCTION_NAME" \
        --environment "Variables={GEMINI_API_KEY=$API_KEY}" \
        --timeout 60 \
        --memory-size 512 \
        --output json > /dev/null
    echo "✅ Configuration updated"
fi

echo ""
echo "🎉 Deployment complete!"
echo ""
echo "📋 Next steps:"
echo "1. Create Function URL in AWS Console"
echo "2. Update frontend with the URL"
echo "3. Test the endpoint"

