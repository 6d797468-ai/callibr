# Volume B03 — AI Runtime Architecture & Prompt Orchestration Engine (POE)

> Extrait généré depuis `Architecture & Engineering Book (AEB).md` le 2026-07-27.

PHASE B — ARCHITECTURE MÉTIER
Volume B3
AI Runtime Architecture & Prompt Orchestration Engine (POE)

Version : 1.0

Statut : Architecture de Référence

Criticité : Très élevée

1. Introduction

Le Prompt Orchestration Engine (POE) est le composant chargé de transformer l'état interne de la simulation en requêtes optimisées vers un ou plusieurs modèles de langage (LLM).

Son objectif n'est pas seulement de générer un prompt, mais de garantir que les réponses du modèle restent cohérentes avec :

le scénario ;
la procédure métier ;
la personnalité du client ;
l'état émotionnel ;
les objectifs pédagogiques ;
les règles de sécurité.

Le POE ne contient aucune règle métier. Il est un moteur de composition de contexte.

2. Position dans l'architecture
                    Simulation Operating Engine
                               │
                               ▼
                     Prompt Orchestration Engine
                               │
        ┌──────────────────────┼──────────────────────┐
        ▼                      ▼                      ▼
  Context Builder       Prompt Compiler        LLM Router
        │                      │                      │
        └──────────────────────┼──────────────────────┘
                               ▼
                       Response Validator
                               │
                               ▼
                     Simulation Operating Engine

Le POE est entièrement piloté par le Simulation Operating Engine.

3. Responsabilités

Le POE est responsable de :

construire le contexte ;
sélectionner les informations pertinentes ;
appliquer les templates de prompts ;
router vers le modèle approprié ;
parser les réponses ;
détecter les violations de rôle ;
mesurer la consommation de tokens ;
gérer le cache ;
appliquer les politiques de sécurité.

Il n'est pas responsable :

des règles métier ;
des transitions de la machine à états ;
des décisions CRM ;
des évaluations QA.
4. Architecture interne
Prompt Orchestration Engine

├── Prompt Compiler
├── Context Builder
├── Memory Manager
├── Prompt Templates
├── Prompt Version Manager
├── Model Registry
├── LLM Router
├── Cache Manager
├── Token Budget Manager
├── Response Validator
├── Output Parser
├── Safety Layer
├── Cost Monitor
└── Telemetry

Chaque composant est remplaçable.

5. Prompt Compiler

Le Prompt Compiler assemble plusieurs fragments.

Entrées :

Persona

+

Scénario

+

Etat courant

+

Historique

+

Variables émotionnelles

+

Objectifs

+

Instructions système

+

Contraintes

Sortie :

Prompt complet

Le prompt est construit à la demande.

Il n'est jamais stocké.

6. Prompt Templates

Les prompts sont versionnés.

Exemple :

Prompt v1.0

↓

Prompt v1.1

↓

Prompt v2.0

Chaque scénario référence une version précise.

Cela permet de rejouer une simulation avec exactement le même comportement.

7. Structure d'un Prompt

Le Prompt Compiler assemble les sections suivantes :

SYSTEM

↓

Platform Policy

↓

Persona

↓

Scenario

↓

Current State

↓

CRM State

↓

Conversation Memory

↓

Available Facts

↓

Response Constraints

L'ordre est fixe.

8. Exemple de composition
System

↓

Tu incarnes uniquement le client.

↓

Persona

↓

Client très impatient.

↓

Scenario

↓

Connexion Internet coupée.

↓

Etat

↓

Patience : 42

↓

CRM

↓

Identité vérifiée

↓

Historique

↓

20 derniers messages

↓

Consignes de réponse

Le modèle ne reçoit jamais d'informations inutiles.

9. Context Builder

Le Context Builder sélectionne les données utiles.

Sources :

état de la simulation ;
conversation récente ;
résumé de l'historique ancien ;
état CRM ;
état émotionnel ;
procédure en cours ;
objectifs restants.

Une politique de priorité est appliquée.

10. Memory Manager

La mémoire est divisée en plusieurs niveaux.

Mémoire immédiate

20 derniers échanges.

Mémoire de travail

Résumé dynamique de la conversation.

Mémoire métier

Etat CRM.

Variables.

Objectifs.

Mémoire scénario

Informations fixes.

Mémoire entreprise

Connaissances importées.

Procédures.

Scripts.

FAQ.

11. Compression du contexte

Lorsque la fenêtre de contexte devient trop grande :

Messages anciens

↓

Résumé

↓

Fusion

