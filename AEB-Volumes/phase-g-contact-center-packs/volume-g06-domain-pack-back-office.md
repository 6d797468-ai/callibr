# Volume G06 — Domain Pack — Back Office

> Extrait généré depuis `Architecture & Engineering Book (AEB).md` le 2026-07-27.

PHASE G — CONTACT CENTER BUSINESS PACKS
Volume G6
Domain Pack — Back Office

Version : 1.0

Statut : Référence métier

Criticité : Critique

1. Vision

Le Domain Pack Back Office simule le travail d'un gestionnaire de dossiers.

Contrairement aux autres packs :

peu ou pas de conversation client ;
forte utilisation des applications métiers ;
nombreuses règles de validation ;
traitement documentaire ;
gestion des priorités.

Le moteur IA agit principalement comme :

superviseur métier ;
générateur de dossiers ;
contrôleur qualité ;
collègue virtuel.
2. Objectifs pédagogiques

L'apprenant doit savoir :

analyser un dossier ;
vérifier les justificatifs ;
appliquer une procédure ;
prendre une décision ;
documenter le traitement ;
respecter les SLA ;
transmettre au bon service.
3. Workflow global
Réception

↓

Qualification

↓

Contrôle documentaire

↓

Vérifications

↓

Décision

↓

Validation

↓

Exécution

↓

Archivage

↓

Clôture
4. Workflow Engine

Nouveau moteur métier.

Il gère :

les files de traitement ;
les états des dossiers ;
les transitions autorisées ;
les règles métier ;
les SLA ;
les affectations.

Le LLM explique.

Le Workflow Engine décide.

5. Cycle de vie d'un dossier
Nouveau

↓

En attente

↓

En cours

↓

Informations manquantes

↓

Validation

↓

Traité

↓

Archivé

Les transitions sont déclaratives.

6. Files de travail

Le moteur gère plusieurs queues.

Exemple.

Priority

Standard

Fraud

Claims

Refunds

Contracts

Documents

Chaque file possède :

priorité ;
SLA ;
compétences requises ;
règles d'affectation.
7. Types de dossiers

Le pack peut couvrir.

Contrat
création
modification
résiliation
Réclamation
analyse
remboursement
correction
Documents
contrôle
validation
rejet
Facturation
correction
avoir
annulation
Fraude
suspicion
blocage
enquête
8. Modèle documentaire

Chaque dossier possède.

Métadonnées
identifiant
propriétaire
date
statut
Documents
pièce d'identité
contrat
facture
justificatif
Historique
actions
décisions
commentaires
9. Workflow déclaratif

Exemple.

workflow:

create_refund

states:

- received

- verification

- validation

- payment

- closed

transitions:

received:

- verification

verification:

- validation

validation:

- payment

payment:

- closed
10. Règles métier

Les règles sont déclaratives.

Exemple.

rules:

refund:

max_amount: 300

mandatory_documents:

- invoice

- identity

Aucune règle n'est codée en dur.

11. Validation documentaire

Le moteur vérifie :

✓ présence

✓ cohérence

✓ validité

✓ lisibilité

✓ dates

✓ signatures

Le LLM peut expliquer les anomalies.

12. Contrôles

Exemple.

Pièce expirée

↓

Refus

Adresse différente

↓

Vérification

Signature absente

↓

Rejet

Tous les contrôles sont versionnés.

13. CRM Back Office

Le CRM contient.

Client
informations
Contrat
historique
Paiements
opérations
Documents
versions
Tickets
suivi
14. Actions

L'agent peut.

accepter
refuser
demander des documents
transférer
fusionner
annuler
suspendre
rouvrir

Toutes les actions sont historisées.

15. SLA Engine

Le Workflow Engine suit.

temps de traitement
retard
urgence
priorité
date limite

Exemple.

Réception

↓

2 heures

↓

Traitement

↓

24 heures

↓

Validation
16. Priorisation

Le moteur calcule automatiquement.

Priorité élevée :

fraude
VIP
délai critique

Priorité normale :

standard

Priorité faible :

demandes planifiées
17. Collaboration

Simulation de plusieurs rôles.

Front Office
Back Office
Superviseur
Validation
Expert

Les dossiers changent d'équipe.

18. Bibliothèque de scénarios
ID	Scénario	Niveau
BO-001	Validation documentaire	1
BO-002	Création contrat	1
BO-003	Remboursement	2
BO-004	Contrôle conformité	2
BO-005	Suspicion fraude	3
BO-006	Dossier incomplet	3
BO-007	Multi-validations	3
BO-008	SLA dépassé	3
19. QA

Critères.

Critère	Pondération
Analyse	20 %
Respect procédure	25 %
Exactitude	20 %
Documentation	15 %
Gestion SLA	10 %
Décision	10 %
20. KPI

Le moteur calcule.

dossiers traités
temps moyen
erreurs
rejets
reprises
qualité documentaire
respect SLA
21. Jeux de données

Le pack fournit.

contrats
documents
justificatifs
dossiers
historiques
décisions
utilisateurs

Toutes les données sont synthétiques.

22. Workflow Templates

Le pack contient des workflows prêts à l'emploi.

remboursement
résiliation
ouverture compte
changement adresse
changement RIB
déclaration sinistre
renouvellement contrat

Les templates sont réutilisables.

23. Escalade

Le moteur détermine.

Agent

↓

Expert

↓

Superviseur

↓

Direction

Les règles d'escalade sont configurables.

24. Audit

Chaque décision génère.

date
utilisateur
justification
documents
règles appliquées

Le journal est immuable.

25. Décisions d'architecture (ADR)

Ce volume formalise les principes suivants :

Le Workflow Engine pilote l'ensemble des transitions de dossiers.
Les règles métier sont déclaratives et versionnées.
Les SLA sont évalués indépendamment du LLM.
Les contrôles documentaires sont configurables.
Les décisions sont entièrement auditables.
26. Critères d'acceptation

Le Domain Pack Back Office est considéré conforme lorsque :

les workflows couvrent les principaux processus ciblés ;
les règles métier sont appliquées automatiquement ;
les transitions de dossiers sont cohérentes ;
les SLA sont correctement calculés ;
les audits permettent de reconstituer l'historique complet d'un traitement.
🏛️ Décision d'architecture majeure : Workflow-Driven Processing Architecture (WDPA)

Je recommande une Workflow-Driven Processing Architecture.

Le Back Office ne doit pas être modélisé comme une suite de conversations, mais comme un moteur de traitement de dossiers piloté par des workflows déclaratifs. Le LLM joue un rôle d'assistance (explication, synthèse, génération de commentaires), tandis que le Workflow Engine garantit la conformité, le respect des transitions et la traçabilité.

Cette architecture rend le moteur réutilisable dans des secteurs variés : banque, assurance, administration, santé, logistique ou e-commerce.

📘 Prochaine étape : G7 — Domain Pack Conduite d'Activité (Real-Time Operations & Dispatch)

Le prochain volume introduira un changement de paradigme : l'apprenant ne gérera plus un seul client ou un seul dossier, mais une activité en temps réel.

Nous y définirons un Operations Engine, chargé de simuler :

les files d'attente en temps réel ;
le pilotage des ressources ;
la planification et la réaffectation des agents ;
les alertes SLA ;
les incidents opérationnels ;
la supervision des flux omnicanaux (voix, chat, e-mail, tickets) ;
les tableaux de bord temps réel ;
les décisions de priorisation et d'escalade.

Ce moteur permettra de former des superviseurs, des planificateurs et des responsables de conduite d'activité, ouvrant ATOS à un public plus large que les seuls conseillers de centre de contacts.
