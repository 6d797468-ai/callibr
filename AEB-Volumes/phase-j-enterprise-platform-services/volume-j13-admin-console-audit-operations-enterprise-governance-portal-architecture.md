# Volume J13 — Admin Console, Audit Operations & Enterprise Governance Portal Architecture

> Extrait généré depuis `Architecture & Engineering Book (AEB).md` le 2026-07-27.

PHASE J — ENTERPRISE PLATFORM SERVICES
Volume J13
Admin Console, Audit Operations & Enterprise Governance Portal Architecture

Version : 1.0

Statut : Enterprise Administration Foundation

Criticité : Critique

1. Vision

L'Admin Console permet d'opérer Callibr sans accès direct aux bases ou aux services internes.

Elle sert :

admins tenant ;
admins plateforme ;
support ;
security ;
customer success ;
operations.

2. Principe fondamental

Toute opération administrative doit être :

autorisée ;
guidée ;
réversible si possible ;
auditée ;
observable.

3. Architecture globale

                    Admin Console


                         │


                         ▼


                    Admin API Layer


       ┌─────────────────┼─────────────────┐


       ▼                 ▼                 ▼


 Governance Views    Operational Actions    Audit Explorer

4. Capabilities

Fonctions :

gestion tenants ;
utilisateurs ;
rôles ;
entitlements ;
extensions ;
intégrations ;
policies ;
audit ;
incidents ;
support actions.

5. Break Glass Access

Accès exceptionnel :

justification ;
approbation ;
durée courte ;
MFA ;
audit renforcé ;
notification.

6. Audit Explorer

Recherche :

acteur ;
tenant ;
ressource ;
action ;
période ;
résultat ;
trace_id.

7. Data Model

AdminAction
-----------

id

actor_id

tenant_id

action

resource

status

approval_id

AdminApproval
-------------

id

requested_by

approved_by

reason

expires_at

8. API interne

Exécuter action admin :

POST /admin/actions

Demander approbation :

POST /admin/approvals

Rechercher audit :

GET /admin/audit

9. Décisions d'architecture (ADR)

ADR-J13-001
Aucune opération admin hors API.

Décision :

Préserver auditabilité et sécurité.

ADR-J13-002
Les actions sensibles exigent approbation.

Décision :

Réduire erreurs et abus.

ADR-J13-003
Break glass est contrôlé.

Décision :

Permettre support urgent sans ouvrir un accès permanent.

ADR-J13-004
L'audit est consultable par rôle.

Décision :

Rendre la gouvernance exploitable.

10. Critères d'acceptation

Admin Console conforme lorsque :

les actions critiques passent par API ;
les approbations existent ;
les accès exceptionnels expirent ;
les audits sont consultables ;
les actions sont corrélées aux traces ;
les droits admin sont limités.

Décision majeure : Governed Administration Plane

L'administration devient elle-même un système gouverné.
