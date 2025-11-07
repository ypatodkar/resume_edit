# 📝 How Prompt Editing Works

## Overview

The prompt editor allows you to customize the AI prompt **for the current browser session only**. This lets you experiment with different prompts without changing the app's default behavior.

## How It Works

### 1. **Session-Based Storage** (Frontend)

- Uses React Context API (`PromptContext`) to store the custom prompt
- Stored in **memory only** (not saved to database or localStorage)
- **Lost when you refresh the page** - returns to default prompt
- This ensures it's truly "session-only" and doesn't persist

### 2. **Frontend Flow**

```
User clicks "⚙️ Edit Prompt" button
    ↓
Navigates to /prompt-editor page
    ↓
User edits prompt in textarea
    ↓
Clicks "Save for Session"
    ↓
Prompt stored in React Context
    ↓
Returns to main page
    ↓
Warning indicator shows: "⚠️ Using custom prompt for this session"
    ↓
When user submits resume optimization
    ↓
Custom prompt is included in API request
```

### 3. **Backend Processing**

When the API receives a request:

```javascript
// In backend-nodejs/index.js

function buildPrompt(jdText, resumeText, customPrompt = null) {
  if (customPrompt) {
    // Use custom prompt and replace placeholders
    return customPrompt
      .replace('{jd_text}', jdText)
      .replace('{resume_text}', resumeText);
  }
  
  // Otherwise use default prompt
  return `[default prompt template]...`;
}
```

**Key Points:**
- If `custom_prompt` is provided → Use it (with placeholder replacement)
- If not provided → Use default prompt
- Placeholders `{jd_text}` and `{resume_text}` are replaced with actual values

### 4. **API Request**

When you submit a resume optimization:

```javascript
// Frontend sends:
{
  "resume_text": "...",
  "job_description": "...",
  "custom_prompt": "Your custom prompt here..."  // Only if set
}
```

## Features

### ✅ What You Can Do

1. **Edit the Prompt**
   - Click "⚙️ Edit Prompt" button
   - Modify the prompt in the textarea
   - Use placeholders: `{jd_text}` and `{resume_text}`

2. **Save for Session**
   - Click "Save for Session"
   - Prompt is stored in memory
   - Warning indicator appears on main page

3. **Reset to Default**
   - Click "Reset to Default"
   - Restores the original default prompt

4. **Clear Custom Prompt**
   - Click "Clear Custom Prompt"
   - Removes custom prompt
   - Returns to using default prompt

### ⚠️ Limitations

1. **Session-Only**
   - Not saved to database
   - Lost on page refresh
   - Not shared across browser tabs

2. **No Validation**
   - No syntax checking
   - No format validation
   - You're responsible for correct JSON schema

3. **Placeholder Replacement**
   - Simple string replacement
   - No advanced templating
   - Must use exact placeholders: `{jd_text}` and `{resume_text}`

## Example Usage

### Default Prompt (Built-in)

The default prompt includes:
- Summary requirements (under 33 words)
- Technical skills formatting
- Projects modification rules (2 projects)
- Work experience section (≤ 15 words)
- JSON output schema

### Custom Prompt Example

You could create a custom prompt like:

```
You are a resume optimizer. 

Job Description:
{jd_text}

Resume:
{resume_text}

Please optimize the resume to match the job description.
Return JSON with summary, skills, and projects.
```

**Note:** This is simplified - you'd need to include the full JSON schema requirements.

## Code Structure

### Frontend Components

1. **PromptContext** (`frontend/src/contexts/PromptContext.tsx`)
   - React Context for storing custom prompt
   - Provides `customPrompt`, `setCustomPrompt`, `clearCustomPrompt`

2. **PromptEditor** (`frontend/src/pages/PromptEditor.tsx`)
   - Page component for editing prompts
   - Textarea for editing
   - Save/Reset/Clear buttons

3. **App.tsx**
   - Checks for `customPrompt` from context
   - Includes it in API request if set
   - Shows warning indicator when custom prompt is active

### Backend

**index.js** (`backend-nodejs/index.js`)
- `buildPrompt()` function handles custom vs default
- Replaces placeholders in custom prompts
- Falls back to default if no custom prompt provided

## Testing Custom Prompts

### 1. Edit Prompt
```
1. Click "⚙️ Edit Prompt"
2. Modify the prompt
3. Click "Save for Session"
```

### 2. Test It
```
1. Go back to main page
2. Enter resume and job description
3. Submit
4. Check if results match your custom prompt
```

### 3. Verify
- Check the warning indicator shows
- Results should reflect your custom prompt's instructions
- JSON structure should still be valid

## Best Practices

1. **Keep JSON Schema**
   - Always include the JSON output schema in your custom prompt
   - Ensure it matches the expected structure

2. **Use Placeholders**
   - Always include `{jd_text}` and `{resume_text}` placeholders
   - Backend will replace them automatically

3. **Test First**
   - Test with a simple resume first
   - Verify JSON output is valid
   - Check all required fields are present

4. **Document Changes**
   - Note what you changed and why
   - Keep a copy of working custom prompts

## Troubleshooting

### Custom Prompt Not Working?

1. **Check if it's saved**
   - Look for warning indicator on main page
   - If missing, prompt wasn't saved

2. **Check placeholders**
   - Must use exact: `{jd_text}` and `{resume_text}`
   - Case-sensitive

3. **Check JSON Schema**
   - Custom prompt must still output valid JSON
   - Include schema requirements in your prompt

4. **Check Browser Console**
   - Look for errors in Network tab
   - Verify `custom_prompt` is in request body

### Prompt Lost After Refresh?

- **This is expected behavior!**
- Custom prompts are session-only
- Refresh = back to default prompt
- This is by design to prevent accidental persistence

## Summary

The prompt editor is a **session-based, in-memory** feature that:
- ✅ Lets you customize prompts temporarily
- ✅ Doesn't persist across page refreshes
- ✅ Doesn't affect other users
- ✅ Easy to reset to default
- ⚠️ Requires you to maintain JSON schema
- ⚠️ No validation or error checking

Perfect for experimenting with different prompt strategies! 🎯

