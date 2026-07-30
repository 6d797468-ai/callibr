# Volume I10 — Growth Engine Architecture

> Extrait généré depuis `Architecture & Engineering Book (AEB).md` le 2026-07-27.

PHASE I — ENTERPRISE PRODUCT & BUSINESS PLATFORM
Volume I10
Growth Engine Architecture

Version : 1.0

Statut : Enterprise Growth Foundation

Criticité : Élevée

1. Vision

Le Growth Engine transforme la valeur produit en adoption, rétention et expansion.

Il ne remplace pas le Product, le Sales ou le Customer Success.

Il les connecte.

Objectif :

Créer une boucle de croissance mesurable et gouvernée.

2. Principe fondamental

La croissance SaaS Enterprise ne vient pas d'une seule acquisition.

Elle vient de boucles :

Activation Loop

Adoption Loop

Expansion Loop

Marketplace Loop

Partner Loop

Learning Loop

3. Architecture globale

                    Growth Engine


                         │


       ┌─────────────────┼─────────────────┐


       ▼                 ▼                 ▼


 Segmentation      Experimentation     Lifecycle Automation


       │                 │                 │


       ▼                 ▼                 ▼


 Recommendations   Product Analytics   Campaign Orchestration

4. Growth Data Foundation

Sources :

Product Events ;
Customer Health ;
Billing ;
CRM ;
Support ;
Marketplace ;
Partner ;
NPS ;
Training Outcomes.

Toutes les décisions growth sont basées sur des données observables.

5. Segmentation

Segments :

nouveau tenant ;
tenant activé ;
tenant dormant ;
utilisateur power user ;
admin inactif ;
client expansion-ready ;
client à risque ;
partenaire actif.

La segmentation déclenche des actions adaptées.

6. Activation Architecture

Objectif :

amener le client à son premier résultat utile.

Exemple pour Callibr :

Tenant created

↓

Admin invited

↓

First Domain Pack installed

↓

First Scenario launched

↓

First Evaluation generated

↓

Activation achieved

7. Onboarding Orchestration

L'onboarding devient un workflow.

Étapes :

configuration tenant ;
import utilisateurs ;
choix Domain Pack ;
création programme ;
simulation test ;
rapport de réussite.

Le système détecte les blocages.

8. Adoption Engine

L'adoption mesure :

fréquence usage ;
profondeur usage ;
nombre d'équipes ;
fonctionnalités utilisées ;
qualité des résultats ;
récurrence.

9. Feature Recommendation

Le moteur recommande :

Domain Pack ;
scénario ;
connecteur ;
dashboard ;
workflow ;
formation ;
extension marketplace.

Les recommandations sont contextualisées par tenant.

10. Experimentation Platform

Tests :

onboarding A/B ;
messages ;
pricing packaging ;
templates ;
recommandations ;
parcours marketplace ;
activation steps.

Chaque expérience possède une hypothèse et une métrique.

11. Lifecycle Automation

Événements déclencheurs :

tenant_created ;
first_simulation_completed ;
usage_drop_detected ;
health_score_low ;
expansion_signal_detected ;
renewal_approaching.

Actions :

email ;
notification ;
tâche Customer Success ;
suggestion in-app ;
playbook partenaire ;
alerte sales.

12. Expansion Signals

Signaux :

quotas proches ;
utilisateurs invités ;
nouveaux départements ;
usage API élevé ;
plusieurs Domain Packs ;
besoin intégration ;
demande support avancée.

Ces signaux alimentent Sales et Customer Success.

13. Retention Engine

Détection du risque :

baisse d'usage ;
absence d'admin ;
échecs fréquents ;
tickets ouverts ;
faible activation ;
renouvellement proche ;
score QA stagnant.

Le système propose des actions correctives.

14. Product-Led Growth Enterprise

Le PLG Enterprise est encadré.

Principes :

valeur rapide ;
expansion contrôlée ;
sécurité tenant ;
approbation admin ;
alignement sales ;
respect contrats.

15. Marketplace Growth Loop

Boucle :

Nouveau besoin client

↓

Asset Marketplace

↓

Installation

↓

Usage

↓

Rating

↓

Meilleure découverte

16. Partner Growth Loop

Boucle :

Partenaire certifié

↓

Nouveaux assets

↓

Nouveaux clients

↓

Revenus partagés

↓

Plus d'investissement partenaire

17. Learning Growth Loop

Spécifique Callibr :

Plus de simulations

↓

Meilleures évaluations

↓

Meilleurs programmes

↓

Plus de valeur client

↓

Plus d'adoption

18. Growth Governance

Règles :

pas de dark patterns ;
respect consentement ;
contrôle fréquence ;
transparence ;
opt-out ;
validation sécurité ;
mesure réelle.

La croissance ne doit jamais dégrader la confiance.

19. Growth Metrics

Métriques :

