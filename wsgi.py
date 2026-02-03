"""
WSGI Entry Point for Vercel Deployment
This file exports the Flask application for serverless deployment
"""

from src.api import app

# Vercel expects the application to be called 'app'
if __name__ == "__main__":
    app.run(debug=False)
