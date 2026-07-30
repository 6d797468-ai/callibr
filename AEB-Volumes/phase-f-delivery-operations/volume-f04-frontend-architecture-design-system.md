# Volume F04 — Frontend Architecture & Design System

> Extrait généré depuis `Architecture & Engineering Book (AEB).md` le 2026-07-27.

PHASE F — DELIVERY, IMPLEMENTATION & ENTERPRISE OPERATIONS
Volume F4
Frontend Architecture & Design System

Version : 1.0

Statut : Référence d'implémentation

Criticité : Critique

1. Vision

Le Frontend est :

une application SaaS multi-tenant ;
une interface temps réel ;
un poste de travail pour l'agent ;
un cockpit pour le formateur ;
un portail d'administration.

Toutes les interfaces partagent le même Design System.

2. Stack recommandée
Domaine	Technologie
Framework	Next.js 16+
Langage	TypeScript
UI	React
Styling	TailwindCSS
Composants	shadcn/ui
Icônes	Lucide
Gestion d'état local	Zustand
Gestion des données	TanStack Query
Formulaires	React Hook Form
Validation	Zod
Graphiques	Apache ECharts
Temps réel	WebSocket
Auth	OAuth2 / OIDC
3. Architecture générale
apps/web/

│

├── app/

├── features/

├── domains/

├── components/

├── layouts/

├── hooks/

├── lib/

├── services/

├── store/

├── providers/

├── styles/

└── assets/
4. Architecture Feature Driven

Chaque fonctionnalité est autonome.

features/

conversation/

crm/

evaluation/

analytics/

voice/

knowledge/

training/
5. Architecture Domain Driven
domains/

simulation/

persona/

scenario/

tenant/

user/

evaluation/

La logique métier reste proche du domaine.

6. Organisation d'une Feature

Exemple.

conversation/

components/

hooks/

pages/

api/

store/

types/

schemas/

utils/
7. Routing

Next.js App Router.

/

login

/dashboard

/simulations

/scenarios

/personas

/evaluations

/settings

/admin
8. Layouts

Trois layouts principaux.

PublicLayout

DashboardLayout

SimulationLayout

Le changement de contexte est instantané.

9. Providers

Le Frontend utilise plusieurs Providers.

Auth

Theme

Query

WebSocket

Notifications

Tenant

Internationalization

Ils sont centralisés.

10. Gestion d'état

Découpage recommandé.

Type	Solution
Données serveur	TanStack Query
État UI	Zustand
Formulaires	React Hook Form
Temps réel	WebSocket Store

Chaque état a une responsabilité unique.

11. Design System

Le système comprend :

couleurs ;
typographie ;
espacements ;
composants ;
animations ;
icônes ;
grilles.

Toutes les interfaces utilisent ces fondations.

12. Tokens

Exemple.

color.primary

color.success

color.warning

color.error

spacing.md

radius.lg

shadow.md

Les thèmes reposent sur ces tokens.

13. Composants

Bibliothèque commune.

Button

Input

Card

Modal

Dialog

Toast

Table

Tabs

Badge

Avatar

Tooltip
14. Composants métier

Exemples.

ConversationWindow

CRMPanel

EmotionGauge

ScenarioTimeline

EvaluationCard

CoachFeedback

VoiceRecorder

Ils encapsulent la logique métier.

15. Simulation Workspace

L'écran principal est découpé en panneaux.

┌──────────────────────────────────────────────┐
│ Toolbar                                      │
├──────────────┬───────────────────────────────┤
│ CRM          │ Conversation                  │
│              │                               │
│              │                               │
├──────────────┼───────────────────────────────┤
│ Procedure    │ Timeline                      │
├──────────────┼───────────────────────────────┤
│ Metrics      │ AI Assistant                  │
└──────────────┴───────────────────────────────┘

Cette disposition optimise le travail du stagiaire.

16. Fenêtre de conversation

Affiche :

messages ;
indicateurs de frappe ;
état émotionnel ;
temps de réponse ;
actions CRM.

