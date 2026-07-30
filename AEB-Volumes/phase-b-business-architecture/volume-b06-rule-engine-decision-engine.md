# Volume B06 — Rule Engine & Decision Engine

> Extrait généré depuis `Architecture & Engineering Book (AEB).md` le 2026-07-27.

PHASE B — ARCHITECTURE MÉTIER
Volume B6
Rule Engine & Decision Engine

Version : 1.0

Statut : Architecture de Référence

Criticité : Critique

1. Introduction

Le Rule Engine est probablement le composant le plus stratégique de toute la plateforme.

Une erreur très fréquente dans les applications IA est de demander au LLM :

"Décide si l'agent a respecté la procédure."

ou

"Décide si le client est satisfait."

Nous ne ferons jamais cela.

Le LLM est probabiliste.

Les règles métier doivent être déterministes.

Le Rule Engine est donc le cerveau métier de la plateforme.

2. Philosophie

Notre architecture sépare clairement :

LLM
↓

Compréhension

Langage

Conversation

Créativité

de

Rule Engine
↓

Décisions

Validation

Contraintes

Calculs

Autorisations

Le Rule Engine ne génère jamais de texte.

Le LLM ne prend jamais de décision métier.

3. Position dans l'architecture
Simulation Engine
        │
        ▼
 Rule Engine
        │
 ┌──────┼───────────────┐
 ▼      ▼               ▼
CRM   Evaluation   Workflow
        │
        ▼
Prompt Compiler

Tous les modules peuvent interroger le Rule Engine.

Aucun module ne recode les règles.

4. Responsabilités

Le Rule Engine est responsable de :

valider les préconditions ;
autoriser ou refuser une action ;
calculer les transitions ;
appliquer les procédures ;
calculer les scores déterministes ;
déclencher les événements ;
détecter les violations ;
calculer les droits ;
appliquer les politiques métier.
5. Ce que le Rule Engine ne fait jamais

Il ne :

dialogue pas avec le LLM ;
ne construit pas de prompts ;
ne gère pas les WebSockets ;
ne lit pas directement PostgreSQL ;
ne connaît pas le frontend.

Il travaille uniquement sur un état métier.

6. Architecture
Rule Engine

├── Rule Registry

├── Decision Engine

├── Policy Engine

├── Expression Evaluator

├── Condition Resolver

├── Event Generator

├── Rule Validator

├── Rule Compiler

├── Rule Version Manager

└── Audit Logger
7. Rule Registry

Toutes les règles sont enregistrées.

Exemple

RULE-001

Vérification identité obligatoire
RULE-002

Client VIP autorise remise
RULE-003

Diagnostic interdit avant qualification
8. Types de règles

Notre moteur distinguera plusieurs familles.

Règles métier

Exemple

Impossible
d'ouvrir un incident

sans identité validée
Règles CRM

Exemple

Une remise

uniquement

si contrat actif
Règles QA

Exemple

Accueil absent

↓

Perte

5 points
Règles émotionnelles

Exemple

Agent interrompt

↓

Stress +10
Règles de sécurité

Exemple

Client mineur

↓

Informations limitées
Règles SaaS

Exemple

Quota dépassé

↓

Simulation refusée
9. DSL des règles

Nous n'écrirons pas les règles en Python.

Nous définirons un DSL.

Exemple conceptuel.

id: RULE-001

name: Identity Verification Required

priority: 100

enabled: true

when:

    current_step: Diagnosis

    identity_verified: false

then:

    deny_action: StartDiagnosis

    emit_event: ProcedureViolation

    message: Identity verification required

Toutes les règles suivent la même structure.

10. Priorités

Chaque règle possède une priorité.

1000

Critique

↓

500

Importante

↓

100

Normale

↓

10

Information

Les règles critiques sont évaluées en premier.

11. Groupes de règles

Les règles sont regroupées.

Support Technique

↓

Qualification
Télévente

↓

Closing
Recouvrement

↓

Paiement

Le moteur charge uniquement les groupes nécessaires.

12. Conditions

Les conditions utilisent des expressions simples.

Exemple

AND

OR

NOT

IN

>

<

=

>=

<=

Pas de logique complexe directement dans le DSL.

La lisibilité est prioritaire.

13. Decision Engine

Le Decision Engine exécute les règles.

