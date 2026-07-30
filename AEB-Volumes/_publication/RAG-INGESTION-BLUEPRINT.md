# Blueprint D'Ingestion RAG AEB

Mise à jour : 2026-07-27

## Objectif

Préparer l'Architecture & Engineering Book pour une recherche sémantique fiable et explicable.

## Source Principale

Utiliser : `../_manifests/rag-manifest.json`.

## Politique De Chunking

Volumes :

- chunking par titres et sections ;
- taille cible : 1200 à 1800 tokens ;
- conserver les tableaux intacts ;
- conserver les blocs de code/YAML/JSON intacts ;
- ajouter metadata phase, volume_id, title, path.

ADR :

- un ADR = un document ;
- garder décision et extrait source ensemble ;
- marquer `requires_human_validation=true`.

Index :

- ingérer comme documents de navigation ;
- priorité inférieure aux volumes et ADR.

## Metadata Minimales

- source: AEB
- document_type
- phase
- volume_id ou adr_id
- title
- path
- generated_on
- requires_human_validation

## Stratégie Retrieval

1. Recherche lexicale pour identifiants exacts : ADR, API, volume, event.
2. Recherche vectorielle pour questions conceptuelles.
3. Reranking par phase et type de document.
4. Réponse avec citations vers fichiers Markdown.

## Guardrails Réponse

- Ne jamais inventer un ADR absent.
- Citer les volumes utilisés.
- Signaler quand un ADR extrait nécessite validation humaine.
- Distinguer `Callibr` produit, `ATOS` noyau interne, `ACS Platform` appellation historique.

## Jeux De Test RAG

Questions de validation :

- Quels volumes définissent le LLM Gateway ?
- Où sont les décisions ADR sur le RBAC/ABAC ?
- Quels endpoints API sont mentionnés pour le billing ?
- Quels modèles de données concernent les subscriptions ?
- Quels Domain Packs couvrent le secteur bancaire ?
- Quelle est la stratégie de reprise après sinistre ?
