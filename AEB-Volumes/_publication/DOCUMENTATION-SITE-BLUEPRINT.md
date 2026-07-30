# Blueprint De Publication Documentaire AEB

Mise à jour : 2026-07-27

## Objectif

Transformer l'Architecture & Engineering Book en site documentaire navigable, versionné et exploitable par humains et agents IA.

## Sources

- Monolithe canonique : `../Architecture & Engineering Book (AEB).md` depuis la racine projet.
- Volumes modulaires : `../phase-*/*.md`.
- Index spécialisés : `../_indexes/`.
- ADR extraits : `../_adr/`.
- Manifests : `../_manifests/`.

## Structure Recommandée Du Site

Navigation :

1. Accueil
2. Master Index
3. Phases A-L
4. ADR Registry
5. API Index
6. Event Index
7. Engine Index
8. Data Model Index
9. Scenario Catalog
10. Normalization Report
11. Publication / RAG Manifests

## Règles De Publication

- Le Master Index est la page d'accueil technique.
- Chaque volume reste une page indépendante.
- Les ADR extraits sont publiés dans une section séparée avec avertissement `à valider`.
- Les liens relatifs doivent rester stables.
- Les volumes historiques dupliqués gardent leur identifiant actuel tant que le plan de renumérotation n'est pas validé.

## Pipeline Recommandé

1. Valider le monolithe.
2. Régénérer les volumes.
3. Régénérer les index spécialisés.
4. Régénérer les manifests.
5. Construire le site statique.
6. Vérifier les liens.
7. Exporter PDF si nécessaire.
8. Publier une version taguée.

## Options Techniques

### Option 1 — MkDocs Material

Avantages :

- simple ;
- navigation claire ;
- recherche intégrée ;
- support Markdown natif ;
- déploiement statique facile.

### Option 2 — Docusaurus

Avantages :

- excellente expérience produit ;
- versioning puissant ;
- composants React ;
- adapté à un portail développeur.

### Option 3 — RAG-first

Avantages :

- ingestion directe via manifests ;
- recherche sémantique ;
- assistant architecture ;
- Q&A sur ADR, API, engines et data models.

## Recommandation

Court terme : MkDocs Material.

Moyen terme : Docusaurus si le Book devient un portail développeur public.

Long terme : site documentaire + RAG interne + génération PDF versionnée.
