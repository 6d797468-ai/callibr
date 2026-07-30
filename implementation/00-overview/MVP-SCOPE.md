# MVP Scope

Mise a jour : 2026-07-27

## Nom

Callibr MVP — Text Simulation Core

## Objectif

Prouver que Callibr peut entrainer un agent sur un scenario de centre de contacts avec simulation IA, CRM fictif, actions metier et evaluation automatique.

## Persona Cible MVP

Agent en formation.

## Domaine Metier MVP

Support Client / SAV.

Pourquoi :

- cas universel ;
- logique simple a comprendre ;
- actions CRM classiques ;
- evaluation QA claire ;
- forte valeur demo.

## Parcours Utilisateur MVP

1. L'utilisateur se connecte.
2. Il selectionne un scenario SAV.
3. Il lance une session.
4. Le client simule exprime son probleme.
5. L'agent pose des questions.
6. L'agent verifie l'identite.
7. L'agent consulte le CRM fictif.
8. L'agent cree ou met a jour un ticket.
9. L'agent propose une resolution.
10. La session se termine.
11. Le systeme genere un score et un feedback.

## Fonctionnalites Incluses

### Backend

- API FastAPI.
- Healthcheck.
- Tenant local.
- Auth minimale.
- Sessions de simulation.
- Messages conversationnels.
- Scenario SAV initial.
- Persona client simple.
- CRM fictif in-memory puis PostgreSQL.
- Actions CRM : verify identity, search customer, create ticket, add note.
- Evaluation QA rule-based.
- Evenements internes.

### Frontend

- Ecran login minimal.
- Liste des scenarios.
- Ecran simulation chat.
- Panneau CRM fictif.
- Panneau objectifs/procedure.
- Rapport final simple.

### Donnees

- un tenant demo ;
- un utilisateur demo ;
- trois clients fictifs ;
- deux scenarios SAV ;
- deux personas ;
- une grille QA simple.

### IA

MVP compatible avec deux modes :

- mode stub deterministe pour tests ;
- mode local/provider via adapter LLM plus tard.

La simulation ne depend pas obligatoirement d'un LLM pour les premiers tests.

## Fonctionnalites Exclues

- voix ;
- STT/TTS ;
- paiement ;
- marketplace ;
- vrais connecteurs CRM ;
- SSO Enterprise ;
- analytics avance ;
- multi-region ;
- mobile app ;
- agent multi-outils autonome.

## Critere De Sortie

Le MVP est pret pour demo lorsque :

- `docker compose up` demarre les services ;
- l'API expose OpenAPI ;
- le frontend permet une session complete ;
- les tests unitaires backend passent ;
- un rapport final est genere ;
- le README explique comment lancer le projet.

