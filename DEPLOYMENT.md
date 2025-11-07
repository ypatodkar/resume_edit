# Deployment Guide: AWS Amplify + Lambda

This guide will help you deploy the Resume Optimizer application to AWS.

## Architecture

- **Frontend**: React app deployed on AWS Amplify
- **Backend**: Flask API deployed on AWS Lambda with API Gateway

## Prerequisites

1. AWS Account
2. AWS CLI installed and configured
3. Node.js and npm installed
4. Python 3.11+ installed
5. Serverless Framework installed globally: `npm install -g serverless`

## Part 1: Deploy Backend to AWS Lambda

### Step 1: Install Serverless Framework

```bash
npm install -g serverless
```

### Step 2: Install Serverless Plugins

```bash
cd backend
npm init -y
npm install --save-dev serverless-python-requirements serverless-wsgi
```

### Step 3: Configure Environment Variables

Create a `.env` file in the backend directory (or set environment variables):

```bash
export GEMINI_API_KEY="your-gemini-api-key"
export MODEL_NAME="gemini-2.5-pro"
```

### Step 4: Deploy to Lambda

```bash
cd backend
serverless deploy
```

This will:
- Create a Lambda function
- Set up API Gateway
- Return an API endpoint URL (e.g., `https://xxxxx.execute-api.us-east-1.amazonaws.com/dev`)

### Step 5: Note the API Endpoint

After deployment, you'll see output like:
```
endpoints:
  ANY - https://xxxxx.execute-api.us-east-1.amazonaws.com/dev/{proxy+}
  ANY - https://xxxxx.execute-api.us-east-1.amazonaws.com/dev
```

**Save this URL** - you'll need it for the frontend configuration.

## Part 2: Deploy Frontend to AWS Amplify

### Step 1: Push Code to GitHub

Make sure your code is pushed to GitHub (already done).

### Step 2: Create Amplify App

1. Go to [AWS Amplify Console](https://console.aws.amazon.com/amplify)
2. Click "New app" → "Host web app"
3. Select "GitHub" and authorize
4. Select your repository: `ypatodkar/resume_edit`
5. Configure build settings:
   - App name: `resume-optimizer`
   - Environment: `amplify.yml` (already in repo)
   - Build settings: Use the `amplify.yml` file

### Step 3: Configure Environment Variables

In Amplify Console → App settings → Environment variables, add:

```
VITE_API_URL=https://your-lambda-api-url.execute-api.us-east-1.amazonaws.com/dev
```

Replace `your-lambda-api-url` with your actual Lambda API Gateway URL from Part 1.

### Step 4: Deploy

1. Click "Save and deploy"
2. Amplify will build and deploy your frontend
3. You'll get a URL like: `https://main.xxxxx.amplifyapp.com`

## Part 3: Update CORS Settings

### Update Lambda CORS

In your `serverless.yml`, the CORS is already configured. If you need to restrict to your Amplify domain:

```yaml
cors:
  origin: 'https://your-amplify-url.amplifyapp.com'
```

Then redeploy:
```bash
cd backend
serverless deploy
```

## Part 4: Testing

1. Visit your Amplify URL
2. Test the resume optimization
3. Check CloudWatch logs for Lambda if there are issues

## Troubleshooting

### Lambda Timeout Issues

If requests timeout, increase timeout in `serverless.yml`:
```yaml
timeout: 60  # Increase from 30 to 60 seconds
```

### CORS Errors

Make sure:
1. CORS is enabled in `serverless.yml`
2. Frontend uses the correct API URL
3. Headers are properly configured

### Environment Variables

Lambda environment variables are set in `serverless.yml`. To update:
1. Edit `serverless.yml`
2. Run `serverless deploy`

Or set via AWS Console:
- Lambda → Configuration → Environment variables

## Cost Optimization

- **Lambda**: Pay per request (very cheap for low traffic)
- **Amplify**: Free tier includes 15 GB storage and 5 GB served per month
- **API Gateway**: First 1 million requests/month are free

## Updating the Deployment

### Update Backend:
```bash
cd backend
serverless deploy
```

### Update Frontend:
- Push to GitHub
- Amplify will auto-deploy (if auto-deploy is enabled)
- Or manually trigger in Amplify Console

## Alternative: Using AWS SAM

If you prefer AWS SAM over Serverless Framework:

1. Create `template.yaml` (SAM template)
2. Deploy with: `sam build && sam deploy --guided`

## Security Best Practices

1. **Never commit API keys** - Use environment variables
2. **Use AWS Secrets Manager** for sensitive data
3. **Enable API Gateway throttling** to prevent abuse
4. **Use IAM roles** with least privilege
5. **Enable CloudWatch logging** for monitoring

## Monitoring

- **Lambda**: CloudWatch Logs and Metrics
- **Amplify**: Built-in monitoring dashboard
- **API Gateway**: CloudWatch metrics

## Cleanup

To remove all resources:

```bash
# Remove Lambda function
cd backend
serverless remove

# Remove Amplify app
# Go to Amplify Console → App settings → Delete app
```

