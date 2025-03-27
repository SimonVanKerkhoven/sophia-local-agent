
import os
from dotenv import load_dotenv

# Charge automatiquement les variables du fichier .env
load_dotenv()

SOPHIA_API_KEY = os.getenv("SOPHIA_API_KEY")
SOPHIA_BASE_URL = "https://sophia.nrb.be/ollama"
MODEL = "llama3.3:latest"