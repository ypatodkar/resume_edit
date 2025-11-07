"""
Debug script to inspect Google Docs structure and find section headers.
"""
import sys
import os

backend_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(backend_root, 'src'))

from src.google_docs_editor import get_docs_service, get_document_text, find_text_in_document


def debug_document(document_id):
    """Prints document structure to help debug section finding."""
    print("=" * 70)
    print("🔍 DEBUGGING GOOGLE DOCS STRUCTURE")
    print("=" * 70)
    
    service = get_docs_service()
    
    # Get full document text
    full_text = get_document_text(service, document_id)
    print(f"\n📄 Document length: {len(full_text)} characters")
    
    # Try to find common headers
    print("\n🔍 Searching for section headers...")
    headers_to_check = [
        'SUMMARY', 'Summary', 'PROFESSIONAL SUMMARY', 'Professional Summary',
        'PROFILE', 'Profile',
        'TECHNICAL SKILLS', 'Technical Skills', 'TECHNICAL SKILLS & TOOLS',
        'Skills', 'SKILLS', 'Core Competencies', 'COMPETENCIES'
    ]
    
    found_headers = []
    for header in headers_to_check:
        matches, _ = find_text_in_document(service, document_id, header)
        if matches:
            print(f"  ✅ Found: '{header}' at index {matches[0][0]}")
            found_headers.append(header)
            # Show context around the header
            start_idx = matches[0][0]
            context_start = max(0, start_idx - 50)
            context_end = min(len(full_text), start_idx + 100)
            context = full_text[context_start:context_end]
            print(f"     Context: ...{context}...")
    
    if not found_headers:
        print("  ❌ No headers found!")
        print("\n📋 Document text (first 500 chars):")
        print(full_text[:500])
        print("\n💡 Tip: Check what your actual section headers are named in the document.")
    else:
        print(f"\n✅ Found {len(found_headers)} header(s)")
    
    print("\n" + "=" * 70)


if __name__ == "__main__":
    document_id = input("Enter your Google Docs Document ID: ").strip()
    if not document_id:
        print("❌ Document ID is required!")
    else:
        debug_document(document_id)


