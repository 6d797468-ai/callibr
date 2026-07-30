# Volume K02 — CI/CD Pipeline Architecture

> Extrait généré depuis `Architecture & Engineering Book (AEB).md` le 2026-07-27.

PHASE K — DEV PLATFORM, DEVSECOPS & PLATFORM ENGINEERING
Volume K02
CI/CD Pipeline Architecture

Version : 1.0

Statut : Delivery Automation Foundation

Criticité : Critique

1. Vision

Le pipeline CI/CD automatise le passage du code à la production.

Il garantit :

qualité ;
sécurité ;
répétabilité ;
rapidité ;
audit ;
rollback.

2. Principe fondamental

Aucun artefact de production ne doit être créé manuellement.

Le pipeline est la seule voie officielle vers les environnements.

3. Architecture globale

                    Commit


                      │


                      ▼


                   CI Pipeline


        ┌─────────────┼─────────────┐


        ▼             ▼             ▼


 Tests          Security Scan      Build


        │             │             │


        └─────────────┼─────────────┘


                      ▼


                  CD Pipeline


                      │


                      ▼


                Staging / Production

4. CI Stages

Étapes :

checkout ;
dependency install ;
format check ;
lint ;
typing ;
unit tests ;
contract tests ;
integration tests ;
security scans ;
build artifacts.

5. CD Stages

Étapes :

artifact selection ;
environment config ;
database migration check ;
deployment ;
smoke tests ;
health verification ;
traffic shift ;
post-deploy monitoring.

6. Quality Gates

Blocages :

tests rouges ;
couverture insuffisante ;
secret détecté ;
vulnérabilité critique ;
rupture contrat API ;
image non signée ;
policy IaC violée.

7. Pipeline as Code

Les pipelines sont versionnés.

Ils doivent être :

revus ;
testés ;
réutilisables ;
modulaires ;
paramétrables.

8. Artifact Promotion

Règle :

build once, promote many.

Le même artefact passe de dev à staging puis production.

9. Data Model

PipelineRun
-----------

id

commit_sha

branch

status

started_at

finished_at

Artifact
--------

id

type

version

digest

signature

DeploymentRun
-------------

id

artifact_id

environment

status

10. API interne

Lire pipeline :

GET /delivery/pipelines/{id}

Promouvoir artefact :

POST /delivery/artifacts/{id}/promote

Déclencher rollback :

POST /delivery/deployments/{id}/rollback

11. Décisions d'architecture (ADR)

ADR-K02-001
Le pipeline est la voie unique de livraison.

Décision :

Interdire les déploiements manuels non tracés.

ADR-K02-002
Les quality gates bloquent la promotion.

Décision :

Préserver stabilité et sécurité.

ADR-K02-003
Les artefacts sont promus sans rebuild.

Décision :

Garantir reproductibilité.

ADR-K02-004
Les pipelines sont versionnés.

Décision :

Rendre la delivery auditable.

12. Critères d'acceptation

CI/CD conforme lorsque :

chaque commit déclenche CI ;
les tests et scans bloquent les erreurs ;
les artefacts sont signés ;
les déploiements sont automatisés ;
les rollbacks sont possibles ;
les runs sont auditables.

Décision majeure : Automated Delivery Control Plane

La livraison devient une chaîne de contrôle automatisée.
