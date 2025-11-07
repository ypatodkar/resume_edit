"""
AWS Lambda handler for Resume Optimizer API
"""
import sys
import os

# Add src directory to Python path
backend_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(backend_root, 'src'))

from app import app
from mangum import Mangum

# Create Mangum adapter for Flask app
handler = Mangum(app, lifespan="off")

def lambda_handler(event, context):
    """
    AWS Lambda handler function.
    
    This wraps the Flask app to work with API Gateway using Mangum.
    """
    return handler(event, context)

