const { GoogleGenerativeAI } = require('@google/generative-ai');
const express = require('express');
const cors = require('cors');

const app = express();
app.use(cors());
app.use(express.json({ limit: '16mb' }));

const MODEL_NAME = process.env.MODEL_NAME || 'gemini-2.5-pro';
const GEMINI_API_KEY = process.env.GEMINI_API_KEY;

if (!GEMINI_API_KEY) {
  console.error('❌ GEMINI_API_KEY environment variable is required');
  process.exit(1);
}

const genai = new GoogleGenerativeAI(GEMINI_API_KEY);

// Build prompt
function buildPrompt(jdText, resumeText, customPrompt = null) {
  if (customPrompt) {
    return customPrompt.replace('{jd_text}', jdText).replace('{resume_text}', resumeText);
  }

  return `You are an expert technical resume editor that intelligently aligns a candidate's resume with a given job description.

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
   - Ensure valid JSON that can be parsed by JSON.parse().

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
${jdText}

==============================
📄 CANDIDATE RESUME
==============================
${resumeText}

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
}

// Extract JSON from text
function extractJSON(text) {
  const jsonMatch = text.match(/\{[\s\S]*\}/);
  if (!jsonMatch) {
    throw new Error('No JSON object found in response');
  }
  try {
    return JSON.parse(jsonMatch[0]);
  } catch (e) {
    throw new Error(`Failed to parse JSON: ${e.message}`);
  }
}

// Call Gemini API
async function callGemini(prompt) {
  const model = genai.getGenerativeModel({
    model: MODEL_NAME,
    systemInstruction: "You are an expert technical resume editor. Always rewrite SUMMARY (mandatory, under 33 words). Always include a work experience section edit (≤ 15 words). Modify exactly 2 projects (if 2+ exist), or 1 if only 1 exists. Mark others as 'no_changes'. Output must be valid JSON only, conforming to the specified schema. Maintain concise, professional tone and avoid keyword stuffing."
  });

  const result = await model.generateContent(prompt);
  const response = await result.response;
  return response.text();
}

// Health check
app.get('/health', (req, res) => {
  res.json({
    status: 'healthy',
    service: 'Resume Optimizer API',
    version: '1.0.0'
  });
});

// Optimize endpoint
app.post('/optimize/text', async (req, res) => {
  const requestTime = new Date();
  
  try {
    const { resume_text, job_description, custom_prompt } = req.body;

    if (!resume_text || !job_description) {
      return res.status(400).json({
        error: 'resume_text and job_description are required'
      });
    }

    // Build prompt
    const prompt = buildPrompt(job_description, resume_text, custom_prompt);

    // Call Gemini
    const responseText = await callGemini(prompt);
    const result = extractJSON(responseText);

    // Normalize
    if (result.fortinet_section && !result.work_experience_section) {
      result.work_experience_section = result.fortinet_section;
      delete result.fortinet_section;
    }

    const responseTime = new Date();
    const duration = (responseTime - requestTime) / 1000;

    console.log(`⏱️  Request processed in ${duration.toFixed(3)}s`);

    res.json(result);
  } catch (error) {
    console.error('❌ Error:', error);
    res.status(500).json({
      error: error.message || 'Internal server error'
    });
  }
});

// Lambda handler - supports both Function URL and API Gateway
exports.handler = async (event, context) => {
  // CORS headers - must be present in all responses
  const corsHeaders = {
    'Access-Control-Allow-Origin': '*',
    'Access-Control-Allow-Headers': 'Content-Type,Authorization',
    'Access-Control-Allow-Methods': 'GET,POST,OPTIONS',
    'Content-Type': 'application/json'
  };

  // Log event structure for debugging
  console.log('Event structure:', JSON.stringify({
    hasRequestContext: !!event.requestContext,
    hasHttp: !!(event.requestContext && event.requestContext.http),
    httpMethod: event.httpMethod,
    path: event.path,
    rawPath: event.rawPath
  }));

  // Detect event source (Function URL vs API Gateway)
  // Function URL: event.requestContext.http.method, event.rawPath
  // API Gateway: event.httpMethod, event.path
  const httpMethod = event.requestContext?.http?.method || event.httpMethod || 'GET';
  const path = event.rawPath || event.requestContext?.http?.path || event.path || '/';
  
  console.log(`Request: ${httpMethod} ${path}`);
  
  // Handle OPTIONS (CORS preflight) - must return 200 with CORS headers
  if (httpMethod === 'OPTIONS' || httpMethod === 'options') {
    console.log('Handling OPTIONS preflight request');
    return {
      statusCode: 200,
      headers: corsHeaders,
      body: ''
    };
  }

  try {
    // Parse body
    let body = {};
    if (event.body) {
      try {
        body = typeof event.body === 'string' ? JSON.parse(event.body) : event.body;
      } catch (e) {
        // If body parsing fails, return error with CORS headers
        return {
          statusCode: 400,
          headers: corsHeaders,
          body: JSON.stringify({ error: 'Invalid JSON in request body' })
        };
      }
    }

    // Route requests - normalize path (remove trailing slash, handle double slashes)
    const normalizedPath = path.replace(/\/+/g, '/').replace(/\/$/, '') || '/';

    // Health check
    if (httpMethod === 'GET' && (normalizedPath === '/health' || normalizedPath === '')) {
      return {
        statusCode: 200,
        headers: corsHeaders,
        body: JSON.stringify({
          status: 'healthy',
          service: 'Resume Optimizer API',
          version: '1.0.0'
        })
      };
    }

    // Optimize endpoint
    if (httpMethod === 'POST' && normalizedPath === '/optimize/text') {
      const { resume_text, job_description, custom_prompt } = body;

      if (!resume_text || !job_description) {
        return {
          statusCode: 400,
          headers: corsHeaders,
          body: JSON.stringify({ error: 'resume_text and job_description are required' })
        };
      }

      const prompt = buildPrompt(job_description, resume_text, custom_prompt);
      const responseText = await callGemini(prompt);
      const result = extractJSON(responseText);

      // Normalize
      if (result.fortinet_section && !result.work_experience_section) {
        result.work_experience_section = result.fortinet_section;
        delete result.fortinet_section;
      }

      return {
        statusCode: 200,
        headers: corsHeaders,
        body: JSON.stringify(result)
      };
    }

    // Not found
    return {
      statusCode: 404,
      headers: corsHeaders,
      body: JSON.stringify({ error: 'Not found', path: normalizedPath })
    };
  } catch (error) {
    console.error('Lambda error:', error);
    return {
      statusCode: 500,
      headers: corsHeaders,
      body: JSON.stringify({ error: error.message || 'Internal server error' })
    };
  }
};

// For local development
if (require.main === module) {
  const PORT = process.env.PORT || 8000;
  app.listen(PORT, () => {
    console.log(`🚀 Server running on http://localhost:${PORT}`);
  });
}

