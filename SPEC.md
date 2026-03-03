# SPEC.md

## Le vrai problème

Un contrat a été modifié suite à un changement de position, une nouvelle directive ou l’apparition d’un nouveau texte de loi. L’émetteur affirme avoir effectué “quelques ajustements”, mais en réalité, l’utilisateur doit comparer manuellement deux versions parfois longues de plusieurs dizaines de pages.

Une simple différence de mot peut modifier totalement le sens d’une clause. L’objectif est donc de détecter automatiquement les changements entre deux versions d’un contrat, d’en analyser le sens, et d’alerter l’utilisateur sur les points potentiellement critiques.

---

## Ce que je construis

Un système intelligent permettant :

- L’upload de deux versions d’un contrat (PDF uniquement)
- La détection des modifications entre les deux versions
- Une analyse sémantique des changements
- Une évaluation du niveau de criticité des modifications
- Une alerte sur les clauses sensibles

Le système ne fait **pas d’analyse juridique**, mais met en évidence les éléments nécessitant une attention particulière.

---

## Techniques IA utilisées

### Extraction structurée

Découpe des contrats en clauses à l’aide de **regex**, en se basant sur les numérotations et titres d’articles afin de structurer le texte avant comparaison.

### Comparaison sémantique

Analyse du sens des modifications et pas uniquement un diff textuel classique.  
L’objectif est d’identifier les changements de signification, même si la structure de la phrase est modifiée.

### Évaluation de criticité

Classification simple du niveau d’impact d’une modification (faible, moyen, élevé), avec les limites liées à la subjectivité de cette évaluation.

---

## Architecture
```
┌──────────────────┐
│ Upload V1 & V2   │
│ (PDF uniquement) │
└─────────┬────────┘
          │
          ▼
┌──────────────────┐
│ Extraction texte │
│ depuis PDF       │
└─────────┬────────┘
          │
          ▼
┌────────────────────────────┐
│ Structuration en clauses   │
│ via Regex (numérotation)   │
└─────────┬──────────────────┘
          │
          ▼
┌────────────────────────────┐
│ Comparaison sémantique     │
│ des clauses                │
└─────────┬──────────────────┘
          │
          ▼
┌────────────────────────────┐
│ Détection des changements  │
│ + Niveau de criticité      │
└─────────┬──────────────────┘
          │
          ▼
┌────────────────────────────┐
│ Interface affichage        │
│ des différences détectées  │
└────────────────────────────┘
```
---

## Stack technique

### Backend

- Python
- FastAPI (API simple pour l’upload et le traitement des contrats)

### Frontend

- HTML
- CSS
- JavaScript
- Interface volontairement simple (2 boutons d’upload + affichage des résultats)

---

## MVP (Minimum Viable Product)

- Upload de deux fichiers PDF
- Extraction du texte
- Découpage en clauses via regex
- Comparaison des clauses
- Mise en évidence des modifications
- Indication d’un niveau de criticité
- Affichage clair des différences

---

## Limites du projet

- Pas d’analyse juridique
- Pas de gestion multi-utilisateurs
- Pas de gestion d’autres formats que PDF

---

## Difficultés anticipées

- Alignement des clauses si la numérotation change
- Subjectivité dans l’évaluation du niveau de criticité

---

## Repository GitHub

https://github.com/CLorieau/projet_dev_ia

