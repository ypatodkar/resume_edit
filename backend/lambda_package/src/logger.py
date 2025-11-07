"""
Logging utility for API requests and responses.
"""
import json
import os
from datetime import datetime

# Calculate BASE_DIR (project root - one level up from backend)
_current_file = os.path.abspath(__file__)
_src_dir = os.path.dirname(_current_file)
_backend_dir = os.path.dirname(_src_dir)
BASE_DIR = os.path.dirname(_backend_dir)


# Log directory
LOG_DIR = os.path.join(BASE_DIR, "data", "logs")
LOG_FILE = os.path.join(LOG_DIR, "api_responses.log")


def ensure_log_directory():
    """Ensure the log directory exists."""
    os.makedirs(LOG_DIR, exist_ok=True)


def log_api_request_response(
    endpoint: str,
    request_time: datetime,
    response_time: datetime,
    duration_seconds: float,
    request_data: dict,
    response_data: dict,
    status_code: int = 200,
    error: str = None,
    use_parallel: bool = False
):
    """
    Log API request and response to a file.
    
    Args:
        endpoint: The API endpoint called
        request_time: Timestamp when request was received
        response_time: Timestamp when response was sent
        duration_seconds: Time taken to process (in seconds)
        request_data: Request data (job_description, resume_text length, etc.)
        response_data: Response data (the JSON response)
        status_code: HTTP status code
        error: Error message if any
        use_parallel: Whether parallel processing was used
    """
    ensure_log_directory()
    
    # Prepare log entry
    log_entry = {
        "timestamp": {
            "request_sent": request_time.isoformat(),
            "response_received": response_time.isoformat(),
            "duration_seconds": round(duration_seconds, 3),
            "duration_formatted": f"{duration_seconds:.3f}s"
        },
        "endpoint": endpoint,
        "processing_mode": "parallel" if use_parallel else "sequential",
        "status_code": status_code,
        "request": {
            "job_description_length": len(request_data.get("job_description", "")),
            "resume_text_length": len(request_data.get("resume_text", "")),
            "has_resume_file": request_data.get("has_resume_file", False)
        },
        "response": response_data if not error else None,
        "error": error
    }
    
    # Append to log file
    try:
        with open(LOG_FILE, "a", encoding="utf-8") as f:
            f.write(json.dumps(log_entry, ensure_ascii=False) + "\n")
    except Exception as e:
        print(f"⚠️ Failed to write to log file: {e}")

