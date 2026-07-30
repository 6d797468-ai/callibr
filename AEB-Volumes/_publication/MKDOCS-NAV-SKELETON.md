# Squelette De Navigation MkDocs

Mise à jour : 2026-07-27

Ce fichier décrit la navigation recommandée. Il n'est pas encore un `mkdocs.yml` opérationnel, afin d'éviter d'imposer un outil avant validation.

```yaml
site_name: Callibr Architecture & Engineering Book
site_description: Architecture de référence Callibr / ATOS
nav:
  - Accueil: AEB-MASTER-INDEX.md
  - Index spécialisés:
      - Normalisation: _indexes/NORMALIZATION-REPORT.md
      - Traçabilité: _indexes/TRACEABILITY-MATRIX.md
      - ADR Index: _indexes/ADR-INDEX.md
      - API Index: _indexes/API-INDEX.md
      - Events: _indexes/EVENT-INDEX.md
      - Engines: _indexes/ENGINE-INDEX.md
      - Data Models: _indexes/DATA-MODEL-INDEX.md
      - Scénarios: _indexes/SCENARIO-CATALOG-INDEX.md
  - ADR Registry: _adr/ADR-REGISTRY.md
  - Manifests: _manifests/README.md
  - Publication:
      - Site Blueprint: _publication/DOCUMENTATION-SITE-BLUEPRINT.md
      - RAG Blueprint: _publication/RAG-INGESTION-BLUEPRINT.md
```

Les phases A-L doivent être injectées automatiquement depuis `volume-manifest.json` pour éviter une navigation manuelle fragile.
```
