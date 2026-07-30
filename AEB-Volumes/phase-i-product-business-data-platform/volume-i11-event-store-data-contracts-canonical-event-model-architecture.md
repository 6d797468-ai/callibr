# Volume I11 — Event Store, Data Contracts & Canonical Event Model Architecture

> Extrait généré depuis `Architecture & Engineering Book (AEB).md` le 2026-07-27.

PHASE I — DATA PLATFORM & KNOWLEDGE SYSTEM
Volume I11
Event Store, Data Contracts & Canonical Event Model Architecture

Version : 1.0

Statut : Enterprise Data Foundation

Criticité : Critique

1. Vision

La Data Platform commence par les événements.

Dans Callibr, chaque action significative doit devenir un fait métier observable :

simulation démarrée ;
message échangé ;
action CRM exécutée ;
règle appliquée ;
score calculé ;
compétence mise à jour ;
coût IA mesuré ;
incident détecté ;
configuration modifiée.

L'Event Store devient la mémoire factuelle de la plateforme.

2. Principe fondamental

Une donnée analytique fiable ne doit pas être reconstruite à partir de tables applicatives instables.

Elle doit provenir d'événements métiers versionnés, horodatés et corrélés.

Modèle recommandé :

Command

↓

Domain Logic

↓

Domain Event

↓

Event Store

↓

Projections

↓

Analytics / Audit / BI / ML

3. Architecture globale

                    Platform Domains


                           │


                           ▼


                    Domain Events


                           │


          ┌────────────────┼────────────────┐


          ▼                ▼                ▼


      Event Store      Event Bus       Contract Registry


          │                │                │


          ▼                ▼                ▼


     Projections      Data Products     Audit & Lineage

4. Responsabilités

L'Event Store fournit :

persistance immuable ;
ordre logique ;
correlation_id ;
causation_id ;
tenant_id ;
version de schéma ;
rejeu ;
snapshot ;
audit ;
publication vers les pipelines data.

5. Canonical Event Model

Tous les événements suivent une enveloppe commune.

Exemple :

{
  "event_id": "evt_01",
  "event_type": "simulation.completed",
  "event_version": "1.0.0",
  "tenant_id": "tenant_001",
  "workspace_id": "workspace_001",
  "aggregate_id": "simulation_123",
  "aggregate_type": "simulation",
  "occurred_at": "2026-07-27T21:00:00Z",
  "correlation_id": "trace_abc",
  "causation_id": "cmd_xyz",
  "payload": {},
  "metadata": {}
}

6. Event Categories

Familles :

identity events ;
tenant events ;
simulation events ;
conversation events ;
CRM events ;
scenario events ;
evaluation events ;
learning events ;
AI runtime events ;
billing events ;
integration events ;
security events ;
system events.

7. Event Contract Registry

Chaque type d'événement possède :

nom ;
description ;
owner ;
version ;
schéma ;
compatibilité ;
exemples ;
règles de rétention ;
classification data.

Le registry empêche la prolifération incontrôlée.

8. Versioning

Règles :

PATCH : correction compatible ;
MINOR : ajout compatible ;
MAJOR : rupture.

Un consommateur ne doit jamais recevoir une rupture sans version explicite.

9. Compatibility Rules

Compatible :

ajouter un champ optionnel ;
ajouter une valeur documentée ;
élargir une description.

Rupture :

supprimer un champ ;
changer un type ;
changer la signification ;
renommer un champ ;
modifier les unités.

10. Ordering

L'ordre global absolu n'est pas requis partout.

L'ordre doit être garanti au minimum par :

tenant ;
aggregate_id ;
session_id ;
conversation_id.

Cette granularité évite les verrous globaux.

11. Idempotence

Chaque événement possède :

event_id ;
idempotency_key ;
source ;
checksum optionnel.

Un consommateur peut retraiter sans créer de doublons métier.

12. Replay

Le replay sert à :

reconstruire des projections ;
recalculer des KPI ;
tester une nouvelle règle ;
auditer un incident ;
entraîner un modèle ;
valider une migration.

Les replays sont contrôlés par tenant et par plage temporelle.

13. Retention

Toutes les données n'ont pas la même durée de conservation.

Exemple :

security.audit : longue rétention ;
conversation.raw : rétention limitée ;
analytics.aggregate : longue rétention ;
ai.prompt.raw : rétention stricte et masquée.

14. Sensitive Event Payload

Les événements peuvent contenir des données sensibles.

Règles :

minimisation ;
masquage ;
chiffrement ;
classification ;
redaction ;
accès contrôlé ;
suppression logique lorsque nécessaire.

15. Projection Architecture

Les projections transforment les événements en vues lisibles.

Exemples :

SessionReadModel ;
AgentProgressView ;
TenantUsageView ;
QualityScoreView ;
BillingUsageView ;
OperationalDashboardView.

16. Data Model

EventRecord
-----------

event_id

event_type

event_version

tenant_id

aggregate_id

aggregate_type

occurred_at

payload

metadata

schema_id

EventSchema
-----------

schema_id

event_type

version

json_schema

owner

status

ProjectionCheckpoint
--------------------

projection_id

tenant_id

last_event_id

last_processed_at

status

17. API interne

Publier événement :

POST /data/events

Lire stream :

GET /data/events/streams/{aggregate_id}

Lister contrats :

GET /data/event-contracts

Lancer replay :

POST /data/events/replay

18. Observabilité

Métriques :

events_per_second ;
consumer_lag ;
projection_delay ;
schema_validation_errors ;
replay_duration ;
dead_letter_events ;
event_store_storage.

19. Décisions d'architecture (ADR)

ADR-I11-001
Les événements métiers sont la base de la Data Platform.

Décision :

Les analyses critiques dérivent d'événements versionnés.

ADR-I11-002
Tous les événements ont une enveloppe canonique.

Décision :

Garantir cohérence, traçabilité et automatisation.

ADR-I11-003
Le replay est une capacité de plateforme.

Décision :

Permettre reconstruction, audit et recalcul.

ADR-I11-004
Les schémas d'événements sont gouvernés.

Décision :

Empêcher les ruptures silencieuses.

20. Critères d'acceptation

Event Store conforme lorsque :

les événements sont immuables ;
les contrats sont versionnés ;
les projections sont reconstructibles ;
les replays sont auditables ;
les données sensibles sont protégées ;
les consommateurs peuvent être idempotents ;
les métriques de lag sont disponibles.

Décision majeure : Event Memory Backbone

La plateforme adopte un Event Memory Backbone.

Le système ne dépend plus seulement de l'état courant.

Il conserve la séquence des faits qui ont produit cet état.
