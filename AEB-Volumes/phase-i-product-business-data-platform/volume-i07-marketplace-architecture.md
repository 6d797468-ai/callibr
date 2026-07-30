# Volume I07 — Marketplace Architecture

> Extrait généré depuis `Architecture & Engineering Book (AEB).md` le 2026-07-27.

PHASE I — ENTERPRISE PRODUCT & BUSINESS PLATFORM
Volume I07
Marketplace Architecture

Version : 1.0

Statut : Enterprise Ecosystem Foundation

Criticité : Élevée

1. Vision

La Marketplace transforme Callibr d'un produit fermé en plateforme extensible.

Elle permet de distribuer :

Domain Packs ;
scénarios ;
personas ;
grilles QA ;
prompts ;
agents ;
connecteurs ;
dashboards ;
templates de workflows ;
datasets d'évaluation.

2. Principe fondamental

Une extension installable doit être gouvernée comme du logiciel.

Elle possède :

manifest ;
version ;
dépendances ;
permissions ;
compatibilité ;
licence ;
propriétaire ;
certification.

3. Architecture globale

                    Marketplace


                         │


        ┌────────────────┼────────────────┐


        ▼                ▼                ▼


 Catalog Service    Review Pipeline   Install Runtime


        │                │                │


        ▼                ▼                ▼


 Extension Store   Certification     Tenant Runtime

4. Types d'assets

Catalogue :

Domain Pack ;
Scenario Pack ;
Persona Pack ;
QA Scorecard ;
Prompt Pack ;
Agent Pack ;
Connector ;
Dashboard ;
Report Template ;
Benchmark Dataset.

Chaque type possède un schéma dédié.

5. Extension Manifest

Exemple :

extension:
  id: banking-contact-center-pack
  name: Banking Contact Center
  type: domain_pack
  version: 1.0.0
  publisher: callibr
  permissions:
    - crm:read
    - simulation:write
  dependencies:
    - qa-core >= 1.0.0
  compatible_with:
    platform: ">=1.0.0"

Le manifest est obligatoire.

6. Catalog Service

Le catalogue stocke :

métadonnées ;
descriptions ;
versions ;
captures ;
compatibilité ;
prix ;
rating ;
certifications.

Il ne stocke pas les secrets.

7. Review Pipeline

Avant publication :

validation schema ;
scan sécurité ;
tests de compatibilité ;
tests fonctionnels ;
revue humaine ;
signature ;
certification.

Une extension non validée reste privée.

8. Certification Levels

Niveaux :

Draft

Internal

Verified

Certified

Enterprise Certified

Les clients Enterprise peuvent restreindre les installations aux extensions certifiées.

9. Install Runtime

Installation :

Tenant

↓

Select Extension

↓

Permission Review

↓

Dependency Check

↓

Configuration

↓

Activation

10. Tenant Installation Boundary

Une extension est installée dans un tenant.

Elle ne peut pas accéder :

aux autres tenants ;
aux secrets globaux ;
aux données non autorisées ;
aux moteurs sans contrat.

11. Permissions

Chaque extension déclare ses besoins.

Exemple :

permissions:
  - scenarios:read
  - scenarios:write
  - evaluation:read
  - crm_runtime:read

L'administrateur approuve avant installation.

12. Dependency Management

Les extensions peuvent dépendre de :

capabilities plateforme ;
Domain Packs ;
connecteurs ;
modèles IA ;
schémas ;
versions API.

Le resolver empêche les installations incompatibles.

13. Versioning

Règles :

MAJOR : rupture ;
MINOR : ajout compatible ;
PATCH : correction.

Un tenant peut rester sur une version spécifique.

14. Update Strategy

Modes :

manual ;
automatic patch ;
scheduled ;
canary ;
tenant-by-tenant.

Les mises à jour critiques peuvent être imposées pour sécurité.

15. Rollback

Toute extension doit pouvoir être désactivée ou revenir à une version précédente.

Conditions :

pas de perte données ;
migrations réversibles lorsque possible ;
snapshot avant migration ;
journal d'installation.

