# Session 1 — Initialisation et cadrage

## Ce que je voulais faire :
L'objectif était de poser les premières pierres du backend en m'appuyant sur mon document spec.md. Je voulais une structure minimale mais solide, sans fichiers superflus, pour garder un contrôle total sur l'arborescence.

## Comment j'ai travaillé avec l'IA :
J'ai soumis un prompt restrictif : "Je veux que tu initialises le backend en prenant en compte le spec.md en ne créant aucun fichier supplémentaire". L'IA a bien respecté la contrainte, me proposant une structure main.py épurée.

## Ce que j'en retiens :
Il est tentant de laisser l'IA générer des dossiers utils/ ou models/ dès le début, mais j'ai préféré imposer une contrainte de simplicité. Cela m'a forcé à bien comprendre chaque ligne de configuration initiale avant de complexifier le système.


# Session 2 — Refonte UX et fondations de l'API

## Ce que je voulais faire :
Cette séance était double : améliorer l'expérience utilisateur (le front était trop brut) et permettre l'upload réel de fichiers via FastAPI.

## Comment j'ai travaillé avec l'IA :

**Côté Frontend :** J'ai demandé un design "user-friendly" avec des boutons d'upload massifs et colorés pour guider l'œil de l'utilisateur. J'ai aussi insisté sur une fonction de "preview" pour afficher le nom complet des fichiers, afin d'éviter les erreurs d'inversion entre la V1 et la V2.

**Côté Backend :** J'ai utilisé un prompt typé "expert" pour implémenter l'endpoint /upload. L'IA a suggéré l'utilisation de UploadFile de FastAPI, ce qui est plus efficace pour la mémoire que de lire tout le fichier d'un coup.

## Ce qui a bloqué ou changé :
J'ai rencontré mes premiers problèmes de CORS (Cross-Origin Resource Sharing). Mon frontend refusait de parler au backend. J'ai dû demander à l'IA de configurer le middleware CORS de manière explicite. C'est une étape classique, mais frustrante quand on ne l'a jamais fait.

## Ce que j'en retiens :
L'ergonomie change tout. Avoir un visuel clair sur quel fichier est chargé (V1 vs V2) réduit drastiquement la charge mentale de l'utilisateur.


# Session 3 — Extraction, parsing et logique d'alignement

## Ce que je voulais faire :
L'enjeu de cette séance était de passer du document PDF brut à une structure de données organisée et comparable, tout en garantissant la qualité de l'information extraite pour l'IA.

## Comment j'ai travaillé avec l'IA :

**Extraction :** J'ai opté pour PyMuPDF (fitz). L'IA m'a aidé à concevoir une regex capable de repérer les structures types ("Article X", "1.1", etc.).

**Stockage :** Pour isoler les problèmes, j'ai demandé à l'IA d'exporter les résultats dans v1.json et v2.json. Cela me permet de valider le parsing avant d'attaquer la comparaison.

**Alignement :** J'ai guidé l'IA vers un algorithme hybride (titres + SequenceMatcher) pour ne pas perdre le fil si un article est déplacé. Précision : j'ai fait le choix d'utiliser l'API Gemini pour sa capacité à gérer de gros volumes de texte (utile dans le cadre des contrats).

## Ce qui a bloqué ou changé (Le pivot technique) :
Initialement, j'avais envisagé d'utiliser une méthode de chunking basique avec un overlap de 20 % pour structurer mes données dans le JSON. C'était une solution de facilité technique, mais j'ai rapidement réalisé (après des tests) ses limites : un découpage arbitraire par blocs de caractères risquait de tronçonner une clause en plein milieu. Parfois, je perdais le contexte de certaines clauses ce qui faussait l'analyse sémantique de l'IA qui recevait des fragments de phrases incohérentes. J'ai donc décidé de renoncer à l'overlap pour privilégier une segmentation sémantique stricte via Regex, garantissant que chaque unité de texte envoyée à l'IA soit une clause complète et logique.

## Ce que j'en retiens :
En IA, le "pre-processing" est souvent plus déterminant que le modèle lui-même. Choisir la segmentation par article plutôt que par chunk arbitraire complexifie mon code Regex, mais assure la fiabilité de l'analyse finale. J'ai appris qu'il vaut mieux passer du temps sur la structure des données que de compenser une mauvaise donnée par un prompt plus complexe.

# Les prompts exacts utilisés : 

## Séance 1 : 

- "Je veux que tu initialise le backend en prenant en compte le spec.md en ne créant aucun fichier supplémentaire"

## Séance 2 : 

- "A partir de l'interface que j'ai réalisée, fais moi un design beaucoup plus user-friendly dans lequel les boutons pour upload les pdf des contrats seront beaucoup plus gros et d'une couleur qui ressort mieux puis fais une sorte de preview pour les deux contrats upload afin que l'utilisateur puisse vérifier que le document qu'il a upload est le bon. On affichera les noms des fichiers en entier."

- "Agis en tant que développeur Python expert pour initialiser le backend de mon projet de comparateur de contrats en utilisant FastAPI. Tu dois créer une structure de projet simple et implémenter un endpoint POST /upload capable d'accepter deux fichiers au format PDF exclusivement. Intègre une validation pour vérifier le type MIME des fichiers (uniquement application/pdf) et configure le middleware CORS pour autoriser les requêtes provenant de mon frontend HTML/JS. Pour cette première phase, l'endpoint doit simplement confirmer la bonne réception en retournant un message de succès incluant le nom des deux fichiers reçus."

## Séance 3 :

- "Maintenant que la communication est établie, nous devons transformer ces fichiers PDF en données structurées. Utilise une bibliothèque performante comme PyMuPDF pour extraire le texte brut des documents. La partie cruciale consiste à implémenter une logique de segmentation : crée une fonction qui utilise des expressions régulières (regex) pour découper le texte en clauses distinctes. La regex doit être capable de repérer les structures classiques de contrats, comme les mentions "Article", les numérotations de type "1.1" ou "I.", et les titres en majuscules. Modifie ensuite l'endpoint de base pour qu'il traite les deux fichiers et retourne une liste organisée de ces clauses pour chaque version, afin de valider que le découpage est cohérent avant l'analyse."

- "Pour l'instant je veux que les résultats soient dans des fichiers json (v1.json et v2.json) stocké dans mon répertoire backend. Dès que j'upload d'autres fichiers, les anciens résultats sont écrasés et remplacés par les résultats des nouveaux fichiers upload."

- "Maintenant il faut faire correspondre intelligemment les clauses de la version 1 avec celles de la version 2, car la numérotation peut parfois changer d'une version à l'autre. Je ne veux pas d'une simple comparaison par index ; implémente un algorithme d'alignement hybride. Il doit d'abord tenter de coupler les clauses par leur titre ou numéro, puis utiliser un calcul de similarité textuelle (comme le SequenceMatcher de Python) pour identifier les clauses qui auraient été déplacées ou légèrement reformulées. L'idée est d'aboutir à une structure de données appairant chaque clause originale à sa nouvelle version, ou de signaler si une clause a été purement supprimée ou ajoutée."