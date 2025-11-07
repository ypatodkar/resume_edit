"""
JSON extraction and saving utilities.
"""
import re
import json
from config import RAW_RESPONSE_FILE


def extract_json_from_text(text):
    """
    Extracts the first valid JSON object from the text, even if the model adds extra text.
    """
    match = re.search(r"\{.*\}", text, re.DOTALL)
    if not match:
        raise ValueError("❌ No JSON object found in Gemini response.")
    json_str = match.group(0).strip()
    try:
        return json.loads(json_str)
    except json.JSONDecodeError as e:
        print("⚠️ Failed to parse JSON. Saving raw output for debugging.")
        with open(RAW_RESPONSE_FILE, "w", encoding="utf-8") as f:
            f.write(text)
        raise e


def save_json_to_file(data, file_path):
    """Saves JSON data to a file."""
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

