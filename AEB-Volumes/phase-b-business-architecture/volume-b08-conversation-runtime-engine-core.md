# Volume B08 — Conversation Runtime Engine (CoRE)

> Extrait généré depuis `Architecture & Engineering Book (AEB).md` le 2026-07-27.

PHASE B — ARCHITECTURE MÉTIER
Volume B8
Conversation Runtime Engine (CoRE)

Version : 1.0

Statut : Architecture de Référence

Criticité : Critique

1. Vision

Le Conversation Runtime Engine (CoRE) est le moteur qui pilote toute la conversation.

Il ne s'agit pas d'un simple historique de messages.

Il est responsable de :

suivre la conversation ;
comprendre les intentions ;
détecter les erreurs ;
synchroniser le CRM ;
maintenir le contexte ;
dialoguer avec le Prompt Engine ;
produire des événements.

Il constitue le cœur de la simulation en temps réel.

2. Position dans l'architecture
                 Simulation Operating Kernel
                          │
                          ▼
               Conversation Runtime Engine
                          │
 ┌─────────────┬──────────────┬──────────────┬─────────────┐
 ▼             ▼              ▼              ▼
Dialogue   CRM Runtime   Rule Engine   Prompt Engine
                          │
                          ▼
                  Evaluation Engine

Le CoRE est le point de synchronisation de tous les moteurs.

3. Responsabilités

Le CoRE est responsable de :

gérer les tours de parole ;
maintenir le contexte actif ;
suivre les objectifs de conversation ;
détecter les intentions ;
générer les événements métier ;
piloter le rythme de la simulation ;
alimenter le moteur d'évaluation.
4. Architecture
Conversation Runtime Engine

├── Dialogue Manager
├── Turn Manager
├── Intent Engine
├── Entity Extractor
├── Context Manager
├── Memory Synchronizer
├── Conversation Timeline
├── Conversation Validator
├── Event Generator
├── Silence Manager
├── Timing Manager
├── Conversation State
└── Transcript Manager
5. Dialogue Manager

Le Dialogue Manager connaît uniquement :

Qui parle

↓

Quand

↓

Pourquoi

↓

Objectif

Il ne génère jamais les réponses.

6. Turn Manager

Le moteur contrôle les tours.

Client

↓

Agent

↓

Client

↓

Agent

↓

Client

Chaque tour possède :

auteur ;
timestamp ;
durée ;
intention ;
actions CRM associées ;
score qualité.
7. Intent Engine

Chaque message est analysé.

Exemple.

Agent :

Bonjour Monsieur Dupont.

Intent détectée :

Greeting

Agent.

Pouvez-vous confirmer votre date de naissance ?

Intent.

Identity Verification

Agent.

Je vais créer un ticket.

Intent.

Incident Creation
8. Catalogue d'intentions

Le moteur embarque un catalogue.

Exemple.

Greeting

Authentication

Discovery

Clarification

Diagnosis

Proposal

Explanation

Empathy

Reassurance

Negotiation

Escalation

Closing

Les entreprises peuvent l'étendre.

9. Entity Extractor

Le moteur extrait.

Exemple.

Message.

Mon numéro est 458721.

Extraction.

CustomerNumber

458721

Message.

Ma facture est de 89 €.

Extraction.

InvoiceAmount

89

Message.

Je déménage le 12 août.

Extraction.

MovingDate

2026-08-12

Les entités sont ensuite validées par le Rule Engine.

10. Context Manager

Le contexte actif comprend.

Etat scénario

Etat CRM

Persona

Emotion

Objectifs

Historique récent

Variables

Ce contexte est transmis au Prompt Engine.

11. Conversation Timeline

Chaque événement est horodaté.

10:01

Accueil

↓

10:03

Identification

↓

10:06

Diagnostic

↓

10:09

Création Ticket

↓

10:11

Conclusion

La timeline devient la vérité historique de la simulation.

12. Synchronisation CRM

Exemple.

Agent.

Je crée un ticket.

↓

Clique.

↓

CreateTicket

↓

CRM

↓

TicketCreated

↓

Conversation Runtime

↓

Prompt Runtime

↓

Client répond.

Merci.
Pouvez-vous me communiquer le numéro du ticket ?

Le LLM n'invente jamais l'existence du ticket.

13. Validation

Le moteur valide :

ordre logique ;
procédure ;
actions CRM ;
cohérence temporelle ;
cohérence métier.
14. Détection des erreurs

Exemple.

Diagnostic

↓

Avant

