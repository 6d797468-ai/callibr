# Volume L01 — ADR Lifecycle & Architecture Decision Records Governance Architecture

> Extrait généré depuis `Architecture & Engineering Book (AEB).md` le 2026-07-27.

PHASE L — PRODUCT GOVERNANCE, ARCHITECTURE GOVERNANCE & ENTERPRISE OPERATIONS
Volume L01
ADR Lifecycle & Architecture Decision Records Governance Architecture

Version : 1.0

Statut : Enterprise Governance Foundation

Criticité : Critique

1. Vision

Les Architecture Decision Records constituent la mémoire décisionnelle de Callibr.

Ils expliquent :

quelle décision a été prise ;
pourquoi ;
quelles options ont été rejetées ;
quels impacts sont acceptés ;
quand réviser la décision.

2. Principe fondamental

Une décision d'architecture non documentée devient une dette invisible.

Un ADR rend la décision visible, discutable et révisable.

3. Architecture globale

                    Architecture Change


                            │


                            ▼


                         ADR Draft


       ┌────────────────────┼────────────────────┐


       ▼                    ▼                    ▼


 Review Board        Impact Analysis        Decision Log


                            │


                            ▼


                       ADR Registry

4. ADR Scope

Un ADR est requis pour :

changement de technologie majeure ;
nouveau bounded context ;
nouveau moteur ;
nouveau provider critique ;
changement data model critique ;
changement sécurité ;
changement API public ;
changement IA production ;
exception à un standard ;
dette technique acceptée.

5. ADR Status

États :

draft ;
proposed ;
accepted ;
rejected ;
superseded ;
deprecated ;
retired.

6. ADR Template

Chaque ADR contient :

contexte ;
problème ;
options ;
décision ;
conséquences ;
risques ;
alternatives rejetées ;
critères de révision ;
owner ;
date.

7. Decision Review

La revue évalue :

fit architecture ;
risque sécurité ;
impact tenant ;
impact data ;
coût ;
réversibilité ;
maintenabilité ;
impact produit ;
impact opérationnel.

8. ADR Registry

Le registry indexe :

id ;
titre ;
status ;
owner ;
domaines impactés ;
services impactés ;
liens RFC ;
liens incidents ;
liens releases.

9. Supersession

Une décision peut en remplacer une autre.

Règle :

un ADR accepté n'est jamais modifié pour changer l'histoire.

Il est superseded par un nouvel ADR.

10. Data Model

ArchitectureDecision
--------------------

id

title

status

owner

date

supersedes

impacted_domains

DecisionOption
--------------

id

adr_id

description

tradeoffs

decision

DecisionReview
--------------

id

adr_id

reviewer

decision

comments

11. API interne

Créer ADR :

POST /governance/adr

Soumettre revue :

POST /governance/adr/{id}/reviews

Lister décisions impactant un service :

GET /governance/adr?service=conversation-engine

12. Décisions d'architecture (ADR)

ADR-L01-001
Les décisions structurantes exigent un ADR.

Décision :

Rendre l'architecture auditable.

ADR-L01-002
Les ADR sont immuables après acceptation.

Décision :

Préserver la mémoire décisionnelle.

ADR-L01-003
Le registry ADR est interrogeable.

Décision :

Relier décisions, code, services et incidents.

ADR-L01-004
Les exceptions aux standards expirent.

Décision :

Éviter la dette permanente.

13. Critères d'acceptation

ADR Governance conforme lorsque :

les décisions structurantes ont un ADR ;
les statuts sont suivis ;
les alternatives sont documentées ;
les ADR acceptés sont immuables ;
les remplacements sont traçables ;
les exceptions ont une date de revue.

Décision majeure : Architecture Memory System

Callibr adopte une mémoire d'architecture explicite et interrogeable.
