import streamlit as st
import os
import json
from shutil import rmtree

from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

from qa_engine import answer_question, add_documents_to_db
from image_to_text_context import image_to_text_context
from export_utils import export_pdf, export_docx
from speech_utils import recognize_speech, speak

# =========================================================
# SESSION STATE (STRICT INIT)
# =========================================================
st.session_state.setdefault("chat_messages", [])
st.session_state.setdefault("current_question", "")
st.session_state.setdefault("image_contexts", [])
st.session_state.setdefault("last_language", "en")

# =========================================================
# PAGE CONFIG
# =========================================================
st.set_page_config(page_title="Study AI", layout="wide")

# =========================================================
# STYLES (CHATGPT-LIKE)
# =========================================================
st.markdown("""
<style>
.chat-container { max-width: 900px; margin: auto; }

.q {
    background: rgba(59,130,246,0.2);
    padding: 14px;
    border-radius: 10px;
    margin-bottom: 6px;
    font-weight: 600;
}

.a {
    background: rgba(255,255,255,0.07);
    padding: 16px;
    border-radius: 10px;
    margin-bottom: 6px;
    line-height: 1.7;
}

.meta {
    font-size: 13px;
    opacity: 0.75;
    margin-bottom: 18px;
}
</style>
""", unsafe_allow_html=True)

# =========================================================
# SIDEBAR
# =========================================================
st.sidebar.title("📘 Study AI")

if st.sidebar.button("🆕 New Chat"):
    st.session_state.chat_messages = []
    st.session_state.image_contexts = []
    st.session_state.current_question = ""
    st.sidebar.success("New chat started")

if st.sidebar.button("🧹 Clear PDFs"):
    rmtree("temp_pdfs", ignore_errors=True)
    st.sidebar.success("PDFs cleared")

# =========================================================
# INFO
# =========================================================
st.info(
    "ℹ️ Ask naturally. Follow-ups like **derive it**, **why?**, **explain more** work.\n\n"
    "📚 Subject is detected automatically.\n"
    "🎤 Telugu + English speech supported."
)

# =========================================================
# MODE
# =========================================================
mode = st.radio(
    "🧠 Mode",
    ["🎓 Exam Mode", "📘 Study Mode", "🌐 Hybrid Mode"]
)

use_web = mode.startswith("🌐")

marks_mode = st.selectbox(
    "Answer depth",
    ["2 Marks", "5 Marks", "8 Marks", "10 Marks"],
    index=2
)

# =========================================================
# PDF UPLOAD
# =========================================================
uploaded_pdfs = st.file_uploader(
    "📄 Upload PDFs",
    type=["pdf"],
    accept_multiple_files=True
)

if uploaded_pdfs:
    splitter = RecursiveCharacterTextSplitter(1000, 200)
    docs = []
    os.makedirs("temp_pdfs", exist_ok=True)

    for pdf in uploaded_pdfs:
        path = f"temp_pdfs/{pdf.name}"
        with open(path, "wb") as f:
            f.write(pdf.getbuffer())

        pages = PyPDFLoader(path).load()
        for p in pages:
            p.metadata["chat_source"] = True
            p.metadata["subject"] = "auto"

        docs.extend(splitter.split_documents(pages))

    add_documents_to_db(docs)
    st.success("✅ PDFs indexed")

# =========================================================
# IMAGE UPLOAD (MULTI)
# =========================================================
uploaded_images = st.file_uploader(
    "🖼️ Upload diagrams (optional)",
    type=["png", "jpg", "jpeg"],
    accept_multiple_files=True
)

if uploaded_images:
    os.makedirs("temp_images", exist_ok=True)
    for img in uploaded_images:
        path = f"temp_images/{img.name}"
        with open(path, "wb") as f:
            f.write(img.getbuffer())

        st.session_state.image_contexts.append(
            image_to_text_context(path)
        )

# =========================================================
# SPEECH INPUT
# =========================================================
if st.button("🎤 Speak Question"):
    with st.spinner("Listening..."):
        text, lang = recognize_speech()

    if text:
        st.session_state.current_question = text
        st.session_state.last_language = lang
        st.success(f"Recognized ({'Telugu' if lang=='te' else 'English'})")
    else:
        st.error("Could not recognize speech")

# =========================================================
# QUESTION INPUT
# =========================================================
question = st.text_area(
    "💬 Ask your question",
    value=st.session_state.current_question,
    height=120,
    placeholder="Ask naturally — subject will be detected automatically"
)

speak_answer = st.checkbox("🔊 Read answer aloud", value=False)

# =========================================================
# ANSWER GENERATION
# =========================================================
if st.button("Get Answer"):
    if question.strip():
        with st.spinner("Thinking..."):
            answer_text = answer_question(
                question=question,
                image_context="\n".join(st.session_state.image_contexts),
                marks_mode=marks_mode,
                use_web=use_web,
                subject="auto",
                chat_history=st.session_state.chat_messages
            )

        st.session_state.chat_messages.append({
            "question": question,
            "answer": answer_text,
        })

        if speak_answer:
            speak(answer_text, st.session_state.last_language)

        st.session_state.current_question = ""

# =========================================================
# DISPLAY CHAT (BUBBLES)
# =========================================================
st.markdown("<div class='chat-container'>", unsafe_allow_html=True)

for msg in st.session_state.chat_messages:
    st.markdown(f"<div class='q'>❓ {msg['question']}</div>", unsafe_allow_html=True)
    st.markdown(f"<div class='a'>🧠 {msg['answer']}</div>", unsafe_allow_html=True)

st.markdown("</div>", unsafe_allow_html=True)
