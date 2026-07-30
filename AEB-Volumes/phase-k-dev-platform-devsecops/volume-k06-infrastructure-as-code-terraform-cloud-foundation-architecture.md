# Volume K06 — Infrastructure as Code, Terraform & Cloud Foundation Architecture

> Extrait généré depuis `Architecture & Engineering Book (AEB).md` le 2026-07-27.

PHASE K — DEV PLATFORM, DEVSECOPS & PLATFORM ENGINEERING
Volume K06
Infrastructure as Code, Terraform & Cloud Foundation Architecture

Version : 1.0

Statut : Infrastructure Foundation

Criticité : Critique

1. Vision

L'infrastructure de Callibr est décrite comme du code.

Elle couvre :

réseau ;
clusters ;
bases ;
stockage ;
IAM cloud ;
secrets ;
observabilité ;
registries ;
DNS ;
certificats.

2. Principe fondamental

Aucune infrastructure production ne doit être créée manuellement.

Chaque ressource doit être déclarée, revue et traçable.

3. Architecture globale

                    Terraform Modules


                           │


                           ▼


                    IaC Pipeline


       ┌──────────────────┼──────────────────┐


       ▼                  ▼                  ▼


 Plan              Policy Check          Apply

4. Module Strategy

Modules :

network ;
kubernetes ;
postgres ;
redis ;
object_storage ;
event_bus ;
observability ;
security ;
dns ;
backup.

5. Environment State

Chaque environnement possède son state.

Règles :

remote backend ;
locking ;
encryption ;
access control ;
backup.

6. Policy as Code

Contrôles :

pas de stockage public ;
chiffrement obligatoire ;
tags obligatoires ;
regions autorisées ;
taille ressources ;
IAM least privilege.

7. Drift

Le drift infrastructure est détecté.

Il déclenche :

alerte ;
revue ;
correction ;
audit.

8. Data Model

InfrastructureModule
--------------------

id

name

version

owner

InfrastructureState
-------------------

id

environment

backend_ref

last_apply

PolicyViolation
---------------

id

module

severity

rule

status

9. API interne

Demander plan :

POST /iac/plans

Lister states :

GET /iac/states

Lire violations :

GET /iac/policy-violations

10. Décisions d'architecture (ADR)

ADR-K06-001
Terraform est le standard IaC principal.

Décision :

Décrire l'infrastructure de manière reproductible.

ADR-K06-002
Les states sont isolés par environnement.

Décision :

Limiter risques de modification croisée.

ADR-K06-003
Policy as Code bloque les ressources non conformes.

Décision :

Intégrer sécurité et FinOps.

ADR-K06-004
Le drift est surveillé.

Décision :

Maintenir cohérence entre Git et cloud.

11. Critères d'acceptation

IaC conforme lorsque :

les ressources sont codées ;
les modules sont versionnés ;
les plans sont revus ;
les states sont sécurisés ;
les policies bloquent les risques ;
le drift est détecté.

Décision majeure : Reproducible Cloud Foundation

L'infrastructure devient reproductible et auditée.
