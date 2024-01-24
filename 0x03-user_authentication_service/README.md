## User Authentication


In Flask, you can declare API routes using the @app.route decorator. You can handle different HTTP methods (GET, POST, etc.) and parameters in these routes. Here's a basic example:

```
from flask import Flask, request, jsonify

app = Flask(__name__)

# Define a basic route
@app.route('/')
def hello_world():
    return 'Hello, World!'

# Define a route with parameters
@app.route('/greet/<name>')
def greet(name):
    return f'Hello, {name}!'

# Define a route for handling POST requests with JSON data
@app.route('/post_example', methods=['POST'])
def post_example():
    data = request.get_json()
    return jsonify({'received_data': data})

# Define a route for setting and getting cookies
@app.route('/set_cookie')
def set_cookie():
    resp = jsonify({'message': 'Cookie set successfully'})
    resp.set_cookie('user', 'John Doe')
    return resp

@app.route('/get_cookie')
def get_cookie():
    username = request.cookies.get('user')
    return f'Hello, {username}!'

# Define a route for retrieving form data
@app.route('/submit_form', methods=['POST'])
def submit_form():
    username = request.form.get('username')
    password = request.form.get('password')
    return f'Form submitted with username: {username}, password: {password}'

# Define a route with custom HTTP status code
@app.route('/custom_status')
def custom_status():
    return 'Custom status code', 418  # 418 is "I'm a teapot" status code

if __name__ == '__main__':
    app.run(debug=True)
```