Pipeline.

Etat actuel

↓

Règles actives

↓

Evaluation

↓

Décision

↓

Evènements
14. Exemple

Etat.

Identité

Non vérifiée

Etape

Diagnostic

Décision.

Diagnostic interdit

↓

Retour

Qualification

Le LLM n'intervient pas.

15. Rule Chaining

Une règle peut déclencher une autre.

Exemple

Ticket créé

↓

Client VIP

↓

Remise autorisée

↓

Notification superviseur

Le moteur évite les boucles infinies grâce à une profondeur maximale configurable.

16. Policy Engine

Les politiques permettent de modifier le comportement selon l'entreprise.

Exemple.

Entreprise A.

Remise maximum

10 %

Entreprise B.

Remise maximum

25 %

Même règle.

Politique différente.

17. Rule Versioning

Toutes les règles sont versionnées.

Procedure

↓

v1

↓

v2

↓

v3

Une ancienne simulation continue d'utiliser la version historique.

18. Validation

Avant publication.

Le moteur vérifie.

identifiants uniques ;
dépendances ;
références valides ;
absence de cycles ;
cohérence des priorités ;
compatibilité avec le DSL.
19. Audit

Chaque décision est enregistrée.

Exemple.

Timestamp

↓

Session

↓

Règle

↓

Résultat

↓

Variables utilisées

↓

Décision

Une entreprise peut expliquer pourquoi une décision a été prise.

20. Explainability

Chaque décision est explicable.

Exemple.

Refus

↓

RULE-003

↓

Identité non vérifiée

L'objectif est qu'un formateur ou un auditeur puisse comprendre immédiatement l'origine d'une décision.

21. Performance

Le Rule Engine doit rester extrêmement rapide.

Objectifs :

Indicateur	Cible
Chargement d'un ensemble de règles	< 10 ms
Évaluation d'une règle simple	< 0,5 ms
Évaluation d'un scénario standard	< 5 ms
Débit cible	> 10 000 évaluations/s par instance

Le Rule Engine ne doit jamais devenir le goulot d'étranglement de la plateforme.

22. Intégration avec les autres moteurs

Le Rule Engine est utilisé par :

Moteur	Utilisation
Simulation Engine	Validation des transitions
Scenario Engine	Vérification des objectifs
CRM Engine	Autorisation des actions
Persona Engine	Déclencheurs comportementaux
Evaluation Engine	Calcul des pénalités et bonus
Analytics Engine	Classification des événements

Ainsi, une règle n'est définie qu'une seule fois.

23. Décisions d'architecture (ADR)

Ce volume fixe plusieurs décisions structurantes :

Toutes les règles métier sont déclaratives.
Les règles sont indépendantes du code Python.
Le moteur de règles est stateless.
Les décisions sont explicables et auditables.
Les règles sont versionnées et rejouables.
Les politiques d'entreprise surchargent les règles sans les modifier.
24. Critères d'acceptation

Le Rule Engine sera considéré conforme lorsque :

une nouvelle règle peut être ajoutée sans modifier le code du moteur ;
les décisions sont identiques pour un même état d'entrée ;
chaque décision est expliquable ;
les règles peuvent être activées, désactivées et versionnées ;
les politiques spécifiques à un tenant sont prises en charge ;
les performances respectent les objectifs définis.
📌 Décision d'architecture majeure (nouvelle)

Après les six premiers volumes, une évolution importante de l'architecture apparaît.

Au lieu de considérer le système comme une simple application SaaS, je recommande de le concevoir comme un Simulation Operating Platform (SOP).

Autrement dit, le produit n'est plus une application avec quelques modules, mais un noyau (Kernel) sur lequel viennent se brancher des moteurs spécialisés :

Simulation Engine
Rule Engine
AI Runtime
CRM Engine
Evaluation Engine
Analytics Engine
Voice Engine (futur)
Marketplace Engine (futur)

Cette approche permettra à terme d'ajouter de nouveaux domaines (banque, assurance, santé, administration, e-commerce, etc.) sans modifier le noyau.

Je proposerai donc, dans la Phase C, une architecture inspirée d'un micro-kernel, avec un Core Kernel stable et des engines modulaires. Cette décision structurante renforcera la maintenabilité, la testabilité et l'évolutivité de la plateforme sur plusieurs années.
