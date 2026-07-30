# Volume G18 — Domain Pack — Public Services & Administration

> Extrait généré depuis `Architecture & Engineering Book (AEB).md` le 2026-07-27.

PHASE G — CONTACT CENTER BUSINESS PACKS
Volume G18
Domain Pack — Public Services & Administration

Version : 1.0

Statut : Enterprise Vertical

Criticité : Élevée

1. Vision

Le Domain Pack Public Services simule les interactions entre un citoyen et un service administratif.

Il couvre :

demandes d'information ;
démarches administratives ;
dépôt de dossiers ;
suivi de demandes ;
renouvellements ;
réclamations ;
orientation vers les services compétents ;
assistance numérique.

L'objectif est de former les agents à appliquer les procédures administratives tout en offrant une relation usager de qualité.

2. Objectifs pédagogiques

À la fin de la formation, l'agent doit être capable de :

identifier correctement l'usager ;
qualifier la demande ;
orienter vers la bonne procédure ;
vérifier la complétude d'un dossier ;
expliquer les étapes administratives ;
respecter les obligations réglementaires ;
documenter les échanges.
3. Architecture fonctionnelle
Citizen

↓

Identity Engine

↓

Case Management Engine

↓

Eligibility Engine

↓

Document Engine

↓

Workflow Engine

↓

Notification Engine

↓

QA Engine
4. Citizen Identity Engine

Le moteur gère :

identité simulée ;
coordonnées ;
historique des démarches ;
représentants légaux ;
préférences de communication.

Toutes les données sont fictives.

5. Case Management Engine

Chaque demande devient un Case.

Cycle de vie :

Création

↓

Qualification

↓

Instruction

↓

Compléments demandés

↓

Décision

↓

Notification

↓

Archivage

Le dossier est l'objet métier principal.

6. Eligibility Engine

Le moteur vérifie automatiquement :

critères d'éligibilité ;
conditions réglementaires ;
pièces obligatoires ;
délais ;
statut administratif.

Les règles sont déclaratives et versionnées.

7. Document Engine

Le moteur gère des documents simulés :

formulaires ;
justificatifs ;
attestations ;
certificats ;
pièces d'identité fictives ;
courriers administratifs.

Le moteur contrôle leur présence et leur validité dans le cadre du scénario.

8. Workflow Engine

Chaque démarche possède un workflow configurable.

Exemple :

Demande

↓

Vérification

↓

Instruction

↓

Validation

↓

Décision

↓

Archivage

Le Workflow Engine est partagé avec les autres Domain Packs.

9. Notification Engine

Le système simule :

courriers ;
e-mails ;
SMS ;
notifications portail ;
rappels de pièces manquantes.

Toutes les notifications sont fictives.

10. Actions disponibles

L'agent peut :

créer un dossier ;
rechercher un dossier ;
demander des pièces complémentaires ;
vérifier l'éligibilité ;
transmettre au service compétent ;
notifier une décision ;
clôturer le dossier.

Toutes les actions sont historisées.

11. Gestion émotionnelle

Le Persona Engine peut simuler :

usager inquiet ;
personne âgée ;
étudiant ;
entrepreneur ;
citoyen en colère ;
personne en difficulté numérique.

L'évolution émotionnelle dépend de la qualité de l'accompagnement.

12. Bibliothèque de scénarios
ID	Scénario	Niveau
GOV-001	Demande d'information	1
GOV-002	Dépôt d'un dossier	1
GOV-003	Pièces manquantes	2
GOV-004	Refus administratif	2
GOV-005	Situation complexe multi-services	3
GOV-006	Contestation d'une décision	3
GOV-007	Accompagnement d'un usager vulnérable	3
GOV-008	Gestion d'un afflux massif de demandes	3
13. KPI métier

Le moteur calcule notamment :

délai moyen de traitement ;
taux de dossiers complets ;
qualité de l'orientation ;
respect des procédures ;
satisfaction simulée des usagers ;
taux de réouverture des dossiers.
14. Évaluation QA
Critère	Pondération
Vérification d'identité	10 %
Qualification de la demande	20 %
Respect de la procédure	25 %
Qualité de l'explication	20 %
Documentation	15 %
Communication	10 %
15. Jeux de données

Le pack comprend :

usagers fictifs ;
dossiers administratifs ;
formulaires ;
justificatifs synthétiques ;
procédures ;
décisions simulées.

Toutes les données sont générées artificiellement.

16. Architecture interne
Identity Engine

↓

Case Engine

↓

Eligibility Engine

↓

Document Engine

↓

Workflow Engine

↓

Notification Engine

↓

Analytics

Les composants sont découplés et réutilisables.

17. Intégration avec les autres moteurs

Le Domain Pack Public Services échange avec :

Conversation Engine pour les échanges avec les usagers ;
Workflow Engine pour les processus administratifs ;
Document Engine partagé ;
QA Engine pour l'évaluation ;
Learning Platform pour les parcours de formation ;
Reporting Platform pour les tableaux de bord.

Cette mutualisation réduit la duplication des composants.

18. Décisions d'architecture (ADR)

Ce volume formalise les principes suivants :

Le dossier administratif est l'objet métier central.
Les règles d'éligibilité sont déclaratives et versionnées.
Les décisions administratives sont prises par des moteurs déterministes, jamais directement par le LLM.
Les documents sont gérés indépendamment du moteur conversationnel.
Toutes les actions sont traçables et auditables.
19. Critères d'acceptation

Le Domain Pack Public Services est considéré conforme lorsque :

les workflows administratifs sont respectés ;
les règles d'éligibilité sont appliquées de manière cohérente ;
les scénarios couvrent des démarches variées ;
les évaluations distinguent les compétences procédurales et relationnelles ;
les journaux d'audit permettent de reconstituer intégralement un dossier.
20. Décision d'architecture majeure : Government Digital Service Architecture (GDSA)

Je recommande une Government Digital Service Architecture (GDSA).

Le moteur repose sur un Case Management Engine générique, capable de représenter toute démarche administrative sous la forme d'un dossier piloté par un workflow déterministe. Le LLM intervient uniquement pour accompagner l'usager, expliquer les démarches et adapter son langage, sans jamais prendre de décision réglementaire.

Cette architecture rend le Domain Pack facilement adaptable à différents pays, organismes et réglementations grâce à des règles déclaratives et des workflows configurables.

📘 État d'avancement

Après ce volume :

✅ G1 à G18 terminés (18 Domain Packs sur 20).
📘 Il reste 2 volumes pour achever la Phase G :
G19 — Collections avancées & Contentieux
G20 — Omnichannel & Digital Engagement

Une fois ces deux derniers volumes terminés, la Phase G sera entièrement achevée. Nous basculerons ensuite vers la Phase H — AI Platform Enterprise, qui définira l'architecture technique complète de la plateforme IA : Agent Runtime, Prompt Compiler, LLM Gateway, orchestration multi-agents, mémoire, sécurité, observabilité et gouvernance. Cette phase constituera le socle technique commun à tous les moteurs métier développés dans les phases précédentes.
