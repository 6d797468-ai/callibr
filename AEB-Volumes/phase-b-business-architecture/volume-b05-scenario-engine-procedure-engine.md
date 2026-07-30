# Volume B05 — Scenario Engine & Procedure Engine

> Extrait généré depuis `Architecture & Engineering Book (AEB).md` le 2026-07-27.

PHASE B — ARCHITECTURE MÉTIER
Volume B5
Scenario Engine & Procedure Engine

Version : 1.0

Statut : Architecture de Référence

Criticité : Critique

1. Objectif

Le Scenario Engine est responsable de :

charger un scénario
valider sa cohérence
instancier une simulation
suivre la progression
piloter les objectifs
appliquer les règles métier
communiquer avec le Simulation Engine

Le scénario est considéré comme une définition exécutable, et non comme un simple document descriptif.

2. Définition d'un scénario

Un scénario est un ensemble structuré comprenant :

Scénario

├── Métadonnées
├── Contexte
├── Client
├── Persona
├── CRM
├── Procédure
├── Objectifs
├── Difficulté
├── Variables
├── Conditions
├── Evènements
├── Evaluation
└── Fin
3. Architecture
Scenario Engine

├── Scenario Loader
├── Scenario Validator
├── Procedure Engine
├── Objective Engine
├── Condition Engine
├── Difficulty Engine
├── Event Dispatcher
├── Transition Manager
├── Scenario Runtime
└── Version Manager
4. Structure logique

Un scénario possède plusieurs couches.

Scénario

↓

Contexte

↓

Procédure

↓

Objectifs

↓

Variables

↓

Conditions

↓

Transitions

↓

Evaluation

Chaque couche est indépendante.

5. Métadonnées

Chaque scénario possède :

id:

code:

nom:

version:

langue:

secteur:

service:

niveau:

temps_estime:

auteur:

date_creation:

date_revision:

statut:
6. Contexte

Le contexte décrit la situation.

Exemple

Entreprise:

Fournisseur Internet

Produit:

Fibre 1 Gbps

Historique:

Client depuis 6 ans

Situation:

Connexion coupée depuis hier

Impact:

Télétravail impossible

Le LLM ne crée jamais ce contexte.

7. CRM Initial

Le scénario définit également l'état du CRM.

Exemple

Client

VIP

Contrat

Actif

Factures

Payées

Tickets ouverts

0

Adresse

Valide

Téléphone

Confirmé

Chaque simulation démarre avec cet état.

8. Variables

Chaque scénario possède ses propres variables.

Exemple

ConnexionActive

false

ModemAllume

true

ClientVIP

true

IncidentReseau

false

RemiseAutorisee

true

Les variables peuvent évoluer.

9. Difficulté

La difficulté est composée de plusieurs dimensions.

Variable	Exemple
Complexité technique	faible → élevée
Niveau émotionnel	calme → agressif
Nombre d'étapes	simple → long
Nombre de décisions	faible → élevé
Nombre d'actions CRM	faible → élevé
Ambiguïté	faible → élevée

La difficulté globale est calculée.

Elle n'est pas choisie arbitrairement.

10. Procédure

Une procédure est une suite d'étapes.

Exemple.

Accueil

↓

Identification

↓

Qualification

↓

Diagnostic

↓

Solution

↓

Validation

↓

Conclusion

Chaque entreprise pourra créer ses propres procédures.

11. Les étapes

Chaque étape possède :

Nom

Description

Objectif

Conditions d'entrée

Conditions de sortie

Actions CRM autorisées

Questions attendues

Erreurs possibles

Temps conseillé
12. Exemple

Identification

Entrée:

Conversation commencée

Sortie:

Client identifié

Actions CRM:

VerifyIdentity

Questions attendues:

Nom

Date naissance

Numéro client
13. Les objectifs

Les objectifs sont séparés de la procédure.

Exemple

Objectifs

↓

Identifier

↓

Créer Ticket

↓

Informer

↓

Résoudre

↓

Conclure

Un scénario peut réussir même si certains objectifs secondaires sont manqués.

14. Types d'objectifs
Obligatoires

Toujours requis.

Optionnels

Améliorent le score.

Cachés

Le stagiaire ne les connaît pas.

Exemple

Le client attend une excuse.

Le système le sait.

Pas l'agent.

Adaptatifs

Activés selon la situation.

15. Conditions

Le moteur gère les conditions.

Exemple

SI

Client VIP

ET

Panne >24h

↓

Autoriser geste commercial
SI

Paiement impayé

↓

Interdire remise
16. Conditions de réussite

Exemple

