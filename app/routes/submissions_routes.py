# submissions_routes.py
import os
import json
import uuid
from flask import Blueprint, request, jsonify, current_app, url_for
from app.db import execute, query_one
from app.reports_utils import create_pdf_report_and_save, send_email_with_attachment

bp = Blueprint("submissions", __name__, url_prefix="/api")

@bp.route("/submit", methods=["POST"])
def submit():
    """
    Expected JSON:
    {
      "session_id": "optional string (if anonymous)",
      "token": "optional jwt",
      "user_email": "user email",
      "answers": { ... }
    }
    """
    payload = request.json or {}
    session_id = payload.get("session_id") or str(uuid.uuid4())
    token = payload.get("token")
    user_email = payload.get("user_email")
    answers = payload.get("answers")
    if not answers:
        return jsonify({"error":"answers required"}), 400

    user_id = None
    # if JWT provided, decode to get user_id -- minimal here
    if token:
        try:
            import jwt, time
            decoded = jwt.decode(token, os.getenv("JWT_SECRET"), algorithms=[os.getenv("JWT_ALGORITHM","HS256")])
            user_id = decoded.get("sub")
        except Exception:
            user_id = None

    # Save response
    resp_id = execute(
        "INSERT INTO responses (user_id, session_id, answers) VALUES (%s,%s,%s)",
        (user_id, session_id, json.dumps(answers))
    )

    # Make a summary (placeholder — you'd call LLM for meaningful summary later)
    summary = "Partial summary: user answered the questionnaire. For detailed analysis, contact us."

    # update the summary
    execute("UPDATE responses SET summary = %s WHERE id = %s", (summary, resp_id))

    # Create PDF
    pdf_path = create_pdf_report_and_save(resp_id, answers, user_email, summary)

    # Save report metadata
    report_id = execute("INSERT INTO reports (response_id, pdf_path, user_email) VALUES (%s,%s,%s)",
                        (resp_id, pdf_path, user_email))

    # Email PDF to user (partial) and admin (notification)
    try:
        send_email_with_attachment(
            to_email=user_email,
            subject="Your Vajra — Partial Career Report",
            body=f"Hi,\n\nAttached is your partial career report. For full guidance, please click the 'Contact Us' link in the PDF or reply to this email.",
            attachment_path=pdf_path
        )
    except Exception as e:
        current_app.logger.error("Failed to send user email: %s", e)

    # Notify admin too (we can send a short email)
    try:
        admin_email = os.getenv("ADMIN_EMAIL")
        send_email_with_attachment(
            to_email=admin_email,
            subject=f"[Vajra] New assessment submitted (id={resp_id})",
            body=f"New submission by {user_email or 'unknown'}. Session {session_id}.",
            attachment_path=None
        )
    except Exception as e:
        current_app.logger.error("Failed to send admin email: %s", e)

    return jsonify({"ok": True, "response_id": resp_id, "report_id": report_id})
