"""
Simple test script for the Resume Optimizer API
"""
import requests
import json
import os

BASE_URL = os.environ.get('API_URL', "http://localhost:8000")


def test_health():
    """Test health check endpoint."""
    print("Testing /health endpoint...")
    response = requests.get(f"{BASE_URL}/health")
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    print()


def test_optimize_text():
    """Test optimize endpoint with text input."""
    print("Testing /optimize/text endpoint...")
    
    data = {
        "resume_text": """
        John Doe
        Software Engineer
        
        SUMMARY
        Software engineer with 3+ years of experience building web applications.
        
        TECHNICAL SKILLS
        Python, JavaScript, React, Node.js, AWS
        
        EXPERIENCE
        Software Engineer at Tech Company
        - Built scalable microservices
        - Implemented CI/CD pipelines
        
        PROJECTS
        1. E-commerce Platform
        - Developed full-stack application using React and Node.js
        Technologies: React, Node.js, MongoDB
        
        2. Task Management App
        - Created RESTful API with Python Flask
        Technologies: Python, Flask, PostgreSQL
        """,
        "job_description": """
        Software Engineer
        
        We are looking for a Software Engineer with experience in:
        - Python, TypeScript, and AWS
        - Data structures and algorithms
        - Microservices architecture
        - CI/CD pipelines
        """
    }
    
    response = requests.post(f"{BASE_URL}/optimize/text", json=data)
    print(f"Status: {response.status_code}")
    
    if response.status_code == 200:
        result = response.json()
        print(f"Response: {json.dumps(result, indent=2)}")
    else:
        print(f"Error: {response.json()}")
    print()


def test_optimize_file():
    """Test optimize endpoint with file upload."""
    print("Testing /optimize endpoint with file upload...")
    
    # Check if resume file exists (relative to project root)
    import os
    backend_root = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(backend_root)
    resume_path = os.path.join(project_root, "data", "input", "resume.docx")
    
    if not os.path.exists(resume_path):
        print(f"⚠️  Resume file not found at {resume_path}")
        print("   Skipping file upload test...")
        return
    
    with open(resume_path, 'rb') as f:
        files = {'resume_file': f}
        data = {
            'job_description': """
            Software Engineer
            
            We are looking for a Software Engineer with experience in:
            - Python, TypeScript, and AWS
            - Data structures and algorithms
            - Microservices architecture
            """
        }
        
        response = requests.post(f"{BASE_URL}/optimize", files=files, data=data)
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print(f"Response keys: {list(result.keys())}")
            print(f"Summary: {result.get('summary', 'N/A')[:100]}...")
        else:
            print(f"Error: {response.json()}")
    print()


if __name__ == "__main__":
    print("=" * 60)
    print("🧪 Testing Resume Optimizer API")
    print("=" * 60)
    print()
    
    try:
        test_health()
        test_optimize_text()
        test_optimize_file()
        
        print("=" * 60)
        print("✅ All tests completed!")
        print("=" * 60)
    except requests.exceptions.ConnectionError:
        print("❌ Error: Could not connect to API.")
        print("   Make sure the Flask server is running:")
        print("   python app.py")
    except Exception as e:
        print(f"❌ Error: {e}")

