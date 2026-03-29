import os
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings

# =========================================================
# EMBEDDINGS
# =========================================================
embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

BASE_PATH = "embeddings"

SUBJECT_MAP = {
    "em waves": "em_waves",
    "electromagnetic waves": "em_waves",
    "analog electronics": "analog",
    "analog 2": "analog",
    "analog communication": "analog_comm",
    "digital communication": "digital_comm",
}

# =========================================================
# HELPERS
# =========================================================
def normalize_subject(subject: str) -> str:
    s = subject.lower()
    for key, folder in SUBJECT_MAP.items():
        if key in s:
            return folder
    return "general"


def get_db_path(subject: str) -> str:
    folder = normalize_subject(subject)
    return os.path.join(BASE_PATH, folder)


def load_or_create_db(subject: str):
    path = get_db_path(subject)
    os.makedirs(path, exist_ok=True)

    try:
        return FAISS.load_local(
            path,
            embeddings,
            allow_dangerous_deserialization=True
        )
    except Exception:
        return FAISS.from_texts(
            ["initialization document"],
            embeddings,
            metadatas=[{"init": True}]
        )


def add_documents(subject: str, docs):
    if not docs:
        return

    db = load_or_create_db(subject)

    valid = [
        d for d in docs
        if d.page_content and d.page_content.strip()
    ]

    if not valid:
        return

    db.add_documents(valid)
    db.save_local(get_db_path(subject))


def similarity_search(subject: str, query: str, k=8):
    db = load_or_create_db(subject)
    return db.similarity_search_with_score(query, k=k)
