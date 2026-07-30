# Volume G13 — Domain Pack — Incident & Problem Management

> Extrait généré depuis `Architecture & Engineering Book (AEB).md` le 2026-07-27.

PHASE G — CONTACT CENTER BUSINESS PACKS
Volume G13
Domain Pack — Incident & Problem Management

Version : 1.0

Statut : Enterprise Core

Criticité : Très élevée

1. Vision

Le Domain Pack Incident & Problem Management entraîne les équipes à gérer des incidents opérationnels tout en développant une démarche d'amélioration continue.

Il couvre :

Incident Management ;
Major Incident Management ;
Problem Management ;
Root Cause Analysis (RCA) ;
Known Error Database (KEDB) ;
Post-Incident Review (PIR).

L'objectif est d'apprendre à restaurer le service rapidement, puis à prévenir les récurrences.

2. Objectifs pédagogiques

À la fin de la formation, l'apprenant doit être capable de :

qualifier un incident ;
distinguer Incident, Problem et Known Error ;
coordonner plusieurs équipes ;
conduire une analyse des causes racines ;
produire un rapport post-incident ;
proposer des actions préventives.
3. Architecture fonctionnelle
Alert / Ticket

↓

Incident Engine

↓

Major Incident Engine

↓

Problem Engine

↓

RCA Engine

↓

Known Error Engine

↓

Continuous Improvement Engine

Chaque moteur possède un rôle clairement défini.

4. Incident Engine

Le moteur gère :

les incidents ;
leur cycle de vie ;
les priorités ;
les SLA ;
les communications.

Son objectif principal est de restaurer le service.

5. Problem Engine

Le Problem Engine intervient lorsque :

plusieurs incidents similaires apparaissent ;
un incident majeur est clôturé ;
une cause profonde reste inconnue.

Le problème devient un objet métier indépendant.

6. Workflow Incident
Détection

↓

Qualification

↓

Priorisation

↓

Diagnostic

↓

Contournement

↓

Résolution

↓

Validation

↓

Clôture
7. Workflow Problem
Création

↓

Analyse

↓

Recherche RCA

↓

Known Error

↓

Correction permanente

↓

Validation

↓

Clôture

Les deux workflows restent indépendants mais liés.

8. Major Incident Management

Le moteur permet de simuler :

cellule de crise ;
coordination multi-équipes ;
communications internes ;
communications clients ;
décisions de priorisation.

Le chronomètre devient un facteur pédagogique.

9. RCA Engine

Le moteur supporte plusieurs méthodes :

5 Why ;
Ishikawa ;
Fault Tree Analysis ;
Timeline Analysis.

L'apprenant choisit la méthode la plus adaptée au scénario.

10. Known Error Database

Le système maintient une base de connaissances contenant :

symptômes ;
causes connues ;
contournements ;
correctifs permanents.

Les futurs scénarios peuvent exploiter cette base.

11. Actions disponibles

L'apprenant peut :

créer un incident ;
déclarer un problème ;
lancer une cellule de crise ;
consulter la KEDB ;
documenter une RCA ;
proposer un plan d'action ;
clôturer le problème.

Toutes les actions sont historisées.

12. Communication de crise

Le moteur simule les échanges avec :

les utilisateurs ;
les responsables métiers ;
les équipes techniques ;
la direction.

Les messages doivent être adaptés au public visé.

13. Bibliothèque de scénarios
ID	Scénario	Niveau
IPM-001	Incident applicatif isolé	1
IPM-002	Incidents récurrents	2
IPM-003	Incident majeur	2
IPM-004	Dégradation progressive	3
IPM-005	Défaillance multi-services	3
IPM-006	RCA complexe	3
IPM-007	Crise inter-équipes	3
IPM-008	Amélioration continue	3
14. KPI métier

Le moteur calcule notamment :

MTTR (Mean Time To Restore) ;
MTTD (Mean Time To Detect) ;
nombre d'incidents récurrents ;
délai moyen d'ouverture d'un Problem ;
temps d'analyse RCA ;
taux de récurrence après correction.
15. Évaluation QA

Critères indicatifs.

Critère	Pondération
Qualification	15 %
Gestion de crise	20 %
Analyse des causes	20 %
Documentation	15 %
Plan d'amélioration	20 %
Communication	10 %
16. Jeux de données

Le pack fournit :

incidents synthétiques ;
journaux d'événements ;
dépendances de services ;
chronologies d'incidents ;
exemples de RCA ;
base Known Error.

Toutes les données sont artificielles.

17. Architecture interne
Incident Engine

↓

Problem Engine

↓

RCA Engine

↓

Known Error Engine

↓

Improvement Engine

↓

Analytics

Chaque moteur peut évoluer indépendamment.

18. Intégration avec les autres moteurs

Le Domain Pack échange avec :

Help Desk ITIL Engine pour les tickets ;
RTO Engine pour les événements temps réel ;
Observability Platform pour les alertes simulées ;
QA Engine pour l'évaluation des décisions ;
Learning Platform pour la remédiation pédagogique.
19. Décisions d'architecture (ADR)

Ce volume formalise les principes suivants :

Les Incidents et les Problems sont des objets métier distincts.
Les analyses RCA sont versionnées et auditables.
Les Known Errors sont réutilisables dans de futurs scénarios.
Les communications de crise sont évaluées indépendamment de la résolution technique.
Les améliorations permanentes sont suivies comme des actions distinctes.
20. Critères d'acceptation

Le Domain Pack Incident & Problem Management est considéré conforme lorsque :

les workflows Incident et Problem restent indépendants mais liés ;
les RCA sont documentées et traçables ;
les scénarios permettent de distinguer correction temporaire et correction permanente ;
les KPI sont cohérents avec les événements simulés ;
les recommandations d'amélioration sont exploitables.
🏛️ Décision d'architecture majeure : Continuous Service Improvement Simulation Architecture (CSISA)

Je recommande une Continuous Service Improvement Simulation Architecture (CSISA).

Le moteur ne s'arrête pas à la résolution d'un incident. Il modélise l'ensemble du cycle d'amélioration continue : détection, restauration, analyse des causes, capitalisation des connaissances et prévention. Cette approche rapproche la plateforme des pratiques ITIL et SRE modernes, tout en restant générique et applicable à d'autres domaines (industrie, télécommunications, santé, cloud, etc.).

📘 État d'avancement

Après ce volume :

✅ G1 à G13 terminés (13 Domain Packs sur 20).
📘 Il reste 7 volumes pour achever la Phase G :
G14 — Banking Contact Center
G15 — Insurance Contact Center
G16 — Healthcare Contact Center
G17 — E-commerce & Retail
G18 — Public Services & Administration
G19 — Collections avancées & Contentieux
G20 — Omnichannel & Digital Engagement

Une fois ces sept volumes terminés, nous entrerons dans la Phase H — AI Platform Enterprise, qui constituera le socle d'orchestration de tous les moteurs IA de la plateforme (LLM Gateway, Agent Runtime, Prompt Compiler, Tool Calling, AI Safety, Model Registry, etc.). Cette phase fera évoluer l'architecture d'un simulateur métier vers une véritable plateforme d'intelligence artificielle d'entreprise.
