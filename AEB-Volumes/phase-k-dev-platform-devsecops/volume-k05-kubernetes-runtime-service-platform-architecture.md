# Volume K05 — Kubernetes Runtime & Service Platform Architecture

> Extrait généré depuis `Architecture & Engineering Book (AEB).md` le 2026-07-27.

PHASE K — DEV PLATFORM, DEVSECOPS & PLATFORM ENGINEERING
Volume K05
Kubernetes Runtime & Service Platform Architecture

Version : 1.0

Statut : Cloud Runtime Foundation

Criticité : Critique

1. Vision

Kubernetes fournit le runtime standard de production pour Callibr.

Il orchestre :

services API ;
workers ;
gateways ;
AI runtime ;
event consumers ;
cron jobs ;
observability agents.

2. Principe fondamental

Kubernetes doit rester une plateforme contrôlée.

Les équipes consomment des abstractions, pas la complexité brute du cluster.

3. Architecture globale

                    Kubernetes Cluster


                           │


        ┌──────────────────┼──────────────────┐


        ▼                  ▼                  ▼


 Namespaces          Workloads          Platform Services


        │                  │                  │


        ▼                  ▼                  ▼


 Network Policies    Autoscaling        Observability

4. Namespace Strategy

Namespaces :

platform ;
apps ;
workers ;
data ;
observability ;
security ;
tenant-dedicated optionnel.

5. Workload Types

Types :

Deployment ;
StatefulSet ;
Job ;
CronJob ;
DaemonSet ;
HorizontalPodAutoscaler.

6. Network Policies

Règles :

deny by default ;
allow explicit ;
namespace isolation ;
egress control ;
database access restricted ;
observability allowed.

7. Resource Management

Chaque workload déclare :

requests ;
limits ;
priority class ;
autoscaling metrics ;
disruption budget.

8. Ingress & Gateway

Entrées :

API Gateway ;
WebSocket Gateway ;
Admin Gateway ;
Webhook Gateway ;
internal ingress.

9. Data Model

Cluster
-------

id

name

region

environment

status

Workload
--------

id

service

namespace

replicas

version

RuntimePolicy
-------------

id

scope

rules

10. API interne

Lire workloads :

GET /runtime/workloads

Scaler service :

POST /runtime/workloads/{id}/scale

Lire santé cluster :

GET /runtime/clusters/{id}/health

11. Décisions d'architecture (ADR)

ADR-K05-001
Kubernetes est le runtime production recommandé.

Décision :

Standardiser orchestration et scalabilité.

ADR-K05-002
Les namespaces isolent les responsabilités.

Décision :

Limiter blast radius.

ADR-K05-003
Les network policies sont restrictives.

Décision :

Réduire mouvement latéral.

ADR-K05-004
Chaque workload déclare ses ressources.

Décision :

Prévenir contention et instabilité.

12. Critères d'acceptation

Kubernetes Platform conforme lorsque :

les workloads sont déclaratifs ;
les namespaces sont structurés ;
les policies réseau existent ;
les ressources sont définies ;
les autoscalers fonctionnent ;
les health checks sont exposés.

Décision majeure : Controlled Kubernetes Platform

Kubernetes devient un runtime gouverné, pas un terrain libre.
