# Volume B07 — CRM Runtime Engine (CRE)

> Extrait généré depuis `Architecture & Engineering Book (AEB).md` le 2026-07-27.

PHASE B — ARCHITECTURE MÉTIER
Volume B7
CRM Runtime Engine (CRE)

Version : 1.0

Statut : Architecture de Référence

Criticité : Critique

1. Vision

Le CRM Runtime Engine est un Digital Twin (jumeau numérique) d'un CRM de centre de contacts.

Il ne s'agit pas d'une base de données contenant quelques clients fictifs.

Il simule :

les clients ;
les contrats ;
les produits ;
les commandes ;
les incidents ;
les factures ;
les paiements ;
les interventions ;
les workflows ;
les autorisations.

Le CRM devient un véritable acteur de la simulation.

2. Pourquoi un CRM Runtime ?

Un agent expérimenté ne fait pas que parler.

Pendant un appel il :

recherche le client
vérifie l'identité
consulte les contrats
ouvre un ticket
applique une remise
consulte les incidents
planifie un rendez-vous
change une offre
ferme un dossier

Notre plateforme doit entraîner ces compétences.

3. Architecture
CRM Runtime Engine

├── Customer Engine
├── Product Engine
├── Contract Engine
├── Subscription Engine
├── Billing Engine
├── Payment Engine
├── Incident Engine
├── Ticket Engine
├── Order Engine
├── Appointment Engine
├── CRM Workflow Engine
├── Permission Engine
├── Search Engine
├── History Engine
├── Audit Engine
└── Event Publisher
4. Bounded Contexts

Le CRM est découpé.

CRM

├── Customers

├── Products

├── Contracts

├── Billing

├── Payments

├── Orders

├── Tickets

├── Knowledge

├── Appointments

└── History

Chaque contexte est indépendant.

5. Customer Aggregate

Le client est un Aggregate.

Customer

│

├── Identity

├── Contacts

├── Addresses

├── Contracts

├── Products

├── Invoices

├── Tickets

├── Notes

├── Preferences

└── History
6. Identity

Exemple.

Customer

id

first_name

last_name

birth_date

customer_number

identity_level

security_questions

preferred_language

Le niveau de vérification est stocké.

7. Products

Exemple.

Internet

Téléphone

TV

Assurance

Cloud

Mobile

VPN

Pack

Le produit est indépendant du scénario.

8. Contrats
Contract

status

start_date

end_date

renewal

commitment

monthly_price

options
9. Facturation

Chaque facture possède.

Invoice

amount

status

due_date

payment_date

payment_method

balance
10. Tickets
Ticket

priority

severity

owner

status

category

sla

resolution
11. Historique

Le CRM conserve.

Tous les appels

Tous les emails

Tous les tickets

Toutes les commandes

Tous les paiements

Toutes les interventions

L'historique est exploitable pendant la simulation.

12. Recherche

Le moteur de recherche doit permettre.

Recherche :

nom
téléphone
contrat
facture
ticket
email
numéro client

Temps cible.

< 100 ms

13. Les Actions CRM

Toutes les actions passent par des commandes.

Jamais directement.

Exemple.

VerifyIdentity

↓

Command
CreateTicket

↓

Command
ApplyDiscount

↓

Command
UpdateAddress

↓

Command
ScheduleTechnician

↓

Command
14. Pipeline d'une action
Agent

↓

Clique

↓

Frontend

↓

API

↓

Command

↓

Rule Engine

↓

CRM Runtime

↓

Event

↓

Simulation Engine

↓

Prompt Compiler

Le LLM apprend immédiatement que l'état CRM a changé.

15. Exemple

Agent.

Clique.

Créer ticket

Le CRM.

Ticket

Status

OPEN

Produit.

TicketCreated

Le Prompt Compiler reçoit.

Ticket créé.

Le client attend maintenant une confirmation.
16. Workflows

Le CRM possède des workflows.

Incident.

Ouvert

↓

Assigné

↓

Diagnostic

↓

Résolution

↓

Validation

↓

Fermé

Commande.

Créée

↓

Paiement

↓

Préparation

↓

