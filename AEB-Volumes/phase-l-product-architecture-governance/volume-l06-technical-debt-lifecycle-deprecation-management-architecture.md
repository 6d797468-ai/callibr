# Volume L06 — Technical Debt, Lifecycle & Deprecation Management Architecture

> Extrait généré depuis `Architecture & Engineering Book (AEB).md` le 2026-07-27.

PHASE L — PRODUCT GOVERNANCE, ARCHITECTURE GOVERNANCE & ENTERPRISE OPERATIONS
Volume L06
Technical Debt, Lifecycle & Deprecation Management Architecture

Version : 1.0

Statut : Enterprise Maintainability Foundation

Criticité : Critique

1. Vision

La dette technique doit être visible, priorisée et traitée.

Elle peut concerner :

code ;
tests ;
architecture ;
données ;
sécurité ;
performance ;
observabilité ;
documentation ;
prompts ;
modèles IA ;
infrastructure.

2. Principe fondamental

La dette acceptée doit avoir un propriétaire et une date de révision.

Sinon elle devient une décision cachée.

3. Architecture globale

                    Debt Signal


                         │


                         ▼


                    Debt Registry


       ┌─────────────────┼─────────────────┐


       ▼                 ▼                 ▼


 Risk Scoring       Remediation Plan     Deprecation

4. Debt Categories

Catégories :

design debt ;
code debt ;
test debt ;
data debt ;
security debt ;
ops debt ;
AI debt ;
documentation debt ;
dependency debt.

5. Debt Scoring

Score :

impact ;
probability ;
cost of delay ;
blast radius ;
customer impact ;
security exposure ;
remediation effort.

6. Debt Budget

Chaque cycle réserve une capacité pour :

remédiation ;
refactoring ;
upgrade ;
documentation ;
tests ;
observabilité.

7. Deprecation Lifecycle

Cycle :

active ;
deprecated ;
migration available ;
sunset scheduled ;
removed.

8. Lifecycle Management

Objets concernés :

API ;
events ;
features ;
connectors ;
domain packs ;
models ;
prompts ;
libraries ;
infrastructure modules.

9. Data Model

TechnicalDebtItem
-----------------

id

title

category

owner

score

status

due_date

DeprecationNotice
-----------------

id

asset_type

asset_id

deprecated_at

sunset_at

MigrationPlan
-------------

id

deprecation_id

steps

owner

10. API interne

Créer dette :

POST /technical-debt/items

Créer dépréciation :

POST /technical-debt/deprecations

Lire registre :

GET /technical-debt/register

11. Décisions d'architecture (ADR)

ADR-L06-001
La dette technique est enregistrée.

Décision :

Rendre les compromis visibles.

ADR-L06-002
Chaque dette possède owner et score.

Décision :

Permettre priorisation.

ADR-L06-003
La dépréciation suit un lifecycle.

Décision :

Protéger clients et intégrations.

ADR-L06-004
Les assets IA ont aussi une dette.

Décision :

Gouverner prompts, datasets et modèles.

12. Critères d'acceptation

Technical Debt Management conforme lorsque :

les dettes sont cataloguées ;
les scores existent ;
les owners sont définis ;
les dépréciations sont annoncées ;
les migrations sont documentées ;
la dette critique est revue régulièrement.

Décision majeure : Visible Technical Debt Economy

Callibr traite la dette comme un portefeuille de risques, pas comme un bruit de fond.
