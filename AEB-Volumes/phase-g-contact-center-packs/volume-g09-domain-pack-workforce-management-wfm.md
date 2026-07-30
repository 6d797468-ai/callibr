# Volume G09 — Domain Pack — Workforce Management (WFM)

> Extrait généré depuis `Architecture & Engineering Book (AEB).md` le 2026-07-27.

PHASE G — CONTACT CENTER BUSINESS PACKS
Volume G9
Domain Pack — Workforce Management (WFM)

Version : 1.0

Statut : Enterprise Core

Criticité : Critique

1. Vision

Le Workforce Management Engine simule le pilotage des ressources humaines d'un centre de contacts.

Son objectif est de permettre à un planificateur ou un responsable WFM de :

prévoir les volumes de contacts ;
calculer les besoins en effectifs ;
construire les plannings ;
suivre l'activité en temps réel ;
gérer les écarts ;
optimiser les coûts.

Le moteur travaille à l'échelle de tout un centre de contacts, et non d'un seul agent.

2. Objectifs pédagogiques

À la fin de la formation, l'apprenant doit être capable de :

analyser des historiques d'activité ;
produire une prévision fiable ;
calculer le nombre d'agents nécessaires ;
construire un planning équilibré ;
suivre les indicateurs opérationnels ;
corriger les dérives en temps réel.
3. Architecture fonctionnelle
Historique

↓

Forecast Engine

↓

Staffing Engine

↓

Scheduling Engine

↓

Intraday Engine

↓

Reporting

Chaque moteur possède ses propres responsabilités.

4. Forecast Engine

Le Forecast Engine estime :

volume d'appels ;
volume de chats ;
volume d'e-mails ;
volume WhatsApp ;
volume réseaux sociaux.

Les prévisions sont établies :

par tranche horaire ;
par jour ;
par semaine ;
par mois.
5. Données d'entrée

Le moteur utilise :

historique des contacts ;
saisonnalité ;
jours fériés ;
campagnes marketing ;
incidents majeurs ;
météo (optionnel) ;
événements exceptionnels.

Tous ces facteurs sont configurables.

6. Staffing Engine

À partir des prévisions, le moteur calcule :

effectif requis ;
effectif disponible ;
marge de sécurité ;
besoins de recrutement temporaire.

Les méthodes de calcul sont interchangeables.

7. Modèles de calcul

Le moteur supporte notamment :

Erlang C ;
Erlang A ;
simulation Monte Carlo ;
modèles statistiques ;
modèles IA.

Chaque organisation peut choisir son modèle.

8. Scheduling Engine

Le moteur génère des plannings en tenant compte :

des contrats ;
des horaires ;
des compétences ;
des pauses ;
des congés ;
des formations ;
des contraintes légales.
9. Contraintes

Exemple.

constraints:

max_daily_hours: 8

min_break_minutes: 20

max_consecutive_days: 6

night_shift_allowed: false

Toutes les contraintes sont déclaratives.

10. Multi-compétences

Chaque agent possède :

agent:

skills:

- sales

- support

- retention

proficiency:

sales: 95

support: 80

retention: 65

Le moteur privilégie les affectations adaptées aux compétences.

11. Intraday Engine

Le moteur suit en temps réel :

trafic réel ;
écart avec le forecast ;
retard ;
surcharge ;
sous-charge.

Il propose automatiquement des actions correctives.

12. Actions disponibles

Le responsable WFM peut :

déplacer des pauses ;
rappeler des agents ;
autoriser des heures supplémentaires ;
ouvrir une file secondaire ;
transférer des compétences ;
modifier un planning.

Chaque décision est simulée et tracée.

13. KPI opérationnels

Le moteur calcule notamment :

Service Level ;
ASA (Average Speed of Answer) ;
AHT (Average Handling Time) ;
Occupancy ;
Shrinkage ;
Forecast Accuracy ;
Schedule Adherence ;
Utilization Rate ;
Backlog.

Les formules sont documentées et versionnées.

14. Gestion des écarts

Le moteur détecte :

sous-effectif ;
sureffectif ;
pics de trafic ;
absentéisme ;
baisse de productivité ;
dérive des temps de traitement.

Il génère des alertes contextualisées.

15. Simulation d'événements

Des événements peuvent survenir pendant l'exercice :

