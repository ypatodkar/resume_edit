"""
Parallel Gemini API client for faster processing.
"""
import concurrent.futures
import google.generativeai as genai
from config import MODEL_NAME
from json_utils import extract_json_from_text
from prompt_builder_parallel import (
    build_summary_prompt,
    build_technical_skills_prompt,
    build_work_experience_prompt,
    build_projects_prompt,
    combine_results
)


def call_gemini_section(prompt, section_name):
    """Calls Gemini for a specific section."""
    try:
        model = genai.GenerativeModel(
            model_name=MODEL_NAME,
            system_instruction=(
                "You are an expert technical resume editor. "
                "Output must be valid JSON only, conforming to the specified schema. "
                "Maintain concise, professional tone and avoid keyword stuffing."
            )
        )
        response = model.generate_content(prompt)
        response_text = response.text.strip()
        result = extract_json_from_text(response_text)
        print(f"  ✅ {section_name} completed")
        return result
    except Exception as e:
        print(f"  ❌ {section_name} failed: {str(e)}")
        raise


def call_gemini_parallel(jd_text: str, resume_text: str, use_parallel=True):
    """
    Calls Gemini API in parallel for different sections.
    
    Args:
        jd_text: Job description text
        resume_text: Resume text
        use_parallel: If True, use parallel processing; if False, use original sequential method
    
    Returns:
        Combined JSON result
    """
    if not use_parallel:
        # Fallback to original method
        from prompt_builder import build_prompt
        from gemini_client import call_gemini
        
        prompt = build_prompt(jd_text, resume_text)
        response_text = call_gemini(prompt)
        result = extract_json_from_text(response_text)
        
        # Normalize
        if 'fortinet_section' in result and 'work_experience_section' not in result:
            result['work_experience_section'] = result.pop('fortinet_section')
        
        return result
    
    print("🚀 Starting parallel processing...")
    
    # Build prompts for each section
    prompts = {
        'summary': build_summary_prompt(jd_text, resume_text),
        'technical_skills': build_technical_skills_prompt(jd_text, resume_text),
        'work_experience': build_work_experience_prompt(jd_text, resume_text),
        'projects': build_projects_prompt(jd_text, resume_text)
    }
    
    # Execute all sections in parallel
    results = {}
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
        # Submit all tasks
        future_to_section = {
            executor.submit(call_gemini_section, prompt, section_name): section_name
            for section_name, prompt in prompts.items()
        }
        
        # Collect results as they complete
        for future in concurrent.futures.as_completed(future_to_section):
            section_name = future_to_section[future]
            try:
                results[section_name] = future.result()
            except Exception as e:
                print(f"  ❌ Error processing {section_name}: {e}")
                # Return empty result for failed section
                if section_name == 'summary':
                    results[section_name] = {"summary": ""}
                elif section_name == 'technical_skills':
                    results[section_name] = {"technical_skills": ""}
                elif section_name == 'work_experience':
                    results[section_name] = {"work_experience_section": {"new_line": ""}}
                elif section_name == 'projects':
                    results[section_name] = {"projects": []}
    
    # Combine results
    combined = combine_results(
        results.get('summary', {}),
        results.get('technical_skills', {}),
        results.get('work_experience', {}),
        results.get('projects', {})
    )
    
    print("✅ Parallel processing completed")
    return combined

