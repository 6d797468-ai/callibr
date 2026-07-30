# Volume C03 — Enterprise Multi-Tenant SaaS Architecture

> Extrait généré depuis `Architecture & Engineering Book (AEB).md` le 2026-07-27.

PHASE C — PLATFORM CORE ARCHITECTURE
Volume C3
Enterprise Multi-Tenant SaaS Architecture

Version : 1.0

Statut : Architecture de Référence

Criticité : Critique

1. Vision

Le multi-tenant ne consiste pas uniquement à séparer les données.

Il faut également isoler :

les utilisateurs ;
les permissions ;
les workflows ;
les modèles IA ;
les scénarios ;
les métriques ;
les coûts ;
les quotas ;
les configurations.

Chaque client doit avoir l'impression de disposer de sa propre plateforme.

2. Les niveaux d'isolation

Notre architecture distingue plusieurs niveaux.

Platform

↓

Tenant

↓

Organization

↓

Workspace

↓

Project

↓

Training Campaign

↓

Simulation Session

Chaque niveau possède son propre contexte.

3. Hiérarchie
ATOS Platform

│

├── Tenant

│      │

│      ├── Organization

│      │       │

│      │       ├── Business Unit

│      │       │        │

│      │       │        ├── Team

│      │       │        │      │

│      │       │        │      └── Users

Cette hiérarchie couvre la majorité des structures d'entreprise.

4. Tenant

Le Tenant représente un client SaaS.

Exemple.

Tenant

id

name

slug

status

plan

region

timezone

language

branding

Le Tenant constitue la frontière principale d'isolation.

5. Organization

Une entreprise peut gérer plusieurs organisations.

Exemple.

Orange

↓

France

↓

Maroc

↓

Espagne

Chaque organisation possède ses propres équipes et campagnes.

6. Business Unit

Exemple.

Support

Commercial

Recouvrement

Technique

VIP

Back Office

Les Business Units permettent de spécialiser les scénarios et les KPI.

7. Workspace

Le Workspace isole un environnement de travail.

Exemples.

Production
Formation
Certification
Sandbox

Les Workspaces peuvent disposer de configurations distinctes.

8. Projects

Chaque projet regroupe.

scénarios ;
personas ;
jeux de données ;
règles ;
modèles IA ;
rapports.

Les projets facilitent la gestion de plusieurs programmes de formation.

9. Campagnes

Une campagne représente un ensemble de simulations.

Exemple.

Onboarding Septembre 2026

↓

200 agents

↓

15 scénarios

↓

Certification finale
10. Sessions

Une session est toujours liée à :

un utilisateur ;
un scénario ;
une campagne (optionnelle) ;
un tenant ;
un workspace.

Elle constitue l'unité de travail élémentaire.

11. RBAC

Les rôles sont hiérarchiques.

Platform Admin

↓

Tenant Admin

↓

Organization Admin

↓

Training Manager

↓

QA Manager

↓

Team Leader

↓

Trainer

↓

Agent

↓

Observer

Les permissions sont héritées.

12. ABAC

En complément du RBAC, des attributs peuvent être utilisés.

Exemple.

Department = Support

Region = Morocco

Language = French

Level = Senior

Une règle peut alors autoriser ou refuser une action selon ces attributs.

13. Context Security

Chaque requête transporte un contexte complet.

tenant_id

organization_id

workspace_id

project_id

campaign_id

user_id

role

permissions

trace_id

Aucun moteur ne travaille sans ce contexte.

14. Isolation des données

Trois modèles sont prévus.

Niveau 1 – MVP

Base PostgreSQL partagée avec tenant_id et politiques de sécurité au niveau des lignes (Row-Level Security).

Niveau 2 – Enterprise

Une base PostgreSQL par Tenant.

Niveau 3 – Dedicated

Une infrastructure complète par client.

Cette stratégie permet d'adapter le coût au niveau d'exigence.

15. Isolation des fichiers

Chaque Tenant possède son espace.

storage/

tenant-001/

tenant-002/

tenant-003/

Aucun partage de fichiers.

16. Isolation des événements

Les événements portent toujours :

tenant_id

organization_id

workspace_id

Les consommateurs ignorent les événements des autres tenants.

17. Isolation des caches

Redis est partitionné.

tenant:001:...

tenant:002:...

tenant:003:...

Les clés ne se mélangent jamais.

