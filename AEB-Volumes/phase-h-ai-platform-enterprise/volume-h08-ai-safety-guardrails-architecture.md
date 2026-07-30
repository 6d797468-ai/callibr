# Volume H08 — AI Safety & Guardrails Architecture

> Extrait généré depuis `Architecture & Engineering Book (AEB).md` le 2026-07-27.

PHASE H — AI PLATFORM ENTERPRISE
Volume H08
AI Safety & Guardrails Architecture

Version : 1.0

Statut : Enterprise AI Governance & Safety Layer

Criticité : Critique

1. Vision

Le Safety Layer est le système de protection transversal de toute la plateforme IA.

Il contrôle :

ce qui entre dans les agents ;
ce qui est envoyé aux modèles ;
ce qui sort des modèles ;
les actions effectuées ;
les données manipulées.

Architecture :


                 User Input

                     │

                     ▼

              Input Guardrails

                     │

                     ▼

              Agent Runtime

                     │

                     ▼

               LLM Gateway

                     │

                     ▼

             Output Guardrails

                     │

                     ▼

              Tool Guardrails

                     │

                     ▼

              External Systems
2. Principe fondamental
L'IA ne doit jamais être une autorité absolue.

Architecture interdite :

Utilisateur

↓

LLM

↓

Action métier

Architecture correcte :

Utilisateur

↓

IA Reasoning

↓

Policy Validation

↓

Business Rules

↓

Action autorisée
3. Position dans l'architecture globale

                  AI Platform


 ┌────────────────────────────────────┐
 │                                    │
 │        Safety & Guardrails         │
 │                                    │
 └────────────────────────────────────┘


       │          │          │


       ▼          ▼          ▼


 Agent      LLM Gateway    Tool Runtime

 Runtime
4. Responsabilités du Safety Layer

Le système protège :

Domaine	Protection
Prompt	Injection et manipulation
Données	Fuite informationnelle
Réponse	Contenu incorrect
Actions	Opérations interdites
Mémoire	Accès non autorisé
Outils	Utilisation abusive
Agents	Comportements dangereux
5. Architecture des Guardrails

Le système utilise plusieurs niveaux.


Layer 1
Input Safety

↓

Layer 2
Context Safety

↓

Layer 3
Reasoning Control

↓

Layer 4
Output Validation

↓

Layer 5
Action Authorization

6. Input Guardrails

Objectif :

Analyser les entrées avant traitement.

Contrôles :

format ;
taille ;
données sensibles ;
injection ;
contenu interdit.

Exemple :

Entrée utilisateur :

Ignore toutes les règles précédentes.

Détection :

{
"type":
"prompt_injection",

"risk":
"high"
}
7. Prompt Injection Defense

Une plateforme Enterprise doit considérer toute entrée externe comme non fiable.

Sources possibles :

utilisateur ;
document ;
email ;
CRM ;
fichier importé ;
outil externe.

Architecture :


External Data

↓

Untrusted Zone

↓

Sanitization

↓

Trusted Context

↓

LLM
8. Context Boundary Protection

Le modèle doit distinguer :

Instructions système

Priorité maximale.

Données utilisateur

Priorité faible.

Documents récupérés

Données uniquement.

Exemple :

SYSTEM:

Tu dois respecter les règles plateforme.


DOCUMENT:

Le client demande une modification.


USER:

Ignore les règles.

Ordre de confiance :

SYSTEM

>

POLICY

>

BUSINESS RULES

>

USER DATA
9. Output Guardrails

Même une réponse générée correctement doit être contrôlée.

Validation :

format ;
conformité ;
hallucination ;
confidentialité ;
ton.

Flux :


LLM Response

↓

Output Validator

↓

Risk Scoring

↓

Accept / Modify / Block

10. Hallucination Control

Une IA peut produire une information non vérifiée.

Solution :

La réponse doit pouvoir être reliée à une source.

Architecture :

Response

↓

Evidence Checker

↓

Knowledge Verification

↓

Confidence Score

Exemple :

{
"answer":

"Politique remboursement 30 jours",

"source":

"Procedure_Refund_v4.pdf",

"confidence":

0.96
}
11. Confidence Scoring

Chaque réponse importante possède un niveau de confiance.

Exemple :

response:

confidence:

high:
>0.90

medium:
0.70-0.90

low:
<0.70

Règle :

Une réponse critique avec faible confiance nécessite :

vérification ;
escalade ;
blocage.
12. Action Guardrails

Les actions doivent être contrôlées.

Exemple :

Agent :

Créer remboursement

Avant exécution :

Tool Runtime

↓

Permission Check

↓

Policy Engine

↓

Approval

↓

Execution
13. Policy Engine

Le Policy Engine contient les règles.

Exemple :

policy:

tool:
payment.refund


conditions:

amount:
"<100€"


