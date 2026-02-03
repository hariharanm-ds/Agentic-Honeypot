"""
WSGI Entry Point for Production Deployment
Comprehensive error handling at WSGI level - ROOT PATH PRIORITY
"""

from main import app
import json
import logging

logger = logging.getLogger(__name__)

class ProductionMiddleware:
    """
    Production-grade WSGI middleware that:
    1. FIRST: Handle root path with pure WSGI (zero Flask involvement)
    2. Then: Pass all other requests to Flask
    3. Always: Return valid JSON, never HTML
    """
    def __init__(self, app):
        self.app = app
    
    def __call__(self, environ, start_response):
        path = environ.get('PATH_INFO', '').rstrip('/') or '/'
        
        try:
            # PRIORITY: Handle root path FIRST at WSGI level (no Flask parsing)
            if path in ['/', ''] or not path.strip('/'):
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
            
            # For all other paths, pass to Flask
            return self.app(environ, start_response)
        
        except Exception as e:
            # Catch ANY error at WSGI level and return valid JSON
            logger.error(f"WSGI error: {type(e).__name__}: {str(e)}")
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

# CRITICAL: Apply middleware BEFORE Flask processes anything
app.wsgi_app = ProductionMiddleware(app.wsgi_app)

if __name__ == "__main__":
    app.run(debug=False)

