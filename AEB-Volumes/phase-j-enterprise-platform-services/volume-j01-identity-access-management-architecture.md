# Volume J01 — Identity & Access Management Architecture

> Extrait généré depuis `Architecture & Engineering Book (AEB).md` le 2026-07-27.

PHASE J — ENTERPRISE PLATFORM SERVICES
Volume J01
Identity & Access Management Architecture

Version : 1.0

Statut : Enterprise Platform Foundation

Criticité : Critique

1. Vision

L'Identity & Access Management est la porte d'entrée de Callibr.

Il répond à quatre questions :

qui est l'utilisateur ?
à quelle organisation appartient-il ?
dans quel contexte agit-il ?
qu'a-t-il le droit de faire ?

2. Principe fondamental

L'identité n'est jamais un simple login.

Elle combine :

utilisateur ;
tenant ;
organisation ;
workspace ;
rôle ;
attributs ;
session ;
contexte de risque.

3. Architecture globale

                    Identity Provider


                           │


                           ▼


                      IAM Service


        ┌──────────────────┼──────────────────┐


        ▼                  ▼                  ▼


 Authentication      Identity Graph      Session Service


        │                  │                  │


        ▼                  ▼                  ▼


 Token Service       Access Context      Audit Trail

4. Modes d'authentification

Support :

email/password ;
magic link ;
OIDC ;
SAML 2.0 ;
SCIM provisioning ;
service accounts ;
API credentials ;
MFA.

5. Identity Federation

Les clients Enterprise peuvent connecter :

Azure AD ;
Okta ;
Google Workspace ;
Keycloak ;
Ping Identity ;
ADFS.

Callibr ne doit pas forcer un annuaire propriétaire.

6. Session Model

Une session contient :

user_id ;
tenant_id ;
organization_id ;
workspace_id ;
roles ;
attributes ;
risk_level ;
issued_at ;
expires_at ;
trace_id.

7. MFA

MFA requis selon :

rôle admin ;
accès données sensibles ;
export ;
configuration sécurité ;
risque élevé ;
politique tenant.

8. Service Accounts

Les intégrations automatisées utilisent des comptes de service.

Règles :

pas de login humain ;
scopes minimaux ;
expiration ;
rotation ;
audit renforcé.

9. Identity Lifecycle

Cycle :

Invited

↓

Active

↓

Suspended

↓

Deprovisioned

↓

Archived

10. Data Model

UserIdentity
------------

id

email

display_name

status

created_at

FederatedIdentity
-----------------

id

user_id

provider

external_subject

TenantMembership
----------------

id

tenant_id

user_id

status

Session
-------

id

user_id

tenant_id

risk_level

expires_at

11. API interne

Créer utilisateur :

POST /iam/users

Créer session :

POST /iam/sessions

Révoquer session :

POST /iam/sessions/{id}/revoke

Lier identité fédérée :

POST /iam/federated-identities

12. Observabilité

Métriques :

login_success_rate ;
login_failure_rate ;
mfa_challenge_rate ;
session_duration ;
token_refresh_rate ;
identity_provider_latency ;
provisioning_errors.

13. Décisions d'architecture (ADR)

ADR-J01-001
L'identité est fédérable.

Décision :

Supporter les annuaires Enterprise existants.

ADR-J01-002
Les sessions portent le contexte tenant.

Décision :

Empêcher les actions hors contexte organisationnel.

ADR-J01-003
Les comptes de service sont séparés des utilisateurs humains.

Décision :

Réduire les risques d'automatisation non contrôlée.

ADR-J01-004
Le MFA est piloté par politique.

Décision :

Adapter sécurité et ergonomie selon le risque.

14. Critères d'acceptation

IAM conforme lorsque :

les utilisateurs peuvent être fédérés ;
les sessions portent le contexte tenant ;
les identités externes sont traçables ;
les comptes de service sont scopés ;
les sessions peuvent être révoquées ;
les événements IAM sont audités.

Décision majeure : Identity as Control Plane

Callibr adopte l'identité comme Control Plane d'accès à toute la plateforme.
