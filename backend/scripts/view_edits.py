"""
Helper script to view resume edits in a readable format.
Useful for manual copy-paste if automatic Google Docs editing fails.
"""
import sys
import os
import json

# Add src directory to Python path
backend_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(backend_root, 'src'))

from src.config import OUTPUT_FILE


def print_edits():
    """Displays resume edits in a readable format."""
    if not os.path.exists(OUTPUT_FILE):
        print(f"❌ {OUTPUT_FILE} not found. Please run resume_optimizer.py first.")
        return
    
    with open(OUTPUT_FILE, 'r', encoding='utf-8') as f:
        edits = json.load(f)
    
    print("=" * 70)
    print("📄 RESUME EDITS SUMMARY")
    print("=" * 70)
    
    # Intro Note
    if edits.get('intro_note'):
        print(f"\n{edits['intro_note']}\n")
    
    # Summary
    if edits.get('summary'):
        print("=" * 70)
        print("📝 REVISED SUMMARY (Copy this to your resume):")
        print("=" * 70)
        print(edits['summary'])
        word_count = len(edits['summary'].split())
        print(f"\n   Word count: {word_count} words {'✅' if word_count < 33 else '⚠️  (Should be under 33)'}")
    
    # Technical Skills
    if edits.get('technical_skills'):
        print("\n" + "=" * 70)
        print("🛠️  REVISED TECHNICAL SKILLS (Copy this to your resume):")
        print("=" * 70)
        print(edits['technical_skills'])
    
    # Work Experience Section
    if edits.get('work_experience_section'):
        work_exp = edits['work_experience_section']
        print("\n" + "=" * 70)
        print("💼 WORK EXPERIENCE SECTION (Copy this line to your resume):")
        print("=" * 70)
        new_line = work_exp.get('new_line', 'N/A')
        print(f'"{new_line}"')
        word_count = len(new_line.split())
        print(f"\n   Word count: {word_count} words {'✅' if word_count <= 15 else '⚠️  (Should be ≤ 15)'}")
    
    # Projects
    if edits.get('projects'):
        print("\n" + "=" * 70)
        print(f"📁 PROJECT EDITS ({len(edits['projects'])} projects):")
        print("=" * 70)
        for i, project in enumerate(edits['projects'], 1):
            project_name = project.get('project_name', 'Unknown')
            status = project.get('status', 'unknown')
            
            print(f"\n{i}. {project_name}")
            
            if status == 'no_changes':
                print("   ✅ No changes needed.")
            elif status == 'modified':
                changes = project.get('changes', {})
                if changes.get('old_point'):
                    print(f"   Change this point: \"{changes['old_point']}\"")
                if changes.get('new_point'):
                    print(f"   To: \"{changes['new_point']}\"")
                if changes.get('old_technologies') and changes.get('new_technologies'):
                    print(f"   Change Technologies to: {changes['new_technologies']}")
    
    # Overall Notes
    if edits.get('overall_notes'):
        print("\n" + "=" * 70)
        print("📋 NOTES:")
        print("=" * 70)
        print(edits['overall_notes'])
    
    print("\n" + "=" * 70)
    print("✅ End of edits summary")
    print("=" * 70)


if __name__ == "__main__":
    print_edits()

