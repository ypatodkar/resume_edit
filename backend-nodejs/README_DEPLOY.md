# 📚 Complete Deployment Guide

## Quick Links

- **Quick Start:** [QUICK_DEPLOY.md](./QUICK_DEPLOY.md) - 5 minute guide
- **Detailed Guide:** [DEPLOY_LAMBDA.md](./DEPLOY_LAMBDA.md) - Full instructions
- **Comparison:** [COMPARISON.md](./COMPARISON.md) - Node.js vs Python

## Your Deployment Package

✅ **Ready to upload:** `lambda_deployment.zip` (1.0 MB)

## Three Ways to Deploy

### 1. AWS Console (Recommended for First Time) 🖥️

**Best for:** Beginners, visual learners

See [QUICK_DEPLOY.md](./QUICK_DEPLOY.md) for step-by-step screenshots guide.

### 2. AWS CLI (Fast Updates) ⚡

**Best for:** Quick updates after initial setup

```bash
# First time - create function
aws lambda create-function \
  --function-name resume-optimizer-api \
  --runtime nodejs18.x \
  --role arn:aws:iam::ACCOUNT:role/lambda-role \
  --handler index.handler \
  --zip-file fileb://lambda_deployment.zip \
  --timeout 60 \
  --memory-size 512 \
  --environment Variables="{GEMINI_API_KEY=your-key}"

# Updates - just upload code
aws lambda update-function-code \
  --function-name resume-optimizer-api \
  --zip-file fileb://lambda_deployment.zip
```

### 3. Deploy Script (Easiest) 🚀

```bash
cd backend-nodejs
./deploy.sh resume-optimizer-api YOUR_API_KEY
```

## Configuration Checklist

- [ ] **Handler:** `index.handler`
- [ ] **Runtime:** `Node.js 18.x` or `20.x`
- [ ] **Timeout:** `60 seconds` (or more)
- [ ] **Memory:** `512 MB` (or more)
- [ ] **Environment:** `GEMINI_API_KEY` = your key
- [ ] **Function URL:** Created and CORS enabled

## Testing

### Test in AWS Console

1. Go to Lambda function
2. Click **"Test"** tab
3. Use this test event:

```json
{
  "httpMethod": "POST",
  "path": "/optimize/text",
  "body": "{\"resume_text\":\"Software Engineer\",\"job_description\":\"Looking for developer\"}"
}
```

### Test with curl

```bash
curl -X POST https://YOUR-FUNCTION-URL/optimize/text \
  -H "Content-Type: application/json" \
  -d '{"resume_text":"Test","job_description":"Test JD"}'
```

## Common Issues

| Issue | Solution |
|-------|----------|
| Handler not found | Set to `index.handler` |
| Module not found | Rebuild zip with `npm install` |
| Timeout | Increase timeout to 60+ seconds |
| CORS error | Enable CORS in Function URL settings |

## Next Steps

1. ✅ Deploy Lambda (you're here!)
2. Create Function URL
3. Update frontend `.env` with Function URL
4. Test end-to-end
5. Deploy frontend to Amplify

## Need Help?

- Check [DEPLOY_LAMBDA.md](./DEPLOY_LAMBDA.md) for detailed troubleshooting
- AWS Lambda Docs: https://docs.aws.amazon.com/lambda/
- CloudWatch Logs: View logs in AWS Console

