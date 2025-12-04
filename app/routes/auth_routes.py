# auth_routes.py
import os
import time
import jwt
from flask import Blueprint, request, jsonify
from email_validator import validate_email, EmailNotValidError
import bcrypt

from app.db import query_one, execute

bp = Blueprint("auth", __name__, url_prefix="/api/auth")

JWT_SECRET = os.getenv("JWT_SECRET", "devsecret")
JWT_ALG = os.getenv("JWT_ALGORITHM", "HS256")
JWT_EXP = int(os.getenv("JWT_EXPIRES_SECONDS", 86400))

@bp.route("/register", methods=["POST"])
def register():
    data = request.json or {}
    email = (data.get("email") or "").strip().lower()
    password = data.get("password") or ""
    name = data.get("name", "")

    if not email or not password:
        return jsonify({"error":"email and password required"}), 400

    try:
        validate_email(email)
    except EmailNotValidError as e:
        return jsonify({"error": str(e)}), 400

    existing = query_one("SELECT id FROM users WHERE email = %s", (email,))
    if existing:
        return jsonify({"error":"Email already registered"}), 400

    pw_hash = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode()
    user_id = execute("INSERT INTO users (email, password_hash, full_name) VALUES (%s,%s,%s)",
                      (email, pw_hash, name))
    token = jwt.encode({"sub": user_id, "email": email, "exp": time.time() + JWT_EXP}, JWT_SECRET, algorithm=JWT_ALG)
    return jsonify({"token": token, "user": {"id": user_id, "email": email, "name": name}})


@bp.route("/login", methods=["POST"])
def login():
    data = request.json or {}
    email = (data.get("email") or "").strip().lower()
    password = data.get("password") or ""

    if not email or not password:
        return jsonify({"error":"email and password required"}), 400

    user = query_one("SELECT id, password_hash, full_name FROM users WHERE email = %s", (email,))
    if not user:
        return jsonify({"error":"Invalid credentials"}), 401

    if not bcrypt.checkpw(password.encode("utf-8"), user["password_hash"].encode("utf-8")):
        return jsonify({"error":"Invalid credentials"}), 401

    token = jwt.encode({"sub": user["id"], "email": email, "exp": time.time() + JWT_EXP}, JWT_SECRET, algorithm=JWT_ALG)
    return jsonify({"token": token, "user": {"id": user["id"], "email": email, "name": user.get("full_name")}})
