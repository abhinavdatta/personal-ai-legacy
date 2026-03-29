import ollama
import subprocess
import time
import socket
import shutil
import sys

from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from web_search import web_search

# =========================================================
# CONFIG
# =========================================================
VECTOR_DB_PATH = "embeddings/vector_store"
OLLAMA_MODEL = "mistral"

embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

# =========================================================
# OLLAMA HELPERS (NO AUTO-RUN AT IMPORT)
# =========================================================
def is_ollama_running(host="127.0.0.1", port=11434):
    try:
        with socket.create_connection((host, port), timeout=1):
            return True
    except OSError:
        return False


def start_ollama():
    ollama_path = shutil.which("ollama")
    if not ollama_path:
        return False

    subprocess.Popen(
        [ollama_path, "serve"],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        creationflags=subprocess.CREATE_NO_WINDOW if sys.platform == "win32" else 0
    )
    return True


def ensure_ollama():
    if not is_ollama_running():
        if start_ollama():
            for _ in range(10):
                if is_ollama_running():
                    break
                time.sleep(1)

# =========================================================
# VECTOR DATABASE
# =========================================================
def load_or_create_db():
    try:
        return FAISS.load_local(
            VECTOR_DB_PATH,
            embeddings,
            allow_dangerous_deserialization=True
        )
    except Exception:
        return FAISS.from_texts(
            ["init"],
            embeddings,
            metadatas=[{"init": True}]
        )


db = load_or_create_db()


def add_documents_to_db(docs):
    valid_docs = [d for d in docs if d.page_content.strip()]
    if not valid_docs:
        return

    db.add_documents(valid_docs)
    db.save_local(VECTOR_DB_PATH)

# =========================================================
# MAIN QA FUNCTION (SAFE)
# =========================================================
def answer_question(
    question,
    image_context="",
    marks_mode="",
    use_web=False,
    subject="auto",
    chat_history=None
):
    """
    Returns:
    {
        answer: str,
        subject: str,
        confidence: float
    }
    """

    ensure_ollama()  # ✅ SAFE runtime call

    # ---------------- Conversation Context ----------------
    conversation_context = ""
    if chat_history:
        for chat in chat_history[-2:]:
            conversation_context += f"""
Previous Q: {chat['question']}
Previous A: {chat['answer']}
"""

    # ---------------- PDF Retrieval ----------------
    retrieved = db.similarity_search(question, k=8)

    textbook_context = "\n".join(d.page_content for d in retrieved[:5])

    # ---------------- Web Fallback ----------------
    web_context = ""
    if use_web and not textbook_context.strip():
        for r in web_search(question):
            web_context += f"{r['snippet']}\n"

    # ---------------- Prompt ----------------
    prompt = f"""
You are an Electronics & Communication Engineering exam assistant.

PREVIOUS CONTEXT:
{conversation_context}

TEXTBOOK CONTEXT:
{textbook_context}

IMAGE CONTEXT:
{image_context}

WEB CONTEXT:
{web_context}

QUESTION:
{question}

ANSWER STYLE:
{marks_mode}

ANSWER:
"""

    response = ollama.chat(
        model=OLLAMA_MODEL,
        messages=[{"role": "user", "content": prompt}]
    )

    answer = response["message"]["content"]

    return {
        "answer": answer,
        "subject": subject if subject != "auto" else "Detected Automatically",
        "confidence": 0.82  # placeholder (Phase 3+ logic)
    }
