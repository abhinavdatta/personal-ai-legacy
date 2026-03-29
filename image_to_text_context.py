import cv2
import pytesseract
import os

# Set Tesseract path only on Windows
if os.name == "nt":
    pytesseract.pytesseract.tesseract_cmd = (
        r"C:\Program Files\Tesseract-OCR\tesseract.exe"
    )

def image_to_text_context(image_path: str) -> str:
    """
    Converts an engineering image (diagram/graph)
    into text context using OCR.
    This is NOT vision understanding.
    """

    img = cv2.imread(image_path)
    if img is None:
        return "Image could not be read."

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    extracted_text = pytesseract.image_to_string(gray)

    # 🔧 PERFORMANCE OPTIMIZATION:
    # Limit OCR text length to avoid huge prompts
    extracted_text = extracted_text[:2000]

    if extracted_text.strip() == "":
        return (
            "An engineering diagram or graph is shown. "
            "No readable text was detected. "
            "Assume standard circuit or graph conventions."
        )

    return f"""
TEXT EXTRACTED FROM IMAGE (OCR):

{extracted_text}

NOTE:
This text comes from an engineering diagram,
circuit, graph, or waveform.
Interpret accordingly.
"""