16. Marketplace Billing

Modèles :

gratuit ;
one-time ;
abonnement ;
usage-based ;
revenue share ;
bundle.

Le Billing Platform calcule les droits et revenus.

17. Publisher Model

Types d'éditeurs :

Callibr ;
partenaire technologique ;
intégrateur ;
cabinet de conseil ;
client privé ;
communauté contrôlée.

Chaque éditeur possède un profil et un niveau de confiance.

18. Private Marketplace

Les grands comptes peuvent disposer d'une marketplace privée.

Usages :

packs internes ;
processus métier ;
scripts approuvés ;
connecteurs propriétaires ;
templates de formation.

19. Security Scanning

Contrôles :

manifest ;
permissions excessives ;
prompts risqués ;
fuites de données ;
dépendances ;
scripts ;
connecteurs externes.

20. Prompt & Agent Safety

Pour les assets IA :

tests injection ;
tests hallucination ;
tests conformité ;
tests biais ;
tests données sensibles.

Un Agent Pack doit passer par le Safety Layer.

21. Quality Metrics

La marketplace suit :

installations ;
désinstallations ;
erreurs ;
rating ;
usage ;
support tickets ;
régressions ;
revenu.

22. Search & Discovery

Le catalogue permet :

recherche ;
filtrage ;
catégories ;
recommandations ;
collections ;
compatibilité par tenant.

23. Data Model

MarketplaceAsset
----------------

id

type

name

publisher_id

status

latest_version

AssetVersion
------------

id

asset_id

version

manifest

signature

certification_level

TenantInstallation
------------------

id

tenant_id

asset_id

version

status

installed_at

Publisher
---------

id

name

type

trust_level

24. API interne

Publier un asset :

POST /marketplace/assets

Soumettre une version :

POST /marketplace/assets/{id}/versions

Installer :

POST /marketplace/installations

Mettre à jour :

POST /marketplace/installations/{id}/upgrade

Désinstaller :

POST /marketplace/installations/{id}/uninstall

25. Décisions d'architecture (ADR)

ADR-I07-001
Toute extension est décrite par un manifest.

Décision :

Rendre l'installation déterministe et auditable.

ADR-I07-002
La marketplace applique une certification.

Décision :

Protéger les tenants Enterprise.

ADR-I07-003
Les permissions sont explicites.

Décision :

Aucune extension ne reçoit d'accès implicite.

ADR-I07-004
Les extensions sont versionnées et rollbackables.

Décision :

Réduire les risques opérationnels.

26. Critères d'acceptation

Marketplace Architecture conforme lorsque :

✅ les assets sont typés ;

✅ les manifests sont validés ;

✅ les permissions sont approuvées ;

✅ les dépendances sont résolues ;

✅ les installations sont isolées par tenant ;

✅ les mises à jour sont contrôlées ;

✅ les extensions IA sont testées ;

✅ les revenus marketplace sont traçables.

🏛️ Décision d'architecture majeure : Extension Trust Platform (ETP)

La marketplace adopte une :

Extension Trust Platform

qui relie :

Manifest

+

Certification

+

Permissions

+

Installation Runtime

+

Billing

+

Telemetry

Objectif :

Permettre l'extension de Callibr sans compromettre sécurité, qualité et stabilité.

📘 État d'avancement
Phase I — Enterprise Product & Business Platform

Terminé :

✅ I01 — Product Operating Model Architecture
✅ I02 — SaaS Multi-Tenant Architecture
✅ I03 — Customer Lifecycle Architecture
✅ I04 — Billing & Subscription Platform Architecture
✅ I05 — Enterprise Integration Platform Architecture
✅ I06 — API Ecosystem Architecture
✅ I07 — Marketplace Architecture

Restants :

I08 — Partner Platform Architecture
I09 — Revenue Architecture
I10 — Growth Engine Architecture

Prochaine étape :

Volume I08 — Partner Platform Architecture

Ce volume définira l'écosystème partenaires : intégrateurs, éditeurs, revendeurs, cabinets de conseil, créateurs de contenu et partenaires technologiques.
