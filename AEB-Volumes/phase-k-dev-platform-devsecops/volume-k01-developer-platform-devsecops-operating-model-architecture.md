# Volume K01 — Developer Platform & DevSecOps Operating Model Architecture

> Extrait généré depuis `Architecture & Engineering Book (AEB).md` le 2026-07-27.

PHASE K — DEV PLATFORM, DEVSECOPS & PLATFORM ENGINEERING
Volume K01
Developer Platform & DevSecOps Operating Model Architecture

Version : 1.0

Statut : Platform Engineering Foundation

Criticité : Critique

1. Vision

La Developer Platform fournit aux équipes et aux agents IA un environnement cohérent pour développer Callibr.

Elle doit réduire :

friction ;
erreurs manuelles ;
temps d'onboarding ;
écarts entre environnements ;
dette opérationnelle.

2. Principe fondamental

La plateforme de développement est un produit interne.

Ses utilisateurs sont :

développeurs ;
architectes ;
QA ;
SRE ;
security engineers ;
data engineers ;
AI engineers ;
agents IA de développement.

3. Architecture globale

                    Developer Experience


                           │


                           ▼


                    Internal Developer Platform


        ┌──────────────────┼──────────────────┐


        ▼                  ▼                  ▼


 Templates          Pipelines          Environments


        │                  │                  │


        ▼                  ▼                  ▼


 Golden Paths       Security Gates     Observability

4. Golden Paths

Un Golden Path définit la façon recommandée de créer :

service API ;
engine ;
worker ;
connector ;
domain pack ;
frontend module ;
data pipeline ;
agent IA.

5. Developer Portal

Le portail interne expose :

catalogue services ;
owners ;
docs ;
runbooks ;
dashboards ;
pipelines ;
environnements ;
templates ;
SLO ;
incidents.

6. Self-Service

Les équipes peuvent créer :

repository module ;
service skeleton ;
database schema ;
topic event ;
feature flag ;
secret request ;
dashboard ;
environment preview.

Tout self-service reste gouverné.

7. DevSecOps Model

La sécurité est intégrée dans :

design ;
code ;
dependencies ;
containers ;
CI ;
CD ;
runtime ;
observability ;
incident response.

8. Engineering Guardrails

Contrôles :

lint ;
typing ;
unit tests ;
contract tests ;
security scan ;
secret scan ;
dependency scan ;
container scan ;
IaC scan ;
policy check.

9. Data Model

ServiceCatalogEntry
-------------------

id

name

owner

type

criticality

repository

runtime

GoldenPathTemplate
------------------

id

name

component_type

version

owner

PlatformRequest
---------------

id

request_type

requested_by

status

approval_required

10. API interne

Créer composant :

POST /dev-platform/components

Lister services :

GET /dev-platform/catalog

Créer environnement preview :

POST /dev-platform/environments/preview

11. Décisions d'architecture (ADR)

ADR-K01-001
La Developer Platform est un produit interne.

Décision :

Mesurer et améliorer l'expérience développeur.

ADR-K01-002
Les Golden Paths sont obligatoires pour les nouveaux composants.

Décision :

Réduire divergence et dette.

ADR-K01-003
La sécurité est intégrée au pipeline.

Décision :

Détecter les risques tôt.

ADR-K01-004
Le catalogue de services est source de vérité.

Décision :

Identifier ownership et criticité.

12. Critères d'acceptation

Developer Platform conforme lorsque :

les composants sont catalogués ;
les Golden Paths existent ;
les templates génèrent des services conformes ;
les contrôles sécurité tournent automatiquement ;
les environnements preview sont possibles ;
les owners sont identifiés.

Décision majeure : Internal Developer Platform as Product

Callibr adopte une plateforme développeur interne pour industrialiser l'ingénierie.