18. Isolation des modèles IA

Chaque Tenant peut choisir.

OpenAI

Anthropic

Mistral

Ollama

vLLM

Azure OpenAI

Le choix est une configuration, pas une dépendance du code.

19. Domain Packs

Chaque Tenant peut installer.

Télécom

Banque

Assurance

Santé

Retail

Les packs sont indépendants.

20. Branding

Chaque Tenant personnalise.

logo ;
couleurs ;
domaine ;
emails ;
certificats ;
rapports.

Le White Label est un objectif de conception.

21. Licences

Le moteur de licences gère.

nombre d'agents ;
nombre de formateurs ;
scénarios ;
stockage ;
minutes voix ;
appels LLM ;
API.

Les quotas sont vérifiés par le Kernel.

22. Facturation

Chaque Tenant expose des métriques de consommation.

Exemples.

Nombre de simulations

↓

Minutes de voix

↓

Tokens IA

↓

Stockage

↓

API Calls

Ces données alimentent la facturation et les tableaux de bord.

23. Régions

Le déploiement peut être régional.

Exemple.

Europe

↓

France
Afrique

↓

Maroc
Amérique

↓

Canada

Les données restent dans la région choisie lorsque les contraintes réglementaires l'exigent.

24. API Multi-Tenant

Toutes les API exigent un contexte.

Exemple.

GET /api/v1/simulations

Headers

X-Tenant-ID

Authorization

X-Workspace-ID

Le Gateway valide le contexte avant toute exécution.

25. Audit

Chaque action journalise.

tenant ;
utilisateur ;
rôle ;
adresse IP (si activée) ;
ressource ;
action ;
résultat ;
trace_id.

Les journaux sont isolés par Tenant.

26. Sauvegarde

Les stratégies sont configurables.

sauvegarde globale ;
sauvegarde par Tenant ;
restauration sélective ;
export des données.

Chaque client peut récupérer uniquement ses propres données.

27. Décisions d'architecture (ADR)

Ce volume fixe les décisions suivantes :

Tous les moteurs sont multi-tenant par conception.
Le contexte de sécurité est obligatoire.
Le RBAC est complété par l'ABAC.
Les Domain Packs sont installables par Tenant.
Les modèles IA sont configurables par Tenant.
Trois niveaux d'isolation des données sont supportés.
Le White Label est une capacité native.
28. Critères d'acceptation

L'architecture Multi-Tenant sera considérée conforme lorsque :

un Tenant ne peut jamais accéder aux données d'un autre ;
les quotas sont appliqués de manière déterministe ;
les permissions sont évaluées avant toute action ;
les Domain Packs sont indépendants ;
les métriques de consommation sont disponibles par Tenant ;
la plateforme peut évoluer d'un mode mutualisé vers un déploiement dédié sans refonte du code.
🏛️ Décision d'architecture majeure : Configuration as Code (CaC)

À partir de ce volume, je recommande que toutes les personnalisations d'un Tenant soient déclaratives.

Concrètement :

les rôles ;
les politiques de sécurité ;
les scénarios ;
les règles métier ;
les personas ;
les workflows ;
les packs métier ;
les configurations LLM ;
les quotas.

…doivent être définis dans des fichiers de configuration versionnés (YAML ou JSON), plutôt que codés en dur.

Exemple :

tenant:
  id: telecom-fr
branding:
  primary_color: "#0055A4"
llm:
  provider: openai
  model: gpt-5.5
domain_packs:
  - telecom
features:
  voice: true
  coaching_realtime: true
quotas:
  monthly_simulations: 50000

Cette approche apporte plusieurs avantages :

déploiements reproductibles ;
gestion des changements par Git ;
audit des configurations ;
automatisation des environnements ;
réduction des développements spécifiques.
Prochain volume : C4 — API Gateway, SDK & Integration Platform

Nous définirons :

l'API REST publique ;
les WebSockets et le streaming ;
les contrats OpenAPI ;
les SDK Python et TypeScript ;
les Webhooks ;
les connecteurs CRM/LMS/BI ;
la stratégie de versionnement des API ;
les mécanismes d'authentification (OAuth2, OIDC, API Keys) ;
les politiques de limitation de débit (Rate Limiting).

Ce volume constituera la porte d'entrée officielle de toute la plateforme, aussi bien pour le frontend que pour les intégrations externes.
