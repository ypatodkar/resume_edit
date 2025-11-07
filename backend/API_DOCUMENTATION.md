# Resume Optimizer API Documentation

Flask REST API for optimizing resumes based on job descriptions using Google's Gemini AI.

## Base URL

```
http://localhost:8000
```

**Note:** Default port is 8000 to avoid macOS AirPlay Receiver conflict. You can change it using the `PORT` environment variable.

## Endpoints

### 1. Health Check

**GET** `/health`

Check if the API is running.

**Response:**
```json
{
  "status": "healthy",
  "service": "Resume Optimizer API",
  "version": "1.0.0"
}
```

---

### 2. Optimize Resume (File or Text)

**POST** `/optimize`

Optimize resume from uploaded file or text input.

**Content-Type:** `multipart/form-data` or `application/json`

**Parameters:**
- `job_description` (required): Job description text
- `resume_file` (optional): `.docx` file upload
- `resume_text` (optional): Plain text resume (required if `resume_file` not provided)
- `parallel` (optional, query param): Enable parallel processing (default: `true`). Set to `false` to use sequential processing.

**Example 1: File Upload (multipart/form-data)**
```bash
curl -X POST http://localhost:8000/optimize \
  -F "job_description=Software Engineer with 5+ years..." \
  -F "resume_file=@resume.docx"
```

**Example 2: Text Input (multipart/form-data)**
```bash
curl -X POST http://localhost:8000/optimize \
  -F "job_description=Software Engineer with 5+ years..." \
  -F "resume_text=John Doe Software Engineer..."
```

**Example 3: JSON (application/json)**
```bash
curl -X POST http://localhost:8000/optimize \
  -H "Content-Type: application/json" \
  -d '{
    "job_description": "Software Engineer with 5+ years...",
    "resume_text": "John Doe Software Engineer..."
  }'
```

**Response:**
```json
{
  "intro_note": "Of course. Here are the final, minimal changes to incorporate these last keywords.",
  "summary": "Software Engineer with expertise in...",
  "technical_skills": "**Specialties / Architecture & Design / Core Skills**\n...",
  "work_experience_section": {
    "new_line": "Enhanced security monitoring with..."
  },
  "projects": [
    {
      "project_name": "Project Name",
      "status": "modified",
      "changes": {
        "old_point": "Old bullet point...",
        "new_point": "New optimized bullet point...",
        "old_technologies": "Python, Flask",
        "new_technologies": "Python, Flask, FastAPI"
      }
    },
    {
      "project_name": "Another Project",
      "status": "no_changes"
    }
  ],
  "overall_notes": "The resume was optimized to align with..."
}
```

---

### 3. Optimize Resume (Text Only - JSON)

**POST** `/optimize/text`

Simplified endpoint that only accepts JSON with text inputs.

**Content-Type:** `application/json`

**Request Body:**
```json
{
  "resume_text": "John Doe\nSoftware Engineer\n...",
  "job_description": "Software Engineer with 5+ years experience...",
  "parallel": true
}
```

**Note:** `parallel` parameter (default: `true`) enables parallel processing which can be 2-3x faster by processing different sections simultaneously.

**Example:**
```bash
curl -X POST http://localhost:8000/optimize/text \
  -H "Content-Type: application/json" \
  -d '{
    "resume_text": "John Doe\nSoftware Engineer...",
    "job_description": "Software Engineer with 5+ years..."
  }'
```

**Response:** Same as `/optimize` endpoint

---

## Error Responses

### 400 Bad Request
```json
{
  "error": "job_description is required"
}
```

### 413 Request Entity Too Large
```json
{
  "error": "File too large. Maximum size is 16MB."
}
```

### 500 Internal Server Error
```json
{
  "error": "Error extracting JSON from Gemini response: ...",
  "raw_response": "..."
}
```

---

## Python Client Example

```python
import requests

# Using file upload
with open('resume.docx', 'rb') as f:
    files = {'resume_file': f}
    data = {
        'job_description': 'Software Engineer with 5+ years...'
    }
    response = requests.post('http://localhost:8000/optimize', files=files, data=data)
    result = response.json()
    print(result)

# Using text input
data = {
    'resume_text': 'John Doe\nSoftware Engineer...',
    'job_description': 'Software Engineer with 5+ years...'
}
response = requests.post('http://localhost:8000/optimize/text', json=data)
result = response.json()
print(result)
```

---

## JavaScript/TypeScript Client Example

```javascript
// Using file upload
const formData = new FormData();
formData.append('resume_file', fileInput.files[0]);
formData.append('job_description', 'Software Engineer with 5+ years...');

fetch('http://localhost:8000/optimize', {
  method: 'POST',
  body: formData
})
.then(response => response.json())
.then(data => console.log(data));

// Using text input
fetch('http://localhost:8000/optimize/text', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({
    resume_text: 'John Doe\nSoftware Engineer...',
    job_description: 'Software Engineer with 5+ years...'
  })
})
.then(response => response.json())
.then(data => console.log(data));
```

---

## Running the API

### Development
```bash
python app.py
```

### Production (using Gunicorn)
```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:8000 app:app
```

### Environment Variables
- `PORT`: Server port (default: 8000)
- `FLASK_DEBUG`: Enable debug mode (default: False)

**Note:** On macOS, port 5000 is often used by AirPlay Receiver. The default port is set to 8000 to avoid conflicts. You can override it:
```bash
PORT=5001 python app.py
```

---

## Response Format

The API returns a JSON object with the following structure:

- `intro_note`: Opening message
- `summary`: Revised summary (under 33 words)
- `technical_skills`: Revised technical skills in grouped format
- `work_experience_section`: Object with `new_line` (≤ 15 words)
- `projects`: Array of project objects with status and changes
- `overall_notes`: Summary of changes made

---

## Notes

- Maximum file size: 16MB
- Supported file formats: `.docx` only
- The API uses Google's Gemini AI for optimization
- All responses are in JSON format
- CORS is enabled for all origins

