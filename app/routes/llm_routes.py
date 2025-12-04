# # app/routes/llm_routes.py
# import os
# import requests
# from flask import Blueprint, request, jsonify, current_app

# bp = Blueprint("llm", __name__, url_prefix="/api/llm")

# # Use clear env names — set these in your .env
# HF_API_KEY = os.getenv("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")
# # Default to a Llama 3.1 instruct model which is known/available on HF (change if desired)
# HF_MODEL = os.getenv("llama-3.3-70b-versatile")

# if not HF_API_KEY:
#     current_app_logger = None
# else:
#     current_app_logger = None  # placeholder — avoid referencing current_app at import time

# HEADERS = {
#     "Authorization": f"Bearer {HF_API_KEY}" if HF_API_KEY else "",
#     "Content-Type": "application/json"
# }

# def hf_inference_url(model_id: str):
#     """Construct HF Inference URL for model_id."""
#     return f"https://api-inference.huggingface.co/models/{model_id}"

# @bp.route("/generate", methods=["POST"])
# def generate():
#     """
#     Expects JSON:
#     {
#       "prompt": "text prompt",
#       "max_tokens": 512,
#       "temperature": 0.2
#     }
#     """
#     payload = request.json or {}
#     prompt = payload.get("prompt")
#     max_tokens = int(payload.get("max_tokens", 512))
#     temp = float(payload.get("temperature", 0.0))

#     if not prompt:
#         return jsonify({"error": "prompt required"}), 400

#     hf_url = hf_inference_url(HF_MODEL)

#     body = {
#         "inputs": prompt,
#         "parameters": {
#             "max_new_tokens": max_tokens,
#             "temperature": temp,
#             # you can add other HF parameters here (top_k, top_p, repetition_penalty, etc.)
#         }
#     }

#     try:
#         # increase timeout for large models; HF may take time
#         r = requests.post(hf_url, headers=HEADERS, json=body, timeout=180)
#         r.raise_for_status()
#     except requests.HTTPError as e:
#         # Helpful diagnostics for common HF errors
#         status = getattr(e.response, "status_code", None)
#         text = getattr(e.response, "text", "")
#         current_app.logger.exception("HF request failed")
#         if status == 410:
#             # Usually means gated model or access/license missing
#             return jsonify({
#                 "error": "model_unavailable",
#                 "detail": "Hugging Face returned 410 (model unavailable or gated). "
#                           "Ensure you accepted the model license on Hugging Face, or choose another model id. "
#                           "Also verify HF_API_KEY has required access."
#             }), 410
#         return jsonify({"error": "inference_failed", "status": status, "detail": text}), 500
#     except requests.RequestException as e:
#         current_app.logger.exception("HF request failed")
#         return jsonify({"error": "inference_failed", "detail": str(e)}), 500

#     # parse response
#     try:
#         out = r.json()
#     except Exception:
#         return jsonify({"ok": True, "model": HF_MODEL, "response": r.text})

#     # Normalize common HF response shapes
#     if isinstance(out, list) and out and isinstance(out[0], dict) and "generated_text" in out[0]:
#         text = out[0]["generated_text"]
#     elif isinstance(out, dict) and "generated_text" in out:
#         text = out["generated_text"]
#     elif isinstance(out, dict) and "error" in out:
#         return jsonify({"error": out.get("error")}), 500
#     else:
#         # fallback: return JSON as-is
#         text = out

#     return jsonify({"ok": True, "model": HF_MODEL, "response": text})
# # app/routes/llm_routes.py# app/routes/llm_routes.py
# import os
# from flask import Blueprint, request, jsonify, current_app
# from groq import Groq

# bp = Blueprint("llm", __name__, url_prefix="/api/llm")

# # Load API key from environment (.env)
# GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# if not GROQ_API_KEY:
#     raise Exception("❌ GROQ_API_KEY not found in environment variables")

# client = Groq(api_key=GROQ_API_KEY)

# # Recommended model (70B)
# MODEL_ID = "llama-3.3-70b-versatile"


# @bp.route("/generate", methods=["POST"])
# def generate():
#     """
#     Expects body:
#     {
#         "prompt": "your txt",
#         "max_tokens": 300,
#         "temperature": 0.3
#     }
#     """

#     data = request.json or {}
#     prompt = data.get("prompt")
#     max_tokens = int(data.get("max_tokens", 300))
#     temp = float(data.get("temperature", 0.3))

#     if not prompt:
#         return jsonify({"error": "Prompt is required"}), 400

#     try:
#         completion = client.chat.completions.create(
#             model=MODEL_ID,
#             messages=[
#                 {"role": "user", "content": prompt}
#             ],
#             max_tokens=max_tokens,
#             temperature=temp,
#         )

#         # FIX: correct path (previous error came from wrong indexing)
#         text = completion.choices[0].message["content"]

#         return jsonify({
#             "ok": True,
#             "model": MODEL_ID,
#             "response": text
#         })

#     except Exception as e:
#         current_app.logger.error(str(e))
#         return jsonify({
#             "error": "llm_error",
#             "detail": str(e)
#         }), 500

# app/routes/llm_routes.py
import os
from flask import Blueprint, request, jsonify, current_app
from groq import Groq

bp = Blueprint("llm", __name__, url_prefix="/api/llm")

# Load API key from .env
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

if not GROQ_API_KEY:
    raise Exception("❌ GROQ_API_KEY not found in environment variables")

client = Groq(api_key=GROQ_API_KEY)

# GROQ Llama 70B
MODEL_ID = os.getenv("LLM_MODEL", "llama-3.3-70b-versatile")


@bp.route("/generate", methods=["POST"])
def generate():
    """
    Body:
    {
        "prompt": "text",
        "max_tokens": 300,
        "temperature": 0.3
    }
    """

    data = request.json or {}
    prompt = data.get("prompt")
    max_tokens = int(data.get("max_tokens", 300))
    temperature = float(data.get("temperature", 0.3))

    if not prompt:
        return jsonify({"error": "Prompt is required"}), 400

    try:
        completion = client.chat.completions.create(
            model=MODEL_ID,
            messages=[
                {"role": "user", "content": prompt}
            ],
            max_tokens=max_tokens,
            temperature=temperature,
        )

        # FIXED — Groq object syntax
        text = completion.choices[0].message.content

        return jsonify({
            "ok": True,
            "model": MODEL_ID,
            "response": text
        })

    except Exception as e:
        current_app.logger.error(str(e))
        return jsonify({
            "error": "llm_error",
            "detail": str(e)
        }), 500

