"""
WSGI Entry Point for Production Deployment
"""

from main import app

class RootPathMiddleware:
    """Middleware that handles root path at WSGI level - completely bypasses Flask"""
    def __init__(self, app):
        self.app = app
    
    def __call__(self, environ, start_response):
        path = environ.get('PATH_INFO', '')
        
        # Handle root path with pure WSGI (no Flask involved)
        if path in ['/', ''] or path.strip('/') == '':
            status = '200 OK'
            response_body = b'{"status":"ok","service":"agentic-honeypot","version":"1.0"}'
            headers = [
                ('Content-Type', 'application/json'),
                ('Content-Length', str(len(response_body))),
                ('Access-Control-Allow-Origin', '*'),
                ('Access-Control-Allow-Methods', 'GET,POST,PUT,DELETE,PATCH,HEAD,OPTIONS'),
                ('Access-Control-Allow-Headers', 'Content-Type,X-API-Key')
            ]
            start_response(status, headers)
            return [response_body]
        
        # For all other paths, use Flask normally
        return self.app(environ, start_response)

# Wrap with pure WSGI middleware (before Flask touches anything)
app.wsgi_app = RootPathMiddleware(app.wsgi_app)

if __name__ == "__main__":
    app.run(debug=False)

