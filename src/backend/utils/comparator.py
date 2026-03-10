import difflib

def match_clauses(v1_clauses: list[dict], v2_clauses: list[dict], similarity_threshold: float = 0.6) -> list[dict]:
    """
    Appaire les clauses de v1_clauses et v2_clauses à l'aide d'un algorithme hybride.
    1. Couplage par titre (correspondance exacte).
    2. Couplage par similarité textuelle (via SequenceMatcher) sur le contenu.
    3. Signalement des clauses ajoutées ou supprimées.
    
    Retourne une liste de correspondances.
    """
    results = []
    v2_matched = set()  # Indices des clauses de v2 déjà appariées
    
    # Étape 1 : Correspondance par titre (ou numéro)
    for i, c1 in enumerate(v1_clauses):
        matched = False
        title1 = c1.get('title', '').strip().lower()
        
        for j, c2 in enumerate(v2_clauses):
            if j in v2_matched:
                continue
            
            title2 = c2.get('title', '').strip().lower()
            
            if title1 and title2 and title1 == title2:
                results.append({
                    "v1_index": i,
                    "v2_index": j,
                    "v1_clause": c1,
                    "v2_clause": c2,
                    "status": "matched_by_title"
                })
                v2_matched.add(j)
                matched = True
                break
                
        if not matched:
            results.append({
                "v1_index": i,
                "v2_index": None,
                "v1_clause": c1,
                "v2_clause": None,
                "status": "unmatched"  # À réévaluer à l'étape 2
            })

    # Étape 2 : Correspondance par similarité textuelle
    for result in results:
        if result["status"] == "unmatched":
            c1 = result["v1_clause"]
            content1 = c1.get("content", "")
            
            best_ratio = 0.0
            best_j = -1
            
            for j, c2 in enumerate(v2_clauses):
                if j in v2_matched:
                    continue
                
                content2 = c2.get("content", "")
                
                # S'il n'y a pas de contenu du tout à comparer, on ignore
                if not content1 and not content2:
                    continue
                    
                ratio = difflib.SequenceMatcher(None, content1, content2).ratio()
                if ratio > best_ratio:
                    best_ratio = ratio
                    best_j = j
                    
            if best_ratio >= similarity_threshold:
                result["v2_index"] = best_j
                result["v2_clause"] = v2_clauses[best_j]
                result["status"] = f"matched_by_similarity ({best_ratio:.2f})"
                v2_matched.add(best_j)
            else:
                result["status"] = "deleted"

    # Étape 3 : Identifier les clauses purement ajoutées dans v2
    for j, c2 in enumerate(v2_clauses):
        if j not in v2_matched:
            results.append({
                "v1_index": None,
                "v2_index": j,
                "v1_clause": None,
                "v2_clause": c2,
                "status": "added"
            })
            
    # Optionnel : trier les résultats pour plus de lisibilité
    def sort_key(item):
        if item["v1_index"] is not None:
            return (0, item["v1_index"])
        else:
            return (1, item["v2_index"])
            
    results.sort(key=sort_key)

    return results
