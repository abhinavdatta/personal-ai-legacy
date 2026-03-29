import os
from datetime import datetime
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet
from docx import Document

def get_downloads_folder():
    """
    Returns the user's Downloads folder path.
    Works for both browser and EXE mode.
    """
    home = os.path.expanduser("~")
    downloads = os.path.join(home, "Downloads")
    os.makedirs(downloads, exist_ok=True)
    return downloads

def _generate_filename(ext: str):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    return f"StudyAI_Answer_{timestamp}.{ext}"

def export_pdf(text: str):
    downloads = get_downloads_folder()
    path = os.path.join(downloads, _generate_filename("pdf"))

    doc = SimpleDocTemplate(path, pagesize=A4)
    styles = getSampleStyleSheet()
    story = []

    for line in text.split("\n"):
        story.append(Paragraph(line.replace("&", "&amp;"), styles["Normal"]))

    doc.build(story)
    return path

def export_docx(text: str):
    downloads = get_downloads_folder()
    path = os.path.join(downloads, _generate_filename("docx"))

    doc = Document()
    for line in text.split("\n"):
        doc.add_paragraph(line)

    doc.save(path)
    return path
