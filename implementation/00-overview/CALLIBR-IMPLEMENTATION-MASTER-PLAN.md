# Callibr Implementation Master Plan

Mise a jour : 2026-07-27

## Vision D'Execution

Callibr doit etre construit comme une plateforme SaaS IA modulaire, mais l'execution doit rester pragmatique.

La premiere version doit prouver une capacite complete :

Agent en formation

↓

Simulation textuelle

↓

Client IA simule

↓

CRM fictif

↓

Actions metier

↓

Evaluation QA

↓

Rapport de progression

## Objectif MVP

Livrer une experience de simulation textuelle exploitable en local et demonstrable.

Le MVP doit etre assez simple pour etre developpe rapidement, mais assez structure pour ne pas etre jete ensuite.

## Strategie

Approche retenue :

Vertical Slice Delivery.

Chaque sprint livre une capacite observable :

- API appelee ;
- logique domaine executee ;
- donnees persistees ;
- evenements emis ;
- tests presents ;
- documentation mise a jour.

## Architecture D'Implementation

Le code doit suivre le Book :

- monorepo ;
- Python/FastAPI pour backend ;
- architecture hexagonale ;
- contrats explicites ;
- event-driven interne ;
- multi-tenant des le debut ;
- observabilite minimale ;
- tests des cas critiques.

## Phases D'Execution

| Phase | Objectif | Resultat attendu |
| --- | --- | --- |
| P0 | Bootstrap | Repo executable localement |
| P1 | Kernel & Identity | Socle technique et contexte tenant |
| P2 | Simulation MVP | Conversation textuelle complete |
| P3 | CRM & Procedures | Actions metier et verification procedure |
| P4 | Evaluation & Coaching | Score QA et feedback |
| P5 | Analytics & Admin | Reporting minimal et gestion tenant |
| P6 | Enterprise Hardening | securite, observabilite, CI/CD, packaging |

## Regle De Priorisation

Priorite 1 :

Tout ce qui rend la simulation de bout en bout possible.

Priorite 2 :

Tout ce qui rend la simulation fiable, testable et observable.

Priorite 3 :

Tout ce qui rend la plateforme extensible.

Priorite 4 :

Tout ce qui rend la plateforme Enterprise.

## Non-Objectifs Du MVP

Le MVP ne couvre pas :

- voix temps reel ;
- marketplace ;
- multi-agent avance ;
- billing reel ;
- integrations externes reelles ;
- Kubernetes production ;
- fine-tuning ;
- analytics enterprise complet ;
- white label avance.

Ces sujets restent dans la roadmap, mais ne doivent pas bloquer la premiere tranche.

## Definition De Succes MVP

Le MVP est reussi lorsque :

- un utilisateur peut lancer une simulation SAV ;
- le client simule repond selon un persona ;
- le CRM fictif affiche et modifie un dossier ;
- au moins quatre actions metier sont executees ;
- une procedure simple est validee ;
- un score QA est produit ;
- un rapport est consultable ;
- les tests critiques passent ;
- l'application demarre localement en moins de 10 minutes.

