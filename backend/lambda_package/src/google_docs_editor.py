"""
Google Docs editor for applying resume edits while preserving formatting.
"""
import re
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import json
import os
import pickle

# Scopes required for Google Docs API
SCOPES = ['https://www.googleapis.com/auth/documents']


def get_credentials():
    """
    Gets valid user credentials from storage or opens a browser to request them.
    """
    # Get backend root directory (where token.pickle and credentials.json are)
    backend_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    
    creds = None
    token_path = os.path.join(backend_root, 'token.pickle')
    creds_path = os.path.join(backend_root, 'credentials.json')
    
    # Load existing token
    if os.path.exists(token_path):
        with open(token_path, 'rb') as token:
            creds = pickle.load(token)
    
    # If there are no (valid) credentials available, let the user log in
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            if not os.path.exists(creds_path):
                raise FileNotFoundError(
                    "❌ credentials.json not found. Please download it from Google Cloud Console.\n"
                    "See README.md for setup instructions."
                )
            flow = InstalledAppFlow.from_client_secrets_file(creds_path, SCOPES)
            creds = flow.run_local_server(port=0)
        
        # Save credentials for next run
        with open(token_path, 'wb') as token:
            pickle.dump(creds, token)
    
    return creds


def get_docs_service():
    """Creates and returns a Google Docs API service object."""
    creds = get_credentials()
    return build('docs', 'v1', credentials=creds)


def find_text_in_document(service, document_id, search_text):
    """
    Finds text in a Google Doc and returns its start and end indices.
    Returns list of (start_index, end_index) tuples.
    """
    doc = service.documents().get(documentId=document_id).execute()
    content = doc.get('body', {}).get('content', [])
    
    matches = []
    current_index = 0
    
    def traverse_elements(elements):
        nonlocal current_index
        for element in elements:
            if 'paragraph' in element:
                para = element['paragraph']
                for text_run in para.get('elements', []):
                    if 'textRun' in text_run:
                        text = text_run['textRun'].get('content', '')
                        start_idx = current_index
                        end_idx = current_index + len(text)
                        
                        # Search for the text (case-insensitive, handle whitespace)
                        search_text_clean = re.sub(r'\s+', ' ', search_text.strip())
                        text_clean = re.sub(r'\s+', ' ', text.strip())
                        
                        if search_text_clean.lower() in text_clean.lower():
                            idx = text_clean.lower().find(search_text_clean.lower())
                            if idx >= 0:
                                match_start = start_idx + idx
                                match_end = match_start + len(search_text_clean)
                                matches.append((match_start, match_end))
                        
                        current_index = end_idx
            elif 'table' in element:
                # Handle tables if needed
                for row in element['table'].get('tableRows', []):
                    for cell in row.get('tableCells', []):
                        traverse_elements(cell.get('content', []))
            elif 'sectionBreak' in element or 'pageBreak' in element:
                current_index += 1
    
    traverse_elements(content)
    return matches, doc


def find_section_paragraph_range(service, document_id, section_header):
    """
    Finds the paragraph range(s) after a section header.
    Returns (start_index, end_index) of the content, handling multiple paragraphs.
    """
    doc = service.documents().get(documentId=document_id).execute()
    content = doc.get('body', {}).get('content', [])
    
    header_idx = None
    current_index = 0
    paragraph_starts = []
    paragraph_ends = []
    paragraph_texts = []
    
    def traverse_elements(elements):
        nonlocal current_index, header_idx
        for element in elements:
            if 'paragraph' in element:
                para_start = current_index
                para = element['paragraph']
                para_text = ''
                
                for text_run in para.get('elements', []):
                    if 'textRun' in text_run:
                        text = text_run['textRun'].get('content', '')
                        para_text += text
                        current_index += len(text)
                
                para_end = current_index
                paragraph_starts.append(para_start)
                paragraph_ends.append(para_end)
                paragraph_texts.append(para_text)
                
                # Check if this paragraph contains the header (case-insensitive)
                para_clean = re.sub(r'\s+', ' ', para_text.strip())
                header_clean = re.sub(r'\s+', ' ', section_header.strip())
                if header_clean.lower() in para_clean.lower():
                    header_idx = len(paragraph_starts) - 1
                
            elif 'table' in element:
                for row in element['table'].get('tableRows', []):
                    for cell in row.get('tableCells', []):
                        traverse_elements(cell.get('content', []))
            elif 'sectionBreak' in element or 'pageBreak' in element:
                current_index += 1
    
    traverse_elements(content)
    
    if header_idx is None or header_idx + 1 >= len(paragraph_starts):
        return None, None
    
    # Get the paragraph after the header
    content_start = paragraph_starts[header_idx + 1]
    
    # For technical skills, it might span multiple paragraphs
    # Look ahead for empty paragraphs or next section header
    content_end = paragraph_ends[header_idx + 1]
    
    # Check if there are more paragraphs after (for multi-paragraph sections)
    # Stop at empty paragraphs or obvious next sections
    next_para_idx = header_idx + 2
    while next_para_idx < len(paragraph_texts):
        next_text = paragraph_texts[next_para_idx].strip()
        # Stop if we hit an empty paragraph or a likely next section header
        if not next_text or len(next_text) < 3:
            break
        # Stop if it looks like another section header (all caps, short)
        if next_text.isupper() and len(next_text) < 50:
            break
        content_end = paragraph_ends[next_para_idx]
        next_para_idx += 1
    
    return content_start, content_end


