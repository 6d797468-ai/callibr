# Volume L02 — RFC, Design Proposal & Collaborative Decision Process Architecture

> Extrait généré depuis `Architecture & Engineering Book (AEB).md` le 2026-07-27.

PHASE L — PRODUCT GOVERNANCE, ARCHITECTURE GOVERNANCE & ENTERPRISE OPERATIONS
Volume L02
RFC, Design Proposal & Collaborative Decision Process Architecture

Version : 1.0

Statut : Enterprise Collaboration Foundation

Criticité : Élevée

1. Vision

Les RFC permettent d'explorer des changements avant de prendre une décision.

Ils servent à :

poser un problème ;
proposer une solution ;
collecter feedback ;
identifier impacts ;
préparer un ADR ;
aligner produit, engineering, sécurité et opérations.

2. Principe fondamental

Le RFC est le lieu de discussion.

L'ADR est le lieu de décision.

3. Architecture globale

                    Idea / Problem


                         │


                         ▼


                       RFC Draft


       ┌─────────────────┼─────────────────┐


       ▼                 ▼                 ▼


 Product Review    Architecture Review   Security Review


                         │


                         ▼


                    Decision / ADR / Backlog

4. RFC Scope

RFC recommandé pour :

nouvelle capacité produit ;
nouveau moteur ;
nouveau flux utilisateur ;
nouvelle API publique ;
nouvelle intégration ;
changement de modèle IA ;
modification UX majeure ;
changement pricing ;
changement gouvernance.

5. RFC Template

Sections :

summary ;
problem statement ;
goals ;
non-goals ;
proposal ;
alternatives ;
risks ;
security impact ;
data impact ;
operations impact ;
migration ;
success metrics.

6. Review Roles

Rôles :

author ;
product reviewer ;
architecture reviewer ;
security reviewer ;
data reviewer ;
operations reviewer ;
customer impact reviewer.

7. Feedback Window

Chaque RFC définit :

date ouverture ;
date fermeture ;
audience ;
mode de décision ;
owner.

8. RFC Outcomes

Résultats :

accepted ;
rejected ;
needs research ;
split ;
converted to ADR ;
converted to PRD ;
deferred.

9. Data Model

RFC
---

id

title

status

owner

created_at

decision_due_at

RFCReview
---------

id

rfc_id

reviewer

area

decision

RFCImpact
---------

id

rfc_id

impact_type

description

severity

10. API interne

Créer RFC :

POST /governance/rfc

Ajouter revue :

POST /governance/rfc/{id}/reviews

Convertir en ADR :

POST /governance/rfc/{id}/convert-to-adr

11. Décisions d'architecture (ADR)

ADR-L02-001
Le RFC précède les changements complexes.

Décision :

Améliorer qualité des décisions.

ADR-L02-002
Les impacts sont explicitement évalués.

Décision :

Éviter les surprises production.

ADR-L02-003
Le RFC peut produire PRD, ADR ou backlog.

Décision :

Connecter discovery et delivery.

ADR-L02-004
Les fenêtres de feedback sont limitées.

Décision :

Préserver vitesse de décision.

12. Critères d'acceptation

RFC Process conforme lorsque :

les changements complexes ont un RFC ;
les reviewers clés sont identifiés ;
les impacts sont renseignés ;
les décisions sont tracées ;
les RFC acceptés produisent des artefacts ;
les RFC rejetés expliquent pourquoi.

Décision majeure : Collaborative Change Design

Callibr adopte un processus de conception collaborative avant les décisions irréversibles.
