import json
import asyncio
from fastapi import APIRouter, File, UploadFile, HTTPException
from utils.pdf_parser import extract_text_from_pdf, segment_into_clauses
from utils.comparator import match_clauses
from utils.ai_analyzer import analyze_clause_diff

router = APIRouter()

@router.post("/upload")
async def upload_contracts(
    file1: UploadFile = File(...),
    file2: UploadFile = File(...)
):
    # Validation du type MIME
    if file1.content_type != "application/pdf" or file2.content_type != "application/pdf":
        raise HTTPException(
            status_code=400, 
            detail="Les deux fichiers doivent être au format PDF (application/pdf)."
        )
    
    bytes1 = await file1.read()
    bytes2 = await file2.read()
    
    # Process file1
    text1 = extract_text_from_pdf(bytes1)
    clauses1 = segment_into_clauses(text1)
    with open("v1.json", "w", encoding="utf-8") as f:
        json.dump(clauses1, f, ensure_ascii=False, indent=4)
    
    # Process file2
    text2 = extract_text_from_pdf(bytes2)
    clauses2 = segment_into_clauses(text2)
    with open("v2.json", "w", encoding="utf-8") as f:
        json.dump(clauses2, f, ensure_ascii=False, indent=4)
        
    # Appairage des clauses (matching hybride)
    raw_mapping = match_clauses(clauses1, clauses2)
    
    # Analyse IA sur les clauses modifiées
    async def analyze_match(m):
        if m["status"].startswith("matched"):
            content1 = m["v1_clause"].get("content", "").strip()
            content2 = m["v2_clause"].get("content", "").strip()
            
            if content1 == content2:
                m["ai_analysis"] = {
                    "has_semantic_change": False,
                    "criticality": "aucun",
                    "explanation": "Le contenu est rigoureusement identique."
                }
            elif content1 and content2:
                m["ai_analysis"] = await analyze_clause_diff(content1, content2)
        return m
        
    mapping = await asyncio.gather(*(analyze_match(m) for m in raw_mapping))
    
    return {
        "message": "Fichiers traités et segmentés avec succès. Résultats sauvegardés dans v1.json et v2.json.",
        "file1_clauses": clauses1,
        "file2_clauses": clauses2,
        "mapping": mapping
    }
