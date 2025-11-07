"""
File reading utilities for resume and job description files.
"""
from docx import Document


def read_docx_text(file_path):
    """Extracts text content from a .docx file."""
    doc = Document(file_path)
    full_text = [para.text.strip() for para in doc.paragraphs if para.text.strip()]
    return "\n".join(full_text)


def read_text_file(file_path):
    """Reads text content from a .txt file."""
    with open(file_path, "r", encoding="utf-8") as f:
        return f.read().strip()

