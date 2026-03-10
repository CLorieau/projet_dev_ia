import fitz  # PyMuPDF
import re

def extract_text_from_pdf(file_bytes: bytes) -> str:
    """Extraire le texte brut d'un fichier PDF."""
    doc = fitz.open(stream=file_bytes, filetype="pdf")
    text = ""
    for page in doc:
         text += page.get_text() + "\n"
    return text

def segment_into_clauses(text: str) -> list[dict]:
    """
    Découper le texte en clauses basées sur une regex métier.
    Gère les "Article X", "1.1", "I.", ou les titres TOUT EN MAJUSCULES.
    """
    # Regex designed to match clause headers at the start of a line.
    # Ex: "Article 1", "1.1", "I.", or "TITRE DE LA CLAUSE"
    pattern = r"(?m)^(Article\s+\d+|[IVX]+\.|\d+\.\d+|[A-Z][A-Z\sÀ-Ÿ]{3,})"
    
    parts = re.split(pattern, text)
    clauses = []
    
    # La première partie (avant le premier match) est souvent un préambule
    if parts[0].strip():
        clauses.append({"title": "Préambule", "content": parts[0].strip()})
        
    for i in range(1, len(parts), 2):
        title = parts[i].strip()
        content = parts[i+1].strip() if i+1 < len(parts) else ""
        clauses.append({"title": title, "content": content})
        
    return clauses
