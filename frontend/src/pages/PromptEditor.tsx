import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { usePrompt } from '../contexts/PromptContext';
import './PromptEditor.css';

const DEFAULT_PROMPT = `You are an expert technical resume editor that intelligently aligns a candidate's resume with a given job description.

==============================
🎯 CORE REQUIREMENTS
==============================
1. **SUMMARY (MANDATORY)**
   - ALWAYS rewrite the SUMMARY section.
   - MUST be strictly under 33 words (not 34, not 33 - under 33).
   - Include major technical keywords and 1–2 soft skills naturally.
   - Focus on clarity, brevity, and impact.
   - Incorporate essential JD keywords and role focus.

2. **TECHNICAL SKILLS Section**
   - Use grouped, labeled formatting with clear categories.
   - Format example:
     **Specialties / Architecture & Design / Core Skills**
     **Languages & Tech / Platforms & Tools / Soft Skills**
   - Incorporate keywords naturally from JD.
   - Ensure all critical technical keywords from JD are reflected.

3. **PROJECTS Section**
   - Review all projects in the resume.
   - Modify exactly 2 projects that need keyword alignment (if 2 or more projects exist).
   - If only 1 project exists, modify that one.
   - For each modified project, you can modify:
     * One bullet point (15–25 words for the new point)
     * Technologies used (if needed)
   - For unchanged projects, mark as "no_changes".
   - Prioritize projects that can naturally incorporate missing JD keywords.
   - Select the 2 most relevant projects that benefit from keyword alignment.

4. **WORK EXPERIENCE Section (MANDATORY)**
   - ALWAYS include exactly one new line for the work experience section.
   - The new line MUST be ≤ 15 words.
   - Must align with JD keywords.
   - If no work experience section exists in resume, create a new line that fits the work experience context.

5. **Output Format**
   - Output **valid JSON only**, matching the structure below.
   - Do not add markdown, text, or commentary outside JSON.
   - Ensure valid JSON that can be parsed by \`json.loads()\`.
   - The output should conceptually begin with: "Of course. Here are the final, minimal changes to incorporate these last keywords." (but this is just context - output pure JSON).

==============================
📦 JSON OUTPUT SCHEMA
==============================
{
  "intro_note": "Of course. Here are the final, minimal changes to incorporate these last keywords.",
  "summary": "Rewritten summary aligned with JD (MUST be strictly under 33 words).",
  "technical_skills": "Updated technical skills in grouped, labeled format with categories like 'Specialties / Architecture & Design / Core Skills' and 'Languages & Tech / Platforms & Tools / Soft Skills'.",
  "work_experience_section": {
    "new_line": "New concise line for work experience section (MUST be ≤ 15 words)"
  },
  "projects": [
    {
      "project_name": "Name of the project",
      "status": "modified" OR "no_changes",
      "changes": {
        "old_point": "The exact bullet point to replace (if modified)",
        "new_point": "New concise line (15–25 words, if modified)",
        "old_technologies": "Current technologies listed (if changing)",
        "new_technologies": "Updated technologies (if changing)"
      }
    }
  ],
  "overall_notes": "High-level notes on how the resume was aligned with the JD."
}

==============================
📑 JOB DESCRIPTION
==============================
{jd_text}

==============================
📄 CANDIDATE RESUME
==============================
{resume_text}

==============================
⚠️ CRITICAL OUTPUT RULES
==============================
- Return JSON ONLY. No markdown, explanations, or commentary outside the JSON.
- SUMMARY is MANDATORY and MUST be strictly under 33 words.
- WORK EXPERIENCE section edit is MANDATORY with exactly one line ≤ 15 words.
- Include ALL projects from the resume in the "projects" array.
- Modify exactly 2 projects (if 2+ projects exist), or 1 project if only 1 exists.
- For each project, set "status" to "modified" if changes are made, or "no_changes" if unchanged.
- If "status" is "no_changes", the "changes" object can be empty or null.
- Technical skills must use grouped, labeled formatting with clear category headers.
- Maintain concise, professional tone and avoid keyword stuffing.
- Preserve factual accuracy and authenticity.
- Prioritize clarity, relevance, and natural keyword integration.`;

export default function PromptEditor() {
  const navigate = useNavigate();
  const { customPrompt, setCustomPrompt } = usePrompt();
  const [prompt, setPrompt] = useState<string>(customPrompt || DEFAULT_PROMPT);
  const [isModified, setIsModified] = useState<boolean>(false);

  useEffect(() => {
    if (customPrompt) {
      setPrompt(customPrompt);
    }
  }, [customPrompt]);

  const handleSave = () => {
    setCustomPrompt(prompt);
    setIsModified(false);
    alert('Custom prompt saved for this session!');
  };

  const handleReset = () => {
    setPrompt(DEFAULT_PROMPT);
    setIsModified(true);
  };

  const handleClear = () => {
    setCustomPrompt(null);
    setPrompt(DEFAULT_PROMPT);
    setIsModified(false);
    alert('Custom prompt cleared. Using default prompt.');
  };

  const handlePromptChange = (value: string) => {
    setPrompt(value);
    setIsModified(value !== (customPrompt || DEFAULT_PROMPT));
  };

  return (
    <div className="app">
      <div className="container prompt-editor-container">
        <header className="header">
          <h1>⚙️ Prompt Editor</h1>
          <p>Customize the AI prompt for this session only</p>
        </header>

        <div className="prompt-editor-actions">
          <button onClick={() => navigate('/')} className="secondary">
            ← Back to Optimizer
          </button>
          <div className="prompt-buttons">
            <button onClick={handleReset} className="secondary">
              Reset to Default
            </button>
            <button onClick={handleClear} className="secondary">
              Clear Custom Prompt
            </button>
            <button 
              onClick={handleSave} 
              className="primary"
              disabled={!isModified}
            >
              Save for Session
            </button>
          </div>
        </div>

        <div className="prompt-info">
          <p>💡 <strong>Note:</strong> Changes to the prompt will only affect this browser session. The default prompt will be restored when you refresh the page.</p>
        </div>

        <div className="form-group">
          <label htmlFor="prompt">Custom Prompt Template</label>
          <textarea
            id="prompt"
            value={prompt}
            onChange={(e) => handlePromptChange(e.target.value)}
            placeholder="Enter your custom prompt..."
            rows={30}
            className="prompt-textarea"
          />
          <div className="char-count">{prompt.length} characters</div>
        </div>

        <div className="prompt-placeholders">
          <h3>Available Placeholders:</h3>
          <ul>
            <li><code>{'{jd_text}'}</code> - Will be replaced with the job description</li>
            <li><code>{'{resume_text}'}</code> - Will be replaced with the resume text</li>
          </ul>
        </div>
      </div>
    </div>
  );
}

