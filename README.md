# Resume Auto Editor

Automatically optimize your resume to match job descriptions using Google's Gemini AI and apply edits directly to Google Docs.

## Project Structure

```
Resume Auto Editor/
├── backend/             # Backend code and scripts
│   ├── app.py               # Flask API server
│   ├── test_api.py          # API test script
│   ├── requirements.txt     # Python dependencies
│   ├── API_DOCUMENTATION.md # API documentation
│   ├── scripts/             # Executable scripts
│   │   ├── resume_optimizer.py    # Main script to generate resume edits
│   │   ├── edit_google_docs.py     # Apply edits to Google Docs
│   │   ├── view_edits.py           # View edits in readable format
│   │   └── debug_google_docs.py    # Debug Google Docs structure
│   ├── src/                  # Source code modules
│   │   ├── config.py              # Configuration and file paths
│   │   ├── file_utils.py          # File reading utilities
│   │   ├── prompt_builder.py      # Gemini prompt construction
│   │   ├── gemini_client.py       # Gemini API client
│   │   ├── json_utils.py          # JSON handling utilities
│   │   └── google_docs_editor.py  # Google Docs API integration
│   ├── token.pickle        # Google auth token (if exists)
│   └── credentials.json    # Google credentials (if exists)
├── data/                 # Data files
│   ├── input/                # Input files
│   │   ├── resume.docx           # Your resume (Word format)
│   │   └── job_description.txt   # Job description text
│   └── output/              # Generated output
│       └── resume_edits.json     # Generated resume edits (JSON)
├── frontend/            # React frontend application
│   ├── src/                # React source code
│   ├── public/             # Public assets
│   └── package.json        # Frontend dependencies
├── output/               # Raw API responses (for debugging)
├── .gitignore           # Git ignore rules
└── README.md            # This file
```

## Quick Start

### Option 1: Command Line Scripts

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Place your files:**
   - Put your resume in `data/input/resume.docx`
   - Put the job description in `data/input/job_description.txt`

3. **Generate resume edits:**
   ```bash
   python backend/scripts/resume_optimizer.py
   ```

4. **View the edits:**
   ```bash
   python backend/scripts/view_edits.py
   ```

5. **Apply to Google Docs (optional):**
   ```bash
   python backend/scripts/edit_google_docs.py
   ```
   - Requires Google Cloud setup (see below)

### Option 2: Flask API (Web Service)

1. **Install dependencies:**
   ```bash
   pip install -r backend/requirements.txt
   ```

2. **Start the Flask server:**
   ```bash
   cd backend
   python app.py
   ```
   Or from project root:
   ```bash
   python backend/app.py
   ```

3. **Use the API:**
   - Health check: `GET http://localhost:8000/health`
   - Optimize resume: `POST http://localhost:8000/optimize`
   - See `backend/API_DOCUMENTATION.md` for detailed API documentation
   - **Note:** Default port is 8000 (to avoid macOS AirPlay Receiver conflict on port 5000)

4. **Test the API:**
   ```bash
   python backend/test_api.py
   ```

### Option 3: React Frontend (Web UI)

1. **Install Node.js** (if not already installed)
   - Download from https://nodejs.org/

2. **Install frontend dependencies:**
   ```bash
   cd frontend
   npm install
   ```

3. **Start the frontend:**
   ```bash
   npm start
   ```
   The app will open at `http://localhost:3000`

4. **Make sure the backend API is running:**
   ```bash
   # In a separate terminal
   cd backend
   python app.py
   ```

5. **Use the web interface:**
   - Paste your resume text in the first textarea
   - Paste the job description in the second textarea
   - Click "Optimize Resume"
   - View results in a beautiful, formatted display

## Google Docs Integration Setup

1. **Set up Google Cloud Project:**
   - Go to https://console.cloud.google.com/
   - Create a new project
   - Enable Google Docs API
   - Create OAuth 2.0 credentials (Desktop app)
   - Download `credentials.json` and place it in the project root

2. **Add yourself as a test user:**
   - Go to "APIs & Services" → "OAuth consent screen"
   - Click "Test users" tab
   - Add your email address

3. **Run the editor:**
   ```bash
   python scripts/edit_google_docs.py
   ```

## Usage

### Generate Resume Edits

```bash
python scripts/resume_optimizer.py
```

This will:
- Read your resume and job description
- Use Gemini AI to generate optimized edits
- Save results to `data/output/resume_edits.json`

### View Edits

```bash
python scripts/view_edits.py
```

Displays all edits in a readable format for manual copy-paste.

### Apply to Google Docs

```bash
python scripts/edit_google_docs.py
```

Automatically applies edits to your Google Docs resume while preserving formatting.

### Debug Google Docs

```bash
python scripts/debug_google_docs.py
```

Helps diagnose issues with finding section headers in your Google Doc.

## Configuration

Edit `src/config.py` to:
- Change file paths
- Update Gemini API key
- Modify model settings

## Features

- ✅ Automatic keyword extraction from job descriptions
- ✅ Smart decision-making: only changes what's necessary
- ✅ Summary optimization (under 34 words)
- ✅ Technical skills alignment
- ✅ Project point updates (when needed, max 25 words)
- ✅ Formatting preservation in Google Docs
- ✅ Partial text replacements throughout resume

## Requirements

- Python 3.7+
- Google Generative AI API key
- Google Cloud credentials (for Google Docs integration)

## Notes

- The script preserves formatting when possible
- Some sections may need manual updates if headers don't match
- All edits are saved in JSON format for review
- Raw API responses are saved in `output/` for debugging

