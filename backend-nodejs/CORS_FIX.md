# CORS Fix for Lambda Function URL

## Problem

CORS error when calling Lambda Function URL from Amplify frontend:
```
Access to XMLHttpRequest at 'https://...lambda-url.../optimize/text' 
from origin 'https://...amplifyapp.com' has been blocked by CORS policy: 
No 'Access-Control-Allow-Origin' header is present
```

## Solution

### 1. Lambda Handler Fix ✅

The handler now:
- ✅ Properly handles Lambda Function URL events (different structure than API Gateway)
- ✅ Returns CORS headers in ALL responses (including errors)
- ✅ Handles OPTIONS preflight requests correctly
- ✅ Normalizes paths (handles double slashes, trailing slashes)

### 2. Lambda Function URL Configuration

When creating/updating your Function URL:

1. Go to Lambda Console → Your Function → Configuration → Function URL
2. Click "Edit" or "Create function URL"
3. Set:
   - **Auth type:** `NONE` (or `AWS_IAM` if you want security)
   - **CORS:** ✅ **Enable CORS**
   - **Allow origins:** `*` (or your specific domain)
   - **Allow methods:** `GET, POST, OPTIONS`
   - **Allow headers:** `Content-Type, Authorization`
   - **Expose headers:** (leave empty or add if needed)
   - **Max age:** `86400` (24 hours)

4. Click **"Save"**

### 3. Frontend URL Fix

Also noticed a double slash in your URL: `//optimize/text`

Check your frontend `.env` file:

```bash
# ❌ Wrong (has trailing slash)
VITE_API_URL=https://your-lambda-url.on.aws/

# ✅ Correct (no trailing slash)
VITE_API_URL=https://your-lambda-url.on.aws
```

Or in your code, ensure no double slashes:

```typescript
// In App.tsx
const API_URL = import.meta.env.VITE_API_URL?.replace(/\/$/, '') || 'http://localhost:8000';
```

## Testing

### Test CORS with curl

```bash
# Test OPTIONS (preflight)
curl -X OPTIONS https://your-lambda-url.on.aws/optimize/text \
  -H "Origin: https://main.d1hmnkmby0w01s.amplifyapp.com" \
  -H "Access-Control-Request-Method: POST" \
  -v

# Should return:
# Access-Control-Allow-Origin: *
# Access-Control-Allow-Methods: GET,POST,OPTIONS
```

### Test from Browser Console

```javascript
fetch('https://your-lambda-url.on.aws/optimize/text', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    resume_text: 'Test',
    job_description: 'Test JD'
  })
})
.then(r => r.json())
.then(console.log)
.catch(console.error);
```

## Redeploy

After fixing the code:

1. **Rebuild zip:**
   ```bash
   cd backend-nodejs
   npm install
   zip -r lambda_deployment.zip . -x "*.git*"
   ```

2. **Upload to Lambda:**
   - Go to Lambda Console
   - Upload new `lambda_deployment.zip`
   - Or use: `aws lambda update-function-code --function-name your-function --zip-file fileb://lambda_deployment.zip`

3. **Verify Function URL CORS:**
   - Check Configuration → Function URL
   - Ensure CORS is enabled

4. **Test:**
   - Try from your Amplify frontend
   - Check browser console for errors

## Common Issues

### Still getting CORS error?

1. **Check Function URL CORS is enabled** in Lambda Console
2. **Verify headers are in response** - check Network tab in browser
3. **Check for double slashes** in URL (`//optimize/text`)
4. **Clear browser cache** - sometimes cached CORS errors persist

### OPTIONS request failing?

- Lambda handler must return 200 for OPTIONS
- Must include all CORS headers
- Body should be empty string

### Different error?

- Check CloudWatch logs for Lambda errors
- Verify API key is set correctly
- Check request format matches expected structure

## Summary

✅ **Fixed:** Handler now properly handles Function URL events and CORS  
✅ **Action needed:** Enable CORS in Lambda Function URL settings  
✅ **Action needed:** Fix double slash in frontend URL if present  

After these changes, CORS should work! 🎉

