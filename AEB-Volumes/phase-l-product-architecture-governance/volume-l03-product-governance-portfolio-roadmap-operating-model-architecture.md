# Volume L03 — Product Governance, Portfolio & Roadmap Operating Model Architecture

> Extrait généré depuis `Architecture & Engineering Book (AEB).md` le 2026-07-27.

PHASE L — PRODUCT GOVERNANCE, ARCHITECTURE GOVERNANCE & ENTERPRISE OPERATIONS
Volume L03
Product Governance, Portfolio & Roadmap Operating Model Architecture

Version : 1.0

Statut : Enterprise Product Governance

Criticité : Critique

1. Vision

Product Governance définit comment Callibr décide quoi construire, dans quel ordre, pour quel résultat.

Elle relie :

stratégie ;
clients ;
roadmap ;
discovery ;
delivery ;
metrics ;
revenue ;
support ;
risques.

2. Principe fondamental

La roadmap n'est pas une liste de fonctionnalités.

C'est un portefeuille d'investissements orienté résultats.

3. Architecture globale

                    Product Strategy


                         │


                         ▼


                   Portfolio Governance


       ┌─────────────────┼─────────────────┐


       ▼                 ▼                 ▼


 Roadmap           Discovery          Delivery


                         │


                         ▼


                    Outcome Measurement

4. Product Portfolio

Portefeuilles :

core simulation ;
AI platform ;
domain packs ;
data platform ;
enterprise services ;
developer platform ;
marketplace ;
growth.

5. Investment Categories

Catégories :

customer value ;
revenue growth ;
platform scalability ;
security ;
compliance ;
technical debt ;
innovation ;
operational excellence.

6. Roadmap Model

Horizons :

Now ;
Next ;
Later ;
Discovery ;
Committed ;
Deprecated.

7. Prioritization

Critères :

customer impact ;
business value ;
risk reduction ;
effort ;
confidence ;
strategic fit ;
regulatory urgency.

8. Decision Forums

Forums :

Product Council ;
Architecture Council ;
Security Council ;
Revenue Council ;
Customer Advisory Board.

9. Data Model

ProductInitiative
-----------------

id

name

portfolio

status

owner

outcome

RoadmapItem
-----------

id

initiative_id

horizon

priority

target_date

InvestmentDecision
------------------

id

initiative_id

decision

rationale

10. API interne

Créer initiative :

POST /product-governance/initiatives

Lire roadmap :

GET /product-governance/roadmap

Enregistrer décision :

POST /product-governance/decisions

11. Décisions d'architecture (ADR)

ADR-L03-001
La roadmap est pilotée par outcomes.

Décision :

Éviter l'accumulation de fonctionnalités sans impact.

ADR-L03-002
Les initiatives appartiennent à un portefeuille.

Décision :

Rendre les investissements visibles.

ADR-L03-003
Les décisions produit sont tracées.

Décision :

Préserver alignement et responsabilité.

ADR-L03-004
La dette et la sécurité sont des catégories d'investissement.

Décision :

Éviter leur marginalisation.

12. Critères d'acceptation

Product Governance conforme lorsque :

les initiatives ont un outcome ;
la roadmap est priorisée ;
les décisions sont documentées ;
les portefeuilles sont équilibrés ;
les risques sont visibles ;
les métriques de succès sont définies.

Décision majeure : Outcome-Driven Product Portfolio

Callibr gouverne sa roadmap comme un portefeuille de résultats mesurables.