def get_text_run_formatting(doc, start_index):
    """
    Gets the text formatting at a specific index.
    """
    content = doc.get('body', {}).get('content', [])
    current_index = 0
    
    def traverse_elements(elements):
        nonlocal current_index
        for element in elements:
            if 'paragraph' in element:
                para = element['paragraph']
                for text_run in para.get('elements', []):
                    if 'textRun' in text_run:
                        text = text_run['textRun'].get('content', '')
                        text_start = current_index
                        text_end = current_index + len(text)
                        
                        if text_start <= start_index < text_end:
                            # Found the text run at this index
                            return text_run['textRun'].get('textStyle', {})
                        
                        current_index = text_end
            elif 'table' in element:
                for row in element['table'].get('tableRows', []):
                    for cell in row.get('tableCells', []):
                        result = traverse_elements(cell.get('content', []))
                        if result:
                            return result
            elif 'sectionBreak' in element or 'pageBreak' in element:
                current_index += 1
        return None
    
    return traverse_elements(content)


def replace_section_content(service, document_id, section_headers, new_content):
    """
    Finds a section by header and replaces its content, preserving formatting.
    """
    doc = service.documents().get(documentId=document_id).execute()
    
    for header in section_headers:
        # Try to find the section header
        matches, _ = find_text_in_document(service, document_id, header)
        if matches:
            print(f"    🔍 Found header: '{header}'")
            # Found header, now find the paragraph after it
            para_start, para_end = find_section_paragraph_range(service, document_id, header)
            
            if para_start is not None and para_end is not None:
                print(f"    📍 Found content range: {para_start} to {para_end}")
                
                # Get the formatting from the first character of existing content
                text_style = get_text_run_formatting(doc, para_start)
                
                # Delete the old content
                requests = [{
                    'deleteContentRange': {
                        'range': {
                            'startIndex': para_start,
                            'endIndex': para_end
                        }
                    }
                }]
                
                # Insert new text with preserved formatting
                # First insert the text
                requests.append({
                    'insertText': {
                        'location': {
                            'index': para_start
                        },
                        'text': new_content
                    }
                })
                
                # Then apply formatting if available
                if text_style:
                    # Build fields list from available style properties
                    style_fields = []
                    if 'fontSize' in text_style or 'magnitude' in text_style:
                        style_fields.append('fontSize')
                    if 'bold' in text_style:
                        style_fields.append('bold')
                    if 'italic' in text_style:
                        style_fields.append('italic')
                    if 'underline' in text_style:
                        style_fields.append('underline')
                    if 'foregroundColor' in text_style:
                        style_fields.append('foregroundColor')
                    if 'backgroundColor' in text_style:
                        style_fields.append('backgroundColor')
                    if 'weightedFontFamily' in text_style or 'fontFamily' in text_style:
                        style_fields.append('weightedFontFamily')
                    
                    if style_fields:
                        # Create a clean textStyle object with only the fields we'll update
                        clean_style = {}
                        if 'fontSize' in text_style:
                            clean_style['fontSize'] = text_style['fontSize']
                        elif 'magnitude' in text_style:
                            clean_style['fontSize'] = text_style['magnitude']
                        if 'bold' in text_style:
                            clean_style['bold'] = text_style['bold']
                        if 'italic' in text_style:
                            clean_style['italic'] = text_style['italic']
                        if 'underline' in text_style:
                            clean_style['underline'] = text_style['underline']
                        if 'foregroundColor' in text_style:
                            clean_style['foregroundColor'] = text_style['foregroundColor']
                        if 'backgroundColor' in text_style:
                            clean_style['backgroundColor'] = text_style['backgroundColor']
                        if 'weightedFontFamily' in text_style:
                            clean_style['weightedFontFamily'] = text_style['weightedFontFamily']
                        elif 'fontFamily' in text_style:
                            clean_style['weightedFontFamily'] = {'fontFamily': text_style['fontFamily']}
                        
                        requests.append({
                            'updateTextStyle': {
                                'range': {
                                    'startIndex': para_start,
                                    'endIndex': para_start + len(new_content)
                                },
                                'textStyle': clean_style,
                                'fields': ','.join(style_fields)
                            }
                        })
                
                try:
                    service.documents().batchUpdate(
                        documentId=document_id,
                        body={'requests': requests}
                    ).execute()
                    print(f"    ✅ Successfully replaced '{header}' section content")
                    return True
                except Exception as e:
                    print(f"    ❌ Error replacing section: {e}")
                    import traceback
                    traceback.print_exc()
                    return False
            else:
                print(f"    ⚠️  Could not find paragraph range after '{header}' header")
        else:
            print(f"    🔍 Header '{header}' not found in document")
    
    return False


