## Authentication
- _Authentication_ is the process of verifying the identity of a user, system, or application. It ensures that the entity trying to access a particular resource or perform an action is who it claims to be. 
- Authentication mechanisms commonly involve the use of credentials such as usernames and passwords, biometric data, security tokens, or other methods to establish the identity of the user or system.

## Session Authentication
- _Session authentication_ specifically refers to the process of verifying the identity of a user for the duration of a session. A session typically starts when a user logs in and ends when they log out. During this time, the user is considered authenticated, and access to various resources is granted based on their identity.

### What is a cookie
- **Cookies** are small pieces of data stored on a user's device by their web browser. They are commonly used to store information about the user, their preferences, and session-related data. 
- Cookies can be either first-party cookies (associated with the domain of the website being visited) or third-party cookies (associated with a domain other than the one the user is currently visiting).

- To send cookies to a user's browser, the server includes a `Set-Cookie` HTTP header in its response. The header contains information about the cookie, such as its name, value, expiration date, path, and domain. Here's an example of a `Set-Cookie` header:

```
Set-Cookie: username=johndoe; expires=Wed, 18 Jan 2024 12:00:00 GMT; path=/; domain=example.com
```

### How to parse a cookie
- To parse cookies on the server side, the incoming HTTP request headers are examined. The `Cookie` header contains the cookies sent by the client. In many programming languages, web frameworks provide libraries or functions to parse and access cookies easily.

- Here's a basic example in Python using the Flask framework:
```
from flask import Flask, request

app = Flask(__name__)

@app.route('/')
def index():
    # Accessing cookies from the request object
    username_cookie = request.cookies.get('username')
    
    # Your code to handle the username_cookie value

    return 'Hello, {}'.format(username_cookie)

if __name__ == '__main__':
    app.run()
```
