# Volume G07 — Domain Pack — Conduite d'Activité & Dispatch

> Extrait généré depuis `Architecture & Engineering Book (AEB).md` le 2026-07-27.

PHASE G — CONTACT CENTER BUSINESS PACKS
Volume G7
Domain Pack — Conduite d'Activité & Dispatch

Version : 1.0

Statut : Référence métier

Criticité : Critique

1. Vision

Le Domain Pack Conduite d'Activité simule le fonctionnement d'un centre de pilotage opérationnel.

Le stagiaire apprend à :

gérer une file d'interventions ;
prioriser les incidents ;
affecter les ressources ;
respecter les SLA ;
gérer les imprévus ;
optimiser la charge de travail.

L'objectif est de prendre des décisions cohérentes dans un environnement dynamique.

2. Objectifs pédagogiques

À la fin de la formation, le coordinateur doit être capable de :

analyser une situation opérationnelle ;
identifier les priorités ;
affecter la bonne ressource ;
réorganiser un planning ;
gérer plusieurs événements simultanément ;
maintenir les engagements de service.
3. Workflow global
Réception des demandes

↓

Qualification

↓

Priorisation

↓

Recherche des ressources

↓

Affectation

↓

Suivi

↓

Réaffectation

↓

Clôture
4. Dispatch Engine

Le Dispatch Engine maintient en permanence :

les interventions ouvertes ;
les techniciens disponibles ;
les compétences ;
la localisation ;
les SLA ;
les urgences ;
les capacités restantes.

Chaque décision met à jour l'état global du système.

5. États d'une intervention
Nouvelle

↓

Qualifiée

↓

Planifiée

↓

En cours

↓

Suspendue

↓

Terminée

ou

Annulée

Chaque transition est historisée.

6. Types d'interventions

Le moteur supporte notamment :

panne Internet ;
installation ;
maintenance préventive ;
remplacement d'équipement ;
expertise technique ;
intervention urgente ;
visite planifiée.

Chaque type possède :

une durée estimée ;
des compétences requises ;
un niveau de priorité.
7. Ressources

Chaque technicien possède :

identifiant ;
compétences ;
certifications ;
secteur géographique ;
horaires ;
charge actuelle ;
disponibilité.

Ces informations évoluent en temps réel.

8. Gestion des compétences

Exemple.

technician:

skills:

- fiber

- xdsl

- router

- wifi

certifications:

- level2

Le moteur refuse une affectation incompatible.

9. Priorisation

Le Dispatch Engine calcule un score de priorité.

Critères possibles :

SLA restant ;
criticité ;
impact client ;
ancienneté ;
type d'incident ;
contraintes réglementaires.

Les pondérations sont configurables.

10. SLA Engine

Chaque intervention possède :

délai maximal de prise en charge ;
délai maximal de résolution ;
objectif de ponctualité ;
pénalités simulées.

Le moteur suit ces indicateurs en continu.

11. Planning

Le planning contient :

créneaux disponibles ;
rendez-vous ;
déplacements ;
temps estimés ;
pauses ;
indisponibilités.

Toute modification est recalculée automatiquement.

12. Carte opérationnelle

Le Domain Pack peut simuler :

plusieurs villes ;
secteurs géographiques ;
distances ;
temps de trajet ;
zones d'intervention.

Ces données permettent d'introduire des contraintes réalistes.

13. Actions disponibles

Le coordinateur peut :

affecter un technicien ;
modifier un planning ;
changer une priorité ;
créer une intervention ;
annuler une mission ;
escalader un incident ;
contacter un superviseur ;
notifier le client.

Chaque action génère un événement.

14. Gestion des événements

Le moteur peut produire des événements en cours de simulation :

panne majeure ;
retard d'un technicien ;
absence ;
embouteillage ;
annulation client ;
nouvelle urgence ;
indisponibilité d'un équipement.

Ces événements obligent l'apprenant à adapter son plan.

15. Files de travail

Le système gère plusieurs files :

urgences ;
aujourd'hui ;
en retard ;
à planifier ;
en attente client ;
escalades.

Les files évoluent dynamiquement.

16. Bibliothèque de scénarios
ID	Scénario	Niveau
DISP-001	Installation standard	1
DISP-002	Technicien absent	1
DISP-003	Deux urgences simultanées	2
DISP-004	Saturation du planning	2
DISP-005	Incident régional	3
DISP-006	Panne majeure	3
DISP-007	Réorganisation complète	3
DISP-008	Gestion de crise	3
17. Évaluation QA

Critères indicatifs.

Critère	Pondération
Priorisation	20 %
Affectation des ressources	20 %
Respect des SLA	20 %
Gestion des imprévus	15 %
Communication	10 %
Documentation	15 %
18. KPI métier

Le pack calcule notamment :

taux de respect des SLA ;
temps moyen d'affectation ;
taux d'utilisation des ressources ;
nombre de réaffectations ;
taux de ponctualité simulé ;
équilibre de charge entre techniciens.
19. Jeux de données

Le pack fournit :

5 000 interventions ;
500 techniciens ;
50 zones géographiques ;
calendriers de disponibilité ;
compétences ;
historiques d'interventions ;
modèles de SLA.

Toutes les données sont synthétiques.

20. Collaboration

Le Dispatch Engine échange avec :

CRM ;
Support Technique ;
SAV ;
Back Office.

Une intervention peut être créée par un appel client, enrichie par le support, validée par le Back Office puis planifiée par la Conduite d'Activité.

21. Décisions d'architecture (ADR)

Ce volume formalise les principes suivants :

Le Dispatch Engine pilote la planification.
Les règles de priorisation sont déclaratives.
Les compétences et disponibilités sont des objets métier.
Les événements temps réel sont injectés par un moteur de simulation.
Les décisions sont entièrement traçables.
22. Critères d'acceptation

Le Domain Pack Conduite d'Activité est considéré conforme lorsque :

les scénarios reproduisent des situations réalistes ;
les SLA sont calculés correctement ;
les affectations respectent les compétences ;
les imprévus entraînent une replanification cohérente ;
les KPI sont calculés de manière reproductible.
🏛️ Décision d'architecture majeure : Real-Time Dispatch Architecture (RTDA)

Je recommande une Real-Time Dispatch Architecture.

Le Dispatch Engine devient un moteur événementiel qui maintient un jumeau numérique (Digital Twin) de l'activité opérationnelle. Les décisions de l'apprenant modifient cet état, tandis que des événements simulés viennent perturber le système en temps réel.

Cette architecture apporte :

une simulation fidèle des centres de pilotage ;
une évaluation objective des arbitrages ;
la possibilité de scénarios multi-équipes et multi-sites ;
une réutilisation du moteur pour la logistique, la maintenance, les interventions terrain et le Field Service Management.
📘 Prochaine étape : G8 — Domain Pack Assurance Qualité (QA) & Coaching

Ce volume marquera une évolution majeure de la plateforme. Au lieu de former un agent, il formera un superviseur ou un coach qualité.

Il introduira un QA & Coaching Engine capable de :

écouter ou relire des conversations simulées ;
appliquer des grilles QA configurables ;
détecter automatiquement les écarts de conformité ;
identifier les compétences à renforcer ;
construire des plans de coaching personnalisés ;
mesurer la progression des agents sur plusieurs sessions ;
générer des tableaux de bord individuels et d'équipe.

Ce moteur fera d'ATOS non seulement une plateforme de simulation, mais aussi une plateforme complète de développement des compétences et de pilotage de la qualité.
