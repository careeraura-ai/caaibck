# # # app.py
# # import os
# # from flask import Flask, jsonify, request
# # from dotenv import load_dotenv

# # load_dotenv()

# # from app.routes.auth_routes import bp as auth_bp
# # from app.routes.questions_routes import bp as q_bp
# # from app.routes.submissions_routes import bp as s_bp

# # def create_app():
# #     app = Flask(__name__)
# #     app.config["JSON_SORT_KEYS"] = False

# #     app.register_blueprint(auth_bp)
# #     app.register_blueprint(q_bp)
# #     app.register_blueprint(s_bp)

# #     # lightweight contact endpoint for clicks from PDF (GET or POST)
# #     @app.route("/api/contact-report", methods=["GET","POST"])
# #     def contact_report():
# #         report_id = request.args.get("report_id") or request.json.get("report_id")
# #         user_email = request.args.get("email") or request.json.get("email")
# #         message = request.args.get("message") or (request.json and request.json.get("message")) or "User clicked contact from PDF"
# #         # save to DB
# #         from app.db import execute
# #         click_id = execute("INSERT INTO contact_clicks (report_id, user_email, message) VALUES (%s,%s,%s)",
# #                            (report_id, user_email, message))
# #         # notify admin
# #         from reports_utils import send_email_with_attachment
# #         admin = os.getenv("ADMIN_EMAIL")
# #         try:
# #              send_email_with_attachment(admin, f"[CareerAura] Contact request for report {report_id}",
# #                            f"User {user_email} clicked contact: {message}", attachment_path=None)

# #         except Exception as e:
# #             app.logger.error("Failed to notify admin: %s", e)
# #         return jsonify({"ok": True, "click_id": click_id})

# #     @app.route("/health", methods=["GET"])
# #     def health():
# #         return jsonify({"ok": True})

# #     return app

# # if __name__ == "__main__":
# #     app = create_app()
# #     port = int(os.getenv("PORT", 5001))
# #     app.run(host="0.0.0.0", port=port, debug=True)

# import os
# from flask import Flask, jsonify, request
# from dotenv import load_dotenv

# load_dotenv()

# # Correct imports from app/
# from app.routes.auth_routes import bp as auth_bp
# from app.routes.question_routes import bp as q_bp
# from app.routes.submissions_routes import bp as s_bp
# from app.db import execute
# from app.reports_utils import send_email_with_attachment


# def create_app():
#     app = Flask(__name__)
#     app.config["JSON_SORT_KEYS"] = False

#     app.register_blueprint(auth_bp)
#     app.register_blueprint(q_bp)
#     app.register_blueprint(s_bp)

#     @app.route("/api/contact-report", methods=["GET", "POST"])
#     def contact_report():
#         data = request.json or {}
        
#         report_id = request.args.get("report_id") or data.get("report_id")
#         user_email = request.args.get("email") or data.get("email")
#         message = request.args.get("message") or data.get("message") or "User clicked contact from PDF"

#         click_id = execute(
#             "INSERT INTO contact_clicks (report_id, user_email, message) VALUES (%s,%s,%s)",
#             (report_id, user_email, message)
#         )

#         admin = os.getenv("ADMIN_EMAIL")

#         try:
#             send_email_with_attachment(
#                 admin,
#                 f"[CareerAura] Contact request for report {report_id}",
#                 f"User {user_email} clicked contact: {message}",
#                 attachment_path=None
#             )
#         except Exception as e:
#             app.logger.error("Admin email failed: %s", e)

#         return jsonify({"ok": True, "click_id": click_id})

#     @app.route("/health", methods=["GET"])
#     def health():
#         return jsonify({"ok": True})

#     return app


# if __name__ == "__main__":
#     app = create_app()
#     port = int(os.getenv("PORT", 5001))
#     app.run(host="0.0.0.0", port=port, debug=True)
from app import create_app
import os

app = create_app()

if __name__ == "__main__":
    port = int(os.getenv("PORT", 5001))
    app.run(host="0.0.0.0", port=port, debug=True)
