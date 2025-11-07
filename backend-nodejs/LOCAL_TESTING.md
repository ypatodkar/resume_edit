# 🧪 Local Testing Guide

Test your Lambda function locally before deploying!

## Prerequisites

- Node.js 18+ installed
- Gemini API key
- Dependencies installed (`npm install`)

## Method 1: Run as Express Server (Recommended) 🚀

The code already supports running as a local Express server!

### Step 1: Set Environment Variable

```bash
export GEMINI_API_KEY=your-api-key-here
```

Or create a `.env` file (see Method 3).

### Step 2: Run the Server

```bash
cd backend-nodejs
npm install
node index.js
```

You should see:
```
🚀 Server running on http://localhost:8000
```

### Step 3: Test Endpoints

#### Health Check
```bash
curl http://localhost:8000/health
```

#### Optimize Resume
```bash
curl -X POST http://localhost:8000/optimize/text \
  -H "Content-Type: application/json" \
  -d '{
    "resume_text": "Software Engineer with 5 years experience",
    "job_description": "Looking for a senior developer"
  }'
```

## Method 2: Test Lambda Handler Directly 🎯

Use the test script to simulate Lambda events:

### Step 1: Set API Key

```bash
export GEMINI_API_KEY=your-api-key-here
```

### Step 2: Run Test Script

```bash
cd backend-nodejs
node test-local.js
```

This will:
- ✅ Test health endpoint
- ✅ Test optimize endpoint with sample data
- ✅ Save full response to `test-response.json`
- ✅ Show timing and status

## Method 3: Use Environment File (.env) 📝

### Step 1: Create `.env` file

```bash
cd backend-nodejs
echo "GEMINI_API_KEY=your-api-key-here" > .env
```

### Step 2: Install dotenv (if not already)

```bash
npm install dotenv
```

### Step 3: Update index.js to load .env

Add at the top of `index.js`:

```javascript
require('dotenv').config();
```

### Step 4: Run

```bash
node index.js
```

## Method 4: Test with Postman/Thunder Client 🛠️

### Setup

1. Start server: `node index.js`
2. Open Postman or VS Code Thunder Client

### Endpoints

**Health Check:**
- Method: `GET`
- URL: `http://localhost:8000/health`

**Optimize Resume:**
- Method: `POST`
- URL: `http://localhost:8000/optimize/text`
- Headers: `Content-Type: application/json`
- Body:
```json
{
  "resume_text": "Your resume text here...",
  "job_description": "Your job description here...",
  "custom_prompt": "Optional custom prompt"
}
```

## Method 5: Test with Frontend Locally 🔗

### Step 1: Start Backend

```bash
cd backend-nodejs
GEMINI_API_KEY=your-key node index.js
```

### Step 2: Update Frontend .env

Create/update `frontend/.env.local`:

```bash
VITE_API_URL=http://localhost:8000
```

### Step 3: Start Frontend

```bash
cd frontend
npm install
npm run dev
```

### Step 4: Test in Browser

Open `http://localhost:5173` (or your Vite port) and test the full flow!

## Sample Test Data

### Minimal Test

```json
{
  "resume_text": "Software Engineer",
  "job_description": "Looking for developer"
}
```

### Full Test

See `test-local.js` for a complete example with:
- Resume with skills, experience, projects
- Detailed job description
- All sections populated

## Troubleshooting

### Error: "GEMINI_API_KEY not set"

```bash
export GEMINI_API_KEY=your-key
# Or use .env file
```

### Error: "Cannot find module"

```bash
npm install
```

### Error: "Port 8000 already in use"

Change port in `index.js`:
```javascript
const PORT = process.env.PORT || 8001; // Use different port
```

### Error: "ECONNREFUSED"

- Make sure server is running
- Check the port number
- Try `curl http://localhost:8000/health` first

### Slow Response?

- Normal: Gemini API calls take 10-30 seconds
- Check your internet connection
- Verify API key is valid

## Expected Output

### Health Check Response

```json
{
  "status": "healthy",
  "service": "Resume Optimizer API",
  "version": "1.0.0"
}
```

### Optimize Response

```json
{
  "intro_note": "...",
  "summary": "Rewritten summary...",
  "technical_skills": "Updated skills...",
  "work_experience_section": {
    "new_line": "New work experience line"
  },
  "projects": [
    {
      "project_name": "Project Name",
      "status": "modified",
      "changes": {
        "old_point": "...",
        "new_point": "..."
      }
    }
  ],
  "overall_notes": "..."
}
```

## Quick Test Commands

```bash
# 1. Install dependencies
npm install

# 2. Set API key
export GEMINI_API_KEY=your-key

# 3. Run server
node index.js

# 4. In another terminal, test health
curl http://localhost:8000/health

# 5. Test optimize
curl -X POST http://localhost:8000/optimize/text \
  -H "Content-Type: application/json" \
  -d '{"resume_text":"Test","job_description":"Test JD"}'
```

## Next Steps

Once local testing works:
1. ✅ Verify all endpoints work
2. ✅ Check response format
3. ✅ Test with real resume data
4. ✅ Deploy to Lambda (see DEPLOY_LAMBDA.md)

Happy testing! 🎉

