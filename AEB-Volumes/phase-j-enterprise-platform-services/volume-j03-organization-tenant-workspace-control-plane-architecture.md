# Volume J03 — Organization, Tenant & Workspace Control Plane Architecture

> Extrait généré depuis `Architecture & Engineering Book (AEB).md` le 2026-07-27.

PHASE J — ENTERPRISE PLATFORM SERVICES
Volume J03
Organization, Tenant & Workspace Control Plane Architecture

Version : 1.0

Statut : Enterprise SaaS Foundation

Criticité : Critique

1. Vision

Le Control Plane organisationnel structure tous les clients.

Il définit :

tenant ;
organization ;
business unit ;
workspace ;
team ;
project ;
campaign.

2. Principe fondamental

Une entreprise cliente n'est pas plate.

Elle possède une hiérarchie opérationnelle.

Cette hiérarchie doit être modélisée pour permissions, reporting, billing, data isolation et configuration.

3. Architecture globale

                    Tenant


                       │


                    Organization


                       │


        ┌──────────────┼──────────────┐


        ▼              ▼              ▼


 Business Unit     Workspace        Team


                       │


                       ▼


                 Programs / Campaigns

4. Tenant

Frontière principale :

sécurité ;
données ;
contrat ;
billing ;
configuration ;
observabilité.

5. Organization

Représente une entité client.

Un tenant peut contenir plusieurs organizations selon contrat.

6. Workspace

Espace de travail isolé pour :

programme de formation ;
pays ;
site ;
marque ;
client final BPO ;
équipe métier.

7. Configuration Inheritance

Hiérarchie :

platform default ;
tenant ;
organization ;
workspace ;
project ;
session.

Chaque niveau peut surcharger avec contrôle.

8. Lifecycle

Tenant :

created ;
provisioning ;
active ;
suspended ;
archived ;
deleted.

Workspace :

draft ;
active ;
paused ;
archived.

9. Data Model

Tenant
------

id

name

status

region

plan_id

Organization
------------

id

tenant_id

name

type

Workspace
---------

id

tenant_id

organization_id

name

settings

Team
----

id

workspace_id

name

10. API interne

Créer tenant :

POST /org-control/tenants

Créer workspace :

POST /org-control/workspaces

Lire hiérarchie :

GET /org-control/tenants/{id}/tree

11. Décisions d'architecture (ADR)

ADR-J03-001
Le tenant est la frontière de sécurité.

Décision :

Toutes les ressources critiques portent tenant_id.

ADR-J03-002
La configuration suit une hiérarchie contrôlée.

Décision :

Permettre personnalisation sans divergence incontrôlée.

ADR-J03-003
Les workspaces sont des frontières opérationnelles.

Décision :

Séparer programmes, pays, marques et équipes.

ADR-J03-004
Le lifecycle est explicite.

Décision :

Industrialiser provisioning, suspension et archivage.

12. Critères d'acceptation

Control Plane conforme lorsque :

les tenants sont provisionnables ;
les workspaces sont isolés ;
la hiérarchie est interrogeable ;
les configurations héritent correctement ;
les états lifecycle sont appliqués ;
les métriques sont filtrables par niveau.

Décision majeure : Organizational Control Plane

La structure client devient une capacité de plateforme, pas un champ secondaire.
