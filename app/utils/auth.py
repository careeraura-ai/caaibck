# import jwt
# from flask import request, jsonify
# from functools import wraps
# from app.config import SECRET_KEY

# def token_required(f):
#     @wraps(f)
#     def decorated(*args, **kwargs):
#         token = None

#         # token from request header
#         if 'Authorization' in request.headers:
#             auth_header = request.headers['Authorization']
#             if auth_header.startswith("Bearer "):
#                 token = auth_header.split(" ")[1]

#         if not token:
#             return jsonify({"error": "Token missing"}), 401

#         try:
#             data = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
#             user_id = data.get("user_id")

#         except jwt.ExpiredSignatureError:
#             return jsonify({"error": "Token expired"}), 401

#         except Exception as e:
#             return jsonify({"error": f"Invalid token: {str(e)}"}), 401

#         # pass user_id to route
#         return f(user_id, *args, **kwargs)

#     return decorated
import jwt
from flask import request, jsonify
from functools import wraps
from app.config import SECRET_KEY, JWT_ALGORITHM

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None

        if "Authorization" in request.headers:
            auth = request.headers["Authorization"]
            if auth.startswith("Bearer "):
                token = auth.split(" ")[1]

        if not token:
            return jsonify({"error": "Token missing"}), 401

        try:
            data = jwt.decode(token, SECRET_KEY, algorithms=[JWT_ALGORITHM])
            user_id = data.get("user_id")

        except jwt.ExpiredSignatureError:
            return jsonify({"error": "Token expired"}), 401

        except Exception as e:
            return jsonify({"error": f"Invalid token: {str(e)}"}), 401

        return f(user_id, *args, **kwargs)

    return decorated
