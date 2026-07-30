# Volume B09 — Evaluation & Quality Intelligence Engine (EQI)

> Extrait généré depuis `Architecture & Engineering Book (AEB).md` le 2026-07-27.

PHASE B — ARCHITECTURE MÉTIER
Volume B9
Evaluation & Quality Intelligence Engine (EQI)

Version : 1.0

Statut : Architecture de Référence

Criticité : Critique

1. Vision

L'EQI est le moteur chargé de transformer une simulation en une évaluation objective, explicable et exploitable.

Il ne se contente pas d'attribuer une note.

Il mesure :

les compétences ;
les erreurs ;
les points forts ;
les axes d'amélioration ;
la progression.

L'objectif est d'obtenir une évaluation comparable à celle d'un responsable qualité expérimenté.

2. Position dans l'architecture
Conversation Runtime
        │
        ▼
Evaluation Engine
        │
 ┌──────┼─────────────┬──────────────┐
 ▼      ▼             ▼              ▼
Rule  QA Grid   Competency      Analytics
Engine          Engine

L'évaluation est alimentée par tous les moteurs.

3. Sources utilisées

L'EQI exploite :

le transcript enrichi ;
les événements ;
la timeline ;
les actions CRM ;
les objectifs ;
les règles ;
les émotions ;
les temps de réponse ;
les silences ;
les interruptions.

Le LLM n'est qu'une source parmi d'autres.

4. Architecture
Evaluation Engine

├── QA Engine
├── Competency Engine
├── KPI Engine
├── Rule Evaluator
├── Behavior Analyzer
├── Communication Analyzer
├── Procedure Analyzer
├── CRM Analyzer
├── Coaching Engine
├── Recommendation Engine
├── Report Builder
└── Certification Engine
5. Philosophie

Nous distinguons deux types d'évaluation.

Déterministe

Calculée par règles.

Exemple :

Identité vérifiée

↓

+10 points
IA

Evaluation qualitative.

Exemple.

Empathie

Qualité des explications

Fluidité

Reformulation

Clarté

Le score final combine les deux.

6. Les compétences

Chaque entreprise définit son référentiel.

Exemple.

Communication

Ecoute

Empathie

Diagnostic

Connaissance produit

CRM

Gestion émotionnelle

Argumentation

Closing

Conformité
7. Modèle de compétence

Chaque compétence possède.

id

name

description

weight

minimum_score

critical

category
8. Grille QA

Une grille QA est composée.

Sections

↓

Critères

↓

Sous-critères

↓

Points

↓

Commentaires
9. Exemple

Accueil.

Salutation

2 points

Présentation.

Identification

3 points

Empathie.

Expression adaptée

4 points

Conclusion.

Résumé

3 points
10. Pondération

Chaque secteur peut définir.

Support

Empathie

20 %

Télévente.

Closing

30 %

Recouvrement.

Respect procédure

35 %
11. Analyse comportementale

Le moteur mesure.

interruptions ;
agressivité ;
reformulations ;
écoute active ;
validation ;
rythme ;
silences.
12. Analyse conversationnelle

Le moteur extrait.

questions ouvertes ;
questions fermées ;
confirmations ;
reformulations ;
objections ;
réponses incomplètes.
13. Analyse CRM

Le moteur mesure.

Actions oubliées

Actions inutiles

Temps CRM

Erreurs CRM

Navigation
14. Analyse procédure

Chaque étape est vérifiée.

Accueil

✓
Identification

✓
Diagnostic

✓
Conclusion

✗
15. Analyse émotionnelle

Le moteur compare.

Emotion initiale.

Stress

85

Emotion finale.

Stress

25

Progression.

Très bonne.

16. Analyse temporelle

Mesures.

Temps total

Temps silence

Temps CRM

Temps parole

Temps diagnostic
17. Détection des erreurs

Le moteur classe.

Critique

Exemple.

Absence d'identification.

Majeure

Mauvaise procédure.

Mineure

Formule oubliée.

Information

Amélioration possible.

18. Coaching Engine

Chaque erreur produit.

