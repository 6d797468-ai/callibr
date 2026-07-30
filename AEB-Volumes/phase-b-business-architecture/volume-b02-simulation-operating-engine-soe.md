# Volume B02 — Simulation Operating Engine (SOE)

> Extrait généré depuis `Architecture & Engineering Book (AEB).md` le 2026-07-27.

PHASE B
Volume B2
Simulation Operating Engine (SOE)

Version : 1.0

Statut : Architecture de Référence

1. Objectif

Le Simulation Operating Engine (SOE) est le cerveau de la plateforme.

Il est responsable de :

piloter une simulation
maintenir l'état métier
faire évoluer le scénario
gérer les émotions
gérer le CRM fictif
communiquer avec le LLM
mesurer les performances
générer les événements

Le SOE est déterministe.

Le LLM n'est jamais le chef d'orchestre.

2. Principe fondamental

Le moteur de simulation est un Operating System spécialisé.

Il possède ses propres processus.

Simulation

↓

Session

↓

Workflow

↓

State Machine

↓

Events

↓

LLM

↓

Evaluation

↓

Analytics

Le LLM est placé au milieu, jamais au sommet.

3. Architecture Interne
Simulation Operating Engine

│

├── Session Manager

├── Scenario Engine

├── Workflow Engine

├── Procedure Engine

├── State Machine

├── Persona Engine

├── Emotion Engine

├── CRM Engine

├── Rule Engine

├── Prompt Compiler

├── Context Builder

├── Event Bus

├── Metrics Collector

├── Evaluation Trigger

└── Report Builder

Chaque composant possède une responsabilité unique.

4. Cycle de Vie d'une Simulation
Création

↓

Chargement

↓

Initialisation

↓

Conversation

↓

Actions CRM

↓

Evaluation Continue

↓

Résolution

↓

Evaluation Finale

↓

Rapport

↓

Archivage

Une session ne saute jamais une étape.

5. Session Manager

Le Session Manager crée une simulation isolée.

Chaque session possède :

SessionID

TenantID

ScenarioID

PersonaID

CurrentState

EmotionState

CRMState

ConversationHistory

Objectives

Metrics

Evaluation

Chaque session est indépendante.

Aucune donnée n'est partagée.

6. Scenario Engine

Responsabilité :

Lire le scénario.

Le scénario est entièrement déclaratif.

Exemple :

Scenario

Nom

Objectif

Contexte

Contraintes

Objectifs

Procédure

Conditions

Variables

Temps maximum

Niveau

Le moteur ne contient aucune logique spécifique au scénario.

7. Workflow Engine

Le Workflow Engine connaît uniquement :

Etape actuelle

↓

Etape suivante

↓

Conditions

↓

Transitions

Exemple

Accueil

↓

Identification

↓

Qualification

↓

Diagnostic

↓

Résolution

↓

Conclusion

Le Workflow Engine ne dialogue jamais avec le LLM.

8. Procedure Engine

Il connaît les procédures.

Par exemple :

Support Technique

Accueil

↓

Vérification Identité

↓

Analyse

↓

Diagnostic

↓

Solution

↓

Validation

↓

Conclusion

Télévente

Accueil

↓

Découverte

↓

Qualification

↓

Argumentaire

↓

Traitement objections

↓

Closing

↓

Vente

Chaque métier possède sa procédure.

9. State Machine

La State Machine est probablement le composant le plus critique.

Elle contient uniquement les états métier.

Exemple

START

↓

GREETING

↓

AUTHENTICATION

↓

UNDERSTANDING

↓

DIAGNOSIS

↓

PROPOSAL

↓

VALIDATION

↓

CLOSING

↓

END

Chaque état définit :

les événements autorisés ;
les actions CRM autorisées ;
les conditions de sortie ;
les erreurs possibles.
10. Machine à États Hiérarchique

La plateforme utilisera une Hierarchical State Machine (HSM).

Exemple

Conversation

│

├── Greeting

├── Discovery

│      │

│      ├── Questions

│      ├── Reformulation

│      └── Validation

├── Resolution

└── Closing

Cette approche permet :

moins de transitions
meilleure lisibilité
réutilisation
11. Event Bus

Tous les composants communiquent uniquement par événements.

Exemple

Agent parle

↓

MessageReceived

↓

Event Bus

↓

Emotion Engine

↓

Rule Engine

↓

Prompt Compiler

Aucun couplage direct.

12. Catalogue des Événements

Quelques événements principaux.

SimulationStarted

MessageReceived

MessageGenerated

CRMActionExecuted

ObjectiveCompleted

EmotionChanged

