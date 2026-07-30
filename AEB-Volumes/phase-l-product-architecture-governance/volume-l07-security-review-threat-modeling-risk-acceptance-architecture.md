# Volume L07 — Security Review, Threat Modeling & Risk Acceptance Architecture

> Extrait généré depuis `Architecture & Engineering Book (AEB).md` le 2026-07-27.

PHASE L — PRODUCT GOVERNANCE, ARCHITECTURE GOVERNANCE & ENTERPRISE OPERATIONS
Volume L07
Security Review, Threat Modeling & Risk Acceptance Architecture

Version : 1.0

Statut : Enterprise Security Governance

Criticité : Critique

1. Vision

Security Review garantit que les changements critiques sont évalués avant production.

Elle couvre :

menaces ;
risques ;
contrôles ;
exceptions ;
acceptation ;
revue ;
preuves.

2. Principe fondamental

La sécurité doit être proportionnelle au risque et intégrée au cycle produit.

3. Architecture globale

                    Change Proposal


                          │


                          ▼


                    Security Review


       ┌──────────────────┼──────────────────┐


       ▼                  ▼                  ▼


 Threat Model       Control Review       Risk Acceptance

4. Threat Modeling Scope

Requis pour :

nouvelle API publique ;
nouvelle intégration ;
nouveau tool IA ;
nouvelle donnée sensible ;
nouveau flux admin ;
changement auth ;
extension marketplace ;
stockage vectoriel ;
export massif.

5. Threat Model

Analyse :

assets ;
actors ;
entrypoints ;
trust boundaries ;
data flows ;
threats ;
mitigations ;
residual risks.

6. Risk Acceptance

Un risque accepté contient :

description ;
justification ;
owner business ;
owner security ;
expiration ;
mitigations ;
review date.

7. Security Gates

Gates :

design review ;
SAST ;
DAST ;
dependency scan ;
container scan ;
secret scan ;
manual review ;
penetration test si nécessaire.

8. Data Model

ThreatModel
-----------

id

subject

owner

status

reviewed_at

SecurityFinding
---------------

id

threat_model_id

severity

description

status

RiskAcceptance
--------------

id

finding_id

accepted_by

expires_at

justification

9. API interne

Créer threat model :

POST /security-governance/threat-models

Créer finding :

POST /security-governance/findings

Accepter risque :

POST /security-governance/risk-acceptances

10. Décisions d'architecture (ADR)

ADR-L07-001
Les changements sensibles exigent threat model.

Décision :

Identifier risques avant production.

ADR-L07-002
Les risques acceptés expirent.

Décision :

Éviter la normalisation du risque.

ADR-L07-003
Les gates sécurité sont intégrés à la delivery.

Décision :

Automatiser les contrôles récurrents.

ADR-L07-004
Les findings critiques bloquent la release.

Décision :

Préserver la posture Enterprise.

11. Critères d'acceptation

Security Review conforme lorsque :

les threat models existent pour les changements sensibles ;
les findings sont suivis ;
les risques acceptés expirent ;
les gates sécurité bloquent les critiques ;
les preuves sont conservées ;
les owners sécurité sont identifiés.

Décision majeure : Risk-Aware Security Governance

Callibr gouverne la sécurité par le risque explicite et la preuve.
