"""
Main script to apply resume edits to Google Docs resume.
"""
import sys
import os

# Add src directory to Python path
backend_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(backend_root, 'src'))

from src.config import OUTPUT_FILE
from src.google_docs_editor import edit_google_docs_resume


def main():
    """Main function to edit Google Docs resume."""
    print("=" * 60)
    print("📄 Google Docs Resume Editor")
    print("=" * 60)
    
    # Get document ID from user
    print("\n📋 To find your Document ID:")
    print("   1. Open your Google Doc")
    print("   2. Look at the URL: https://docs.google.com/document/d/DOCUMENT_ID/edit")
    print("   3. Copy the DOCUMENT_ID part\n")
    
    document_id = input("Enter your Google Docs Document ID: ").strip()
    
    if not document_id:
        print("❌ Document ID is required!")
        return
    
    # Check if edits file exists
    if not os.path.exists(OUTPUT_FILE):
        print(f"❌ {OUTPUT_FILE} not found. Please run resume_optimizer.py first.")
        return
    
    print(f"\n📖 Loading edits from {OUTPUT_FILE}...")
    
    try:
        edit_google_docs_resume(document_id, OUTPUT_FILE)
        print("\n✅ Resume updated successfully in Google Docs!")
        print("   Please review the changes in your document.")
    except FileNotFoundError as e:
        print(f"\n❌ {e}")
        print("\n📝 Setup Instructions:")
        print("   1. Go to https://console.cloud.google.com/")
        print("   2. Create a new project or select existing one")
        print("   3. Enable Google Docs API")
        print("   4. Create OAuth 2.0 credentials")
        print("   5. Download credentials.json and place it in this directory")
    except Exception as e:
        print(f"\n❌ Error: {e}")


if __name__ == "__main__":
    main()

