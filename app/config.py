# import os
# from dotenv import load_dotenv
# import os

# # -----------------------------
# # FLASK SECRET KEY
# # -----------------------------
# SECRET_KEY = os.environ.get("SECRET_KEY", "super-secret-key-change-this")

# # -----------------------------
# # DATABASE CONFIG
# # -----------------------------
# DB_HOST = os.environ.get("DB_HOST", "localhost")
# DB_USER = os.environ.get("DB_USER", "root")
# DB_PASSWORD = os.environ.get("DB_PASSWORD", "Jithu.Nara@3")   # <-- PUT YOUR PASSWORD HERE
# DB_NAME = os.environ.get("DB_NAME", "career_assessment")

# # -----------------------------
# # JWT CONFIG
# # -----------------------------
# JWT_EXPIRATION_HOURS = 24

# # Load .env file if exists
# load_dotenv()

# # ---------------------------------
# # BASIC APP CONFIG
# # ---------------------------------
# SECRET_KEY = os.getenv("SECRET_KEY", "super-secret-key-change-this")
# JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", SECRET_KEY)

# # ---------------------------------
# # DATABASE CONFIG
# # ---------------------------------
# DB_HOST = os.getenv("DB_HOST", "localhost")
# DB_USER = os.getenv("DB_USER", "root")
# DB_PASSWORD = os.getenv("DB_PASSWORD", "Jithu.Nara@360")
# DB_NAME = os.getenv("DB_NAME", "career_ai")

# # Build MySQL connection dict (used in db.py)
# MYSQL_CONFIG = {
#     "host": DB_HOST,
#     "user": DB_USER,
#     "password": DB_PASSWORD,
#     "database": DB_NAME,
#     "cursorclass": None,
# }

# # ---------------------------------
# # ALLOWED ORIGINS FOR FRONTEND
# # ---------------------------------
# CORS_ORIGINS = [
#     "http://localhost:5173",
#     "http://127.0.0.1:5173",
# ]

import os
from dotenv import load_dotenv
from pymysql.cursors import DictCursor

# Load .env
load_dotenv()

# -----------------------------
# SECRET KEYS
# -----------------------------
SECRET_KEY = os.getenv("JWT_SECRET", "super-secret-key")
JWT_ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")
JWT_EXPIRES_SECONDS = int(os.getenv("JWT_EXPIRES_SECONDS", 86400))

# -----------------------------
# MYSQL CONFIG (UNIFIED)
# -----------------------------
MYSQL_CONFIG = {
    "host": os.getenv("MYSQL_HOST", "127.0.0.1"),
    "port": int(os.getenv("MYSQL_PORT", 3306)),
    "user": os.getenv("MYSQL_USER", "root"),
    "password": os.getenv("MYSQL_PASSWORD", ""),
    "database": os.getenv("MYSQL_DB", "careeraura_db"),
    "cursorclass": DictCursor
}

# -----------------------------
# EMAIL CONFIG
# -----------------------------
SMTP_HOST = os.getenv("SMTP_HOST")
SMTP_PORT = int(os.getenv("SMTP_PORT", 587))
SMTP_USER = os.getenv("SMTP_USER")
SMTP_PASS = os.getenv("SMTP_PASS")
ADMIN_EMAIL = os.getenv("ADMIN_EMAIL")
FROM_EMAIL = os.getenv("FROM_EMAIL")

# -----------------------------
# APP CONFIG
# -----------------------------
APP_BASE_URL = os.getenv("APP_BASE_URL", "http://localhost:5173")

# -----------------------------
# LLM CONFIG
# -----------------------------
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
LLM_MODEL = os.getenv("LLM_MODEL", "llama-3.3-70b-versatile")
