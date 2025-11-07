# Upload to Lambda

## Build the Zip File

**Prerequisites:** Docker Desktop must be running

```bash
cd backend
./build.sh
```

This creates `lambda_deployment.zip` - ready to upload!

## Upload Steps

1. Go to [AWS Lambda Console](https://console.aws.amazon.com/lambda)
2. Create function (or select existing)
3. Upload `lambda_deployment.zip`
4. **Handler:** `lambda_handler.lambda_handler`
5. **Runtime:** `Python 3.11`
6. **Environment variable:** `GEMINI_API_KEY` = your-api-key
7. **Timeout:** 60 seconds
8. **Memory:** 512 MB

Done! Your Lambda function will work.

