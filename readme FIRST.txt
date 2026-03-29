# Study AI – Local Desktop Application

Study AI is a fully local, exam-oriented AI assistant designed for
engineering students. It answers questions using uploaded textbooks,
class notes, and diagrams, with optional internet support.

The application runs entirely on the user's computer using Ollama,
ensuring privacy and offline capability.

---

## Features

- PDF-based question answering (RAG)
- Diagram, circuit & graph understanding (OCR)
- Marks-based answers (2 / 5 / 8 / 10 marks)
- Exam Mode (strict PDF-only answers)
- Optional internet fallback (Hybrid Mode)
- Source citations with page numbers
- Fully local LLM (no cloud API required)
- Windows desktop application

---

## Modes of Operation

### 🎓 Exam Mode
- Uses only uploaded PDFs
- Internet disabled
- Long, derivation-style answers
- Safe for university exams

### 📘 Study Mode
- PDFs + images
- Flexible answer length
- Concept-focused explanations

### 🌐 Hybrid Mode
- PDFs first
- Internet used only if PDFs are insufficient
- Web sources clearly labeled

---

## System Requirements

- Windows 10 / 11
- Ollama for Windows
- At least one Ollama model (e.g. mistral, deepseek)
- Tesseract OCR (for image uploads)
- Minimum 8 GB RAM recommended

---

## Installation

1. Run `StudyAI_Setup.exe`
2. Install Ollama from https://ollama.com
3. Pull a model:
ollama pull mistral
4. Launch Study AI from Desktop or Start Menu

---

## Usage

1. Upload PDFs (textbooks, notes)
2. (Optional) Upload diagrams or graphs
3. Select usage mode
4. Ask academic questions
5. Review answers with sources

---

## Notes

- Images are converted to text using OCR
- The AI does not directly "see" images
- Internet usage is optional and transparent
- No user data is sent to external servers

---

## WARNING:
- THIS BUILD IS UNFINISHED AND I DONT HAVE ANY INTENTIONS TO FIX THIS OR CONTINUE THIS PROJECT
-download venv from here :-https://drive.google.com/file/d/1xN93chPIEF6tAy8NHhevylbA38WNo43j/view?usp=sharing
-create these files in the root folder
	-------   / (Root)
			   |-data---|
			   |        |-images(upload images for training ai)
			   |		|-pdfs(upload pdfs for training ai)
			   |				
			   |-temp_images
			   |-temp_pdfs
