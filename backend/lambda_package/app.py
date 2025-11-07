"""
Flask API for Resume Optimization
"""
from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import sys
import tempfile
import json
from datetime import datetime
from werkzeug.utils import secure_filename

# Add src directory to Python path
backend_root = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(backend_root)
sys.path.insert(0, os.path.join(backend_root, 'src'))

from src.config import MODEL_NAME
from src.file_utils import read_docx_text, read_text_file
from src.prompt_builder import build_prompt
from src.gemini_client import call_gemini
from src.gemini_client_parallel import call_gemini_parallel
from src.json_utils import extract_json_from_text
from src.logger import log_api_request_response

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Configuration
ALLOWED_EXTENSIONS = {'docx'}
MAX_FILE_SIZE = 16 * 1024 * 1024  # 16MB max file size
UPLOAD_FOLDER = tempfile.gettempdir()


def allowed_file(filename):
    """Check if file extension is allowed."""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint."""
    return jsonify({
        'status': 'healthy',
        'service': 'Resume Optimizer API',
        'version': '1.0.0'
    }), 200


@app.route('/optimize', methods=['POST'])
def optimize_resume():
    """
    Optimize resume based on job description.
    
    Accepts:
    - resume_file: (optional) .docx file upload
    - resume_text: (optional) plain text resume
    - job_description: (required) job description text
    
    Returns:
    - JSON response with resume edits
    """
    # Record request time
    request_time = datetime.now()
    
    try:
        # Get job description (required)
        job_description = request.form.get('job_description') or request.json.get('job_description') if request.is_json else None
        
        if not job_description:
            return jsonify({
                'error': 'job_description is required'
            }), 400
        
        # Get resume text from file or text input
        resume_text = None
        
        # Check if resume file was uploaded
        if 'resume_file' in request.files:
            file = request.files['resume_file']
            if file.filename:
                if not allowed_file(file.filename):
                    return jsonify({
                        'error': 'Invalid file type. Only .docx files are allowed.'
                    }), 400
                
                # Save uploaded file temporarily
                filename = secure_filename(file.filename)
                temp_path = os.path.join(UPLOAD_FOLDER, filename)
                file.save(temp_path)
                
                try:
                    # Read the docx file
                    resume_text = read_docx_text(temp_path)
                except Exception as e:
                    return jsonify({
                        'error': f'Error reading resume file: {str(e)}'
                    }), 400
                finally:
                    # Clean up temp file
                    if os.path.exists(temp_path):
                        os.remove(temp_path)
        
        # Check if resume text was provided directly
        if not resume_text:
            resume_text = request.form.get('resume_text') or (request.json.get('resume_text') if request.is_json else None)
        
        if not resume_text:
            return jsonify({
                'error': 'Either resume_file or resume_text must be provided'
            }), 400
        
        # Validate inputs
        if len(job_description.strip()) < 10:
            return jsonify({
                'error': 'Job description is too short (minimum 10 characters)'
            }), 400
        
        if len(resume_text.strip()) < 50:
            return jsonify({
                'error': 'Resume text is too short (minimum 50 characters)'
            }), 400
        
        # Check if parallel processing is enabled (default: True)
        use_parallel = request.args.get('parallel', 'true').lower() == 'true'
        
        if use_parallel:
            # Use parallel processing for faster results
            print("🚀 Using parallel processing mode...")
            try:
                result = call_gemini_parallel(job_description, resume_text, use_parallel=True)
            except Exception as e:
                print(f"⚠️ Parallel processing failed, falling back to sequential: {e}")
                use_parallel = False  # Track that we fell back
                # Fallback to sequential
                print("🤖 Building Gemini prompt...")
                prompt = build_prompt(job_description, resume_text)
                print("🚀 Sending request to Gemini...")
                response_text = call_gemini(prompt)
                print("🧩 Extracting JSON response...")
                result = extract_json_from_text(response_text)
        else:
            # Use original sequential method
            print("🤖 Building Gemini prompt...")
            prompt = build_prompt(job_description, resume_text)
            print("🚀 Sending request to Gemini...")
            response_text = call_gemini(prompt)
            print("🧩 Extracting JSON response...")
            try:
                result = extract_json_from_text(response_text)
            except Exception as e:
                response_time = datetime.now()
                duration = (response_time - request_time).total_seconds()
                log_api_request_response(
                    endpoint="/optimize",
                    request_time=request_time,
                    response_time=response_time,
                    duration_seconds=duration,
                    request_data={
                        "job_description": job_description,
                        "resume_text": resume_text,
                        "has_resume_file": 'resume_file' in request.files
                    },
                    response_data={},
                    status_code=500,
                    error=f'Error extracting JSON from Gemini response: {str(e)}',
                    use_parallel=use_parallel
                )
                return jsonify({
                    'error': f'Error extracting JSON from Gemini response: {str(e)}',
                    'raw_response': response_text[:500] if len(response_text) > 500 else response_text
                }), 500
        
        # Normalize: Convert old 'fortinet_section' to 'work_experience_section' if present
        if 'fortinet_section' in result and 'work_experience_section' not in result:
            result['work_experience_section'] = result.pop('fortinet_section')
            print("  🔄 Normalized: Converted 'fortinet_section' to 'work_experience_section'")
        
        # Record response time and log
        response_time = datetime.now()
        duration = (response_time - request_time).total_seconds()
        
        log_api_request_response(
            endpoint="/optimize",
            request_time=request_time,
            response_time=response_time,
            duration_seconds=duration,
            request_data={
                "job_description": job_description,
                "resume_text": resume_text,
                "has_resume_file": 'resume_file' in request.files
            },
            response_data=result,
            status_code=200,
            use_parallel=use_parallel
        )
        
        print(f"⏱️  Request processed in {duration:.3f}s")
        
        # Return the result
        return jsonify(result), 200
        
    except Exception as e:
        import traceback
        error_trace = traceback.format_exc()
        print(f"❌ Error: {error_trace}")
        
        # Record response time and log error
        response_time = datetime.now()
        duration = (response_time - request_time).total_seconds()
        
        log_api_request_response(
            endpoint="/optimize",
            request_time=request_time,
            response_time=response_time,
            duration_seconds=duration,
            request_data={
                "job_description": request.form.get('job_description') or (request.json.get('job_description') if request.is_json else ""),
                "resume_text": "",
                "has_resume_file": 'resume_file' in request.files
            },
            response_data={},
            status_code=500,
            error=f'Internal server error: {str(e)}',
            use_parallel=False
        )
        
        return jsonify({
            'error': f'Internal server error: {str(e)}',
            'trace': error_trace if app.debug else None
        }), 500


@app.route('/optimize/text', methods=['POST'])
def optimize_resume_text():
    """
    Simplified endpoint that accepts JSON with resume_text and job_description.
    
    Request body (JSON):
    {
        "resume_text": "...",
        "job_description": "..."
    }
    """
    # Record request time
    request_time = datetime.now()
    
    if not request.is_json:
        response_time = datetime.now()
        duration = (response_time - request_time).total_seconds()
        log_api_request_response(
            endpoint="/optimize/text",
            request_time=request_time,
            response_time=response_time,
            duration_seconds=duration,
            request_data={},
            response_data={},
            status_code=400,
            error='Content-Type must be application/json',
            use_parallel=False
        )
        return jsonify({
            'error': 'Content-Type must be application/json'
        }), 400
    
    data = request.get_json()
    
    resume_text = data.get('resume_text')
    job_description = data.get('job_description')
    custom_prompt = data.get('custom_prompt')  # Optional custom prompt
    
    if not resume_text:
        response_time = datetime.now()
        duration = (response_time - request_time).total_seconds()
        log_api_request_response(
            endpoint="/optimize/text",
            request_time=request_time,
            response_time=response_time,
            duration_seconds=duration,
            request_data={"job_description": job_description or ""},
            response_data={},
            status_code=400,
            error='resume_text is required',
            use_parallel=False
        )
        return jsonify({
            'error': 'resume_text is required'
        }), 400
    
    if not job_description:
        response_time = datetime.now()
        duration = (response_time - request_time).total_seconds()
        log_api_request_response(
            endpoint="/optimize/text",
            request_time=request_time,
            response_time=response_time,
            duration_seconds=duration,
            request_data={"resume_text": resume_text},
            response_data={},
            status_code=400,
            error='job_description is required',
            use_parallel=False
        )
        return jsonify({
            'error': 'job_description is required'
        }), 400
    
    # Check if parallel processing is enabled (default: True)
    use_parallel = request.json.get('parallel', True) if request.is_json else True
    
    # Use custom prompt if provided, otherwise use default
    if custom_prompt:
        print("📝 Using custom prompt from session...")
        # Replace placeholders in custom prompt
        prompt = custom_prompt.replace('{jd_text}', job_description).replace('{resume_text}', resume_text)
        print("🚀 Sending request to Gemini with custom prompt...")
        response_text = call_gemini(prompt)
        print("🧩 Extracting JSON response...")
        try:
            result = extract_json_from_text(response_text)
        except Exception as e:
            response_time = datetime.now()
            duration = (response_time - request_time).total_seconds()
            log_api_request_response(
                endpoint="/optimize/text",
                request_time=request_time,
                response_time=response_time,
                duration_seconds=duration,
                request_data={
                    "job_description": job_description,
                    "resume_text": resume_text,
                    "has_custom_prompt": True
                },
                response_data={},
                status_code=500,
                error=f'Error extracting JSON from Gemini response: {str(e)}',
                use_parallel=False
            )
            return jsonify({
                'error': f'Error extracting JSON from Gemini response: {str(e)}',
                'raw_response': response_text[:500] if len(response_text) > 500 else response_text
            }), 500
        
        # Normalize: Convert old 'fortinet_section' to 'work_experience_section' if present
        if 'fortinet_section' in result and 'work_experience_section' not in result:
            result['work_experience_section'] = result.pop('fortinet_section')
            print("  🔄 Normalized: Converted 'fortinet_section' to 'work_experience_section'")
        
        # Record response time and log
        response_time = datetime.now()
        duration = (response_time - request_time).total_seconds()
        
        log_api_request_response(
            endpoint="/optimize/text",
            request_time=request_time,
            response_time=response_time,
            duration_seconds=duration,
            request_data={
                "job_description": job_description,
                "resume_text": resume_text,
                "has_resume_file": False,
                "has_custom_prompt": True
            },
            response_data=result,
            status_code=200,
            use_parallel=False
        )
        
        print(f"⏱️  Request processed in {duration:.3f}s")
        
        return jsonify(result), 200
    elif use_parallel:
        # Use parallel processing for faster results
        print("🚀 Using parallel processing mode...")
        try:
            result = call_gemini_parallel(job_description, resume_text, use_parallel=True)
        except Exception as e:
            print(f"⚠️ Parallel processing failed, falling back to sequential: {e}")
            use_parallel = False  # Track that we fell back
            # Fallback to sequential
            print("🤖 Building Gemini prompt...")
            prompt = build_prompt(job_description, resume_text)
            print("🚀 Sending request to Gemini...")
            response_text = call_gemini(prompt)
            print("🧩 Extracting JSON response...")
            result = extract_json_from_text(response_text)
    else:
        # Use original sequential method
        print("🤖 Building Gemini prompt...")
        prompt = build_prompt(job_description, resume_text)
        print("🚀 Sending request to Gemini...")
        response_text = call_gemini(prompt)
        print("🧩 Extracting JSON response...")
        try:
            result = extract_json_from_text(response_text)
        except Exception as e:
            response_time = datetime.now()
            duration = (response_time - request_time).total_seconds()
            log_api_request_response(
                endpoint="/optimize/text",
                request_time=request_time,
                response_time=response_time,
                duration_seconds=duration,
                request_data={
                    "job_description": job_description,
                    "resume_text": resume_text
                },
                response_data={},
                status_code=500,
                error=f'Error extracting JSON from Gemini response: {str(e)}',
                use_parallel=use_parallel
            )
            return jsonify({
                'error': f'Error extracting JSON from Gemini response: {str(e)}',
                'raw_response': response_text[:500] if len(response_text) > 500 else response_text
            }), 500
    
    # Normalize: Convert old 'fortinet_section' to 'work_experience_section' if present
    if 'fortinet_section' in result and 'work_experience_section' not in result:
        result['work_experience_section'] = result.pop('fortinet_section')
        print("  🔄 Normalized: Converted 'fortinet_section' to 'work_experience_section'")
    
    # Record response time and log
    response_time = datetime.now()
    duration = (response_time - request_time).total_seconds()
    
    log_api_request_response(
        endpoint="/optimize/text",
        request_time=request_time,
        response_time=response_time,
        duration_seconds=duration,
        request_data={
            "job_description": job_description,
            "resume_text": resume_text,
            "has_resume_file": False,
            "has_custom_prompt": bool(custom_prompt)
        },
        response_data=result,
        status_code=200,
        use_parallel=use_parallel if not custom_prompt else False
    )
    
    print(f"⏱️  Request processed in {duration:.3f}s")
    
    return jsonify(result), 200


@app.errorhandler(413)
def request_entity_too_large(error):
    """Handle file too large error."""
    return jsonify({
        'error': 'File too large. Maximum size is 16MB.'
    }), 413


@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors."""
    return jsonify({
        'error': 'Endpoint not found',
        'available_endpoints': [
            'GET /health',
            'POST /optimize',
            'POST /optimize/text'
        ]
    }), 404


if __name__ == '__main__':
    # Run the Flask app
    # Default to 8000 to avoid macOS AirPlay Receiver conflict on port 5000
    port = int(os.environ.get('PORT', 8000))
    debug = os.environ.get('FLASK_DEBUG', 'False').lower() == 'true'
    
    print("=" * 60)
    print("🚀 Resume Optimizer API")
    print("=" * 60)
    print(f"📡 Running on http://localhost:{port}")
    print(f"🔧 Debug mode: {debug}")
    print("\nAvailable endpoints:")
    print("  GET  /health          - Health check")
    print("  POST /optimize        - Optimize resume (file or text)")
    print("  POST /optimize/text   - Optimize resume (JSON only)")
    print("=" * 60)
    print(f"\n💡 To use a different port, set PORT environment variable:")
    print(f"   PORT=5001 python app.py")
    print("=" * 60)
    
    app.run(host='0.0.0.0', port=port, debug=debug)

