
# 🤖 Sophia Local Agent (PL/I Analyzer)

Sophia Local Agent est une API locale basée sur Flask, conçue pour fonctionner avec l'extension [Continue](https://continue.dev) dans VS Code.  
Elle agit comme un "faux serveur Ollama" pour connecter votre propre logique d'analyse de code PL/I à une interface IA intégrée à votre éditeur.

---

## 🚀 Fonctionnalités

- Lecture de documents internes (PDF, DOCX, XLSX, CSV)
- Extraction automatique des bonnes pratiques à l'initialisation
- Relecture et analyse de code PL/I selon vos standards internes
- API compatible avec les routes `POST /api/generate` et `POST /api/chat` (format Ollama / Continue)
- Mémoire conversationnelle persistante en SQLite

---

## 🧱 Structure du projet

```
sophia-local-agent/
├── app.py                # L'API Flask principale
├── config.py             # Configuration (API Sophia, modèle, etc.)
├── file_loader.py        # Extraction de texte depuis différents formats de fichier
├── memory_manager.py     # Sauvegarde et chargement des échanges utilisateur ↔ agent
├── sophia_agent.py       # Logique de génération et d'analyse via Sophia
├── .env                  # Clé API Sophia (non versionnée)
├── requirements.txt      # Dépendances Python
├── sources/              # 📚 Dossier des documents internes (bonnes pratiques PL/I)
│   ├── guide_pl1.pdf
│   └── normes_docx.docx
└── sophia_memory.db      # Base SQLite créée automatiquement (ignorée par Git)
```

---

## ⚙️ Prérequis

- Python 3.10+
- `pip`
- [Continue extension pour VS Code](https://marketplace.visualstudio.com/items?itemName=Continue.continue)

---

## 📥 Installation

### 1. Clone ou extrait le projet
```bash
git clone monprojet/sophia-local-agent.git
cd sophia-local-agent
```

### 2. Crée un environnement virtuel (recommandé)
```bash
python -m venv venv
source venv/bin/activate  # (ou venv\Scripts\activate sous Windows)
```

### 3. Installe les dépendances
```bash
pip install -r requirements.txt
```

### 4. Crée ton fichier `.env`
```env
SOPHIA_API_KEY=sk-...
```

### 5. Ajoute tes documents internes dans `sources/`
(Ex : PDF ou DOCX expliquant les normes de codage PL/I)

---

## ▶️ Lancement de l'API
```bash
python app.py
```

> L'API sera accessible sur : `http://localhost:8000`

---

## ⚡ Intégration avec VS Code (Continue)

### Exemple de config Continue (`~/.continue/config.json`)

```json
{
  "models": [
    {
      "title": "Sophia Local Agent (PL1)",
      "provider": "ollama",
      "model": "llama3.3:latest",
      "apiBase": "http://localhost:8000",
      "systemMessage": "Tu es un expert PL/I. Sois critique et donne des conseils de refacto.",
      "requestOptions": {
        "headers": {
          "Content-Type": "application/json"
        }
      }
    }
  ],
  "slashCommands": [
    {
      "name": "auditPL1",
      "description": "Analyse le code PL/I sélectionné",
      "model": "Sophia Local Agent (PL1)",
      "prompt": "{{selection}}"
    }
  ]
}
```

> Tu peux maintenant sélectionner du code dans VS Code, taper `/auditPL1`, et recevoir une analyse complète basée sur ton contexte métier.

---

## 🧠 Comment fonctionne le code

### 1. `app.py`  
Expose les routes :
- `/api/generate` → appel direct via Continue
- `/api/chat` → simulation d'une conversation multi-message
- `/` → vérification en navigateur
- `/api/<path>` → fallback pour debug

### 2. `sophia_agent.py`  
- Construit un prompt enrichi avec :
  - Les bonnes pratiques extraites au démarrage
  - L'historique de conversation
- Envoie ce prompt à Sophia via `requests.post(...)`
- Enregistre la réponse dans une base SQLite

### 3. `file_loader.py`  
- Lit tous les fichiers dans `sources/`
- Supporte `.pdf`, `.docx`, `.csv`, `.xlsx`
- Retourne le contenu brut utilisé comme contexte de bonne pratique

### 4. `memory_manager.py`  
- Gère l'historique : insère, lit, et suit les échanges

---

## 🧪 Exemple de requête CURL

```bash
curl -X POST http://localhost:8000/api/generate \
  -H "Content-Type: application/json" \
  -d '{
    "model": "llama3.3:latest",
    "prompt": "Voici du code PL/I : ...\nFais une relecture critique.",
    "stream": false
  }'
```

---

## 🛡️ Sécurité & Git

Ajoute ce `.gitignore` :

```gitignore
.env
sophia_memory.db
__pycache__/
*.pyc
venv/
```

---

## 📬 Besoin d’aide ?
- Teste ton API localement avec Postman / curl
- Vérifie que Continue appelle bien `/api/generate` ou `/api/chat`
- Active les logs dans `app.py` si besoin

---

✅ Avec ce projet, tu rends Sophia capable de devenir un **expert PL/I** intégré à ton IDE, **formé par tes documents internes** et prêt à t’assister au quotidien.
