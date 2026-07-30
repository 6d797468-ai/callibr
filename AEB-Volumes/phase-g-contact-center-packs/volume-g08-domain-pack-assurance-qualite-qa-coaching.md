# Volume G08 — Domain Pack — Assurance Qualité (QA) & Coaching

> Extrait généré depuis `Architecture & Engineering Book (AEB).md` le 2026-07-27.

PHASE G — CONTACT CENTER BUSINESS PACKS
Volume G8
Domain Pack — Assurance Qualité (QA) & Coaching

Version : 1.0

Statut : Architecture Core

Criticité : Critique

1. Vision

Le QA & Coaching Engine transforme chaque simulation en opportunité d'apprentissage.

Son objectif n'est pas uniquement de donner une note.

Il doit expliquer :

pourquoi l'agent a obtenu cette note ;
quelles compétences sont acquises ;
lesquelles doivent être développées ;
comment progresser.

Le moteur doit être suffisamment générique pour fonctionner avec tous les métiers :

SAV
Support Technique
Télévente
Rétention
Recouvrement
Back Office
Dispatch
futurs Domain Packs
2. Architecture globale
Simulation

↓

Conversation Engine

↓

Business Engine

↓

QA Engine

↓

Competency Engine

↓

Coaching Engine

↓

Learning Analytics

↓

Dashboard

Le LLM n'évalue jamais seul.

Le score est construit par plusieurs moteurs spécialisés.

3. Philosophie

Une erreur n'est pas une faute.

C'est un indicateur pédagogique.

Le système doit expliquer :

ce qui est correct ;
ce qui manque ;
ce qui peut être amélioré.
4. QA Engine

Le QA Engine calcule :

Score global
Score par compétence
Score procédure
Score communication
Score conformité
Score métier

Il utilise :

événements
CRM
actions
états
transcript
Business Engine
5. Sources d'évaluation

Le moteur fusionne :

Conversation

Actions CRM

Evénements

Workflow

Décisions

Temps

Respect des procédures

Business Engine

6. Architecture d'évaluation
Transcript

↓

Segmentation

↓

Analyse

↓

Détection

↓

Scoring

↓

Explications

↓

Recommandations
7. Compétences évaluées

Le système ne note pas uniquement une conversation.

Il mesure des compétences.

Exemple.

Communication
clarté
politesse
vocabulaire
professionnalisme
Relation Client
empathie
écoute
reformulation
gestion émotionnelle
Métier
procédure
outils
CRM
conformité
Résolution
efficacité
diagnostic
décision
documentation
Productivité
temps
fluidité
organisation
8. Competency Engine

Chaque compétence possède :

competency:

id: empathy

category: communication

weight: 12

rules:

- detect_empathy

- active_listening

- reassurance

Les compétences sont entièrement configurables.

9. Rubriques QA

Exemple.

qa_form:

opening:
weight: 10

verification:
weight: 10

needs_analysis:
weight: 15

resolution:
weight: 25

documentation:
weight: 20

closing:
weight: 20

Chaque entreprise peut définir sa propre grille.

10. Détection automatique

Le moteur détecte notamment :

✔ Salutation

✔ Vérification identité

✔ Reformulation

✔ Excuses

✔ Empathie

✔ Résumé

✔ Validation

✔ Clôture

Mais également :

❌ interruption

❌ oubli procédure

❌ promesse incorrecte

❌ information incohérente

❌ non-respect du script

11. Multi-évaluateurs

Le score final est obtenu par fusion de plusieurs évaluations.

Rule Engine

+

Business Engine

+

LLM Judge

+

Supervisor Rules

↓

Final Score

Ainsi, le LLM ne peut pas modifier seul une note.

12. LLM Judge

Le LLM intervient uniquement sur les éléments qualitatifs.

Exemple.

qualité d'explication
fluidité
naturel
pédagogie
empathie

Jamais sur :

procédure
CRM
conformité
workflow
13. Coaching Engine

Après l'évaluation, le système génère un coaching.

Il produit :

Points forts

↓

Axes d'amélioration

↓

Exercices

↓

Objectifs

↓

Nouvelle simulation recommandée

14. Learning Path

Le moteur construit automatiquement un parcours.

Exemple.

Empathie

↓

Gestion client difficile

↓

Objections

↓

Télévente

↓

Niveau avancé

Chaque simulation influence le parcours.

15. Adaptive Learning

Le moteur adapte :

difficulté
personas
procédures
émotions
complexité métier

Selon les performances précédentes.

Deux apprenants n'auront pas le même parcours.

