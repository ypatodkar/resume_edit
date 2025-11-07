"""
Gemini API client for resume optimization.
"""
import google.generativeai as genai
from config import MODEL_NAME


def call_gemini(prompt):
    """Calls the Gemini API with the given prompt."""
    model = genai.GenerativeModel(
        model_name=MODEL_NAME,
        system_instruction=(
            "You are an expert technical resume editor. "
            "Always rewrite SUMMARY (mandatory, under 33 words). "
            "Always include a work experience section edit (≤ 15 words). "
            "Modify exactly 2 projects (if 2+ exist), or 1 if only 1 exists. Mark others as 'no_changes'. "
            "Output must be valid JSON only, conforming to the specified schema. "
            "Maintain concise, professional tone and avoid keyword stuffing."
        )
    )
    response = model.generate_content(prompt)
    return response.text.strip()