StateChanged

ProcedureViolation

CustomerSatisfied

CustomerUpset

TicketOpened

TicketClosed

SimulationFinished

EvaluationCompleted

Dans la V1, nous viserons un catalogue d'environ 120 à 180 événements métier, couvrant l'ensemble du cycle de vie d'une simulation.

13. Persona Engine

Le Persona Engine ne génère pas les réponses.

Il maintient le profil psychologique.

Exemple

Nom

Age

Connaissance

Patience

Stress

Colère

Confiance

Politesse

Style

Débit

Niveau technique

Objectif
14. Emotion Engine

Le client possède plusieurs émotions simultanément.

Pas une seule.

Patience

Colère

Stress

Confiance

Anxiété

Satisfaction

Fatigue

Engagement

Chaque émotion varie entre 0 et 100.

Exemple :

Patience

100

↓

83

↓

71

↓

52

↓

26

↓

0
15. Moteur d'Influence

Chaque action influence plusieurs variables.

Exemple

Agent reformule.

Patience

+8

Confiance

+12

Stress

-5

Agent interrompt.

Patience

-15

Stress

+18

Colère

+12

Agent oublie l'identification.

Confiance

-10

Agent résout rapidement.

Satisfaction

+25

Stress

-20

Le LLM ne calcule rien.

Le moteur calcule.

16. Objective Engine

Chaque scénario possède des objectifs.

Exemple :

Identifier

Créer Ticket

Informer Client

Résoudre

Conclure

Chaque objectif possède un état :

Non commencé

↓

En cours

↓

Réussi

↓

Échoué
17. Rule Engine

Le Rule Engine contient uniquement des règles.

Exemple :

SI

Client VIP

ET

Panne >48h

ALORS

Remise possible

ou

SI

Identité non vérifiée

ALORS

Interdire ouverture incident

Les règles sont stockées dans un format déclaratif (par exemple YAML ou JSON) afin d'être versionnées et modifiées sans recompilation.

18. CRM Engine

Le CRM Engine maintient l'état du CRM.

Il expose uniquement des commandes.

VerifyIdentity

CreateTicket

UpdateAddress

ApplyDiscount

CreateComplaint

Escalate

ScheduleCallback

Chaque commande produit un événement.

19. Prompt Compiler

Le Prompt Compiler reçoit :

Scénario

+

Etat

+

CRM

+

Emotion

+

Historique

+

Objectifs

+

Procédure

Il construit ensuite le prompt destiné au LLM.

Le LLM ne voit jamais toute la base.

Seulement ce qui est nécessaire.

20. Context Builder

Le Context Builder sélectionne :

les 20 derniers messages ;
les informations CRM pertinentes ;
l'étape actuelle de la procédure ;
les variables émotionnelles utiles ;
les règles de comportement de la persona.

Il applique ensuite une stratégie de compression lorsque le contexte devient trop volumineux.

21. Response Validator

Après la réponse du LLM.

Le moteur valide.

Réponse

↓

Parser

↓

Validation

↓

Guardrails

↓

Filtrage

↓

Utilisateur

Si le LLM sort du personnage.

Réponse rejetée.

Nouvelle génération.

22. Metrics Collector

Pendant toute la simulation :

Temps de réponse

Nombre interruptions

Empathie détectée

Questions ouvertes

Questions fermées

Silences

Actions CRM

Temps moyen

Objectifs atteints

Toutes ces métriques sont historisées pour alimenter l'évaluation et les tableaux de bord.

23. Pourquoi cette architecture ?

Une erreur courante consiste à déléguer au LLM :

la logique métier ;
la progression du scénario ;
les règles QA ;
les validations CRM.

Cette plateforme adopte l'approche inverse :

le moteur orchestre ;
les règles décident ;
les événements synchronisent ;
le LLM interprète et joue un rôle.

Cette séparation améliore la fiabilité, la reproductibilité et la capacité à tester le système.

24. Ce qui vient ensuite : Volume B3

Le prochain volume sera consacré au Prompt Compiler & AI Runtime, qui décrira en détail :

l'architecture complète des prompts ;
les templates de System Prompt ;
la construction dynamique du contexte ;
le routage entre plusieurs modèles LLM ;
la gestion de la mémoire de conversation ;
les stratégies de réduction des coûts (cache, résumé, sélection de contexte) ;
les garde-fous (guardrails) et la validation des sorties.

Ce volume fera le lien entre l'architecture métier que nous venons de définir et l'implémentation concrète de la couche IA. Il servira directement de référence pour développer le moteur Python de génération de prompts et d'orchestration des modèles.
