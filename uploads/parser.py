import fitz
from docx import Document
import pytesseract
from PIL import Image
import os

# PDF
def extract_pdf(path):
    doc = fitz.open(path)
    text = ""
    for page in doc:
        text += page.get_text()
    return text

# DOCX
def extract_docx(path):
    doc = Document(path)
    return "\n".join([p.text for p in doc.paragraphs])

# TXT
def extract_txt(path):
    with open(path, "r", encoding="utf-8") as f:
        return f.read()

# IMAGE (OCR)
def extract_image(path):
    img = Image.open(path)
    return pytesseract.image_to_string(img)

# MAIN PARSER
def parse_resume(file_path):
    ext = file_path.split(".")[-1].lower()

    if ext == "pdf":
        return extract_pdf(file_path)
    elif ext == "docx":
        return extract_docx(file_path)
    elif ext == "txt":
        return extract_txt(file_path)
    elif ext in ["png", "jpg", "jpeg"]:
        return extract_image(file_path)
    else:
        return ""