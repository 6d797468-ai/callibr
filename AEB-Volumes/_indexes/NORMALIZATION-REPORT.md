# Rapport De Normalisation Éditoriale

Mise à jour : 2026-07-27

## Synthèse

- Source : `Architecture & Engineering Book (AEB).md`.
- Lignes du monolithe : 55916.
- Volumes détectés : 124.
- ADR détectés : 287.
- Endpoints API détectés : 205.
- Événements détectés : 112.
- Engines/services détectés : 1022.
- Modèles de données détectés : 213.
- Entrées scénario détectées : 169.

## Comptage Par Phase

| Phase | Volumes |
| --- | --- |
| A | 1 |
| B | 11 |
| C | 5 |
| D | 3 |
| E | 6 |
| F | 6 |
| G | 22 |
| H | 15 |
| I | 20 |
| J | 15 |
| K | 10 |
| L | 10 |

## Incohérences À Corriger

- Identifiants de volumes dupliqués : `B04`, `G06`.
- La Phase A reste un bloc composite `A00-A02`; une normalisation stricte devrait produire `A00`, `A01`, `A02` séparés.
- La nomenclature doit rester : `Callibr` pour le produit, `ATOS` pour le noyau interne, `ACS Platform` pour l’appellation historique.
- Les exemples YAML/JSON doivent être convertis en blocs Markdown typés.
- Les titres du monolithe doivent être convertis progressivement en vrais niveaux Markdown.
- Les ADR doivent être extraits en fichiers dédiés après validation de leur périmètre.

## Artefacts Générés

- [Index ADR](ADR-INDEX.md)
- [Registre ADR extrait](../_adr/ADR-REGISTRY.md)
- [Index API](API-INDEX.md)
- [Index Événements](EVENT-INDEX.md)
- [Index Engines & Services](ENGINE-INDEX.md)
- [Index Data Models](DATA-MODEL-INDEX.md)
- [Index Catalogue Scénarios](SCENARIO-CATALOG-INDEX.md)
- [Matrice De Traçabilité](TRACEABILITY-MATRIX.md)
- [Plan de renumérotation contrôlée](../_normalization/VOLUME-RENUMBERING-PLAN.md)
- [Manifests publication/RAG](../_manifests/README.md)
- [Blueprint site documentaire](../_publication/DOCUMENTATION-SITE-BLUEPRINT.md)
- [Blueprint ingestion RAG](../_publication/RAG-INGESTION-BLUEPRINT.md)

## Prochaine Action Recommandée

Créer une passe de publication documentaire : extraction des index spécialisés vers un site statique ou une base RAG, puis validation humaine du plan de renumérotation avant toute modification du monolithe canonique.
