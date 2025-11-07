"""
Main entry point for resume optimization using Gemini API.
"""
import sys
import os

# Add src directory to Python path
backend_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(backend_root, 'src'))

from config import RESUME_FILE, JD_FILE, OUTPUT_FILE
from file_utils import read_docx_text, read_text_file
from prompt_builder import build_prompt
from gemini_client import call_gemini
from json_utils import extract_json_from_text, save_json_to_file


def main():
    """Main pipeline for resume optimization."""
    print("📄 Reading resume and job description...")
    resume_text = read_docx_text(RESUME_FILE)
    jd_text = read_text_file(JD_FILE)

    print("🤖 Building Gemini prompt...")
    prompt = build_prompt(jd_text, resume_text)

    print("🚀 Sending request to Gemini...")
    response_text = call_gemini(prompt)

    print("🧩 Extracting JSON response...")
    try:
        result = extract_json_from_text(response_text)
    except Exception as e:
        print(f"❌ Error extracting JSON: {e}")
        return

    print("💾 Saving output to file...")
    save_json_to_file(result, OUTPUT_FILE)

    print(f"✅ Resume edits saved to {OUTPUT_FILE}")


# =========================================================
# RUN SCRIPT
# =========================================================
if __name__ == "__main__":
    main()