↓

Validation

↓

Injection

Le résumé ne remplace jamais :

les variables métier ;
les actions CRM ;
les objectifs.
12. Token Budget Manager

Chaque modèle possède un budget maximal.

Exemple :

Contexte maximum

100 000 tokens

↓

Réservation sortie

2 000

↓

Réservation sécurité

500

↓

Budget disponible

97 500

Le moteur adapte automatiquement la taille du contexte.

13. Model Registry

Tous les modèles sont enregistrés dans un registre.

Chaque entrée décrit :

fournisseur ;
version ;
coût ;
latence cible ;
capacité de contexte ;
langues ;
disponibilité.

Le reste du système ne dépend jamais d'un fournisseur spécifique.

14. LLM Router

Le routeur sélectionne le modèle en fonction de la tâche.

Exemples :

Tâche	Type de modèle
Simulation client	Conversation
Evaluation QA	Raisonnement
Résumé	Compression
Traduction	Multilingue
Génération de scénario	Créativité

Cette décision est pilotée par une politique configurable.

15. Cache Manager

Certaines réponses peuvent être réutilisées.

Exemples :

résumés ;
prompts compilés ;
procédures ;
FAQ.

Le cache est invalidé dès qu'une variable métier change.

16. Response Validator

Toutes les réponses passent par un pipeline de validation.

Réponse

↓

JSON valide ?

↓

Respect du rôle ?

↓

Respect du scénario ?

↓

Respect des contraintes ?

↓

Acceptée

Sinon :

Nouvelle génération

ou

Fallback
17. Output Parser

Le LLM renvoie une structure normalisée.

Exemple conceptuel :

message

emotion_delta

confidence

optional_metadata

Le parser valide les champs et rejette les réponses incomplètes ou incohérentes.

18. Safety Layer

La Safety Layer vérifie notamment :

divulgation du prompt ;
sortie de rôle ;
langage inapproprié ;
hallucination sur l'état CRM ;
tentative de modifier les règles métier.
19. Coût

Chaque appel est tracé.

Métriques :

fournisseur ;
modèle ;
nombre de tokens ;
coût estimé ;
latence ;
taux de succès.

Ces informations alimentent les tableaux de bord FinOps.

20. Observabilité

Chaque génération produit un enregistrement.

Exemple :

Prompt ID

Session ID

Scenario ID

Model

Version Prompt

Prompt Tokens

Completion Tokens

Latency

Cache Hit

Validation Result

Les contenus sensibles peuvent être masqués selon la politique de confidentialité.

21. Gestion des erreurs

Le POE prévoit plusieurs stratégies :

nouvelle tentative avec le même modèle ;
bascule vers un modèle secondaire ;
réduction du contexte ;
utilisation d'un prompt simplifié ;
arrêt contrôlé de la simulation avec journalisation de l'incident.
22. Versionnement

Trois éléments sont versionnés indépendamment :

les templates de prompts ;
les politiques de routage ;
les modèles LLM.

Une simulation historique peut ainsi être rejouée avec les mêmes paramètres si les dépendances sont toujours disponibles.

23. Décisions d'architecture (ADR)

Ce volume fixe plusieurs décisions importantes :

Le Prompt Compiler est stateless.
Le contexte est construit à chaque requête.
Les prompts sont versionnés.
Le LLM ne reçoit jamais directement la base de données.
Le LLM ne calcule jamais les règles métier.
Le LLM ne modifie jamais directement l'état de la simulation.
Les sorties du LLM sont toujours validées avant d'être utilisées.
24. Critères d'acceptation

Le Prompt Orchestration Engine sera considéré conforme lorsque :

il supporte plusieurs fournisseurs de modèles ;
il compile un prompt de manière déterministe à partir d'un état donné ;
il gère automatiquement le budget de contexte ;
il valide toutes les réponses avant leur utilisation ;
il expose des métriques complètes de coût, de latence et de qualité ;
il permet de rejouer une simulation avec la même version de prompt et les mêmes politiques de routage.
Prochaine étape

Nous respecterons le plan initial.

Le Volume B4 portera sur le Customer Persona Engine & Emotion Engine, qui définira de manière détaillée :

le modèle psychologique des personas ;
les profils comportementaux ;
la matrice émotionnelle ;
la jauge de patience ;
les déclencheurs émotionnels ;
les règles d'évolution des émotions ;
les interactions entre émotions, procédures et réponses du LLM.

C'est ce document qui donnera au client simulé un comportement crédible, cohérent et reproductible, indépendamment du modèle de langage utilisé.