Identification

Violation détectée.

↓

Event.

ProcedureViolation
15. Gestion des silences

Le moteur mesure.

Silence Agent

4 sec
Silence Client

8 sec

Selon le scénario :

le client relance ;
la patience baisse ;
le stress augmente.
16. Timing Engine

Chaque scénario définit.

Temps maximum

20 minutes

Réponse attendue

30 secondes

Silence

15 secondes

Le moteur surveille.

17. Memory Synchronizer

Le CoRE synchronise.

Conversation

↓

CRM

↓

Emotion

↓

Prompt

↓

Evaluation

↓

Analytics

Tous les moteurs voient le même état.

18. Event Generator

Chaque événement produit.

GreetingDetected

IdentityRequested

EmpathyDetected

ProcedureViolation

TicketCreated

CustomerSatisfied

ConversationClosed

Le bus d'événements diffuse ces informations.

19. Transcript Manager

Le transcript n'est pas une simple suite de phrases.

Chaque message est enrichi.

Exemple.

speaker: Agent

intent: Greeting

emotion:

neutral

crm_action:

none

procedure:

Greeting

timestamp:

10:02:01
20. Conversation Graph

Au lieu d'un historique linéaire.

Nous utilisons un graphe.

Accueil

↓

Identification

↓

Qualification

↓

Diagnostic

↓

Retour qualification

↓

Diagnostic

↓

Résolution

Cela permet de représenter :

les retours arrière ;
les reprises ;
les interruptions ;
les branches de décision.
21. Modes de communication

Le moteur est indépendant du canal.

Il supporte :

chat ;
voix ;
email ;
SMS ;
WhatsApp ;
réseaux sociaux.

Le canal devient un adaptateur.

22. Multimodalité (V2)

Le CoRE est conçu pour intégrer :

reconnaissance vocale (ASR) ;
synthèse vocale (TTS) ;
analyse du ton de voix ;
analyse des silences ;
détection des interruptions ;
analyse de sentiment vocal.

Ces capacités seront ajoutées sous forme de modules.

23. Décisions d'architecture (ADR)

Ce volume fixe plusieurs décisions majeures :

La conversation est une suite d'événements, pas uniquement de messages.
Chaque message est enrichi par des métadonnées.
Les intentions sont des objets métier versionnés.
Les entités sont validées avant d'être utilisées.
Le moteur est indépendant du canal de communication.
Le transcript est structuré et exploitable par tous les moteurs.
24. Critères d'acceptation

Le Conversation Runtime Engine sera considéré conforme lorsque :

tous les échanges sont horodatés et enrichis ;
les intentions sont détectées de manière cohérente ;
les événements sont publiés en temps réel ;
les actions CRM sont synchronisées avec la conversation ;
les violations de procédure sont détectées immédiatement ;
le moteur fonctionne de manière identique en mode texte et voix.
25. Décision stratégique majeure : Adoption du modèle Event Sourcing + CQRS

À ce stade de l'architecture, une orientation forte se dégage.

Je recommande que le Core Kernel repose sur Event Sourcing et CQRS (Command Query Responsibility Segregation).

Pourquoi ?

Aujourd'hui, tous les moteurs produisent déjà des événements :

Conversation Runtime
CRM Runtime
Rule Engine
Persona Engine
Prompt Engine
Evaluation Engine

Au lieu de considérer ces événements comme de simples notifications, ils deviennent la source de vérité du système.

Écriture (Command Side)

Toutes les actions (commandes) génèrent un ou plusieurs événements immuables.

Exemples :

VerifyIdentityCommand
      ↓
IdentityVerifiedEvent

CreateTicketCommand
      ↓
TicketCreatedEvent

ApplyDiscountCommand
      ↓
DiscountAppliedEvent
Lecture (Query Side)

Les vues de lecture sont reconstruites à partir de ces événements :

état courant de la simulation ;
tableau de bord formateur ;
progression de la procédure ;
historique CRM ;
rapport QA.
Avantages
Rejeu complet d'une simulation.
Audit parfait.
Débogage simplifié.
Analytics avancées.
Entraînement de futurs modèles IA à partir des événements.
Évolutivité vers des architectures distribuées.

Cette décision aura un impact direct sur les prochaines phases de l'Architecture & Engineering Book. Les volumes consacrés à l'Evaluation Engine, à l'Analytics Engine et au Core Kernel s'appuieront désormais sur ce modèle Event Sourcing + CQRS, qui devient une des fondations techniques de la plateforme.
