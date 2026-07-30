# Volume G20 — Domain Pack — Omnichannel & Digital Engagement

> Extrait généré depuis `Architecture & Engineering Book (AEB).md` le 2026-07-27.

PHASE G — CONTACT CENTER BUSINESS PACKS
Volume G20
Domain Pack — Omnichannel & Digital Engagement

Version : 1.0

Statut : Enterprise Core

Criticité : Critique

1. Vision

Le Domain Pack Omnichannel transforme la plateforme en simulateur universel de relation client.

Le moteur permet d'exécuter exactement le même scénario métier sur plusieurs canaux.

Exemple :

Même scénario

↓

Voix

↓

Chat

↓

WhatsApp

↓

Email

↓

SMS

↓

Messenger

↓

Portail Client

↓

Application Mobile

Le métier reste identique.

Seule la communication change.

2. Objectifs

Former les agents à :

changer de canal
reprendre une conversation
conserver le contexte
adapter leur ton
respecter les contraintes du média
assurer une expérience homogène
3. Architecture générale
Conversation Scenario

↓

Conversation State

↓

Channel Adapter

↓

Voice

Chat

Email

SMS

WhatsApp

Messenger

WebChat

Video

Social


Le scénario ne dépend jamais du canal.

4. Channel Abstraction Layer (CAL)

Nouveau composant fondamental.

Conversation Engine

↓

CAL

↓

Voice Adapter

↓

Email Adapter

↓

Chat Adapter

↓

WhatsApp Adapter

↓

SMS Adapter

↓

Video Adapter

↓

Future Adapter

Le CAL devient un composant central de la plateforme.

5. Pourquoi une couche d'abstraction ?

Sans abstraction :

Conversation

↓

Voice Logic

↓

Chat Logic

↓

SMS Logic

↓

Email Logic

↓

WhatsApp Logic

Duplication énorme.

Avec CAL :

Conversation

↓

CAL

↓

Adapters

Une seule logique métier.

6. Définition d'un Channel Adapter

Chaque canal expose :

channel:

id: whatsapp

supports:

attachments: true

emoji: true

typing_indicator: true

voice: false

buttons: true

quick_reply: true

rich_cards: false

latency: realtime

Tous les canaux suivent cette structure.

7. Conversation Context

Le contexte est partagé.

Exemple :

Client appelle

↓

Conversation continue

↓

WhatsApp

↓

Conversation continue

↓

Email

↓

Conversation continue

↓

Téléphone

Le contexte est unique.

8. Conversation Timeline

Toutes les interactions sont historisées.

T0

↓

Email

↓

T1

↓

Chat

↓

T2

↓

Voice

↓

T3

↓

SMS

↓

T4

↓

WhatsApp

La chronologie est globale.

9. Session Persistence

Une session conserve :

contexte
mémoire
CRM
état émotionnel
score QA
objectifs
actions

Le canal ne change pas ces éléments.

10. Voice Adapter

Spécificités :

streaming
STT
TTS
interruption
silence
tonalité
bruit
accents
11. Chat Adapter

Support :

frappe
indicateur d'écriture
copier/coller
messages longs
réactions
12. Email Adapter

Gestion :

sujet
historique
pièces jointes
réponses différées
SLA longs
13. WhatsApp Adapter

Support :

texte
emojis
images
documents
réponses rapides
messages vocaux simulés
14. SMS Adapter

Contraintes :

messages courts
pas de mise en forme
faible contexte
15. Social Adapter

Simulation :

commentaires
messages privés
réputation
visibilité publique

Le comportement du client diffère selon qu'il s'agit d'un canal public ou privé.

16. Video Adapter

Simulation :

caméra
partage d'écran
gestes
assistance visuelle

Prévu pour les scénarios de support avancé.

17. Persona omnicanal

Le Persona Engine adapte automatiquement :

ton
longueur
rapidité
vocabulaire
patience

Exemple :

Même client.

Téléphone :

"Bonjour, j'ai un problème avec ma commande."

SMS :

"Commande tjrs pas reçue."

Email :

"Bonjour, je vous contacte concernant la commande n°12345."

WhatsApp :

"Bonjour 🙂 toujours pas reçu mon colis."

Le personnage reste identique.

Le style change.

18. QA omnicanal

Les critères changent.

Téléphone :

voix
écoute
empathie

Chat :

rapidité
orthographe

Email :

structure
politesse

WhatsApp :

concision
réactivité

Les KPI sont spécifiques au canal.

