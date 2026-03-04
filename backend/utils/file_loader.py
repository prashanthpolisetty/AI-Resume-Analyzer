import os
import fitz  # PyMuPDF
import docx  # python-docx

def extract_text_from_pdf(file_path):
    """Extract text from a PDF file using PyMuPDF."""
    try:
        text = ""
        with fitz.open(file_path) as doc:
            for page in doc:
                text += page.get_text()
        return text.strip()
    except Exception as e:
        raise ValueError(f"Failed to extract PDF text: {e}")

def extract_text_from_docx(file_path):
    """Extract text from a DOCX file using python-docx."""
    try:
        doc = docx.Document(file_path)
        text = "\n".join([para.text for para in doc.paragraphs])
        return text.strip()
    except Exception as e:
        raise ValueError(f"Failed to extract DOCX text: {e}")

def extract_text_from_txt(file_path):
    """Extract text from a plain TXT file."""
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return f.read().strip()
    except Exception as e:
        raise ValueError(f"Failed to extract TXT text: {e}")

def extract_resume_text(file_path):
    """
    Dispatches to the appropriate extractor based on file extension.
    Supported: .pdf, .docx, .txt
    """
    ext = os.path.splitext(file_path)[1].lower()
    
    if ext == ".pdf":
        return extract_text_from_pdf(file_path)
    elif ext == ".docx":
        return extract_text_from_docx(file_path)
    elif ext == ".txt":
        return extract_text_from_txt(file_path)
    else:
        raise ValueError("Unsupported file type. Only PDF, DOCX, and TXT are supported.")
