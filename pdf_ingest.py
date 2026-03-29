import os
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS

PDF_FOLDER = "data/pdfs/"
VECTOR_DB_PATH = "embeddings/vector_store"

documents = []

for file in os.listdir(PDF_FOLDER):
    if file.endswith(".pdf"):
        loader = PyPDFLoader(os.path.join(PDF_FOLDER, file))
        documents.extend(loader.load())

splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=200
)

docs = splitter.split_documents(documents)

embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

db = FAISS.from_documents(docs, embeddings)
db.save_local(VECTOR_DB_PATH)

print("✅ PDF ingestion completed successfully")

