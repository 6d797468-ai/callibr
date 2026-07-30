# Volume I16 — Knowledge Graph & Semantic Layer Architecture

> Extrait généré depuis `Architecture & Engineering Book (AEB).md` le 2026-07-27.

PHASE I — DATA PLATFORM & KNOWLEDGE SYSTEM
Volume I16
Knowledge Graph & Semantic Layer Architecture

Version : 1.0

Statut : Enterprise Knowledge Foundation

Criticité : Élevée

1. Vision

Le Knowledge Graph relie les concepts métier de Callibr :

scénarios ;
compétences ;
procédures ;
règles ;
personas ;
erreurs ;
actions CRM ;
domain packs ;
KPI ;
formations ;
certifications.

Il permet de comprendre les relations, pas seulement de chercher du texte.

2. Principe fondamental

Une plateforme d'apprentissage intelligente doit savoir pourquoi deux éléments sont liés.

Exemple :

Erreur de vérification d'identité

↓

impacte

Conformité

↓

réduit

Score QA

↓

déclenche

Module de coaching

3. Architecture globale

                    Domain Models


                         │


                         ▼


                    Ontology Layer


                         │


          ┌──────────────┼──────────────┐


          ▼              ▼              ▼


       Graph Store    Semantic API    Reasoning Engine


                         │


                         ▼


             Recommendations / Search / Analytics

4. Ontology

L'ontologie définit :

entités ;
relations ;
contraintes ;
synonymes ;
hiérarchies ;
équivalences ;
règles de raisonnement.

5. Core Entities

Entités :

Tenant ;
DomainPack ;
Scenario ;
Procedure ;
Step ;
Rule ;
Competency ;
Skill ;
Agent ;
Persona ;
Error ;
CoachingAction ;
Certification ;
KPI.

6. Relationships

Exemples :

Scenario requires Competency ;
Procedure contains Step ;
Rule validates Action ;
Error impacts KPI ;
CoachingAction improves Skill ;
DomainPack defines Procedure ;
Persona challenges Agent.

7. Semantic Layer

Le Semantic Layer expose un vocabulaire commun aux moteurs.

Il évite que chaque engine possède sa propre définition de :

compétence ;
erreur ;
résolution ;
conformité ;
progression ;
certification.

8. Reasoning Engine

Capacités :

déduire lacunes ;
recommander exercices ;
relier erreurs et compétences ;
identifier prérequis ;
construire parcours ;
expliquer scores.

9. Graph + Vector

Le graphe et la recherche vectorielle sont complémentaires.

Vector :

similarité sémantique.

Graph :

relations explicites.

Architecture :

Hybrid Retrieval

↓

Vector Candidates

+

Graph Expansion

↓

Grounded Answer

10. Multi-Tenant Graph

Deux couches :

global ontology ;
tenant-specific graph.

Les clients peuvent étendre le graphe sans modifier le noyau global.

11. Data Model

GraphNode
---------

id

tenant_id

type

properties

version

GraphEdge
---------

id

tenant_id

source_id

target_id

relation_type

properties

OntologyTerm
------------

id

name

definition

domain

status

12. API interne

Créer relation :

POST /knowledge-graph/edges

Interroger graphe :

POST /knowledge-graph/query

Obtenir recommandations :

GET /knowledge-graph/recommendations/{agent_id}

13. Décisions d'architecture (ADR)

ADR-I16-001
Les concepts métier sont modélisés dans un graphe.

Décision :

Rendre les relations explicites et interrogeables.

ADR-I16-002
Le graphe distingue ontologie globale et extensions tenant.

Décision :

Supporter standardisation et personnalisation.

ADR-I16-003
Le graphe complète le RAG vectoriel.

Décision :

Améliorer précision et explicabilité.

ADR-I16-004
Le raisonnement doit rester explicable.

Décision :

Chaque recommandation expose ses chemins de preuve.

14. Critères d'acceptation

Knowledge Graph conforme lorsque :

les concepts clés sont modélisés ;
les relations sont versionnées ;
les extensions tenant sont isolées ;
les recommandations exposent leurs preuves ;
le graphe enrichit le retrieval ;
le Semantic Layer est utilisé par les moteurs.

Décision majeure : Semantic Operating Layer

Callibr adopte un Semantic Operating Layer pour relier apprentissage, simulation, QA et connaissances métier.
