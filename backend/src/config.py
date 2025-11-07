"""
Configuration constants for resume optimization.
"""
import google.generativeai as genai

# =========================================================
# FILE PATHS
# =========================================================
import os

# Base directory (project root - one level up from backend)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Input files
RESUME_FILE = os.path.join(BASE_DIR, "data", "input", "resume.docx")
JD_FILE = os.path.join(BASE_DIR, "data", "input", "job_description.txt")

# Output files
OUTPUT_FILE = os.path.join(BASE_DIR, "data", "output", "resume_edits.json")
RAW_RESPONSE_FILE = os.path.join(BASE_DIR, "output", "raw_response.txt")

# =========================================================
# MODEL CONFIG
# =========================================================
MODEL_NAME = "gemini-2.5-pro"
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")  # Get from environment variable

# =========================================================
# GEMINI INITIALIZATION
# =========================================================
genai.configure(api_key=GEMINI_API_KEY)