def get_text_at_index(doc, start_index, end_index):
    """Extracts text content between start_index and end_index."""
    content = doc.get('body', {}).get('content', [])
    extracted_text = []
    current_index = 0
    
    def traverse_elements(elements):
        nonlocal current_index
        for element in elements:
            if 'paragraph' in element:
                para = element['paragraph']
                for text_run in para.get('elements', []):
                    if 'textRun' in text_run:
                        text = text_run['textRun'].get('content', '')
                        text_start = current_index
                        text_end = current_index + len(text)
                        
                        # Extract overlapping portion
                        overlap_start = max(text_start, start_index)
                        overlap_end = min(text_end, end_index)
                        
                        if overlap_start < overlap_end:
                            # Calculate relative position in text
                            rel_start = overlap_start - text_start
                            rel_end = overlap_end - text_start
                            extracted_text.append(text[rel_start:rel_end])
                        
                        current_index = text_end
            elif 'table' in element:
                for row in element['table'].get('tableRows', []):
                    for cell in row.get('tableCells', []):
                        traverse_elements(cell.get('content', []))
    
    traverse_elements(content)
    return ''.join(extracted_text)


def replace_text_preserving_format(service, document_id, old_text, new_text):
    """
    Replaces text in a Google Doc while preserving the formatting of the first character.
    """
    matches, doc = find_text_in_document(service, document_id, old_text)
    
    if not matches:
        print(f"⚠️  Text not found: '{old_text[:50]}...'")
        return False
    
    # Use the first match
    start_index, end_index = matches[0]
    
    # Get formatting from the start position
    requests = [{
        'deleteContentRange': {
            'range': {
                'startIndex': start_index,
                'endIndex': end_index
            }
        }
    }, {
        'insertText': {
            'location': {
                'index': start_index
            },
            'text': new_text
        }
    }]
    
    try:
        service.documents().batchUpdate(
            documentId=document_id,
            body={'requests': requests}
        ).execute()
        return True
    except Exception as e:
        print(f"❌ Error replacing text: {e}")
        return False


def replace_full_paragraph(service, document_id, old_text, new_text):
    """
    Replaces an entire paragraph while preserving paragraph-level formatting.
    """
    matches, doc = find_text_in_document(service, document_id, old_text)
    
    if not matches:
        print(f"⚠️  Paragraph not found: '{old_text[:50]}...'")
        return False
    
    start_index, end_index = matches[0]
    
    # Find paragraph boundaries (search backwards and forwards)
    content = doc.get('body', {}).get('content', [])
    
    # Try to find the paragraph containing this text
    para_start = start_index
    para_end = end_index
    
    # Simple approach: replace the matched text
    requests = [{
        'deleteContentRange': {
            'range': {
                'startIndex': para_start,
                'endIndex': para_end
            }
        }
    }, {
        'insertText': {
            'location': {
                'index': para_start
            },
            'text': new_text
        }
    }]
    
    try:
        service.documents().batchUpdate(
            documentId=document_id,
            body={'requests': requests}
        ).execute()
        return True
    except Exception as e:
        print(f"❌ Error replacing paragraph: {e}")
        return False


