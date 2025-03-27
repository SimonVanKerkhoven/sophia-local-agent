from flask import Flask, request, jsonify
from config import SOPHIA_API_KEY, SOPHIA_BASE_URL, MODEL
from sophia_agent import ask_sophia
from memory_manager import init_db

init_db()
app = Flask(__name__)

@app.route("/api/generate", methods=["POST"])
def generate():
    data = request.get_json()
    prompt = data.get("prompt", "")

    if not prompt:
        return jsonify({"error": "prompt manquant"}), 400

    try:
        response = ask_sophia(prompt)
        return jsonify({
            "model": "llama3.3:latest",
            "response": response,
            "done": True,
            "done_reason": "stop"
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/api/chat", methods=["POST"])
def chat():
    data = request.get_json()
    messages = data.get("messages", [])

    if not messages:
        return jsonify({"error": "Aucun message fourni"}), 400

    try:
        # On concatène tous les messages pour générer un prompt complet
        prompt = ""
        for msg in messages:
            role = msg.get("role")
            content = msg.get("content")

            if isinstance(content, list):
                # Si le contenu est une liste (Continue parfois structure comme ça)
                content = "\n".join([c.get("text", "") for c in content if isinstance(c, dict)])

            if role == "system":
                prompt += f"[System Instructions]: {content}\n"
            elif role == "user":
                prompt += f"Utilisateur: {content}\n"
            elif role == "assistant":
                prompt += f"SophiaBot: {content}\n"

        # Appel à SophiaBot avec le prompt reconstruit
        response = ask_sophia(prompt.strip())

        return jsonify({
            "message": {
                "role": "assistant",
                "content": response
            }
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# ✅ Route générique pour capturer les appels inconnus comme /api/chat
@app.route("/api/<path:path>", methods=["POST", "GET"])
def fallback(path):
    return jsonify({
        "error": f"Endpoint non supporté : /api/{path}"
    }), 404

# ✅ Home route si on ouvre dans un navigateur
@app.route("/", methods=["GET"])
def home():
    return "✅ SophiaBot API est en ligne !", 200

if __name__ == "__main__":
    app.run(port=8000)
