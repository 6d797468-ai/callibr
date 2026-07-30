# Volume K04 — Containers, Docker & Software Supply Chain Security Architecture

> Extrait généré depuis `Architecture & Engineering Book (AEB).md` le 2026-07-27.

PHASE K — DEV PLATFORM, DEVSECOPS & PLATFORM ENGINEERING
Volume K04
Containers, Docker & Software Supply Chain Security Architecture

Version : 1.0

Statut : Secure Artifact Foundation

Criticité : Critique

1. Vision

Chaque composant Callibr est livré sous forme d'artefact immuable.

Les conteneurs doivent être :

minimaux ;
signés ;
scannés ;
reproductibles ;
traçables ;
compatibles runtime.

2. Principe fondamental

La chaîne logicielle est une surface d'attaque.

Chaque dépendance, image et build doit être vérifiable.

3. Architecture globale

                    Source Code


                        │


                        ▼


                    Build System


        ┌───────────────┼───────────────┐


        ▼               ▼               ▼


 Container Image     SBOM            Signature


                        │


                        ▼


                    Artifact Registry

4. Container Standards

Règles :

base image approuvée ;
non-root user ;
read-only filesystem si possible ;
healthcheck ;
minimal packages ;
no secrets ;
explicit version tags ;
digest pinning.

5. SBOM

Chaque artefact possède un Software Bill of Materials.

Il liste :

packages ;
versions ;
licenses ;
origins ;
checksums ;
vulnerabilities.

6. Image Signing

Les images sont signées.

Le cluster refuse les images non signées en production.

7. Vulnerability Scanning

Scans :

dependencies ;
OS packages ;
container image ;
licenses ;
secrets ;
malware optionnel.

8. Artifact Registry

Le registry conserve :

image ;
digest ;
signature ;
SBOM ;
scan results ;
provenance ;
retention policy.

9. Data Model

ArtifactRecord
--------------

id

name

version

digest

type

signature_status

SBOMRecord
----------

id

artifact_id

format

storage_ref

VulnerabilityFinding
--------------------

id

artifact_id

severity

package

status

10. API interne

Publier artefact :

POST /supply-chain/artifacts

Lire SBOM :

GET /supply-chain/artifacts/{id}/sbom

Vérifier signature :

POST /supply-chain/artifacts/{id}/verify

11. Décisions d'architecture (ADR)

ADR-K04-001
Les images sont immuables.

Décision :

Déployer par digest, pas par tag mutable.

ADR-K04-002
Les SBOM sont obligatoires.

Décision :

Connaître la composition logicielle.

ADR-K04-003
Les images production sont signées.

Décision :

Empêcher artefacts non approuvés.

ADR-K04-004
Les vulnérabilités critiques bloquent la promotion.

Décision :

Réduire exposition supply chain.

12. Critères d'acceptation

Supply Chain conforme lorsque :

les images sont non-root ;
les artefacts sont signés ;
les SBOM existent ;
les scans bloquent les risques critiques ;
les digests sont utilisés ;
les provenances sont auditables.

Décision majeure : Trusted Artifact Pipeline

Callibr ne déploie que des artefacts vérifiés.
