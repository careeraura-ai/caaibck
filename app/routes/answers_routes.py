# from flask import Blueprint, request, jsonify
# from app.db import execute, query_one
# from app.utils.auth import token_required

# answers_bp = Blueprint("answers", __name__)

# @answers_bp.route("/save", methods=["POST"])
# @token_required
# def save_answer(current_user):
#     data = request.get_json()

#     user_id = current_user["id"]
#     question_id = data.get("question_id")
#     answer = data.get("answer")

#     if not question_id or not answer:
#         return jsonify({"error": "Missing question_id or answer"}), 400

#     # Check if question exists
#     question = query_one("SELECT id FROM questions WHERE id = %s", (question_id,))
#     if not question:
#         return jsonify({"error": "Invalid question_id"}), 400

#     # Insert into user_answers
#     execute(
#         "INSERT INTO user_answers (user_id, question_id, answer) VALUES (%s, %s, %s)",
#         (user_id, question_id, answer)
#     )

#     return jsonify({"message": "Answer saved successfully"})
from flask import Blueprint, request, jsonify
from app.db import query_one, query_all, execute
from app.utils.auth import token_required

answers_bp = Blueprint("answers", __name__, url_prefix="/api/answers")

@answers_bp.route("/submit", methods=["POST"])
@token_required
def submit_answer(current_user):
    data = request.json
    question_id = data.get("question_id")
    answer = data.get("answer")

    if not question_id or answer is None:
        return jsonify({"error": "question_id and answer required"}), 400

    # Save user answer
    execute("""
        INSERT INTO user_answers (user_id, question_id, answer)
        VALUES (%s, %s, %s)
    """, (current_user["id"], question_id, answer))

    # Get next question
    next_q = query_one("""
        SELECT * FROM questions 
        WHERE q_order > (SELECT q_order FROM questions WHERE id = %s)
        ORDER BY q_order ASC
        LIMIT 1
    """, (question_id,))

    if not next_q:
        return jsonify({"done": True, "message": "All questions completed!"})

    return jsonify({
        "done": False,
        "next_question": {
            "id": next_q["id"],
            "text": next_q["question_text"],
            "type": next_q["question_type"],
            "options": next_q["options"]
        }
    })
