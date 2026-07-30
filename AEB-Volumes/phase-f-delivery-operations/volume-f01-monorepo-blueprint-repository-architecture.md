# Volume F01 — Monorepo Blueprint & Repository Architecture

> Extrait généré depuis `Architecture & Engineering Book (AEB).md` le 2026-07-27.

PHASE F — DELIVERY, IMPLEMENTATION & ENTERPRISE OPERATIONS
Volume F1
Monorepo Blueprint & Repository Architecture

Version : 1.0

Statut : Architecture de Référence

Criticité : Critique

1. Vision

Le dépôt Git n'est pas un simple stockage de code.

Il est :

l'architecture vivante du produit ;
la source de vérité ;
le point d'entrée des développeurs ;
le point d'entrée des agents IA ;
le référentiel documentaire ;
le référentiel d'ingénierie.

L'organisation du dépôt doit donc refléter l'architecture métier.

2. Principes

Le monorepo doit être :

modulaire ;
découplé ;
facilement navigable ;
indexable par le RAG ;
stable dans le temps.

Les chemins deviennent des conventions d'architecture.

3. Vue globale
atos/

│

├── docs/

├── architecture/

├── adr/

├── prompts/

├── schemas/

├── contracts/

├── packages/

├── services/

├── engines/

├── platform/

├── infrastructure/

├── deployments/

├── tools/

├── scripts/

├── datasets/

├── tests/

├── examples/

└── .github/
4. Dossier docs/

Contient :

docs/

Vision

Roadmap

Glossaire

User Guides

Developer Guides

Operations

Training

Documentation utilisateur.

5. Dossier architecture/

Contient :

Phase-A

Phase-B

Phase-C

Phase-D

Phase-E

Phase-F

L'Architecture & Engineering Book.

Chaque volume est indépendant.

6. ADR
adr/

ADR-0001

ADR-0002

ADR-0003

...

Chaque ADR est autonome.

Versionné.

7. Prompts
prompts/

platform/

architecture/

engines/

tasks/

qa/

review/

evaluation/

Les prompts sont du code.

8. Contracts
contracts/

api/

events/

commands/

queries/

websocket/

crm/

voice/

Les contrats sont isolés.

9. Schemas
schemas/

json/

yaml/

protobuf/

database/

Tous les schémas partagés.

10. Packages

Les packages partagés.

packages/

core/

kernel/

sdk/

common/

telemetry/

security/

events/

auth/

storage/

llm/

Aucun métier ici.

11. Platform

Services transverses.

platform/

identity/

gateway/

runtime/

observability/

configuration/

scheduler/

notification/

Ces composants servent tous les Engines.

12. Engines

Le cœur du produit.

engines/

conversation/

crm/

evaluation/

analytics/

coaching/

knowledge/

voice/

reporting/

Chaque moteur est autonome.

13. Services

Services applicatifs.

services/

api/

websocket/

worker/

scheduler/

admin/

sync/

Ils orchestrent les moteurs.

14. Infrastructure
infrastructure/

docker/

kubernetes/

terraform/

ansible/

monitoring/

network/

Toute l'infrastructure est versionnée.

15. Deployments
deployments/

dev/

staging/

preprod/

production/

Chaque environnement possède sa configuration.

16. Datasets

Le projet versionne.

datasets/

golden/

benchmarks/

evaluation/

training/

fixtures/

Ces données servent aux tests et aux benchmarks.

17. Tools

Outils internes.

tools/

cli/

migration/

scaffold/

generator/

benchmark/

Ils accélèrent le développement.

18. Scripts

Scripts ponctuels.

scripts/

bootstrap/

maintenance/

cleanup/

release/

Les scripts critiques migrent ensuite vers des outils dédiés.

19. Tests
tests/

unit/

integration/

contract/

performance/

e2e/

chaos/

Les tests globaux du dépôt.

Les moteurs conservent également leurs tests locaux.

20. GitHub
.github/

workflows/

actions/

templates/

labels/

policies/

Toute l'automatisation GitHub.

21. Conventions de nommage

Exemples :

conversation_engine

crm_engine

evaluation_engine

voice_runtime

platform_gateway

Pas d'abréviations ambiguës.

22. README

Chaque dossier important possède :

README.md

Le README décrit :

responsabilité ;
architecture ;
dépendances ;
interfaces ;
exemples.
23. Ownership

Chaque répertoire possède un propriétaire.

Exemple.

owner:

reviewers:

team:

criticality:

Cela facilite les revues.

24. CODEOWNERS

Le dépôt utilise un fichier CODEOWNERS.

Exemple.

engines/conversation/

↓

Conversation Team

Principal Architect

Les revues sont automatisées.

25. Workspace Python

Le projet est organisé comme un workspace.

Chaque moteur reste installable indépendamment.

Exemple.

pip install -e engines/conversation

Cela accélère les tests locaux.

26. Gestion des dépendances

Règles.

Un Engine.

↓

Ne dépend jamais.

↓

D'un autre Engine.

Il dépend uniquement :

des Packages ;
des Contracts ;
des APIs internes ;
du Kernel.
27. Matrice des dépendances
Architecture

↓

Contracts

↓

Packages

↓

Platform

↓

Engines

↓

Services

↓

Applications

Les dépendances remontantes sont interdites.

28. Industrialisation

Le dépôt doit permettre.

développement local ;
CI ;
tests ;
génération de documentation ;
benchmarks ;
génération de prompts ;
génération de SDK.

Tout provient du même référentiel.

29. Bootstrap

Un nouveau développeur doit pouvoir lancer.

git clone

↓

bootstrap

↓

docker compose up

↓

pytest

↓

application opérationnelle

L'onboarding doit être inférieur à une heure.

30. Décisions d'architecture (ADR)

Ce volume formalise les principes suivants :

Monorepo unique.
Architecture documentaire intégrée.
Moteurs isolés.
Packages partagés.
Infrastructure versionnée.
Documentation co-localisée.
Ownership explicite.
31. Critères d'acceptation

Le Blueprint du dépôt est considéré conforme lorsque :

chaque composant possède un emplacement défini ;
les dépendances sont unidirectionnelles ;
les responsabilités sont clairement séparées ;
les conventions de nommage sont homogènes ;
le dépôt est directement exploitable par les développeurs et les agents IA.
🏛️ Décision d'architecture majeure : Repository as an Operating System (RaOS)

Je recommande de considérer le dépôt Git comme un Repository Operating System.

Il ne contient pas seulement du code.

Il contient :

l'architecture ;
les décisions ;
les contrats ;
les données de test ;
les prompts ;
les pipelines ;
les outils ;
les procédures d'exploitation.

Ainsi, un nouveau développeur — ou un nouvel agent IA — peut reconstruire le système en s'appuyant uniquement sur le dépôt, sans dépendre d'une connaissance implicite.

📘 Prochaine étape : F2 — API Contracts & Communication Architecture

Le prochain volume définira l'ensemble des interfaces de communication de la plateforme :

conventions REST ;
API Gateway ;
WebSocket temps réel ;
contrats d'événements (Event Bus) ;
Commandes et Requêtes (CQRS) ;
contrats CRM fictif ;
API Voice (STT/TTS) ;
versionnement des API ;
stratégie de compatibilité ascendante.

Ce document servira de base à la génération des SDK, des clients Frontend et des intégrations externes, garantissant une communication cohérente entre tous les composants d'ATOS.
