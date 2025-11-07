"""
Parallel prompt builders for different sections.
"""
import json


def build_summary_prompt(jd_text: str, resume_text: str) -> str:
    """Builds prompt for summary section only."""
    return f"""
You are an expert technical resume editor. Rewrite ONLY the SUMMARY section of the resume.

REQUIREMENTS:
- MUST be strictly under 33 words
- Include major technical keywords from the job description
- Include 1–2 soft skills naturally
- Focus on clarity, brevity, and impact
- Incorporate essential JD keywords and role focus

OUTPUT FORMAT (JSON only):
{{
  "summary": "Your rewritten summary here (under 33 words)"
}}

JOB DESCRIPTION:
{jd_text}

CANDIDATE RESUME:
{resume_text}

Return ONLY valid JSON with the summary field.
"""


def build_technical_skills_prompt(jd_text: str, resume_text: str) -> str:
    """Builds prompt for technical skills section only."""
    return f"""
You are an expert technical resume editor. Update ONLY the TECHNICAL SKILLS section.

REQUIREMENTS:
- Use grouped, labeled formatting with clear categories
- Format example:
  **Specialties / Architecture & Design / Core Skills**
  **Languages & Tech / Platforms & Tools / Soft Skills**
- Incorporate keywords naturally from JD
- Ensure all critical technical keywords from JD are reflected

OUTPUT FORMAT (JSON only):
{{
  "technical_skills": "Your updated technical skills in grouped format"
}}

JOB DESCRIPTION:
{jd_text}

CANDIDATE RESUME:
{resume_text}

Return ONLY valid JSON with the technical_skills field.
"""


def build_work_experience_prompt(jd_text: str, resume_text: str) -> str:
    """Builds prompt for work experience section only."""
    return f"""
You are an expert technical resume editor. Create ONE new line for the work experience section.

REQUIREMENTS:
- Exactly one new line
- MUST be ≤ 15 words
- Must align with JD keywords
- If no work experience section exists, create a line that fits the work experience context

OUTPUT FORMAT (JSON only):
{{
  "work_experience_section": {{
    "new_line": "Your new concise line here (≤ 15 words)"
  }}
}}

JOB DESCRIPTION:
{jd_text}

CANDIDATE RESUME:
{resume_text}

Return ONLY valid JSON with the work_experience_section field.
"""


def build_projects_prompt(jd_text: str, resume_text: str) -> str:
    """Builds prompt for projects section only."""
    return f"""
You are an expert technical resume editor. Review and update the PROJECTS section.

REQUIREMENTS:
- Review ALL projects from the resume
- Modify exactly 2 projects that need keyword alignment (if 2 or more projects exist)
- If only 1 project exists, modify that one
- For each modified project, you can modify:
  * One bullet point (15–25 words for the new point)
  * Technologies used (if needed)
- For unchanged projects, mark as "no_changes"
- Prioritize projects that can naturally incorporate missing JD keywords
- Select the 2 most relevant projects that benefit from keyword alignment

OUTPUT FORMAT (JSON only):
{{
  "projects": [
    {{
      "project_name": "Name of the project",
      "status": "modified" OR "no_changes",
      "changes": {{
        "old_point": "The exact bullet point to replace (if modified)",
        "new_point": "New concise line (15–25 words, if modified)",
        "old_technologies": "Current technologies listed (if changing)",
        "new_technologies": "Updated technologies (if changing)"
      }}
    }}
  ]
}}

JOB DESCRIPTION:
{jd_text}

CANDIDATE RESUME:
{resume_text}

Return ONLY valid JSON with the projects array. Include ALL projects from the resume.
"""


def combine_results(summary_result, skills_result, work_exp_result, projects_result):
    """Combines parallel results into final JSON structure."""
    combined = {
        "intro_note": "Of course. Here are the final, minimal changes to incorporate these last keywords.",
        "summary": summary_result.get("summary", ""),
        "technical_skills": skills_result.get("technical_skills", ""),
        "work_experience_section": work_exp_result.get("work_experience_section", {}),
        "projects": projects_result.get("projects", []),
        "overall_notes": "The resume has been optimized to align with the job description. Summary, technical skills, work experience, and projects have been updated to incorporate key terms and requirements."
    }
    
    # Normalize work_experience_section if needed
    if 'fortinet_section' in combined['work_experience_section']:
        combined['work_experience_section'] = {
            'new_line': combined['work_experience_section'].get('fortinet_section', {}).get('new_line', '')
        }
    
    return combined

