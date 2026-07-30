# Volume B04 (partie 2) — Customer Persona Engine & Behavior Simulation Engine (BSE)

> Extrait généré depuis `Architecture & Engineering Book (AEB).md` le 2026-07-27.

PHASE B — ARCHITECTURE MÉTIER
Volume B4
Customer Persona Engine & Behavior Simulation Engine (BSE)

Version : 1.0

Statut : Architecture de Référence

Criticité : Critique

1. Objectif

Le Behavior Simulation Engine (BSE) est responsable du comportement du client virtuel.

Le LLM ne crée pas la personnalité.

Le LLM interprète une personnalité définie par le moteur.

Le BSE décide :

comment pense le client ;
comment il réagit ;
son niveau de patience ;
sa manière de parler ;
sa coopération ;
sa mémoire émotionnelle ;
ses limites.
2. Philosophie

Le client IA n'est pas un personnage figé.

Il possède un état psychologique vivant.

Persona

+

Emotion

+

Historique

+

Contexte

+

Evénements

=

Comportement

Deux simulations identiques peuvent produire des conversations légèrement différentes tout en restant conformes au scénario.

3. Architecture
Behavior Simulation Engine

├── Persona Library

├── Emotion Engine

├── Mood Engine

├── Patience Engine

├── Trust Engine

├── Cooperation Engine

├── Speech Style Engine

├── Memory Engine

├── Trigger Engine

├── Behavior Policy

├── Response Constraints

└── Randomization Engine
4. Persona

Une Persona est un modèle psychologique.

Elle ne dépend pas du métier.

Exemple :

Agressif

Patient

Stressé

Méfiant

Ironique

Très bavard

Expert

Débutant

Passif

Confus

Très pressé

Très poli

Senior

Professionnel

Chaque persona peut être utilisée dans :

SAV
Télévente
Assurance
Banque
Support
Santé
Administration
5. Structure d'une Persona
id:

name:

description:

speech_style:

cooperation:

patience:

stress:

trust:

assertiveness:

verbosity:

technical_level:

empathy_level:

memory_accuracy:

interrupt_probability:

negotiation_style:

frustration_growth:

calming_speed:
6. Exemple
name: Angry Customer

patience: 25

trust: 20

stress: 80

verbosity: 35

interrupt_probability: 85

technical_level: 40

cooperation: 15

calming_speed: 8

Le LLM reçoit ces valeurs.

Il ne les invente jamais.

7. Les Variables Psychologiques

Notre moteur utilise plusieurs dizaines de variables.

Première version :

Variable	Description
Patience	Temps avant rupture
Stress	Niveau de tension
Colère	Intensité émotionnelle
Confiance	Confiance envers l'agent
Coopération	Volonté d'aider
Satisfaction	Etat positif
Fatigue	Lassitude
Confusion	Compréhension
Engagement	Implication
Politesse	Niveau de courtoisie
Assertivité	Tendance à imposer son point de vue
Impulsivité	Réactivité émotionnelle
8. Emotion Engine

Le client possède plusieurs émotions simultanément.

Exemple :

Patience

████████░░

80

Stress

█████░░░░░

50

Colère

██░░░░░░░░

20

Confiance

███████░░░

70

Les émotions évoluent indépendamment.

9. Patience Engine

La patience n'est pas une simple minuterie.

Elle dépend de nombreux facteurs.

Patience

↓

Temps d'attente

↓

Questions répétées

↓

Empathie

↓

Résolution

↓

Silences

↓

Interruptions

↓

Evolution
10. Trust Engine

La confiance évolue.

Exemple

Agent :

Je comprends votre situation.

Confiance :

+5

Agent :

Je vais vérifier votre dossier.

+3

Agent :

Je ne sais pas.

-8

Agent :

Ignore la question.

-12

11. Cooperation Engine

Le client peut décider de :

répondre
éviter
refuser
mentir
être vague
raccrocher
changer de sujet

Cette décision dépend :

Cooperation

+

Trust

+

Stress

+

Persona
12. Speech Style Engine

Chaque persona possède son style.

Variables.

Longueur phrases

Vocabulaire

Politesse

Ponctuation

Humour