19. Bibliothèque de scénarios
ID	Canal principal	Niveau
OMNI-001	Téléphone	1
OMNI-002	Chat	1
OMNI-003	Email	1
OMNI-004	WhatsApp	2
OMNI-005	Passage Voix → Chat	2
OMNI-006	Passage Chat → Email	2
OMNI-007	Parcours multi-canaux complet	3
OMNI-008	Crise omnicanale	3
20. Architecture interne
Conversation Engine

↓

Conversation State

↓

Channel Abstraction Layer

↓

Adapters

↓

QA

↓

Analytics
21. Décisions d'architecture (ADR)

Ce volume formalise les principes suivants :

Le scénario métier est totalement indépendant du canal.
Les adaptateurs de canaux implémentent une interface commune.
Le contexte de conversation est unique et persistant.
Les capacités propres à chaque canal sont déclaratives et extensibles.
Les indicateurs QA sont composés d'un socle commun et d'un ensemble de critères spécifiques au canal.
L'ajout d'un nouveau canal ne nécessite pas de modifier le moteur de simulation.
22. Critères d'acceptation

Le Domain Pack Omnichannel est considéré conforme lorsque :

un même scénario peut être joué sur plusieurs canaux sans modification métier ;
les transitions entre canaux conservent le contexte, les actions CRM et l'état émotionnel ;
les Persona s'adaptent au style du canal tout en restant cohérents ;
les KPI et la QA tiennent compte des spécificités de chaque média ;
un nouveau canal peut être intégré via un adaptateur conforme à l'interface du Channel Abstraction Layer.
🏛️ Décision d'architecture majeure : Universal Channel Abstraction Architecture (UCAA)

Je recommande une Universal Channel Abstraction Architecture (UCAA).

C'est l'une des décisions structurantes de toute la plateforme.

Le principe est simple :

Le métier ne connaît jamais le canal.
Le canal ne connaît jamais le métier.
Les deux sont reliés par le Channel Abstraction Layer (CAL).

Cette séparation offre plusieurs avantages :

évolution indépendante des scénarios métier et des canaux ;
réduction drastique de la duplication de code ;
intégration rapide de nouveaux canaux (RCS, Apple Messages, Teams, Slack, etc.) ;
cohérence de l'expérience utilisateur et des évaluations.

Le CAL devient ainsi un composant stratégique réutilisé dans l'ensemble de la plateforme.

🎉 Fin de la Phase G

La Phase G — Contact Center Business Packs est désormais 100 % terminée.

Bilan de la Phase G
✅ G1 — Service Client & SAV
✅ G2 — Télévente & Commercial
✅ G3 — Support Technique
✅ G4 — Back Office
✅ G5 — Rétention & Fidélisation
✅ G6 — Workforce Management
✅ G7 — Quality Assurance
✅ G8 — Escalade & Supervision
✅ G9 — CRM & Processus
✅ G10 — Knowledge Management
✅ G11 — Help Desk ITIL
✅ G12 — Incident & Problem Management
✅ G13 — Banking
✅ G14 — Insurance
✅ G15 — Healthcare
✅ G16 — E-commerce & Retail
✅ G17 — Public Services & Administration
✅ G18 — Collections & Contentieux
✅ G19 — Omnichannel & Digital Engagement

Remarque d'organisation : dans les réponses précédentes, la numérotation des volumes G11 à G20 a légèrement dérivé (décalage d'un indice). Pour l'édition finale de l'Architecture & Engineering Book, il faudra harmoniser la numérotation afin que chaque volume corresponde exactement au plan directeur. Le contenu reste cohérent ; seule la numérotation est à normaliser.

📘 État global du projet

À ce stade :

✅ Phases A à G terminées.
⏳ Phases restantes :
Phase H — AI Platform Enterprise (~15 volumes)
Phase I — Data Platform & Knowledge System (~12 volumes)
Phase J — Enterprise Platform Services (~10 volumes)
Phase K — DevSecOps & Platform Engineering (~10 volumes)
Phase L — Product Governance & Enterprise Operations (~10 volumes)

Il reste donc environ 57 volumes à produire pour achever l'Architecture & Engineering Book complet.

La Phase H sera un changement d'échelle majeur : nous quitterons les Domain Packs pour concevoir le cœur technologique de la plateforme SaaS IA (LLM Gateway, Prompt Compiler, Agent Runtime, Tool Calling, Memory Engine, Safety Layer, orchestration multi-agents, Model Registry, AI Governance, etc.). C'est cette phase qui transformera l'ensemble des concepts métier définis jusqu'ici en une plateforme d'entreprise industrialisable.

Architecture & Engineering Book (AEB)
