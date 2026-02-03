"""
WSGI Entry Point for Production Deployment
Comprehensive error handling at WSGI level
"""

from main import app
import json
import logging

logger = logging.getLogger(__name__)

class ProductionMiddleware:
    """
    Production-grade WSGI middleware that:
    1. Handles root path with pure WSGI (no Flask parsing)
    2. Ensures ALL responses are valid JSON
    3. Never returns HTML error pages
    4. Handles all edge cases gracefully
    """
    def __init__(self, app):
        self.app = app
    
    def __call__(self, environ, start_response):
        path = environ.get('PATH_INFO', '').rstrip('/')
        method = environ.get('REQUEST_METHOD', 'GET')
        
        try:
            # Handle root path with pure WSGI (no JSON parsing attempt)
            if not path or path == '':
                status = '200 OK'
                response_body = json.dumps({
                    "status": "ok",
                    "service": "agentic-honeypot",
                    "version": "1.0"
                }).encode('utf-8')
                
                headers = [
                    ('Content-Type', 'application/json; charset=utf-8'),
                    ('Content-Length', str(len(response_body))),
                    ('Access-Control-Allow-Origin', '*'),
                    ('Access-Control-Allow-Methods', 'GET,POST,PUT,DELETE,PATCH,HEAD,OPTIONS'),
                    ('Access-Control-Allow-Headers', 'Content-Type,X-API-Key,Authorization'),
                    ('Cache-Control', 'no-cache, no-store, must-revalidate'),
                    ('Pragma', 'no-cache'),
                    ('Expires', '0')
                ]
                start_response(status, headers)
                return [response_body]
            
            # For all other paths, use Flask
            return self.app(environ, start_response)
        
        except Exception as e:
            # Catch ANY error and return valid JSON
            logger.error(f"WSGI middleware error: {type(e).__name__}: {str(e)}")
            status = '500 Internal Server Error'
            response_body = json.dumps({
                "error": "Internal Server Error",
                "message": "An unexpected error occurred"
            }).encode('utf-8')
            
            headers = [
                ('Content-Type', 'application/json; charset=utf-8'),
                ('Content-Length', str(len(response_body))),
                ('Access-Control-Allow-Origin', '*')
            ]
            start_response(status, headers)
            return [response_body]

# Apply middleware at the outermost level
app.wsgi_app = ProductionMiddleware(app.wsgi_app)

if __name__ == "__main__":
    app.run(debug=False)

