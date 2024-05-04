from flask import Flask, request, abort
import re
import html

app = Flask(__name__)

# Regular expressions for detecting SQL injection and XSS patterns
SQLI_REGEX = re.compile(r'.*?(select|union|insert|update|delete|drop|alter|create).*?', re.IGNORECASE)
XSS_REGEX = re.compile(r'<\s*script[^>]*>.*?<\s*/\s*script\s*>', re.IGNORECASE)

@app.before_request
def firewall():
    # Inspect request parameters
    if request.method == 'GET':
        params = request.args
    elif request.method == 'POST':
        params = request.form
    else:
        params = {}

    # Check for SQL injection
    for key, value in params.items():
        if SQLI_REGEX.match(value):
            # Block request if SQL injection detected
            abort(403)  # Forbidden

    # Check for XSS
    for key, value in params.items():
        if XSS_REGEX.search(value):
            # Sanitize the value to prevent XSS
            sanitized_value = html.escape(value)
            params[key] = sanitized_value

@app.route('/')
def index():
    return 'Welcome to the protected web application!'

if __name__ == '__main__':
    app.run(debug=True)