une explication ;
une recommandation ;
un exercice ;
une ressource.

Exemple.

Erreur

Aucune reformulation.

↓

Conseil

Reformulez la demande du client.

↓

Exercice recommandé

Simulation "Ecoute Active Niveau 1"
19. Adaptive Learning

Le moteur détecte.

Agent faible.

↓

Empathie.

↓

Proposer.

Module.

Empathie Avancé.

Agent faible.

↓

CRM.

↓

Proposer.

CRM Niveau 2.

La plateforme adapte automatiquement le parcours.

20. Certification

Chaque compétence possède un niveau.

Débutant

↓

Junior

↓

Confirmé

↓

Senior

↓

Expert

Le niveau est calculé automatiquement.

21. Rapport

Le rapport contient.

score global ;
score QA ;
score CRM ;
score communication ;
score émotion ;
chronologie ;
erreurs ;
recommandations ;
progression ;
certification.
22. Explainable AI

Toutes les conclusions doivent être justifiées.

Exemple.

Empathie

78 %

↓

Détection

4 formulations empathiques

↓

1 occasion manquée

↓

Score final

Le système évite les évaluations opaques.

23. IA dans l'évaluation

Le LLM intervient uniquement pour les critères subjectifs :

qualité de la reformulation ;
naturel de la conversation ;
clarté des explications ;
pertinence des réponses.

Les critères objectifs (procédure, CRM, temps, règles) restent calculés par le moteur.

24. Benchmark

Le moteur permet de comparer.

un agent à lui-même ;
un agent à son équipe ;
une équipe à une autre ;
un site à un autre ;
une campagne à une autre.

Les comparaisons sont anonymisables.

25. Export

Les rapports sont exportables.

PDF
JSON
Excel
API REST
Webhooks

Ils peuvent alimenter un LMS, un SIRH ou un outil BI.

26. Décisions d'architecture (ADR)

Ce volume fixe plusieurs décisions structurantes :

Les scores sont hybrides (règles + IA).
Les évaluations sont explicables.
Les compétences sont configurables par tenant.
Les recommandations sont liées aux compétences.
Les rapports sont générés à partir des événements de la simulation.
Les évaluations sont rejouables.
27. Critères d'acceptation

L'EQI sera considéré conforme lorsque :

une grille QA peut être créée sans développement ;
les scores sont reproductibles à partir des mêmes événements ;
chaque pénalité est justifiée ;
les recommandations sont personnalisées ;
les rapports sont exportables ;
les compétences peuvent évoluer sans modifier le moteur.
28. Extension stratégique : Enterprise Competency Graph (ECG)

Pour une version Enterprise, je recommande d'ajouter un Enterprise Competency Graph.

Au lieu de gérer les compétences comme une simple liste, elles deviennent un graphe de connaissances.

Exemple :

Ecoute Active
      │
      ├── Reformulation
      │
      ├── Validation
      │
      └── Questions ouvertes

Chaque compétence dépend de sous-compétences, ce qui permet :

d'identifier précisément les causes d'un faible score ;
de proposer des plans de progression ciblés ;
de mesurer l'impact d'une formation sur des compétences connexes ;
de construire des parcours adaptatifs beaucoup plus pertinents.
📌 Évolution architecturale recommandée

À partir de ce volume, je recommande officiellement que le Core Kernel expose une API d'événements standardisée (Simulation Event API).

Tous les moteurs (Conversation, CRM, Rule, Persona, Prompt, Evaluation, Analytics) échangeront exclusivement via cette API, avec un schéma d'événement versionné.

Cette décision apporte plusieurs avantages :

découplage fort entre les moteurs ;
ajout de nouveaux modules sans modifier le noyau ;
meilleure observabilité ;
intégration facilitée avec des services externes (LMS, BI, Data Lake) ;
évolution vers une architecture distribuée ou multi-régions.

Cette API d'événements constituera l'une des fondations de la Phase C, où nous définirons le Core Kernel, le bus d'événements, les contrats d'échange, la persistance Event Sourcing et les interfaces publiques de la plateforme.
