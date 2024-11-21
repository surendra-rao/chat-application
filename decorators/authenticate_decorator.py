from functools import wraps
from flask import request, current_app
from flask_socketio import disconnect
import jwt
import base64

def authenticate_decorator(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        auth_header = request.headers.get('Authorization')
        print(auth_header, "Header received")
        
        # Check for 'Bearer' prefix and extract token
        if auth_header and auth_header.startswith("Bearer "):
            token = auth_header.split(" ")[1]
        else:
            print("Authentication token missing or malformed.")
            disconnect()
            return

        # Ensure the token has the correct padding for Base64 decoding
        token += "=" * ((4 - len(token) % 4) % 4)  # Add necessary padding if missing
        print(token)
        
        try:
            # Decode the token
            decoded_token = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=["HS256"])
            request.user = decoded_token['user_id']
        except jwt.ExpiredSignatureError:
            print("Token has expired.")
            disconnect()
            return
        except jwt.InvalidTokenError:
            print("Invalid authentication token.")
            disconnect()
            return
        except Exception as e:
            print(f"Unexpected error during token decoding: {e}")
            disconnect()
            return
        
        return f(*args, **kwargs)
    return decorated_function
