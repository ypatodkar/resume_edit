# 🚀 Quick Deploy Guide (5 Minutes)

## ✅ Prerequisites Check

- [ ] AWS Account created
- [ ] `lambda_deployment.zip` file ready (✅ You have it!)
- [ ] Gemini API key ready

## 📋 Step-by-Step (AWS Console)

### 1️⃣ Create Lambda Function

1. Open [AWS Lambda Console](https://console.aws.amazon.com/lambda)
2. Click **"Create function"**
3. Settings:
   ```
   Function name: resume-optimizer-api
   Runtime: Node.js 18.x
   Architecture: x86_64
   ```
4. Click **"Create function"**

### 2️⃣ Upload Code

1. Scroll to **"Code source"** section
2. Click **"Upload from"** → **".zip file"**
3. Click **"Upload"** → Select `lambda_deployment.zip`
4. Wait for upload ✅

### 3️⃣ Set Handler

1. Click **"Runtime settings"** → **"Edit"**
2. Handler: `index.handler`
3. Click **"Save"**

### 4️⃣ Add Environment Variable

1. Go to **"Configuration"** tab
2. Click **"Environment variables"** → **"Edit"**
3. Add:
   ```
   Key: GEMINI_API_KEY
   Value: [Your Gemini API Key]
   ```
4. Click **"Save"**

### 5️⃣ Configure Timeout

1. **"Configuration"** → **"General configuration"** → **"Edit"**
2. Timeout: `60 seconds`
3. Memory: `512 MB`
4. Click **"Save"**

### 6️⃣ Create Function URL (For Frontend)

1. **"Configuration"** → **"Function URL"** → **"Create function URL"**
2. Auth type: `NONE` (or `AWS_IAM` for security)
3. CORS: ✅ Enable
4. Click **"Save"**
5. **Copy the URL** - You'll need this! 📋

### 7️⃣ Test It!

1. Go to **"Test"** tab
2. Create test event:
   ```json
   {
     "httpMethod": "POST",
     "path": "/optimize/text",
     "body": "{\"resume_text\":\"Test\",\"job_description\":\"Test JD\"}"
   }
   ```
3. Click **"Test"**
4. Check response ✅

## 🎯 Update Frontend

Update your frontend `.env` file:

```bash
VITE_API_URL=https://YOUR-FUNCTION-URL-HERE
```

## 🔄 Update Code Later

1. Make changes to `index.js`
2. Rebuild zip:
   ```bash
   cd backend-nodejs
   npm install
   zip -r lambda_deployment.zip . -x "*.git*"
   ```
3. Upload new zip to Lambda (same as Step 2)

## ✅ Done!

Your Lambda is deployed and ready to use! 🎉

