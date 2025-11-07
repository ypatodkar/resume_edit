# 🔧 CORS Fix - Step by Step

## Current Issues

1. ❌ Double slash in URL: `//optimize/text` 
2. ❌ CORS headers not present in response
3. ❌ Lambda function may not be updated

## Step 1: Rebuild Lambda Package

```bash
cd backend-nodejs
npm install
zip -r lambda_deployment.zip . -x "*.git*" "node_modules/.cache/*" "*.log"
```

## Step 2: Upload to Lambda

1. Go to [AWS Lambda Console](https://console.aws.amazon.com/lambda)
2. Select your function
3. Click **"Upload from"** → **".zip file"**
4. Upload `lambda_deployment.zip`
5. Wait for upload to complete ✅

## Step 3: Configure Function URL CORS

1. Go to **Configuration** → **Function URL**
2. Click **"Edit"**
3. **Enable CORS** (toggle ON)
4. Set:
   - **Allow origins:** `*` (or `https://main.d1hmnkmby0w01s.amplifyapp.com`)
   - **Allow methods:** `GET`, `POST`
   - **Allow headers:** `Content-Type`
5. Click **"Save"**

## Step 4: Fix Frontend URL (Double Slash)

### Option A: Fix Environment Variable in Amplify

1. Go to [AWS Amplify Console](https://console.aws.amazon.com/amplify)
2. Select your app
3. Go to **Environment variables**
4. Find `VITE_API_URL`
5. **Remove trailing slash** if present:
   - ❌ Wrong: `https://...lambda-url.on.aws/`
   - ✅ Correct: `https://...lambda-url.on.aws`
6. **Save** and **Redeploy**

### Option B: Fix in Code (Already Done)

The code already normalizes URLs, but you need to redeploy frontend:

```bash
cd frontend
npm run build
# Then redeploy to Amplify
```

## Step 5: Test CORS

### Test OPTIONS (Preflight)

```bash
curl -X OPTIONS https://jrdh2glkrlugxuedfmh3fhgpm40zzpbr.lambda-url.us-east-2.on.aws/optimize/text \
  -H "Origin: https://main.d1hmnkmby0w01s.amplifyapp.com" \
  -H "Access-Control-Request-Method: POST" \
  -v
```

**Expected response:**
```
< HTTP/1.1 200 OK
< Access-Control-Allow-Origin: *
< Access-Control-Allow-Methods: GET,POST,OPTIONS
< Access-Control-Allow-Headers: Content-Type,Authorization
```

### Test POST Request

```bash
curl -X POST https://jrdh2glkrlugxuedfmh3fhgpm40zzpbr.lambda-url.us-east-2.on.aws/optimize/text \
  -H "Content-Type: application/json" \
  -H "Origin: https://main.d1hmnkmby0w01s.amplifyapp.com" \
  -d '{"resume_text":"test","job_description":"test"}' \
  -v
```

**Should return:** JSON response with CORS headers

## Step 6: Check CloudWatch Logs

1. Go to Lambda → **Monitor** → **View CloudWatch logs**
2. Look for:
   - `Event structure:` - Shows event format
   - `Request: OPTIONS /optimize/text` - Shows OPTIONS being handled
   - `Handling OPTIONS preflight request` - Confirms handler is working

## Common Issues

### Still Getting CORS Error?

1. **Clear browser cache** - CORS errors can be cached
2. **Check Function URL CORS is enabled** in Lambda Console
3. **Verify Lambda code is updated** - Check CloudWatch logs
4. **Check for double slash** - Should be `/optimize/text` not `//optimize/text`

### OPTIONS Request Not Working?

- Check CloudWatch logs to see if OPTIONS request reaches Lambda
- Verify handler returns 200 with CORS headers
- Ensure Function URL CORS is enabled

### Double Slash Still There?

- Check Amplify environment variable `VITE_API_URL`
- Remove trailing slash
- Redeploy frontend

## Quick Verification

Run this in browser console on your Amplify site:

```javascript
fetch('https://jrdh2glkrlugxuedfmh3fhgpm40zzpbr.lambda-url.us-east-2.on.aws/optimize/text', {
  method: 'OPTIONS',
  headers: {
    'Origin': 'https://main.d1hmnkmby0w01s.amplifyapp.com',
    'Access-Control-Request-Method': 'POST'
  }
})
.then(r => {
  console.log('Status:', r.status);
  console.log('Headers:', [...r.headers.entries()]);
  return r.text();
})
.then(console.log)
.catch(console.error);
```

**Should show:**
- Status: 200
- Headers include: `Access-Control-Allow-Origin: *`

## Summary Checklist

- [ ] Lambda function updated with new code
- [ ] Function URL CORS enabled in Lambda Console
- [ ] Frontend environment variable has no trailing slash
- [ ] Frontend redeployed to Amplify
- [ ] Tested OPTIONS request returns CORS headers
- [ ] Browser cache cleared

After completing all steps, CORS should work! 🎉