Ironie

Argot

Débit

Répétitions

Expressions régionales
13. Exemple

Client âgé

Parle lentement

Utilise des phrases longues

Hésite

Pose plusieurs questions

Cherche à être rassuré

Client très pressé

Réponses courtes

Interrompt

Demande la solution

S'impatiente rapidement
14. Trigger Engine

Chaque persona possède des déclencheurs.

Exemple

Temps d'attente > 60 sec

↓

Stress +15
Agent coupe la parole

↓

Colère +20
Agent reformule

↓

Confiance +10
Agent s'excuse

↓

Stress -8
15. Escalade émotionnelle

Les émotions ne changent jamais brutalement.

Exemple

Calme

↓

Agacé

↓

Frustré

↓

Très irrité

↓

En colère

↓

Très agressif

↓

Rupture

Chaque transition est progressive.

16. Désescalade

Le moteur prévoit aussi le retour au calme.

Exemple

Agent empathique

↓

Stress -10

↓

Confiance +8

↓

Patience +6

↓

Colère -5
17. Memory Engine

Le client se souvient.

Exemple

Agent :

Je vais vérifier.

Deux minutes plus tard.

Le client dira :

Vous m'aviez dit que vous vérifiiez.

Le moteur conserve les promesses importantes.

18. Randomization Engine

Sans aléatoire, toutes les simulations seraient identiques.

Nous introduisons une variabilité contrôlée.

Exemple

Patience initiale

Configuration

40

Variation

±5

Simulation A

37

Simulation B

43

Cette variation reste dans des bornes définies.

19. Response Constraints

Le moteur peut imposer :

Ne jamais révéler le scénario

Ne jamais aider l'agent

Ne jamais inventer un produit

Ne jamais modifier le CRM

Ne jamais parler des prompts

Ne jamais sortir du rôle
20. Persona Library

La plateforme inclura une bibliothèque de personas.

Version MVP :

Famille	Exemples
Emotionnelle	Calme, anxieux, agressif, frustré
Relationnelle	Coopératif, méfiant, exigeant
Communication	Bavard, silencieux, confus
Technique	Expert, novice
Temporelle	Pressé, disponible
Négociation	Flexible, ferme, opportuniste

Les entreprises pourront créer leurs propres personas.

21. Compatibilité Scénario ↔ Persona

Toutes les combinaisons ne sont pas pertinentes.

Exemple :

Scénario

↓

Télévente

↓

Persona

↓

Très bavard

Compatible.

Support N2

↓

Persona

↓

Expert informatique

Compatible.

Recouvrement

↓

Persona

↓

Très agressif

Compatible.

Le moteur vérifie la cohérence avant de lancer une simulation.

22. Décisions d'architecture (ADR)

Ce volume fixe plusieurs décisions structurantes :

Les personas sont des ressources métier versionnées.
Les émotions sont pilotées par le moteur, jamais par le LLM.
Les transitions émotionnelles sont déterministes, avec une variabilité contrôlée.
Le LLM interprète un état émotionnel, il ne le calcule pas.
Les entreprises peuvent enrichir la bibliothèque sans modifier le code.
23. Perspectives d'évolution

À partir de la V2, le moteur pourra intégrer :

profils culturels et linguistiques ;
styles de communication propres à certains secteurs (banque, santé, assurance) ;
objectifs cachés (par exemple obtenir une remise sans réellement vouloir résilier) ;
personnalités composites (plusieurs traits dominants avec des poids différents) ;
adaptation progressive de la difficulté selon le niveau de l'agent.

Ces évolutions resteront compatibles avec le modèle de données défini dans ce volume.

Ce qui vient ensuite : Volume B5 — Scenario Engine & Procedure Engine

Le prochain volume définira la structure complète des scénarios :

modèle de données d'un scénario ;
procédures métier configurables ;
objectifs obligatoires et facultatifs ;
règles de réussite et d'échec ;
variables de contexte ;
niveaux de difficulté ;
moteur de progression du scénario ;
système de validation des étapes.

Ce document constituera le contrat de référence pour toutes les simulations de la plateforme et servira directement à la conception des interfaces d'administration et du backend Python.
