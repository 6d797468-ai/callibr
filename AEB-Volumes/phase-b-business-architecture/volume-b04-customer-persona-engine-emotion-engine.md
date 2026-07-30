# Volume B04 — Customer Persona Engine & Emotion Engine

> Extrait généré depuis `Architecture & Engineering Book (AEB).md` le 2026-07-27.

PHASE B — ARCHITECTURE MÉTIER
Volume B4
Customer Persona Engine & Emotion Engine

Version : 1.0

Statut : Architecture de Référence

Criticité : Critique

1. Objectif

Le Customer Persona Engine est responsable de définir qui est le client.

Le Emotion Engine est responsable de définir comment il se sent.

Le LLM est responsable de définir comment il parle.

Cette séparation est fondamentale.

           Persona
              │
              ▼
        Emotion Engine
              │
              ▼
      Prompt Compiler
              │
              ▼
             LLM
              │
              ▼
     Réponse conversationnelle
2. Principe fondamental

Une persona est permanente.

Une émotion est dynamique.

Exemple

Persona :

impatient
bavard
poli

Ces caractéristiques ne changent pratiquement jamais pendant une simulation.

En revanche :

Patience

↓

Confiance

↓

Stress

↓

Colère

↓

Satisfaction

évoluent en permanence.

3. Architecture
Customer Persona Engine

│

├── Persona Registry

├── Personality Model

├── Behaviour Rules

├── Communication Style

├── Trigger Catalog

└── Prompt Adapter


Emotion Engine

│

├── Emotion State

├── Emotion Calculator

├── Influence Matrix

├── Trigger Evaluator

├── Recovery Engine

└── Escalation Engine
4. Persona Registry

Toutes les personas sont stockées sous forme déclarative.

Exemple

persona_id: angry_customer

name: Client en colère

base_traits:

  patience: 25

  politeness: 35

  technical_level: 40

  trust: 20

  verbosity: 55

  flexibility: 15

communication:

  interrupts: true

  uses_short_sentences: true

  speaks_fast: true

  accepts_humor: false

goals:

  résoudre rapidement

  être entendu

  obtenir une compensation

Le moteur ne contient aucune persona codée en dur.

5. Familles de Personas

La plateforme est conçue pour être extensible.

Exemples de familles :

Comportement
Calme
Patient
Pressé
Agressif
Ironique
Passif
Coopératif
Exigeant
Communication
Très bavard
Très silencieux
Direct
Indirect
Confus
Organisé
Compétence
Débutant
Intermédiaire
Expert
Relation commerciale
Nouveau client
Fidèle
VIP
Client perdu
Prospect

Une persona est une combinaison de plusieurs dimensions.

6. Personality Model

Le moteur utilise plusieurs axes.

Patience

Assertivité

Confiance

Empathie

Flexibilité

Stress

Rationalité

Impulsivité

Tolérance

Coopération

Chaque variable varie entre 0 et 100.

7. Emotion State

Contrairement à la persona, les émotions évoluent.

Etat initial :

Patience: 45

Stress: 60

Colère: 70

Confiance: 20

Satisfaction: 10

Fatigue: 15

Après plusieurs bonnes réponses :

Patience: 62

Stress: 35

Colère: 20

Confiance: 58

Satisfaction: 55
8. Variables émotionnelles

Le moteur V1 utilisera :

Patience

Stress

Colère

Confiance

Frustration

Anxiété

Fatigue

Satisfaction

Coopération

Urgence

Toutes sont indépendantes.

9. Jauge de Patience

La patience est la variable centrale.

Elle influence :

longueur des réponses ;
fréquence des interruptions ;
politesse ;
acceptation des explications ;
probabilité d'abandon.

Exemple

100

Très calme

↓

80

Patient

↓

60

Agacé

↓

40

Impatient

↓

20

Très énervé

↓

0

Abandon
10. Influence Matrix

Chaque événement modifie plusieurs variables.

Exemple

Agent reformule correctement.

Patience: +8

Confiance: +10

