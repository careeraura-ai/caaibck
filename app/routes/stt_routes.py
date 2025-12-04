from flask import Blueprint, request, jsonify
from groq import Groq
import os

bp = Blueprint("stt", __name__, url_prefix="/api")

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

@bp.route("/stt", methods=["POST"])
def stt_transcribe():
    if "audio" not in request.files:
        return jsonify({"error": "No audio uploaded"}), 400

    audio = request.files["audio"]

    try:
        result = client.audio.transcriptions.create(
            model="whisper-large-v3",
            file=audio,
            response_format="json"
        )
        return jsonify({"text": result.text})

    except Exception as e:
        return jsonify({"error": str(e)}), 500
