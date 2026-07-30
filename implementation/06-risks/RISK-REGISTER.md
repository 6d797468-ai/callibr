# Risk Register

Mise a jour : 2026-07-27

| ID | Risque | Probabilite | Impact | Mitigation |
| --- | --- | --- | --- | --- |
| R-001 | Sur-architecture avant MVP | Haute | Haut | vertical slices, scope MVP strict |
| R-002 | LLM trop tot dans la boucle critique | Moyenne | Haut | stub deterministe puis adapter |
| R-003 | Multi-tenant oublie dans les donnees | Moyenne | Critique | tenant context des Sprint 02 |
| R-004 | Frontend construit sans workflow reel | Moyenne | Moyen | commencer par parcours simulation |
| R-005 | Tests repousses | Haute | Haut | tests des le Sprint 00 |
| R-006 | CRM fictif trop generique | Moyenne | Moyen | domaine SAV comme premier pack |
| R-007 | Evaluation QA floue | Moyenne | Haut | scorecard rule-based initiale |
| R-008 | Documentation de lancement absente | Moyenne | Moyen | README obligatoire a chaque sprint |
| R-009 | Couplage engines | Moyenne | Haut | contracts + ports |
| R-010 | Donnees demo insuffisantes | Haute | Moyen | seed demo versionne |

## Risque Principal

Le plus grand risque est de vouloir implementer l'ensemble du Book au lieu de livrer une premiere capacite complete.

Decision :

Le MVP doit rester centre sur une simulation SAV textuelle.