Stress: -5

Agent coupe la parole.

Patience: -18

Colère: +12

Stress: +8

Agent s'excuse.

Confiance: +6

Colère: -5

Patience: +4

Le moteur applique ces règles.

Le LLM ne les calcule jamais.

11. Trigger Catalog

Chaque événement possède des déclencheurs.

Exemple

Attente longue

↓

Stress +10
Erreur CRM

↓

Confiance -12
Bonne explication

↓

Stress -8
Absence d'empathie

↓

Colère +10

Les déclencheurs sont entièrement configurables.

12. Escalation Engine

Certaines combinaisons provoquent une escalade.

Exemple

Patience <20

ET

Colère >80

↓

Client menace de résilier

Autre exemple

Stress >85

↓

Client coupe fréquemment la parole

Les réactions restent déterminées par les règles.

Le LLM les exprime naturellement.

13. Recovery Engine

Le client peut également se calmer.

Exemple

Bonne écoute

↓

Stress -10
Empathie

↓

Confiance +15
Solution rapide

↓

Satisfaction +25
14. Prompt Adapter

Le Prompt Adapter transforme l'état émotionnel en consignes.

Exemple interne :

Patience = 15

Confiance = 20

Colère = 85

Le Prompt Adapter génère :

Le client est très irrité.

Il répond brièvement.

Il coupe parfois la parole.

Il doute des informations.

Il souhaite une résolution immédiate.

Ainsi, le prompt reste compact.

15. Evolution des émotions

Le moteur est piloté par une boucle.

Message Agent

↓

Analyse

↓

Détection

↓

Calcul émotion

↓

Nouvel état

↓

Prompt

↓

LLM

↓

Réponse

Les émotions évoluent après chaque interaction.

16. Limites d'évolution

Toutes les variables sont bornées.

Exemple

0 ≤ Patience ≤ 100

0 ≤ Stress ≤ 100

0 ≤ Satisfaction ≤ 100

Cela évite des états incohérents.

17. Profils avancés

Une même persona peut évoluer.

Exemple

Client VIP

Jour normal

↓

Très poli

↓

Panne majeure

↓

Très exigeant

↓

Toujours poli


Le style reste identique.

L'émotion change.

---

# 18. Personnalités composites

Une persona est composée de plusieurs couches.

Exemple

text
VIP

+

Expert Informatique

+

Très Pressé

+

Peu Tolérant

Le moteur fusionne ces caractéristiques.

19. Observabilité

Toutes les évolutions émotionnelles sont tracées.

Exemple

10:05

Patience

45 → 52

Cause :

Bonne reformulation
10:08

Confiance

40 → 25

Cause :

Erreur procédure

Ces données alimentent ensuite le rapport pédagogique.

20. Décisions d'architecture (ADR)

Ce volume fixe plusieurs règles fondamentales :

Les personas sont déclaratives et versionnées.
Les émotions sont calculées par le moteur, jamais par le LLM.
Une persona est indépendante d'un scénario.
Les réactions émotionnelles sont déterministes.
Le LLM reçoit uniquement une synthèse comportementale.
Les paramètres émotionnels sont configurables par organisation.
21. Critères d'acceptation

Le Customer Persona Engine sera considéré conforme lorsque :

une même persona produit un comportement cohérent d'une simulation à l'autre ;
les émotions évoluent selon des règles configurables ;
les déclencheurs sont modifiables sans changer le code ;
les changements d'état sont historisés ;
le Prompt Adapter transforme correctement l'état interne en consignes conversationnelles.
Conclusion architecturale

Avec ce volume, nous avons défini la psychologie du client.

Le prochain volume (B5) sera consacré au Scenario Engine & Procedure Engine. Il décrira comment les scénarios sont modélisés, versionnés, configurés, validés et exécutés, indépendamment des personas. C'est ce moteur qui permettra à une entreprise de créer ses propres parcours métier (SAV, support, vente, rétention, recouvrement, etc.) sans modifier le code de la plateforme.
