# Comparateur de contrats avec alertes

## Description

Ce projet permet de comparer deux versions d’un contrat (format PDF) afin de détecter automatiquement les modifications apportées.

Les contrats sont découpés en clauses à l’aide de regex (basées sur la numérotation des articles), puis comparés afin d’identifier les changements et signaler les points potentiellement critiques.

Backend développé en **Python avec FastAPI**, frontend simple en **HTML/CSS/JS**.

---

## Installation

Cloner le dépôt :

```bash
git clone https://github.com/CLorieau/projet_dev_ia.git
cd projet_dev_ia
```

Créer un environnement virtuel (optionnel mais recommandé) :

```bash
python -m venv venv
source venv/bin/activate  # Windows : venv\Scripts\activate
```

Installer les dépendances :

```bash
pip install -r requirements.txt
```

---

## Utilisation

Lancer le serveur :

```bash
uvicorn main:app --reload
```

Accéder à l’application via en ouvrant le fichier **index.html** dans votre navigateur.


Uploader les deux versions du contrat (PDF uniquement) pour obtenir l’analyse des modifications.