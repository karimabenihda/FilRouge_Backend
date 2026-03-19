import os
from pypdf import PdfReader
from fastapi import APIRouter, HTTPException
from app.schemas.chatbot import ResponseMsg, RequestMsg
from app.api.qwen import query 

ARTIFACTS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "../upload")
PDF_PATH      = os.path.join(ARTIFACTS_DIR, "ELAN_Base_Connaissances.pdf")

chatbot_router = APIRouter()

# ── État global ───────────────────────────────────────────────────────────────
knowledge_base:       str  = ""
conversation_history: list = []

# ── Chargement PDF ────────────────────────────────────────────────────────────
def load_pdf(path: str) -> str:
    reader = PdfReader(path)
    pages  = [page.extract_text() for page in reader.pages]
    texte  = "\n".join(p for p in pages if p and p.strip())
    print(f"   → {len(reader.pages)} pages lues")
    return texte

def build_system_prompt(knowledge: str) -> str:
    return f"""Tu es l'assistant virtuel d'ÉLAN, la plateforme e-commerce de Maisonnette spécialisée dans les équipements de maison.

Ton rôle est de répondre aux questions des clients de manière claire, amicale et professionnelle.

RÈGLES :
- Réponds UNIQUEMENT en te basant sur la base de connaissances ci-dessous.
- Si la réponse est absente, dis : "Je n'ai pas cette information. Veuillez contacter notre service client."
- Sois concis et direct. Utilise le vouvoiement.

────────────────────────────────────────
BASE DE CONNAISSANCES ÉLAN :
────────────────────────────────────────
{knowledge}
────────────────────────────────────────
"""

def startup_chatbot():
    global knowledge_base, conversation_history
    knowledge_base = load_pdf(PDF_PATH)
    conversation_history = [
        {"role": "system", "content": build_system_prompt(knowledge_base)}
    ]

# ── POST /chat ────────────────────────────────────────────────────────────────
@chatbot_router.post("/chat", response_model=ResponseMsg)
def chat(request: RequestMsg):
    if not request.query.strip():
        raise HTTPException(status_code=400, detail="Le message ne peut pas être vide.")

    conversation_history.append({
        "role": "user",
        "content": request.query
    })

    response = query({
        "model": "Qwen/Qwen2.5-7B-Instruct:together",
        "messages": conversation_history,
        "max_tokens": 512,
        "temperature": 0.3,
    })

    print("RESPONSE BRUTE :", response)
    try:
        reply = response["choices"][0]["message"]["content"]
    except (KeyError, IndexError):
        raise HTTPException(status_code=502, detail="Réponse inattendue du modèle.")

    conversation_history.append({
        "role": "assistant",
        "content": reply
    })

    return ResponseMsg(reply=reply)

# ── DELETE /reset ─────────────────────────────────────────────────────────────
@chatbot_router.delete("/reset")
def reset():
    global conversation_history
    conversation_history = [
        {"role": "system", "content": build_system_prompt(knowledge_base)}
    ]
    return {"message": "Conversation réinitialisée avec succès."}