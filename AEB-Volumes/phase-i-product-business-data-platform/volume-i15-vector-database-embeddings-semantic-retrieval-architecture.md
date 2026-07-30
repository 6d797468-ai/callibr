# Volume I15 — Vector Database, Embeddings & Semantic Retrieval Architecture

> Extrait généré depuis `Architecture & Engineering Book (AEB).md` le 2026-07-27.

PHASE I — DATA PLATFORM & KNOWLEDGE SYSTEM
Volume I15
Vector Database, Embeddings & Semantic Retrieval Architecture

Version : 1.0

Statut : Enterprise Retrieval Foundation

Criticité : Critique

1. Vision

La Vector Database permet la recherche sémantique et le RAG.

Elle indexe :

documents ;
procédures ;
scénarios ;
transcriptions ;
feedback QA ;
connaissances métier ;
exemples de conversations ;
politiques internes.

2. Principe fondamental

La recherche vectorielle n'est pas une base documentaire complète.

Elle est une couche de retrieval qui doit être gouvernée avec :

source ;
version ;
tenant ;
permissions ;
fraîcheur ;
qualité ;
traçabilité.

3. Architecture globale

                    Knowledge Sources


                           │


                           ▼


                    Ingestion Pipeline


                           │


          ┌────────────────┼────────────────┐


          ▼                ▼                ▼


      Chunking        Embeddings       Vector Index


                           │


                           ▼


                    Retrieval Gateway


                           │


                           ▼


                     RAG / Agents / Search

4. Embedding Pipeline

Étapes :

extraction ;
normalisation ;
classification ;
chunking ;
metadata enrichment ;
embedding ;
indexation ;
validation ;
publication.

5. Chunking Strategy

Stratégies :

par section ;
par paragraphe ;
par procédure ;
par question-réponse ;
par fenêtre glissante ;
par structure métier.

Le chunking doit préserver le sens opérationnel.

6. Metadata

Chaque chunk porte :

tenant_id ;
source_id ;
document_version ;
domain_pack ;
language ;
classification ;
permissions ;
valid_from ;
valid_until ;
checksum.

7. Multi-Tenant Isolation

Isolation :

namespace par tenant ;
filtre tenant obligatoire ;
permissions par document ;
séparation possible par collection ;
chiffrement selon sensibilité.

8. Hybrid Search

La recherche combine :

vector search ;
keyword search ;
metadata filters ;
recency boost ;
authority score ;
permission filter.

9. Retrieval Policy

La policy décide :

sources autorisées ;
nombre de chunks ;
score minimum ;
filtres ;
langue ;
fraîcheur ;
redaction.

10. Embedding Model Registry

Chaque embedding est lié à :

modèle ;
version ;
dimensions ;
date ;
dataset ;
paramètres.

Changer de modèle exige réindexation contrôlée.

11. Reindexing

Déclencheurs :

document modifié ;
nouveau modèle ;
chunking changé ;
metadata corrigée ;
permission changée.

Le reindexing est traçable.

12. Retrieval Evaluation

Mesures :

precision@k ;
recall@k ;
MRR ;
coverage ;
hallucination rate ;
answer groundedness ;
latency ;
cost.

13. Data Model

KnowledgeSource
---------------

id

tenant_id

type

uri

version

classification

Chunk
-----

id

source_id

text

metadata

checksum

EmbeddingRecord
---------------

id

chunk_id

model_id

vector_ref

created_at

RetrievalQuery
--------------

id

tenant_id

query

filters

results

trace_id

14. API interne

Indexer source :

POST /retrieval/sources/index

Rechercher :

POST /retrieval/search

Réindexer :

POST /retrieval/sources/{id}/reindex

Évaluer retrieval :

POST /retrieval/evaluations

15. Décisions d'architecture (ADR)

ADR-I15-001
La recherche sémantique est multi-tenant par conception.

Décision :

Empêcher toute fuite de connaissance entre clients.

ADR-I15-002
Chaque chunk est traçable jusqu'à sa source.

Décision :

Rendre le RAG explicable.

ADR-I15-003
Le retrieval est évalué automatiquement.

Décision :

Mesurer qualité et risque hallucination.

ADR-I15-004
Les embeddings sont versionnés.

Décision :

Permettre réindexation contrôlée.

16. Critères d'acceptation

Vector Platform conforme lorsque :

les sources sont versionnées ;
les chunks sont traçables ;
les permissions filtrent les résultats ;
les embeddings sont associés à un modèle ;
le retrieval est mesuré ;
la réindexation est contrôlée.

Décision majeure : Governed Retrieval Architecture

Le RAG de Callibr s'appuie sur un retrieval gouverné, mesurable et explicable.
