# Volume K03 — GitOps, Environment Promotion & Configuration Drift Architecture

> Extrait généré depuis `Architecture & Engineering Book (AEB).md` le 2026-07-27.

PHASE K — DEV PLATFORM, DEVSECOPS & PLATFORM ENGINEERING
Volume K03
GitOps, Environment Promotion & Configuration Drift Architecture

Version : 1.0

Statut : Deployment Governance Foundation

Criticité : Critique

1. Vision

GitOps fait du dépôt Git la source de vérité des environnements.

Il gouverne :

manifests Kubernetes ;
Helm values ;
Kustomize overlays ;
policies ;
secrets references ;
rollouts ;
environment promotion.

2. Principe fondamental

L'état désiré est déclaré dans Git.

Le cluster converge vers cet état.

Les changements directs en production sont détectés comme drift.

3. Architecture globale

                    Git Repository


                         │


                         ▼


                    GitOps Controller


       ┌─────────────────┼─────────────────┐


       ▼                 ▼                 ▼


   Dev Cluster       Staging Cluster     Production Cluster

4. Environment Model

Environnements :

local ;
dev ;
ci ;
staging ;
preprod ;
production ;
dr.

Chaque environnement possède une configuration explicite.

5. Promotion Flow

Flux :

dev validated ;
artifact signed ;
staging promotion ;
integration tests ;
approval ;
production promotion ;
monitoring.

6. Drift Detection

Détecte :

resource changed ;
replica count modified ;
policy disabled ;
image tag changed ;
secret reference altered ;
network policy removed.

7. Secrets References

Git ne stocke jamais les secrets en clair.

Il stocke :

secret references ;
sealed secrets ;
external secret bindings ;
vault paths.

8. Data Model

Environment
-----------

id

name

region

cluster_ref

status

GitOpsApplication
-----------------

id

environment_id

repository

path

sync_status

PromotionRequest
----------------

id

artifact_id

from_environment

to_environment

status

9. API interne

Demander promotion :

POST /gitops/promotions

Lire drift :

GET /gitops/applications/{id}/drift

Synchroniser :

POST /gitops/applications/{id}/sync

10. Décisions d'architecture (ADR)

ADR-K03-001
Git est la source de vérité des environnements.

Décision :

Rendre les changements auditables.

ADR-K03-002
Les promotions suivent un flux contrôlé.

Décision :

Réduire les risques de mise en production.

ADR-K03-003
Le drift est détecté.

Décision :

Identifier les changements hors processus.

ADR-K03-004
Les secrets ne sont pas stockés en clair.

Décision :

Préserver la sécurité opérationnelle.

11. Critères d'acceptation

GitOps conforme lorsque :

les manifests sont versionnés ;
les clusters convergent automatiquement ;
les promotions sont tracées ;
le drift est visible ;
les secrets sont référencés ;
les changements production passent par revue.

Décision majeure : Git as Runtime Source of Truth

Git devient le registre opérationnel de l'état désiré.