Le rendu est en temps réel.

17. CRM fictif

Le panneau CRM permet :

rechercher un client ;
vérifier l'identité ;
créer un ticket ;
appliquer un geste commercial ;
consulter l'historique.

Les actions sont synchronisées avec le moteur de simulation.

18. Tableau de bord formateur

Il présente :

progression des apprenants ;
scores QA ;
statistiques ;
relecture des conversations ;
comparaisons.

Les données sont agrégées.

19. Tableau de bord administrateur

Fonctions :

gestion des tenants ;
licences ;
utilisateurs ;
modèles IA ;
Domain Packs ;
paramètres globaux.
20. Temps réel

Le Frontend écoute notamment :

conversation.message

crm.updated

emotion.changed

voice.partial

voice.final

evaluation.updated

notification.created

Les composants se mettent à jour sans rechargement.

21. Notifications

Types :

information ;
succès ;
avertissement ;
erreur ;
tâche terminée.

Une file unique gère leur affichage.

22. Accessibilité

Objectifs :

navigation clavier complète ;
compatibilité avec les lecteurs d'écran ;
contraste conforme ;
composants accessibles ;
gestion du focus.

La conformité WCAG 2.2 AA est la cible.

23. Internationalisation

Architecture prévue :

fr

en

es

de

ar

Toutes les chaînes sont externalisées.

Les scénarios peuvent être multilingues.

24. Responsive

Trois modes principaux.

Desktop (prioritaire)
Tablette
Mobile (consultation et administration légère)

Le poste de simulation est optimisé pour les grands écrans.

25. Performance

Objectifs indicatifs :

Indicateur	Cible
First Contentful Paint	< 2 s
Interaction initiale	< 3 s
Changement de page	< 500 ms
Réception WebSocket	Temps réel
26. Sécurité

Le Frontend :

ne contient aucun secret ;
valide les permissions avant affichage ;
applique les contrôles RBAC/ABAC transmis par le Backend ;
protège contre les attaques XSS et CSRF selon les mécanismes adaptés.
27. Tests

Chaque composant dispose de :

tests unitaires ;
tests d'intégration ;
tests visuels ;
tests d'accessibilité.

Les parcours critiques sont couverts par des tests de bout en bout.

28. Décisions d'architecture (ADR)

Ce volume formalise les principes suivants :

Architecture Feature Driven.
Design System unique.
Gestion d'état spécialisée.
Temps réel par WebSocket.
Internationalisation native.
Accessibilité intégrée.
Composants métier réutilisables.
29. Critères d'acceptation

Le Frontend est considéré conforme lorsque :

toutes les fonctionnalités utilisent le Design System ;
les composants sont réutilisables ;
les états sont clairement séparés ;
les interfaces temps réel fonctionnent sans rechargement ;
les tableaux de bord restent cohérents entre domaines.
🏛️ Décision d'architecture majeure : Frontend Operating System (FOS)

Je recommande de concevoir le Frontend comme un Frontend Operating System.

Le Design System, les Providers, les composants métier, la gestion d'état et les mécanismes temps réel constituent une plateforme commune sur laquelle viennent se brancher les différents Domain Packs (SAV, Télévente, Support, Recouvrement, etc.).

Cette approche garantit une expérience utilisateur homogène tout en permettant d'ajouter de nouveaux domaines métier avec un impact limité sur le reste de l'application.

📘 Prochaine étape : F5 — Implementation Roadmap & Sprint Execution Plan

Le prochain volume transformera l'architecture en plan d'exécution opérationnel :

organisation des Epics ;
découpage en Features et User Stories ;
planification des sprints ;
dépendances entre modules ;
critères de "Definition of Ready" et "Definition of Done" ;
stratégie POC → MVP → Beta → Enterprise → Production ;
jalons de validation technique, métier et IA.

Ce document servira de feuille de route détaillée pour piloter le développement d'ATOS jusqu'à sa mise en production.
