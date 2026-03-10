import os
import json
from google import genai
from google.genai import types
from dotenv import load_dotenv

# Charger les variables d'environnement depuis .env
load_dotenv()

# Initialiser le client (utilise automatiquement GEMINI_API_KEY de l'environnement)
client = genai.Client()

async def analyze_clause_diff(text_v1: str, text_v2: str) -> dict:
    """
    Analyse les différences sémantiques entre deux versions d'une clause à l'aide de l'API Gemini.
    Ne réalise pas d'analyse juridique.
    Retourne un dictionnaire avec : has_semantic_change, criticality, explanation.
    """
    system_instruction = (
        "Tu es un assistant spécialisé dans l'analyse de textes. Ton rôle est de comparer deux versions d'une clause "
        "d'un contrat pour détecter si le SENS a été modifié (au-delà des simples changements de ponctuation ou de formatage).\n"
        "RÈGLE STRICTE : TU NE DOIS EN AUCUN CAS RÉALISER D'ANALYSE JURIDIQUE NI DONNER D'AVIS JURIDIQUE.\n\n"
        "Dès que tu détectes une modification autre que cosmétique, tu dois indiquer qu'il y a un changement sémantique, et "
        "évaluer le niveau de criticité en respectant très rigoureusement les barèmes suivants :\n"
        "- NOTION DE PROPORTION (CRITIQUE) : Si des montants ou des durées sont modifiés, tu dois absolument prendre en compte l'ordre de grandeur ! Une augmentation de 20€ d'une pénalité est 'faible'. Une augmentation de 5 000€ ou 10 000€ est 'élevé'. Passer de 12 à 13 mois est 'faible'. Passer de 12 à 48 mois est 'élevé'. Raisonne toujours en termes de proportion et d'impact réel.\n"
        "- 'faible' : Reformulation, modification mineure d'un lieu, délai très court, augmentation d'amende négligeable, ou processus administratif.\n"
        "- 'moyen' : Ajout d'une précision supplémentaire sur le périmètre (sans inverser le principe général), modification d'une modalité de paiement mineure, ou ajustement de date moyen.\n"
        "- 'élevé' : Augmentation exponentielle ou majeure d'une durée (ex: doublée), augmentation vertigineuse d'une amende/pénalité, inversion de responsabilité, suppression d'une garantie forte, ajout d'une obligation lourde.\n\n"
        "Fournis aussi une brève explication analytique (maximum 3 phrases) pour alerter factuellement sur le changement ("
        "ex: 'La pénalité passe de 100€ à 10 000€, ce qui représente une augmentation majeure du risque financier.'). Aucun conseil légal."
    )

    user_prompt = (
        f"Version 1 :\n{text_v1}\n\n"
        f"Version 2 :\n{text_v2}\n\n"
        "Compare ces deux versions selon les critères définis. Retourne uniquement le JSON."
    )

    try:
        # Appel asynchrone au modèle Gemini
        response = await client.aio.models.generate_content(
            model='gemini-2.5-flash',
            contents=user_prompt,
            config=types.GenerateContentConfig(
                system_instruction=system_instruction,
                temperature=0.1,
                response_mime_type="application/json",
                response_schema=types.Schema(
                    type=types.Type.OBJECT,
                    properties={
                        "has_semantic_change": types.Schema(type=types.Type.BOOLEAN),
                        "criticality": types.Schema(
                            type=types.Type.STRING,
                            description="Niveau de criticité parmi 'faible', 'moyen', 'élevé', ou 'aucun'"
                        ),
                        "explanation": types.Schema(type=types.Type.STRING)
                    },
                    required=["has_semantic_change", "criticality", "explanation"]
                )
            )
        )

        content = response.text
        if content:
            return json.loads(content)
        else:
            return {
                "has_semantic_change": False,
                "criticality": "aucun",
                "explanation": "La réponse de l'IA est vide."
            }
    except Exception as e:
        return {
            "has_semantic_change": False,
            "criticality": "aucun",
            "explanation": f"Erreur lors de l'appel à l'API IA : {str(e)}"
        }