def find_section_content(service, document_id, section_headers):
    """
    Finds content after a section header.
    Returns (start_index, end_index) of the content, or None if not found.
    """
    doc = service.documents().get(documentId=document_id).execute()
    content = doc.get('body', {}).get('content', [])
    
    for header in section_headers:
        matches, _ = find_text_in_document(service, document_id, header)
        if matches:
            # Found the header, now find the content after it
            header_end = matches[0][1]
            
            # Look for the next section or end of document
            # For now, return a range - this may need adjustment
            return header_end, None
    
    return None, None


def get_document_text(service, document_id):
    """Gets all text content from the document."""
    doc = service.documents().get(documentId=document_id).execute()
    content = doc.get('body', {}).get('content', [])
    
    def extract_text(elements):
        text_parts = []
        for element in elements:
            if 'paragraph' in element:
                para = element['paragraph']
                for text_run in para.get('elements', []):
                    if 'textRun' in text_run:
                        text_parts.append(text_run['textRun'].get('content', ''))
            elif 'table' in element:
                for row in element['table'].get('tableRows', []):
                    for cell in row.get('tableCells', []):
                        text_parts.extend(extract_text(cell.get('content', [])))
        return text_parts
    
    return ''.join(extract_text(content))


def find_and_replace_section(service, document_id, section_headers, new_content, old_content_hint=None):
    """
    Finds a section by header and replaces its content.
    """
    doc = service.documents().get(documentId=document_id).execute()
    
    # Try to find section header
    header_found = False
    header_end_idx = None
    
    for header in section_headers:
        matches, _ = find_text_in_document(service, document_id, header)
        if matches:
            header_found = True
            header_end_idx = matches[0][1]
            break
    
    if not header_found:
        print(f"  ⚠️  Could not find section headers: {section_headers}")
        return False
    
    # Get document text to find the old content
    full_text = get_document_text(service, document_id)
    
    # Try to find the old content after the header
    if old_content_hint:
        # Search for old content starting from after the header
        header_pos = full_text.find(header)
        if header_pos >= 0:
            after_header = full_text[header_pos + len(header):]
            old_start = after_header.find(old_content_hint)
            if old_start >= 0:
                # Found old content - now find its position in document
                matches_old, doc_ref = find_text_in_document(service, document_id, old_content_hint)
                if matches_old:
                    old_start_idx = matches_old[0][0]
                    # Find end of paragraph or next section
                    # For simplicity, replace until next newline or section break
                    old_end_idx = matches_old[0][1]
                    
                    # Look for end of paragraph
                    content_after = full_text[header_pos + len(header) + old_start:]
                    next_newline = content_after.find('\n', len(old_content_hint))
                    if next_newline > 0:
                        # Try to find the actual end index
                        pass
                    
                    # Replace the content
                    requests = [{
                        'deleteContentRange': {
                            'range': {
                                'startIndex': old_start_idx,
                                'endIndex': old_end_idx
                            }
                        }
                    }, {
                        'insertText': {
                            'location': {
                                'index': old_start_idx
                            },
                            'text': new_content
                        }
                    }]
                    
                    try:
                        service.documents().batchUpdate(
                            documentId=document_id,
                            body={'requests': requests}
                        ).execute()
                        return True
                    except Exception as e:
                        print(f"  ❌ Error: {e}")
                        return False
    
    # Fallback: just insert after header
    print(f"  ⚠️  Could not find exact old content. Manual update may be needed.")
    return False