16. Feedback explicable

Le moteur explique chaque note.

Exemple.

Empathie

72/100

Vous avez reconnu le problème du client.

Vous n'avez cependant pas reformulé son inquiétude.

La prochaine fois, reformulez avant de proposer une solution.

Toutes les remarques sont justifiées par des événements observés.

17. KPI pédagogiques

Le moteur suit notamment :

progression
temps d'apprentissage
nombre de simulations
taux de réussite
niveau moyen
vitesse de progression
compétences acquises
18. Dashboard Superviseur

Le superviseur visualise :

scores individuels ;
progression par compétence ;
tendances d'équipe ;
difficultés récurrentes ;
simulations échouées ;
besoins de coaching ;
comparaisons anonymisées entre équipes si la politique de l'entreprise l'autorise.
19. Coaching Assisté par IA

Le Coach IA peut générer :

un plan de coaching de 30 jours ;
des exercices ciblés ;
des simulations de remédiation ;
des conseils adaptés au profil de l'apprenant ;
des recommandations de contenu pédagogique.

Le formateur conserve toujours la possibilité de modifier ou compléter ces recommandations.

20. Certification

Le moteur peut délivrer :

Bronze

↓

Silver

↓

Gold

↓

Expert

↓

Master

Les critères de certification sont configurables.

21. Jeux de données

Le pack comprend :

plusieurs milliers de conversations annotées ;
des grilles QA sectorielles ;
des profils d'apprenants synthétiques ;
des parcours pédagogiques ;
des historiques de progression ;
des modèles de coaching.

Toutes les données sont synthétiques ou anonymisées.

22. API d'évaluation

Toutes les évaluations passent par une API stable.

Exemple.

POST /api/v1/evaluations

{
  "session_id":"...",
  "domain_pack":"support_n1",
  "conversation":"...",
  "events":[...],
  "crm_actions":[...]
}

Réponse :

{
  "overall_score": 87,
  "competencies": [],
  "recommendations": [],
  "learning_path": [],
  "coach_feedback": {}
}
23. Décisions d'architecture (ADR)

Ce volume formalise les principes suivants :

Le QA Engine est indépendant du moteur conversationnel.
Les grilles QA sont versionnées et configurables.
Les compétences sont des objets métier réutilisables.
Le LLM intervient uniquement sur les évaluations qualitatives.
Les recommandations pédagogiques sont explicables et traçables.
24. Critères d'acceptation

Le QA & Coaching Engine est considéré conforme lorsque :

les scores sont reproductibles pour un même scénario ;
chaque note est justifiée par des éléments observables ;
les plans de coaching sont personnalisés ;
les parcours d'apprentissage s'adaptent aux performances ;
les tableaux de bord permettent un suivi individuel et collectif.
🏛️ Décision d'architecture majeure : Explainable Learning Intelligence Architecture (ELIA)

Je recommande une Explainable Learning Intelligence Architecture (ELIA).

Le principe fondamental est que chaque décision pédagogique doit être explicable. Les notes ne sont jamais de simples valeurs numériques : elles sont construites à partir d'événements, de règles métier et d'analyses qualitatives clairement identifiées.

Cette architecture repose sur plusieurs moteurs spécialisés :

Conversation Engine : orchestre les échanges avec le client simulé.
Business Engines : appliquent les règles métier propres à chaque Domain Pack.
QA Engine : calcule les scores à partir d'éléments observables.
Competency Engine : suit l'évolution des compétences dans le temps.
Coaching Engine : génère des recommandations et des parcours personnalisés.
Learning Analytics Engine : consolide les données pour les tableaux de bord et les indicateurs.
📘 Prochaine étape : G9 — Domain Pack Workforce Management (WFM) & Operations

Le prochain volume fera évoluer la plateforme vers la simulation des activités de pilotage d'un centre de contacts.

Il introduira un Workforce Management Engine (WFM Engine) couvrant :

prévisions de volumes de contacts (forecasting) ;
planification des effectifs (staffing) ;
construction des plannings (scheduling) ;
gestion de l'adhérence (adherence) ;
suivi des pauses et des absences ;
calcul des indicateurs opérationnels (ASA, AHT, Occupancy, Service Level, Abandon Rate) ;
simulation de crises opérationnelles et d'arbitrages de capacité.

Avec ce volume, la plateforme ne formera plus seulement les agents et les superviseurs : elle couvrira également les métiers du pilotage opérationnel d'un centre de contacts, ouvrant la voie à une simulation complète de l'écosystème BPO.