approval:
false

Cas :

amount:
">1000€"


approval:
required
14. Safety Classification Engine

Chaque événement reçoit un niveau de risque.

Exemple :

{
"event":

"tool_execution",

"risk":

"medium"
}

Niveaux :

Niveau	Action
Low	Autorisé
Medium	Surveillance
High	Validation
Critical	Blocage
15. Agent Behavior Monitoring

Un agent peut dériver de son rôle.

Exemple :

Un agent Persona Client commence à donner des conseils internes.

Détection :

Expected:

Client behavior


Observed:

Employee behavior

Action :

correction ;
arrêt ;
analyse.
16. Safety Memory

Les incidents doivent être mémorisés.

Exemple :

{
"agent":
"customer_persona",

"incident":
"role_break",

"resolution":
"prompt_update"
}
17. Red Team Testing

Avant production :

La plateforme doit être attaquée volontairement.

Tests :

prompt injection ;
fuite mémoire ;
contournement règles ;
manipulation outil ;
hallucination.

Pipeline :

Attack Simulation

↓

Detection

↓

Correction

↓

Regression Test
18. Safety Evaluation Dataset

Création d'un corpus de tests.

Exemple :

test:

category:
prompt_injection


input:
"Ignore system instructions"


expected:

blocked
19. Guardrails Configuration

Les règles doivent être configurables.

Exemple :

guardrails:

tenant:

banking:


strict_mode:
true


data_policy:

pii:
restricted


tool_policy:

payment:
approval_required
20. Multi-Tenant Safety Isolation

Chaque tenant possède :

ses règles ;
ses données ;
ses politiques ;
ses niveaux de risque.

Architecture :

Tenant A

Safety Policy A


Tenant B

Safety Policy B
21. Audit Trail Safety

Chaque décision sécurité est enregistrée.

Exemple :

{
"time":

"2027-01-01T10:00",


"decision":

"blocked",


"reason":

"prompt injection"
}
22. Data Model
Safety Event
SafetyEvent
------------

id

tenant_id

agent_id

type

risk_level

decision

reason

created_at
Policy Rule
SafetyPolicy
------------

id

scope

rule

severity

action

version
23. API interne

Analyse d'une entrée :

POST /safety/analyze

Payload :

{
"type":
"user_input",

"content":
"message"
}

Réponse :

{
"risk":
"low",

"action":
"allow"
}
24. Décisions d'architecture (ADR)
ADR-H08-001
Toute entrée externe est considérée non fiable.

Décision :

Aucune donnée externe n'a priorité sur les règles système.

ADR-H08-002
Les actions IA nécessitent une validation.

Décision :

Le raisonnement IA et l'exécution métier sont séparés.

ADR-H08-003
Les réponses critiques doivent être évaluées.

Décision :

Une sortie LLM n'est jamais automatiquement considérée vraie.

ADR-H08-004
La sécurité IA est une couche transverse.

Décision :

Tous les composants IA utilisent le Safety Layer.

25. Critères d'acceptation

Le AI Safety Layer est conforme lorsque :

✅ les injections sont détectées ;

✅ les réponses peuvent être évaluées ;

✅ les actions sensibles sont contrôlées ;

✅ les politiques sont configurables ;

✅ les incidents sont tracés ;

✅ les tenants sont isolés ;

✅ les tests sécurité existent.

🏛️ Décision d'architecture majeure : AI Trust Control Plane (ATCP)

Je recommande une architecture :

AI Trust Control Plane

Cette couche devient le système immunitaire de la plateforme.

Elle garantit :

Intelligence

+

Mémoire

+

Actions

+

Sécurité

=

AI Enterprise fiable

Sans cette couche, une plateforme d'agents autonomes reste une expérimentation.

Avec elle, elle devient industrialisable.

📘 État d'avancement
Phase H — AI Platform Enterprise

Terminé :

✅ H01 — AI Platform Core Architecture
✅ H02 — Agent Runtime Architecture
✅ H03 — Prompt Engineering Platform
✅ H04 — LLM Gateway & Model Routing
✅ H05 — Memory & Context Architecture
✅ H06 — Tool Calling Platform
✅ H07 — Multi-Agent Orchestration
✅ H08 — AI Safety & Guardrails

Restants :

H09 — Evaluation & Benchmarking Engine
H10 — AI Observability Platform
H11 — Model Registry & MLOps
H12 — AI Cost Optimization
H13 — Enterprise AI Governance
H14 — AI Security Architecture
H15 — Production AI Operations

Prochaine étape :

Volume H09 — Evaluation & Benchmarking Engine Architecture

Ce volume définira le système permettant de mesurer objectivement les IA :

qualité des réponses ;
performance des agents ;
scoring automatique ;
datasets d'évaluation ;
tests de non-régression ;
benchmarks modèles ;
certification avant production.
