from file_loader import load_all_documents
from memory_manager import load_history, save_message
import requests
import os
from config import SOPHIA_API_KEY, SOPHIA_BASE_URL, MODEL

HEADERS = {
    "Authorization": f"Bearer {SOPHIA_API_KEY}",
    "Content-Type": "application/json"
}

# Charger une seule fois le contexte documentaire
DOCUMENT_CONTEXT = load_all_documents()

def build_prompt():
    history = load_history()
    prompt_parts = [
        "Tu es SophiaBot, un agent expert en relecture de code mainframe PL1.",
        "Tu évalues chaque extrait de code à la lumière des bonnes pratiques suivantes :",
        DOCUMENT_CONTEXT,
        "Voici l'historique de la conversation :"
    ]

    for role, message in history[-10:]:
        prefix = "Utilisateur:" if role == "user" else "SophiaBot:"
        prompt_parts.append(f"{prefix} {message}")

    prompt_parts.append("Nouvelle demande de l’utilisateur :")
    return "\n".join(prompt_parts)

def ask_sophia(user_message):
    save_message("user", user_message)
    full_prompt = build_prompt() + "\n" + user_message

    payload = {
        "model": MODEL,
        "prompt": full_prompt,
        "stream": False
    }

    response = requests.post(f"{SOPHIA_BASE_URL}/api/generate", json=payload, headers=HEADERS)
    response_data = response.json()

    sophia_reply = response_data.get('response', '[Erreur dans la réponse]')
    save_message("sophia", sophia_reply)

    return sophia_reply
