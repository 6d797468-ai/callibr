# Volume G12 — Domain Pack — Help Desk ITIL

> Extrait généré depuis `Architecture & Engineering Book (AEB).md` le 2026-07-27.

PHASE G — CONTACT CENTER BUSINESS PACKS
Volume G12
Domain Pack — Help Desk ITIL

Version : 1.0

Statut : Enterprise Core

Criticité : Très élevée

1. Vision

Le Domain Pack Help Desk ITIL simule le fonctionnement d'un centre de services informatique conforme aux pratiques ITIL.

L'apprenant ne doit pas uniquement résoudre un incident.

Il doit appliquer les processus :

qualification ;
catégorisation ;
priorisation ;
diagnostic ;
résolution ;
documentation ;
clôture.

Le moteur reproduit fidèlement les contraintes d'un Service Desk moderne.

2. Objectifs pédagogiques

À la fin de la formation, l'apprenant doit être capable de :

qualifier correctement une demande ;
distinguer un Incident d'une Service Request ;
appliquer les SLA ;
consulter la base de connaissances ;
documenter la résolution ;
décider d'une escalade.
3. Architecture fonctionnelle
User Request

↓

Classification Engine

↓

ITSM Engine

↓

Knowledge Engine

↓

CMDB Engine

↓

Resolution Engine

↓

QA Engine

Chaque moteur est indépendant.

4. ITSM Engine

Le moteur maintient :

les tickets ;
les utilisateurs ;
les services ;
les actifs ;
les SLA ;
les files de support ;
les groupes techniques.

Toutes les actions sont historisées.

5. Types de tickets

Le système distingue :

Incident ;
Service Request ;
Access Request ;
Information Request ;
Standard Change ;
Emergency Change (simulation) ;
Major Incident (simulation).

Chaque type possède un workflow spécifique.

6. Workflow Incident
Nouveau

↓

Qualification

↓

Catégorisation

↓

Priorisation

↓

Diagnostic

↓

Résolution

↓

Validation

↓

Clôture

Les transitions sont contrôlées par le moteur.

7. Priorisation

La priorité est calculée à partir :

de l'impact ;
de l'urgence ;
du service concerné ;
des engagements SLA.

Exemple :

priority_matrix:

impact:
  high

urgency:
  high

priority:
  P1

Les matrices sont configurables.

8. SLA Engine

Chaque ticket possède :

délai de prise en charge ;
délai de résolution ;
niveau d'escalade ;
temps restant.

Le moteur surveille les dépassements.

9. CMDB Engine

Le moteur simule une Configuration Management Database.

Chaque élément de configuration (CI) possède :

identifiant ;
type ;
propriétaire ;
dépendances ;
état ;
historique.

Les scénarios peuvent impliquer plusieurs CI.

10. Knowledge Engine

Le Service Desk peut consulter une base de connaissances simulée.

Elle contient :

procédures ;
FAQ ;
solutions connues ;
guides techniques ;
erreurs fréquentes.

Le moteur évalue si l'apprenant utilise efficacement ces ressources.

11. Actions disponibles

L'agent peut :

créer un ticket ;
modifier la catégorie ;
mettre à jour la priorité ;
consulter la CMDB ;
rechercher un article de connaissance ;
escalader ;
résoudre ;
clôturer.

Chaque action génère un événement.

12. Escalades

Le moteur gère plusieurs niveaux :

L1

↓

L2

↓

L3

↓

Expert

↓

Éditeur

Chaque niveau possède ses propres compétences.

13. Bibliothèque de scénarios
ID	Scénario	Niveau
ITIL-001	Réinitialisation de mot de passe	1
ITIL-002	Imprimante indisponible	1
ITIL-003	Application métier inaccessible	2
ITIL-004	Incident réseau	2
ITIL-005	Panne serveur	3
ITIL-006	Incident majeur	3
ITIL-007	Dépendances multiples	3
ITIL-008	Gestion d'une crise IT	3
14. KPI métier

Le moteur calcule notamment :

First Contact Resolution (FCR) ;
Respect des SLA ;
Temps moyen de résolution (MTTR) ;
Nombre d'escalades ;
Réouvertures de tickets ;
Utilisation de la base de connaissances.
15. Évaluation QA

Critères indicatifs.

Critère	Pondération
Qualification	15 %
Priorisation	15 %
Diagnostic	20 %
Respect du processus ITIL	20 %
Documentation	15 %
Communication	15 %
16. Jeux de données

Le pack fournit :

plusieurs milliers de tickets synthétiques ;
une CMDB simulée ;
une base de connaissances ;
des profils utilisateurs ;
des services ;
des actifs informatiques.

Toutes les données sont artificielles.

17. Architecture interne
Classification Engine

↓

Ticket Engine

↓

SLA Engine

↓

CMDB Engine

↓

Knowledge Engine

↓

Resolution Engine

↓

Analytics

Chaque composant est indépendant.

18. Intégration avec les autres moteurs

Le Help Desk ITIL échange avec :

Conversation Engine pour les interactions avec les utilisateurs ;
Workflow Engine pour les changements d'état ;
QA Engine pour l'évaluation ;
Reporting Platform pour les KPI ;
Learning Platform pour recommander des exercices ciblés.

Cette séparation garantit une forte réutilisabilité des composants.

19. Décisions d'architecture (ADR)

Ce volume formalise les principes suivants :

Le moteur ITSM applique les workflows et ne dépend pas du LLM.
Les SLA sont gérés par un composant dédié.
La CMDB est un objet métier indépendant.
Les règles de priorisation sont déclaratives.
La base de connaissances est versionnée et peut être enrichie sans modifier le moteur.
20. Critères d'acceptation

Le Domain Pack Help Desk ITIL est considéré conforme lorsque :

les workflows ITIL sont respectés ;
les tickets suivent des transitions valides ;
les SLA sont surveillés correctement ;
les scénarios reproduisent des situations réalistes ;
les évaluations sont cohérentes et explicables.
🏛️ Décision d'architecture majeure : IT Service Management Simulation Architecture (ITSA)

Je recommande une IT Service Management Simulation Architecture (ITSA).

Le moteur reproduit les composants clés d'une plateforme ITSM (tickets, SLA, CMDB, connaissances, workflows) sans chercher à copier un outil existant. Cette approche permet d'entraîner les apprenants sur les concepts et les processus, tout en gardant une architecture générique, modulaire et réutilisable pour différents contextes (Service Desk, MSP, support SaaS, NOC, etc.).

📘 État d'avancement

Après ce volume :

✅ G1 à G12 terminés (12 Domain Packs sur 20).
📘 Il reste 8 volumes pour achever la Phase G :
G13 — Incident & Problem Management
G14 — Banking Contact Center
G15 — Insurance Contact Center
G16 — Healthcare Contact Center
G17 — E-commerce & Retail
G18 — Public Services & Administration
G19 — Collections avancées & Contentieux
G20 — Omnichannel & Digital Engagement

Une fois ces huit volumes terminés, nous commencerons la Phase H — AI Platform Enterprise, qui décrira l'architecture complète de l'orchestration des agents IA, du Prompt Compiler, du LLM Gateway, des outils (Tool Calling), du registre d'agents et des mécanismes de sécurité et de gouvernance des modèles.