Identité vérifiée

ET

Incident créé

ET

Client informé

↓

Simulation réussie
17. Conditions d'échec

Exemple

Client raccroche

↓

Fin immédiate
Temps dépassé

↓

Echec
Violation procédure critique

↓

Echec
18. Arbre de transitions

Contrairement à un arbre figé, notre moteur utilise un graphe.

Accueil

↓

Identification

↓

Qualification

↓

Diagnostic

↓

Escalade

↓

Résolution

↓

Conclusion

Mais une branche peut revenir en arrière.

Diagnostic

↓

Information manquante

↓

Qualification

Le scénario reste flexible.

19. Evènements

Chaque étape peut produire des événements.

Exemple

IdentityVerified
CustomerUpset
TicketCreated
ProcedureCompleted
DiscountApplied
20. Timers

Chaque scénario peut définir :

Temps total

Temps réponse

Temps silence

Temps diagnostic

Temps résolution

Ces informations servent à l'évaluation.

21. Randomisation

Le moteur introduit des variations.

Exemple.

Nom du client.

Adresse.

Produit.

Montant facture.

Ancienneté.

Date.

Toutes ces données peuvent être tirées à partir d'un jeu de données.

Le scénario reste identique.

22. Variantes

Un scénario peut posséder plusieurs variantes.

Support Internet

↓

Version A

↓

Client calme
Support Internet

↓

Version B

↓

Client agressif
Support Internet

↓

Version C

↓

Client VIP

Le cœur du scénario est partagé.

23. Versionnement

Les scénarios sont immuables.

Exemple

Internet Support

↓

v1.0

↓

v1.1

↓

v2.0

Une simulation historique référence toujours la version utilisée.

24. Validation

Avant publication.

Le moteur vérifie.

procédure valide ;
objectifs cohérents ;
transitions accessibles ;
conditions non contradictoires ;
variables définies ;
personas compatibles ;
actions CRM existantes.

Un scénario invalide ne peut jamais être publié.

25. DSL (Domain Specific Language)

Plutôt que de coder les scénarios en Python, nous définirons un DSL déclaratif (YAML ou JSON) décrivant :

les étapes ;
les transitions ;
les objectifs ;
les règles ;
les événements ;
les actions CRM.

Le backend interprète ce DSL au moment de l'exécution.

Cette décision est essentielle : elle permet aux équipes métier de créer ou modifier des scénarios sans changer le code de l'application.

26. Bibliothèque de scénarios

La plateforme sera livrée avec un catalogue organisé par domaines :

Support technique
Service client
Télévente
Rétention
Fidélisation
Recouvrement
Assistance administrative
Banque
Assurance
E-commerce
Santé
Énergie
Télécommunications

Chaque scénario sera indépendant de l'entreprise et pourra être spécialisé via des paramètres (produits, procédures, scripts, règles).

27. Décisions d'architecture (ADR)

Ce volume fixe plusieurs décisions structurantes :

Un scénario est une ressource métier versionnée.
Les procédures sont déclaratives.
Les règles sont interprétées par le Rule Engine.
Les transitions sont pilotées par une machine à états, jamais par le LLM.
Les objectifs et la procédure sont deux concepts distincts.
Les scénarios sont exécutés à partir d'un DSL, pas de code Python spécifique.
28. Critères d'acceptation

Le Scenario Engine sera considéré conforme lorsque :

un scénario peut être créé sans développement logiciel ;
une même procédure peut être réutilisée dans plusieurs scénarios ;
les scénarios sont versionnés et rejouables ;
toutes les transitions sont validées avant publication ;
les objectifs, événements et actions CRM sont entièrement configurables ;
le moteur peut exécuter un scénario de manière déterministe à partir du DSL.
Évolution proposée

À partir de ce point, je propose une légère amélioration du plan initial.

Avant de documenter le CRM Engine, il serait judicieux d'insérer un nouveau volume :

B6 — Rule Engine & Decision Engine

Ce moteur est transversal : il applique les règles métier utilisées par le Scenario Engine, le CRM Engine, le moteur d'évaluation et le Simulation Operating Engine. En le définissant avant le CRM, nous éviterons des redondances et disposerons d'un langage de règles unique pour toute la plateforme.

Je recommande donc que la suite de la Phase B soit :

B6 — Rule Engine & Decision Engine
B7 — CRM Simulator Engine
B8 — Conversation Engine
B9 — Evaluation & QA Engine
B10 — Analytics & Coaching Engine

Cette légère réorganisation renforce la cohérence de l'architecture sans remettre en cause les fondations déjà établies.
