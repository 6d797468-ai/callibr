# Volume J02 — RBAC, ABAC & Policy Enforcement Architecture

> Extrait généré depuis `Architecture & Engineering Book (AEB).md` le 2026-07-27.

PHASE J — ENTERPRISE PLATFORM SERVICES
Volume J02
RBAC, ABAC & Policy Enforcement Architecture

Version : 1.0

Statut : Enterprise Security Foundation

Criticité : Critique

1. Vision

Le service d'autorisation décide si une action est permise.

Il doit fonctionner pour :

interfaces web ;
API ;
workers ;
agents IA ;
connecteurs ;
marketplace ;
exports ;
administration.

2. Principe fondamental

RBAC donne une base simple.

ABAC permet les décisions contextuelles.

Policy Engine garantit la cohérence.

3. Architecture globale

                    Access Request


                          │


                          ▼


                    Policy Enforcement Point


                          │


                          ▼


                    Policy Decision Point


        ┌─────────────────┼─────────────────┐


        ▼                 ▼                 ▼


      RBAC              ABAC            Risk Context

4. RBAC

Rôles standards :

tenant_admin ;
workspace_admin ;
trainer ;
supervisor ;
agent ;
qa_reviewer ;
wfm_manager ;
billing_admin ;
integration_admin ;
security_admin.

5. ABAC

Attributs :

tenant ;
workspace ;
department ;
region ;
data_classification ;
resource_owner ;
time ;
risk_level ;
purpose ;
subscription_plan.

6. Policy Model

Exemple :

policy:
  id: export_sensitive_report
  effect: allow
  subject:
    role: qa_reviewer
  resource:
    type: report
    classification: confidential
  condition:
    mfa: true
    tenant_match: true

7. Permission Evaluation

Flux :

action demandée ;
construction contexte ;
lecture rôles ;
lecture attributs ;
évaluation policy ;
décision ;
audit.

8. Deny by Default

Toute action non explicitement autorisée est refusée.

Les exceptions doivent être déclarées.

9. Human Approval Gates

Certaines actions exigent approbation :

export massif ;
suppression données ;
installation extension sensible ;
changement policy ;
accès partenaire ;
modification billing.

10. Data Model

Role
----

id

tenant_id

name

permissions

Policy
------

id

tenant_id

name

rules

status

AccessDecision
--------------

id

subject_id

action

resource

decision

reason

trace_id

11. API interne

Évaluer permission :

POST /authorization/decide

Créer rôle :

POST /authorization/roles

Publier policy :

POST /authorization/policies

Auditer décision :

GET /authorization/decisions/{id}

12. Décisions d'architecture (ADR)

ADR-J02-001
RBAC et ABAC sont combinés.

Décision :

Offrir simplicité et précision.

ADR-J02-002
Le Policy Decision Point est central.

Décision :

Éviter les décisions dispersées dans le code.

ADR-J02-003
Deny by default.

Décision :

Réduire les permissions implicites.

ADR-J02-004
Les décisions sont auditées.

Décision :

Rendre l'autorisation explicable.

13. Critères d'acceptation

Authorization conforme lorsque :

chaque action critique passe par le PDP ;
les rôles sont tenant-scoped ;
les attributs sont disponibles ;
les refus sont explicables ;
les décisions sont auditables ;
les approbations humaines sont configurables.

Décision majeure : Policy-Driven Authorization

La sécurité d'accès devient déclarative et vérifiable.
