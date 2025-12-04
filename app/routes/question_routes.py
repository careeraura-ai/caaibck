from flask import Blueprint, jsonify
from app.db import query_all
from app.utils.auth import token_required   # ✅ FIXED


questions_bp = Blueprint("questions", __name__, url_prefix="/api/questions")

@questions_bp.get("/")
def get_questions():
    rows = query_all("SELECT id, section, q_order, question_text, question_type, options FROM questions ORDER BY section, q_order")

    # Convert JSON strings into actual JSON arrays
    formatted = []
    for row in rows:
        formatted.append({
            "id": row["id"],
            "section": row["section"],
            "order": row["q_order"],
            "text": row["question_text"],
            "type": row["question_type"],
            "options": None if row["options"] is None else eval(row["options"])
        })

    return jsonify({"questions": formatted})

@questions_bp.route("/first", methods=["GET"])
@token_required
def get_first_question(current_user):
    q = query_one("""
        SELECT * FROM questions ORDER BY q_order ASC LIMIT 1
    """)
    return jsonify({
        "id": q["id"],
        "text": q["question_text"],
        "type": q["question_type"],
        "options": q["options"]
    })
