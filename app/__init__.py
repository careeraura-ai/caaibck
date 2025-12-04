# # backend/app/__init__.py

# import os
# from flask import Flask, jsonify, request
# from dotenv import load_dotenv

# load_dotenv()

# def create_app():
#     app = Flask(__name__)
#     app.config["JSON_SORT_KEYS"] = False

#     # Import blueprints *after* app is created
#     from app.routes.auth_routes import bp as auth_bp
#     from app.routes.question_routes import bp as questions_bp
#     from app.routes.submissions_routes import bp as submissions_bp
#     from app.routes.llm_routes import bp as llm_bp
    
#     app.register_blueprint(llm_bp)
#     app.register_blueprint(auth_bp)
#     app.register_blueprint(questions_bp)
#     app.register_blueprint(submissions_bp)

#     @app.route("/health")
#     def health():
#         return jsonify({"ok": True})

# from flask_cors import CORS

# def create_app():
#     app = Flask(__name__)
#     CORS(app, resources={r"/*": {"origins": "*"}})

#     return app

import os
from flask import Flask, jsonify
from flask_cors import CORS
from dotenv import load_dotenv

load_dotenv()

def create_app():
    load_dotenv()
    app = Flask(__name__)
    app.config["SECRET_KEY"] = os.getenv("JWT_SECRET", "default-secret")

    # --- CORS SETTINGS ---
    CORS(app,
         resources={r"/*": {"origins": [
             "http://localhost:5173",          # local dev
             "https://caai.vercel.app"         # your Vercel frontend
         ]}},
         supports_credentials=True)
    
    # CORS(app)  # allow frontend requests
    # app.config["JSON_SORT_KEYS"] = False

    # ---- REGISTER BLUEPRINTS ----
    from app.routes.auth_routes import bp as auth_bp
    from app.routes.submissions_routes import bp as submissions_bp
    from app.routes.llm_routes import bp as llm_bp
    from app.routes.stt_routes import bp as stt_bp
    from app.routes.question_routes import questions_bp
    from app.routes.answers_routes import answers_bp
    
    app.register_blueprint(answers_bp, url_prefix="/api/answers")
    app.register_blueprint(questions_bp)
    app.register_blueprint(stt_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(submissions_bp)
    app.register_blueprint(llm_bp)

    # ---- HEALTH CHECK ----
    @app.route("/health", methods=["GET"])
    def health():
        return jsonify({"ok": True})

    return app