campagne marketing imprévue ;
panne informatique ;
crise sanitaire ;
météo extrême ;
grève ;
lancement de produit ;
panne d'un opérateur.

Ces événements modifient instantanément les prévisions.

16. Bibliothèque de scénarios
ID	Scénario	Niveau
WFM-001	Journée normale	1
WFM-002	Hausse de trafic	1
WFM-003	Absentéisme important	2
WFM-004	Erreur de forecast	2
WFM-005	Double campagne marketing	3
WFM-006	Panne généralisée	3
WFM-007	Centre saturé	3
WFM-008	Gestion de crise multi-sites	3
17. Évaluation QA

Critères indicatifs.

Critère	Pondération
Qualité du forecast	20 %
Pertinence du staffing	20 %
Optimisation des plannings	20 %
Gestion Intraday	20 %
Respect des contraintes	10 %
Documentation	10 %
18. KPI pédagogiques

Le moteur mesure :

précision des prévisions ;
équilibre des plannings ;
coût simulé des décisions ;
qualité des arbitrages ;
respect des SLA ;
progression du planificateur.
19. Jeux de données

Le pack fournit :

plusieurs années d'historique synthétique ;
profils d'agents ;
contrats de travail ;
calendriers ;
campagnes commerciales ;
jours fériés ;
historiques d'absentéisme.

Toutes les données sont synthétiques.

20. Architecture interne du WFM Engine
Forecast Engine

↓

Capacity Engine

↓

Staffing Engine

↓

Scheduling Engine

↓

Intraday Engine

↓

Analytics Engine

Chaque sous-moteur peut évoluer indépendamment.

21. Intégration avec les autres moteurs

Le WFM Engine échange avec :

Conversation Engine (volumes réels de contacts) ;
Dispatch Engine (affectation des ressources terrain) ;
QA Engine (besoins de formation identifiés) ;
Learning Platform (planification des formations) ;
CRM Simulator (typologie des flux) ;
Reporting Platform (KPI consolidés).

Cette intégration permet de simuler l'impact d'une décision WFM sur l'ensemble de l'écosystème.

22. Décisions d'architecture (ADR)

Ce volume formalise les principes suivants :

Le WFM Engine est composé de sous-moteurs spécialisés et faiblement couplés.
Les modèles de prévision sont interchangeables.
Les contraintes sociales, contractuelles et réglementaires sont déclaratives.
Les décisions Intraday sont historisées pour permettre des replays et des analyses.
Les KPI opérationnels sont calculés par des composants dédiés, indépendants du LLM.
23. Critères d'acceptation

Le Domain Pack Workforce Management est considéré conforme lorsque :

les prévisions sont reproductibles à partir des mêmes données d'entrée ;
les plannings respectent les contraintes définies ;
les scénarios de crise entraînent des adaptations cohérentes ;
les KPI sont calculés de manière vérifiable ;
les simulations permettent d'expliquer les conséquences de chaque décision.
🏛️ Décision d'architecture majeure : Workforce Intelligence Architecture (WIA)

Je recommande une Workforce Intelligence Architecture (WIA).

Le WFM Engine ne se limite pas à produire un planning. Il maintient une vision dynamique de la capacité opérationnelle du centre de contacts et alimente les autres moteurs de la plateforme avec des informations fiables sur les ressources disponibles, les compétences, les contraintes et les performances.

Cette architecture transforme le simulateur en un véritable Digital Twin d'un centre de contacts, où les décisions prises dans un domaine (formation, planification, qualité, support ou vente) ont des répercussions mesurables sur l'ensemble du système.

📘 Prochaine étape : G10 — Domain Pack Supervision Temps Réel (Real-Time Command Center)

Le prochain volume introduira le Real-Time Operations Engine (RTO Engine), chargé de superviser un centre de contacts minute par minute.

Il couvrira notamment :

supervision des files d'attente en direct ;
suivi des KPI en temps réel ;
détection d'anomalies opérationnelles ;
alertes intelligentes et priorisation ;
pilotage des superviseurs ;
gestion des crises et plans de continuité ;
tableaux de bord temps réel et recommandations d'actions.

Ce volume complétera le WFM en passant de la planification au pilotage opérationnel en temps réel, avec un moteur événementiel conçu pour entraîner les superviseurs à prendre les bonnes décisions sous forte pression.
