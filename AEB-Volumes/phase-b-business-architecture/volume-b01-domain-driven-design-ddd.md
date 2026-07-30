# Volume B01 — Domain Driven Design (DDD)

> Extrait généré depuis `Architecture & Engineering Book (AEB).md` le 2026-07-27.

PHASE B — ARCHITECTURE MÉTIER
Volume B1
Domain Driven Design (DDD)

Version : 1.0

Statut : Architecture de Référence

1. Pourquoi utiliser le Domain Driven Design ?

Le projet n'est pas un simple logiciel.

Il est constitué de plusieurs métiers différents :

Centre de contacts
CRM
IA
Formation
Evaluation QA
Reporting
Administration
Authentification
Facturation SaaS

Si tout est développé dans un seul "backend", celui-ci deviendra rapidement un monolithe difficile à maintenir.

Nous allons donc découper le système en Bounded Contexts.

2. Vision Globale
                     ACS PLATFORM

                     Enterprise

                           │

 ┌───────────────────────────────────────────────────────┐
 │                                                       │
 │                 Training Domain                       │
 │                                                       │
 └───────────────────────────────────────────────────────┘

 ┌───────────────────────────────────────────────────────┐
 │                 Simulation Domain                     │
 └───────────────────────────────────────────────────────┘

 ┌───────────────────────────────────────────────────────┐
 │                    AI Domain                          │
 └───────────────────────────────────────────────────────┘

 ┌───────────────────────────────────────────────────────┐
 │                  CRM Domain                           │
 └───────────────────────────────────────────────────────┘

 ┌───────────────────────────────────────────────────────┐
 │               Evaluation Domain                       │
 └───────────────────────────────────────────────────────┘

 ┌───────────────────────────────────────────────────────┐
 │                 Analytics Domain                      │
 └───────────────────────────────────────────────────────┘

 ┌───────────────────────────────────────────────────────┐
 │             Administration Domain                     │
 └───────────────────────────────────────────────────────┘

Chaque domaine possède :

son modèle
ses services
ses événements
ses règles métier
3. Les Bounded Contexts
3.1 Identity Domain

Responsabilité :

Gestion des utilisateurs.

Contient :

organisations
utilisateurs
rôles
permissions
authentification
SSO
MFA

Aucun autre domaine ne connaît les détails d'authentification.

3.2 Training Domain

Responsabilité :

Tout ce qui concerne les formations.

Contient :

parcours
modules
certifications
progression
historique
objectifs

Il ne connaît rien du LLM.

3.3 Scenario Domain

Responsabilité :

Gestion des scénarios.

Contient :

scénarios
versions
variantes
difficultés
langues
secteurs
procédures

Exemple :

Support Technique

↓

Connexion Internet

↓

Niveau 1

↓

Client Furieux
3.4 Persona Domain

Responsabilité :

Les profils psychologiques.

Exemple

Patient

Agressif

Confus

Très bavard

Ironique

Passif

Anxieux

Méfiant

Expert

Débutant

Une persona est totalement indépendante d'un scénario.

3.5 Simulation Domain

C'est le cœur de la plateforme.

Il orchestre :

conversation
état
événements
progression
CRM
IA

Ce domaine est déterministe.

Le LLM ne décide jamais.

3.6 Conversation Domain

Responsabilité :

Stocker la conversation.

Contient

messages

timestamps

speaker

metadata

confidence

tokens

latence

Aucune logique métier.

3.7 CRM Domain

Responsabilité

Simulation du CRM.

Contient

clients

contrats

factures

tickets

historique

produits

commandes

Le CRM est simulé.

Aucune donnée réelle.

3.8 Procedure Domain

Très important.

Il contient uniquement les règles métier.

Exemple :

Support Internet

Accueil

↓

Identification

↓

Diagnostic

↓

Test Box

↓

Escalade

↓

Conclusion

Toutes les entreprises pourront créer leurs propres procédures.

3.9 Rule Engine Domain

Ne contient AUCUN prompt.

Seulement des règles.

Exemple

SI

identité non vérifiée

ALORS

diagnostic interdit

ou

SI

ticket créé

ET

client informé

ALORS

objectif atteint
3.10 AI Domain

Responsabilité

Toute l'IA.

Sous-domaines :

Prompt Compiler

↓

Context Builder

↓

Memory Builder

↓

LLM Router

↓

Response Validator

↓

Guardrails

↓

Output Parser

Ce domaine ne contient aucune règle métier.

3.11 Evaluation Domain

Responsabilité

Calculer :

score QA
conformité
empathie
écoute active
résolution

Il peut utiliser un LLM.

Mais le calcul final est hybride.

LLM

règles

métriques.

3.12 Coaching Domain

Produit les recommandations.

Exemple

Tu interromps souvent le client.

↓

Exercice conseillé

↓

Gestion des objections.
3.13 Analytics Domain

Responsabilité

Toutes les statistiques.

Exemple

Temps moyen

Score moyen

Progression

Erreurs fréquentes

Top scénarios

Top difficultés
3.14 Notification Domain

Emails

SMS

Push

Webhook

Slack

Teams

3.15 Billing Domain

Gestion SaaS.

Plans

Facturation

Abonnements

Licences

Consommation IA

Quota

4. Agrégats (Aggregates)

Voici les principaux agrégats du domaine :

Organization
│
├── Users
├── Licenses
└── Settings
Scenario
│
├── Persona
├── Procedure
├── Objectives
├── Difficulty
└── CRM Template
SimulationSession
│
├── Conversation
├── CRM State
├── Emotion State
├── Evaluation
└── Metrics
Evaluation
│
├── QA Scores
├── Violations
├── Strengths
└── Improvements
5. Value Objects

Quelques exemples.

EmotionState

patience

stress

confidence

anger
CRMAction

action

timestamp

success

duration
QA Score

Empathy

Listening

Procedure

Resolution

Closing
6. Domain Events

Tous les domaines communiquent via des événements.

Jamais par appels directs lorsque ce n'est pas nécessaire.

Exemples.

SimulationStarted
ConversationMessageReceived
IdentityVerified
TicketCreated
ProcedureCompleted
CustomerEmotionChanged
SimulationFinished
EvaluationCompleted
ReportGenerated
7. Pourquoi cette architecture est importante

L'un des risques majeurs des applications basées sur les LLM est de placer toute la logique dans les prompts. Cette approche devient rapidement difficile à tester, à expliquer et à maintenir.

Dans cette plateforme :

le domaine métier définit les règles ;
le moteur de simulation orchestre les états ;
le Rule Engine applique les contraintes ;
le CRM Simulator gère les actions métier ;
le LLM joue uniquement le rôle du client ou de l'évaluateur selon le contexte.

Cette séparation garantit un comportement reproductible et facilite les tests automatisés.

Ce que couvrira le Volume B2

Le prochain volume sera consacré au Simulation Engine, qui est le composant central de la plateforme. Il détaillera notamment :

l'architecture interne du moteur de simulation ;
la machine à états complète ;
le cycle de vie d'une session ;
le moteur d'émotions ;
la jauge de patience ;
le moteur d'objectifs ;
les événements internes ;
les interactions avec le CRM simulé ;
les contrats avec le Prompt Compiler et le LLM.

À partir de ce volume, nous commencerons à définir les interfaces et les contrats techniques qui serviront directement de base au développement du backend Python.