def apply_resume_edits(service, document_id, edits_json):
    """
    Applies resume edits from JSON to Google Doc.
    
    Args:
        service: Google Docs API service object
        document_id: Google Docs document ID
        edits_json: Dictionary containing edits from resume_edits.json
    """
    print(f"📝 Applying edits to Google Doc: {document_id}\n")
    
    # Get full document text first to help with finding sections
    full_text = get_document_text(service, document_id)
    
    # 1. Replace summary
    if edits_json.get('summary'):
        print("  ✏️  Updating summary...")
        # Try multiple possible header names
        summary_headers = ['SUMMARY', 'Summary', 'PROFESSIONAL SUMMARY', 'Professional Summary', 'PROFILE', 'Profile']
        
        success = replace_section_content(
            service, document_id, summary_headers, edits_json['summary']
        )
        
        if not success:
            print("  ⚠️  Could not find summary section automatically.")
            print(f"  📋 New summary: {edits_json['summary']}")
            print("  💡 Please update manually in Google Docs.")
    
    # 2. Replace technical skills
    if edits_json.get('technical_skills'):
        print("  ✏️  Updating technical skills...")
        # Try more variations of the header name
        skills_headers = [
            'TECHNICAL SKILLS', 
            'Technical Skills', 
            'TECHNICAL SKILLS & TOOLS',
            'Technical Skills & Tools',
            'Skills', 
            'SKILLS',
            'Core Competencies',
            'COMPETENCIES',
            'Competencies',
            'TECHNICAL COMPETENCIES',
            'Technical Competencies'
        ]
        
        # Also try to find by partial match if exact header not found
        success = replace_section_content(
            service, document_id, skills_headers, edits_json['technical_skills']
        )
        
        if not success:
            print("  ⚠️  Could not find technical skills section automatically.")
            print("  🔍 Trying to find by searching document structure...")
            
            # Alternative approach: search for common skill keywords to locate section
            doc = service.documents().get(documentId=document_id).execute()
            doc_text = get_document_text(service, document_id)
            
            # Look for skill-related keywords near potential headers
            skill_keywords = ['Python', 'Java', 'JavaScript', 'React', 'AWS', 'Docker']
            found_keyword = None
            for keyword in skill_keywords:
                if keyword in doc_text:
                    found_keyword = keyword
                    break
            
            if found_keyword:
                print(f"  📍 Found skill keyword '{found_keyword}' in document")
                # Try to find and replace based on keyword context
                matches, _ = find_text_in_document(service, document_id, found_keyword)
                if matches:
                    print(f"  💡 Found skills content, but header matching failed.")
                    print(f"  📋 New skills to paste manually: {edits_json['technical_skills']}")
            else:
                print(f"  📋 New skills: {edits_json['technical_skills']}")
            print("  💡 Please update manually in Google Docs.")
    
    # 3. Apply resume edits (partial replacements)
    if edits_json.get('resume_edits'):
        print(f"  ✏️  Applying {len(edits_json['resume_edits'])} text replacements...")
        for i, edit in enumerate(edits_json['resume_edits'], 1):
            old_phrase = edit.get('WordOrPhrase', '')
            new_phrase = edit.get('new_word_or_phrase', '')
            
            if old_phrase and new_phrase:
                print(f"    [{i}/{len(edits_json['resume_edits'])}] Replacing: '{old_phrase[:50]}...'")
                success = replace_text_preserving_format(
                    service, document_id, old_phrase, new_phrase
                )
                if not success:
                    print(f"      ⚠️  Could not find this text. Please update manually.")
    
    # 4. Apply project edit
    if edits_json.get('project_edit') and edits_json['project_edit'] is not None:
        project_edit = edits_json['project_edit']
        old_point = project_edit.get('old_point', '')
        new_point = project_edit.get('new_point', '')
        
        if old_point and new_point:
            print(f"  ✏️  Updating project: {project_edit.get('project_name', 'Unknown')}")
            success = replace_text_preserving_format(
                service, document_id, old_point, new_point
            )
            if not success:
                print(f"  ⚠️  Could not find project point. Please update manually.")
    
    print("\n✅ Edit process completed!")
    print("💡 Note: Some sections may need manual updates. Check the warnings above.")


def edit_google_docs_resume(document_id, edits_json_path):
    """
    Main function to edit a Google Docs resume.
    
    Args:
        document_id: Google Docs document ID (from URL: docs.google.com/document/d/DOCUMENT_ID/edit)
        edits_json_path: Path to resume_edits.json file
    """
    # Load edits
    with open(edits_json_path, 'r', encoding='utf-8') as f:
        edits = json.load(f)
    
    # Get service
    service = get_docs_service()
    
    # Apply edits
    apply_resume_edits(service, document_id, edits)

