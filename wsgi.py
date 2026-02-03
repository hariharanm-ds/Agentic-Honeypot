"""
WSGI Entry Point for Production Deployment
Minimal middleware - only handle GET / at WSGI level
"""

from main import app
import json

class RootOnlyMiddleware:
    """WSGI middleware - only intercept GET / requests, pass everything else to Flask"""
    def __init__(self, app):
        self.app = app
    
    def __call__(self, environ, start_response):
        path = environ.get('PATH_INFO', '').rstrip('/') or '/'
        method = environ.get('REQUEST_METHOD', 'GET')
        
        # Only handle GET / at WSGI level (zero Flask involvement)
        if path in ['/', ''] and method == 'GET':
            status = '200 OK'
            response_body = json.dumps({
                "status": "ok",
                "service": "agentic-honeypot",
                "version": "1.0"
            }).encode('utf-8')
            
            headers = [
                ('Content-Type', 'application/json; charset=utf-8'),
                ('Content-Length', str(len(response_body))),
                ('Access-Control-Allow-Origin', '*')
            ]
            start_response(status, headers)
            return [response_body]
        
        # If POST/PUT/DELETE on /, reject at WSGI level
        if path in ['/', ''] and method in ['POST', 'PUT', 'DELETE', 'PATCH']:
            status = '405 Method Not Allowed'
            response_body = json.dumps({
                "error": "Method Not Allowed",
                "message": "Only GET allowed on root endpoint"
            }).encode('utf-8')
            
            headers = [
                ('Content-Type', 'application/json; charset=utf-8'),
                ('Content-Length', str(len(response_body))),
                ('Access-Control-Allow-Origin', '*')
            ]
            start_response(status, headers)
            return [response_body]
        
        # For all other requests (/api/*, etc.), pass to Flask
        return self.app(environ, start_response)

# Apply middleware at outermost level
app.wsgi_app = RootOnlyMiddleware(app.wsgi_app)

if __name__ == "__main__":
    app.run(debug=False)

