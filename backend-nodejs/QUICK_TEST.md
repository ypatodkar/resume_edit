# ⚡ Quick Local Test (2 Minutes)

## Step 1: Set API Key

```bash
export GEMINI_API_KEY=your-api-key-here
```

## Step 2: Install Dependencies (if not done)

```bash
cd backend-nodejs
npm install
```

## Step 3: Start Server

```bash
npm start
# or
node index.js
```

You should see:
```
🚀 Server running on http://localhost:8000
```

## Step 4: Test It!

### Option A: Test Script (Easiest)

In a **new terminal**:

```bash
cd backend-nodejs
npm test
# or
node test-local.js
```

This will:
- ✅ Test health endpoint
- ✅ Test optimize endpoint
- ✅ Show results and timing
- ✅ Save response to `test-response.json`

### Option B: Manual curl

```bash
# Health check
curl http://localhost:8000/health

# Optimize resume
curl -X POST http://localhost:8000/optimize/text \
  -H "Content-Type: application/json" \
  -d '{
    "resume_text": "Software Engineer with 5 years experience",
    "job_description": "Looking for a senior developer"
  }'
```

## Expected Output

### Health Check
```json
{"status":"healthy","service":"Resume Optimizer API","version":"1.0.0"}
```

### Optimize Response
```json
{
  "summary": "...",
  "technical_skills": "...",
  "work_experience_section": {"new_line": "..."},
  "projects": [...]
}
```

## Troubleshooting

**"GEMINI_API_KEY not set"**
```bash
export GEMINI_API_KEY=your-key
```

**"Port 8000 in use"**
- Change port: `PORT=8001 node index.js`
- Or kill process using port 8000

**"Cannot find module"**
```bash
npm install
```

## Next Steps

✅ Once local testing works → Deploy to Lambda!

See [DEPLOY_LAMBDA.md](./DEPLOY_LAMBDA.md) for deployment guide.

