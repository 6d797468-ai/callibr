# Volume G00 — Domain Pack Framework

> Extrait généré depuis `Architecture & Engineering Book (AEB).md` le 2026-07-27.

PHASE G — CONTACT CENTER BUSINESS PACKS
Volume G0
Domain Pack Framework

Version : 1.0

Statut : Architecture Métier

Criticité : Critique

1. Vision

Un Domain Pack est une extension métier autonome.

Il ne contient pas uniquement des scénarios.

Il contient :

les connaissances métier ;
les procédures ;
les règles ;
les personas ;
les CRM fictifs ;
les évaluations QA ;
les KPI ;
les prompts IA.

Le moteur reste identique.

Le métier change uniquement par configuration.

2. Principe

ATOS fonctionne selon ce modèle.

                    ATOS Platform

                         │

       ┌─────────────────┼─────────────────┐

       ▼                 ▼                 ▼

  Domain Pack      Domain Pack      Domain Pack

      SAV          Télévente      Support N1

       ▼                 ▼                 ▼

 Personnas      Procédures      CRM fictif

       ▼                 ▼                 ▼

 Prompts      Evaluation QA     Workflows
3. Contenu d'un Domain Pack

Chaque pack contient exactement les mêmes dossiers.

domain-pack/

README.md

manifest.yaml

configuration/

prompts/

personas/

crm/

procedures/

knowledge/

qa/

kpis/

analytics/

datasets/

fixtures/

examples/

tests/

Ainsi OpenCode peut générer automatiquement un nouveau métier.

4. Manifest

Chaque Domain Pack possède un manifeste.

Exemple.

id: support_n1

name: Support Niveau 1

version: 1.0.0

industry: telecom

language:

- fr

- en

difficulty:

- easy

- medium

- hard
5. Configuration

Configuration générale.

voice_enabled: true

crm_enabled: true

evaluation_enabled: true

knowledge_enabled: true

actions_enabled: true
6. Personas

Le pack contient ses personas.

Exemple.

personas/

angry_customer.yaml

happy_customer.yaml

elderly_customer.yaml

professional_customer.yaml

confused_customer.yaml
7. Procédures

Chaque procédure métier.

verify_identity.yaml

refund.yaml

cancel_subscription.yaml

create_ticket.yaml

escalation.yaml
8. Actions CRM

Le pack déclare les actions disponibles.

Exemple.

VerifyIdentity

SearchCustomer

CreateTicket

TransferCall

Refund

CancelOrder

CreateIncident
9. Connaissances

Le pack possède sa base documentaire.

knowledge/

faq/

manuals/

policies/

products/

pricing/

Ces documents alimentent le moteur RAG.

10. QA

Chaque métier possède sa grille qualité.

Exemple.

Greeting

Empathy

Compliance

Verification

Accuracy

Resolution

Closing

Les pondérations sont spécifiques au métier.

11. KPI

Chaque pack définit ses indicateurs.

Exemple.

AHT

FCR

CSAT

NPS

TransferRate

EscalationRate
12. Analytics

Les dashboards sont également configurables.

Exemple.

TopScenarios

AgentRanking

AverageScore

FailureReasons

TrendAnalysis
13. Prompts

Le pack contient tous les prompts.

prompts/

persona.md

coach.md

evaluation.md

rag.md

emotion.md

system.md

Les prompts sont versionnés.

14. Datasets

Chaque métier fournit :

datasets/

customers.json

products.json

contracts.json

tickets.json

Ces données servent au CRM simulé.

15. Fixtures

Les fixtures servent aux tests.

fixtures/

scenario_easy

scenario_medium

scenario_hard
16. Tests

Chaque pack possède.

tests IA ;
tests métier ;
tests QA ;
benchmarks ;
scénarios de régression.
17. Versionnement

Chaque pack possède :

major.minor.patch

Le moteur connaît les versions compatibles.

18. Publication

Cycle.

Draft

↓

Internal

↓

Validated

↓

Published

↓

Deprecated
19. Signature

Chaque pack est signé.

Cela garantit :

authenticité ;
intégrité ;
compatibilité.
20. Marketplace

À terme.

ATOS pourra charger.

Support Telecom

↓

Banque

↓

Assurance

↓

Energie

↓

Administration

↓

E-commerce

Sans redéploiement.

21. Dépendances

Un Domain Pack ne dépend jamais d'un autre.

Ils ne partagent que :

Kernel
Contracts
Platform API
22. Industrialisation

Un générateur peut créer.

atos create-domain insurance

↓

Génère automatiquement.

structure
manifest
prompts
CRM
QA
datasets
23. Critères de qualité

Un Domain Pack est accepté lorsque.

✓ Personas validés

✓ QA validée

✓ CRM cohérent

✓ Procédures cohérentes

✓ Benchmarks réussis

✓ Prompts testés

24. ADR

Décisions.

Les métiers sont des extensions.
Aucun code spécifique.
Configuration > Développement.
Tous les packs utilisent les mêmes contrats.
25. Critères d'acceptation

Un Domain Pack est conforme lorsque :

il respecte la structure standard ;
il peut être chargé sans modification du moteur ;
ses scénarios passent les tests de validation ;
ses prompts et ses règles QA sont versionnés.
🏛️ Décision d'architecture majeure : Domain Pack Architecture (DPA)

Je recommande officiellement une Domain Pack Architecture.

Les moteurs d'ATOS deviennent totalement indépendants des métiers. Chaque secteur (télécom, banque, assurance, énergie, e-commerce, santé, secteur public...) est encapsulé dans un pack autonome, installable, versionnable et distribuable.

Cette séparation ouvre plusieurs perspectives :

Marketplace de Domain Packs ;
personnalisation par client sans fork du code ;
cycles de mise à jour indépendants entre plateforme et contenu métier ;
industrialisation de la création de nouveaux domaines.
📘 Phase G — Plan complet

Je recommande la structure suivante pour la Phase G :

Volume	Contenu
G0	Framework des Domain Packs (terminé)
G1	Service Après-Vente (SAV)
G2	Support Technique N1/N2
G3	Télévente & Vente Conseil
G4	Rétention & Fidélisation
G5	Recouvrement
G6	Back Office
G7	Conduite d'Activité / Dispatch
G8	Assurance Qualité (QA) & Coaching
G9	Bibliothèque Universelle de Personas
G10	Bibliothèque Universelle de Procédures
G11	Domain Pack Builder SDK
G12	Marketplace & Certification des Domain Packs

À partir du G1, chaque volume sera un guide métier complet, avec :

les processus opérationnels ;
les modèles de données CRM simulés ;
les scénarios d'entraînement ;
les personas spécifiques ;
les règles QA ;
les prompts spécialisés ;
les KPI ;
les jeux de données de démonstration ;
les critères d'évaluation.

C'est cette bibliothèque qui donnera à ATOS une profondeur métier difficile à reproduire et permettra d'ajouter de nouveaux secteurs sans modifier le cœur de la plateforme.
