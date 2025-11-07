# CORS Solution - Lambda Function URL

## Issue: No OPTIONS Method in CORS Settings

Lambda Function URL CORS settings might not show OPTIONS as an option. **This is okay!** The handler already handles OPTIONS requests.

## Solution 1: Configure CORS in Lambda Console

### Step-by-Step:

1. **Go to Lambda Console** → Your Function → **Configuration** → **Function URL**

2. **Click "Edit"** (or "Create function URL" if it doesn't exist)

3. **Set these values:**
   - **Auth type:** `NONE`
   - **CORS:** ✅ **Enable CORS** (toggle it ON)
   - **Allow origins:** `*` (or your specific domain like `https://main.d1hmnkmby0w01s.amplifyapp.com`)
   - **Allow methods:** Select `GET` and `POST` (OPTIONS is handled automatically)
   - **Allow headers:** `Content-Type, Authorization` (or just `Content-Type`)
   - **Expose headers:** (leave empty)
   - **Max age:** `86400` (optional, 24 hours)

4. **Click "Save"**

### Important Notes:

- ✅ **OPTIONS is handled automatically** by Lambda when CORS is enabled
- ✅ **Our handler also handles OPTIONS** - double protection!
- ✅ **Just select GET and POST** in the methods list
- ✅ **Use `*` for origins** if you want to allow all domains

## Solution 2: If CORS Toggle Doesn't Work

If the CORS toggle doesn't appear or work, the handler will still work because:

1. **Our handler returns CORS headers in ALL responses**
2. **Our handler handles OPTIONS requests explicitly**
3. **This works even without Lambda's CORS feature enabled**

### Test It:

```bash
# Test OPTIONS (preflight)
curl -X OPTIONS https://your-lambda-url.on.aws/optimize/text \
  -H "Origin: https://main.d1hmnkmby0w01s.amplifyapp.com" \
  -H "Access-Control-Request-Method: POST" \
  -v

# Should return 200 with CORS headers
```

## Solution 3: Use API Gateway Instead (Alternative)

If Function URL CORS is problematic, you can use API Gateway:

1. **Create API Gateway REST API**
2. **Create resource:** `/optimize`
3. **Create method:** `POST` and `OPTIONS`
4. **Point to Lambda function**
5. **Enable CORS** in API Gateway (has full OPTIONS support)
6. **Deploy API**

But Function URL should work fine with our handler!

## Current Handler Status

✅ **Already handles:**
- OPTIONS preflight requests
- CORS headers in all responses
- Function URL event structure
- Path normalization

## What to Do Now

1. **Enable CORS in Function URL** (just toggle it ON, select GET and POST)
2. **Set Allow origins:** `*` or your specific domain
3. **Set Allow headers:** `Content-Type`
4. **Save**
5. **Test from your frontend**

The handler code is already correct - it will work even if Lambda's CORS UI doesn't show OPTIONS!

## Verification

After saving, test with:

```bash
# Should return CORS headers
curl -X POST https://your-lambda-url.on.aws/optimize/text \
  -H "Content-Type: application/json" \
  -H "Origin: https://main.d1hmnkmby0w01s.amplifyapp.com" \
  -d '{"resume_text":"test","job_description":"test"}' \
  -v
```

Look for these headers in response:
- `Access-Control-Allow-Origin: *`
- `Access-Control-Allow-Methods: GET,POST,OPTIONS`
- `Access-Control-Allow-Headers: Content-Type,Authorization`

If you see these, CORS is working! 🎉