activation rate ;
time to value ;
weekly active teams ;
feature adoption ;
retention rate ;
expansion qualified accounts ;
conversion trial-paid ;
marketplace attach rate ;
partner sourced revenue ;
NRR contribution.

20. Growth Dashboard

Vue :

funnel acquisition ;
activation ;
adoption ;
rétention ;
expansion ;
marketplace ;
partenaires ;
expériences.

21. AI-Assisted Growth

L'IA peut aider à :

segmenter ;
résumer signaux ;
recommander actions ;
prioriser comptes ;
générer messages ;
détecter anomalies ;
prédire churn.

Les actions automatiques sensibles restent validées.

22. Data Model

GrowthSegment
-------------

id

name

criteria

status

GrowthExperiment
----------------

id

name

hypothesis

metric

status

GrowthSignal
------------

id

tenant_id

signal_type

score

detected_at

GrowthAction
------------

id

tenant_id

action_type

status

owner

Campaign
--------

id

segment_id

channel

status

23. API interne

Créer segment :

POST /growth/segments

Lancer expérience :

POST /growth/experiments

Consulter signaux :

GET /growth/signals

Déclencher playbook :

POST /growth/playbooks/{id}/run

Obtenir recommandations :

GET /growth/recommendations/{tenant_id}

24. Décisions d'architecture (ADR)

ADR-I10-001
La croissance est pilotée par événements.

Décision :

Les actions growth se déclenchent sur des signaux observables.

ADR-I10-002
L'expérimentation est gouvernée.

Décision :

Toute expérience possède hypothèse, métrique et arrêt contrôlé.

ADR-I10-003
La croissance respecte la confiance Enterprise.

Décision :

Interdire les mécanismes opaques ou intrusifs.

ADR-I10-004
Les boucles marketplace et partenaires font partie du growth.

Décision :

La croissance de la plateforme vient aussi de l'écosystème.

25. Critères d'acceptation

Growth Engine conforme lorsque :

✅ les segments sont calculables ;

✅ l'activation est mesurée ;

✅ les recommandations sont contextualisées ;

✅ les expériences sont traçables ;

✅ les signaux d'expansion sont détectés ;

✅ les risques de churn déclenchent des actions ;

✅ les boucles marketplace et partenaires sont mesurées ;

✅ la gouvernance growth protège la confiance client.

🏛️ Décision d'architecture majeure : Ethical Growth Operating System (EGOS)

La plateforme adopte un :

Ethical Growth Operating System

qui relie :

Product Analytics

+

Segmentation

+

Experimentation

+

Lifecycle Automation

+

Recommendations

+

Customer Success

+

Revenue

Objectif :

Faire croître Callibr par la valeur mesurée, pas par la pression artificielle.

📚 Fin de la Phase I — Bilan

La Phase I — Enterprise Product & Business Platform est désormais complète.

Elle couvre :

I01 — Product Operating Model Architecture
I02 — SaaS Multi-Tenant Architecture
I03 — Customer Lifecycle Architecture
I04 — Billing & Subscription Platform Architecture
I05 — Enterprise Integration Platform Architecture
I06 — API Ecosystem Architecture
I07 — Marketplace Architecture
I08 — Partner Platform Architecture
I09 — Revenue Architecture
I10 — Growth Engine Architecture

Cette phase transforme l'architecture IA et technique en plateforme SaaS Enterprise commercialisable, intégrable, mesurable et extensible.

Recommandation stratégique pour l'édition finale

Le document doit être réparti en volumes physiques pour améliorer :

lecture ;
maintenance ;
revue ;
recherche ;
indexation RAG ;
travail par agents IA ;
évolution incrémentale.

Structure recommandée :

AEB-Volumes/

├── AEB-MASTER-INDEX.md
├── phase-a-foundations/
├── phase-b-business-architecture/
├── phase-c-platform-core/
├── phase-d-engineering-standards/
├── phase-e-ai-engineering/
├── phase-f-delivery-operations/
├── phase-g-contact-center-packs/
├── phase-h-ai-platform-enterprise/
└── phase-i-product-business-platform/

Chaque volume doit rester autonome, mais renvoyer au Master Index.

Décision finale de structuration

Le fichier original reste le livre monolithique de référence.

Les fichiers séparés deviennent les volumes opérationnels de lecture, revue et implémentation.

Note de continuité — Alignement avec la roadmap canonique

Le document contient déjà la Phase G jusqu'au Volume G20 et la Phase H jusqu'au Volume H15.

La roadmap cible demande ensuite une Phase I consacrée à la Data Platform.

Comme les identifiants I01 à I10 sont déjà utilisés par la couche Enterprise Product & Business Platform, la Data Platform est ajoutée comme extension structurée de la Phase I avec les volumes I11 à I20.

Cette décision évite de casser les références existantes tout en complétant le livre selon la trajectoire cible.
