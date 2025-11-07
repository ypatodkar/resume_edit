# Deploy Lambda Function - Step by Step Guide

## Prerequisites

- AWS Account
- AWS CLI installed (optional, but helpful)
- `lambda_deployment.zip` file ready

## Method 1: AWS Console (Easiest) 🎯

### Step 1: Create Lambda Function

1. Go to [AWS Lambda Console](https://console.aws.amazon.com/lambda)
2. Click **"Create function"**
3. Choose:
   - **Author from scratch**
   - **Function name:** `resume-optimizer-api`
   - **Runtime:** `Node.js 18.x` or `Node.js 20.x`
   - **Architecture:** `x86_64`
   - Click **"Create function"**

### Step 2: Upload Code

1. Scroll down to **"Code source"** section
2. Click **"Upload from"** → **".zip file"**
3. Click **"Upload"** and select `lambda_deployment.zip`
4. Wait for upload to complete

### Step 3: Configure Handler

1. In **"Runtime settings"**, click **"Edit"**
2. Set **Handler:** `index.handler`
3. Click **"Save"**

### Step 4: Set Environment Variables

1. Go to **"Configuration"** tab
2. Click **"Environment variables"** → **"Edit"**
3. Add:
   - **Key:** `GEMINI_API_KEY`
   - **Value:** `your-gemini-api-key-here`
4. Click **"Save"**

### Step 5: Configure Timeout & Memory

1. Go to **"Configuration"** → **"General configuration"**
2. Click **"Edit"**
3. Set:
   - **Timeout:** `60 seconds` (or more if needed)
   - **Memory:** `512 MB` (or more for faster execution)
4. Click **"Save"**

### Step 6: Create API Gateway (Optional - for HTTP access)

1. Go to **"Configuration"** → **"Function URL"** (or use API Gateway)
2. Click **"Create function URL"**
3. Choose:
   - **Auth type:** `NONE` (or `AWS_IAM` for security)
   - **CORS:** Enable if calling from browser
4. Click **"Save"**
5. Copy the **Function URL** (you'll need this for your frontend)

## Method 2: AWS CLI (Faster for Updates) ⚡

### Install AWS CLI (if not installed)

```bash
# macOS
brew install awscli

# Or download from: https://aws.amazon.com/cli/
```

### Configure AWS Credentials

```bash
aws configure
# Enter your:
# - AWS Access Key ID
# - AWS Secret Access Key
# - Default region (e.g., us-east-1)
# - Default output format (json)
```

### Deploy Function

```bash
cd backend-nodejs

# Create function (first time only)
aws lambda create-function \
  --function-name resume-optimizer-api \
  --runtime nodejs18.x \
  --role arn:aws:iam::YOUR_ACCOUNT_ID:role/lambda-execution-role \
  --handler index.handler \
  --zip-file fileb://lambda_deployment.zip \
  --timeout 60 \
  --memory-size 512 \
  --environment Variables="{GEMINI_API_KEY=your-api-key-here}"

# Update function (for subsequent deployments)
aws lambda update-function-code \
  --function-name resume-optimizer-api \
  --zip-file fileb://lambda_deployment.zip

# Update environment variables
aws lambda update-function-configuration \
  --function-name resume-optimizer-api \
  --environment Variables="{GEMINI_API_KEY=your-api-key-here}" \
  --timeout 60 \
  --memory-size 512
```

### Create Function URL

```bash
aws lambda create-function-url-config \
  --function-name resume-optimizer-api \
  --auth-type NONE \
  --cors '{"AllowOrigins": ["*"], "AllowMethods": ["GET", "POST", "OPTIONS"], "AllowHeaders": ["Content-Type"]}'
```

## Method 3: Using Serverless Framework (Advanced) 🚀

### Install Serverless

```bash
npm install -g serverless
```

### Create `serverless.yml`

```yaml
service: resume-optimizer

provider:
  name: aws
  runtime: nodejs18.x
  region: us-east-1
  timeout: 60
  memorySize: 512
  environment:
    GEMINI_API_KEY: ${env:GEMINI_API_KEY}

functions:
  api:
    handler: index.handler
    events:
      - http:
          path: /{proxy+}
          method: ANY
          cors: true
      - http:
          path: /
          method: ANY
          cors: true

package:
  patterns:
    - '!node_modules/.cache/**'
    - '!*.git/**'
```

### Deploy

```bash
GEMINI_API_KEY=your-key serverless deploy
```

## Testing Your Deployment

### Test via AWS Console

1. Go to Lambda function
2. Click **"Test"** tab
3. Create new test event:

```json
{
  "httpMethod": "POST",
  "path": "/optimize/text",
  "body": "{\"resume_text\":\"Software Engineer with 5 years experience\",\"job_description\":\"Looking for a senior developer\"}"
}
```

4. Click **"Test"**
5. Check the response

### Test via Function URL

```bash
curl -X POST https://YOUR-FUNCTION-URL/optimize/text \
  -H "Content-Type: application/json" \
  -d '{
    "resume_text": "Software Engineer with 5 years experience",
    "job_description": "Looking for a senior developer"
  }'
```

### Test Health Endpoint

```bash
curl https://YOUR-FUNCTION-URL/health
```

## Troubleshooting

### Error: "Handler not found"
- Check handler is set to `index.handler`
- Ensure `index.js` is in the root of the zip

### Error: "Module not found"
- Make sure `node_modules` is included in the zip
- Rebuild: `npm install && zip -r lambda_deployment.zip .`

### Error: "Timeout"
- Increase timeout in Lambda configuration
- Check CloudWatch logs for slow operations

### Error: "Memory limit exceeded"
- Increase memory allocation
- Check for memory leaks in code

### View Logs

```bash
# Via AWS Console
# Go to Lambda → Monitor → View CloudWatch logs

# Via CLI
aws logs tail /aws/lambda/resume-optimizer-api --follow
```

## Update Frontend

After deployment, update your frontend to use the Lambda URL:

```typescript
// frontend/.env or frontend/.env.production
VITE_API_URL=https://YOUR-FUNCTION-URL
```

## Cost Estimate

- **Free Tier:** 1M requests/month free
- **After Free Tier:** ~$0.20 per 1M requests
- **Compute:** $0.0000166667 per GB-second

Very affordable for most use cases! 💰

