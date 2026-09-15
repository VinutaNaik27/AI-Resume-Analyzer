import fitz
from docx import Document

def extract_resume_text(path):
    if path.lower().endswith(".pdf"):
        doc = fitz.open(path)
        text = "\n".join(page.get_text() for page in doc)
        doc.close()
        return text

    if path.lower().endswith(".docx"):
        doc = Document(path)
        return "\n".join(p.text for p in doc.paragraphs if p.text.strip())

    raise ValueError("Only PDF and DOCX files are supported.")
