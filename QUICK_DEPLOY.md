# Quick Deployment Guide

## Prerequisites

1. **AWS Account** with appropriate permissions
2. **AWS CLI** installed and configured: `aws configure`
3. **Node.js** installed (for Serverless Framework)
4. **Python 3.11+** installed

## Step 1: Install Serverless Framework

```bash
npm install -g serverless
```

## Step 2: Deploy Backend (Lambda)

```bash
cd backend

# Install serverless plugins
npm install

# Set your Gemini API key
export GEMINI_API_KEY="your-api-key-here"

# Deploy to AWS
serverless deploy
```

After deployment, you'll get an API URL like:
```
https://xxxxx.execute-api.us-east-1.amazonaws.com/dev
```

**Save this URL!**

## Step 3: Deploy Frontend (Amplify)

### Option A: Using AWS Console (Recommended)

1. Go to [AWS Amplify Console](https://console.aws.amazon.com/amplify)
2. Click **"New app"** → **"Host web app"**
3. Select **GitHub** and authorize
4. Select repository: `ypatodkar/resume_edit`
5. Branch: `main`
6. Build settings: Use `amplify.yml` (auto-detected)
7. **Add environment variable:**
   - Key: `VITE_API_URL`
   - Value: `https://your-lambda-url.execute-api.us-east-1.amazonaws.com/dev`
8. Click **"Save and deploy"**

### Option B: Using AWS CLI

```bash
# Install Amplify CLI
npm install -g @aws-amplify/cli

# Initialize Amplify
cd frontend
amplify init

# Add hosting
amplify add hosting

# Publish
amplify publish
```

## Step 4: Update CORS (if needed)

If you get CORS errors, update `backend/serverless.yml`:

```yaml
cors:
  origin: 'https://your-amplify-url.amplifyapp.com'
```

Then redeploy:
```bash
cd backend
serverless deploy
```

## Environment Variables

### Lambda (Backend)
Set in `serverless.yml` or AWS Console:
- `GEMINI_API_KEY`: Your Gemini API key
- `MODEL_NAME`: `gemini-2.5-pro` (optional)

### Amplify (Frontend)
Set in Amplify Console:
- `VITE_API_URL`: Your Lambda API Gateway URL

## Testing

1. Visit your Amplify URL
2. Test the resume optimization feature
3. Check CloudWatch logs if there are issues

## Updating

### Update Backend:
```bash
cd backend
serverless deploy
```

### Update Frontend:
- Push to GitHub (Amplify auto-deploys)
- Or manually trigger in Amplify Console

## Troubleshooting

### Lambda Timeout
Increase timeout in `serverless.yml`:
```yaml
timeout: 60
```

### CORS Issues
1. Check CORS settings in `serverless.yml`
2. Verify `VITE_API_URL` in Amplify
3. Check browser console for errors

### Module Not Found
Make sure all dependencies are in `requirements.txt` and `serverless.yml` has proper Python requirements configuration.

## Cost Estimate

- **Lambda**: ~$0.20 per 1M requests
- **API Gateway**: First 1M requests/month free
- **Amplify**: Free tier includes 15 GB storage, 5 GB served/month
- **Total**: Essentially free for low-medium traffic

## Cleanup

```bash
# Remove Lambda
cd backend
serverless remove

# Remove Amplify app
# Go to Amplify Console → Delete app
```