Expédition

↓

Livrée
17. Permissions

Toutes les actions sont contrôlées.

Exemple.

Agent Junior.

Peut

Créer ticket

×

Ne peut pas

Appliquer remise

Agent Senior.

Créer ticket

✓

Escalade

✓

Remise

✓
18. Historique Temps Réel

Chaque action est enregistrée.

Timestamp

Utilisateur

Action

Résultat

Durée

Session
19. Dataset Simulation

Le CRM n'utilise pas de données codées en dur.

Il charge des jeux de données.

Exemple.

Dataset

Télécom

100 000 clients
Dataset

Banque

250 000 clients
Dataset

Assurance

80 000 contrats

Les datasets sont interchangeables.

20. Générateur de Données

Le système intègre un Synthetic Data Generator.

Il produit :

clients
contrats
adresses
paiements
commandes
tickets

Ces données sont cohérentes entre elles.

Par exemple, un client ne pourra pas posséder un contrat mobile créé avant sa date de naissance.

21. Digital Twin

Le CRM Runtime est conçu comme un jumeau numérique.

Deux modes sont prévus.

Mode Standard

Données entièrement fictives.

Mode Enterprise

Import d'un modèle métier.

Exemple.

SAP

↓

Mapping

↓

CRM Runtime

ou

Salesforce

↓

Mapping

↓

CRM Runtime

Le client réel n'est jamais importé.

Seule la structure métier est reproduite.

22. Event Publishing

Toutes les modifications produisent un événement.

IdentityVerified

TicketCreated

DiscountApplied

InvoicePaid

AddressUpdated

AppointmentScheduled

ContractModified

Le reste du système se synchronise via ces événements.

23. Audit

Le CRM Runtime est entièrement audité.

Chaque action enregistre :

utilisateur ;
rôle ;
commande ;
résultat ;
règle appliquée ;
durée ;
identifiant de session.

Cette traçabilité facilite les analyses pédagogiques.

24. Décisions d'architecture (ADR)

Ce volume fixe plusieurs décisions importantes :

Le CRM est piloté par des commandes (Command Pattern).
Les modifications d'état passent par le Rule Engine.
Toutes les actions produisent des événements.
Les données sont synthétiques et versionnées.
Le modèle métier est indépendant du secteur d'activité.
Les workflows sont configurables.
25. Critères d'acceptation

Le CRM Runtime Engine sera considéré conforme lorsque :

un secteur métier peut être ajouté sans modifier le moteur ;
les actions sont validées par le Rule Engine ;
les workflows sont configurables ;
les données sont cohérentes et reproductibles ;
chaque action est auditée ;
le moteur peut être utilisé sans aucun LLM.
📌 Nouvelle décision stratégique (Architecture V2)

Après sept volumes, une évolution naturelle se dessine.

Je recommande désormais de ne plus considérer la plateforme comme un simple Simulation Operating Platform, mais comme un AI Training Operating System (ATOS).

Pourquoi ce changement ?

Le moteur que nous construisons est suffisamment générique pour entraîner :

des agents de centres de contacts ;
des commerciaux ;
des conseillers bancaires ;
des agents d'assurance ;
des opérateurs industriels ;
des techniciens de maintenance ;
des agents administratifs ;
des assistants médicaux.

Le domaine « centre de contacts » devient alors un plugin métier, et non le cœur du système.

Conséquences

Le Core Kernel reste inchangé :

Session Engine
Rule Engine
Scenario Engine
Prompt Orchestration Engine
CRM Runtime Engine
Evaluation Engine
Analytics Engine

Les domaines métier (Télécom, Banque, Assurance, Santé, Administration, etc.) deviennent des packs de simulation qui s'appuient sur ce noyau.

C'est une décision d'architecture majeure. Elle augmente la complexité initiale, mais elle transforme la plateforme en un véritable système d'exploitation pour la simulation et la formation assistées par IA, capable d'évoluer bien au-delà du seul secteur des centres de contacts. Cette décision devra être évaluée en fonction de la stratégie produit et des ressources disponibles, mais elle offre un potentiel de réutilisation et d'extension très important.
