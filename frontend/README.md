# Resume Optimizer Frontend

React frontend for the Resume Optimizer API.

## Features

- 📝 Input resume text and job description
- 🚀 Optimize resume with AI
- ✨ Beautiful, formatted display of results
- 📋 Copy buttons for easy copying
- 📱 Responsive design
- 🎨 Modern UI with gradient backgrounds

## Setup

1. **Install dependencies:**
   ```bash
   cd frontend
   npm install
   ```

2. **Start the development server:**
   ```bash
   npm start
   ```

3. **Make sure the backend API is running:**
   ```bash
   cd ../backend
   python app.py
   ```

The frontend will run on `http://localhost:3000` and will proxy API requests to `http://localhost:8000`.

## Environment Variables

Create a `.env` file in the `frontend` directory to customize the API URL:

```
REACT_APP_API_URL=http://localhost:8000
```

## Build for Production

```bash
npm run build
```

This creates an optimized production build in the `build` folder.

## Features

- **Tabbed Interface**: View summary, skills, work experience section, projects, and notes separately
- **Word Count Validation**: Shows if summary is under 33 words and work experience line is under 15 words
- **Copy Buttons**: Easy copy-to-clipboard functionality
- **Status Badges**: Visual indicators for project changes
- **Raw JSON Viewer**: Expandable section to view the raw API response
- **Responsive Design**: Works on desktop and mobile devices

