from flask import request, jsonify
from functools import wraps
import jwt
from utils.jwt import decode_jwt_token

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        # Check if token is provided in headers
        if 'Authorization' in request.headers:
            token = request.headers['Authorization'].split(" ")[1]
        
        if not token:
            return jsonify({"message": "Authorization token is missing!"}), 403
        
        try:
            # Decode the token
            data = decode_jwt_token(token)
            if data.get("error"):
                return jsonify({"message": data["error"]}), 401
            
            # print("data 23 : ", data)
            # current_user = data['user_id']  # Retrieve user_id from decoded token
            current_user = data
        except jwt.ExpiredSignatureError:
            return jsonify({"message": "Token has expired"}), 401
        except jwt.InvalidTokenError:
            return jsonify({"message": "Invalid token"}), 401

        return f(current_user, *args, **kwargs)  # Pass user_id to the route
    return decorated
