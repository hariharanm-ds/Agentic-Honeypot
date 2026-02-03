"""
WSGI Entry Point for Production Deployment
Handles root path with pure WSGI to bypass Flask's request parsing
"""

from main import app
import json

class RootPathMiddleware:
    """Middleware that handles root path at WSGI level - completely bypasses Flask"""
    def __init__(self, app):
        self.app = app
    
    def __call__(self, environ, start_response):
        path = environ.get('PATH_INFO', '').rstrip('/')
        
        # Handle root path with pure WSGI (no Flask involved, no parsing)
        if not path or path == '':
            status = '200 OK'
            response_body = json.dumps({
                "status": "ok",
                "service": "agentic-honeypot",
                "version": "1.0"
            }).encode('utf-8')
            headers = [
                ('Content-Type', 'application/json'),
                ('Content-Length', str(len(response_body))),
                ('Access-Control-Allow-Origin', '*'),
                ('Access-Control-Allow-Methods', 'GET,POST,PUT,DELETE,PATCH,HEAD,OPTIONS'),
                ('Access-Control-Allow-Headers', 'Content-Type,X-API-Key,Authorization'),
                ('Cache-Control', 'no-cache, no-store, must-revalidate')
            ]
            start_response(status, headers)
            return [response_body]
        
        # For all other paths, use Flask
        return self.app(environ, start_response)

# Wrap with WSGI middleware at the outermost level
app.wsgi_app = RootPathMiddleware(app.wsgi_app)

if __name__ == "__main__":
    app.run(debug=False)

