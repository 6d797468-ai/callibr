# Volume J07 — White Label, Branding & Tenant Experience Architecture

> Extrait généré depuis `Architecture & Engineering Book (AEB).md` le 2026-07-27.

PHASE J — ENTERPRISE PLATFORM SERVICES
Volume J07
White Label, Branding & Tenant Experience Architecture

Version : 1.0

Statut : Enterprise Experience Foundation

Criticité : Élevée

1. Vision

Le White Label permet à un client Enterprise d'adapter l'expérience Callibr à sa marque.

Éléments :

logo ;
couleurs ;
typographie ;
domaine personnalisé ;
emails ;
portail ;
rapports ;
terminologie ;
catalogues.

2. Principe fondamental

La personnalisation ne doit jamais créer un fork du produit.

Elle doit être déclarative.

3. Architecture globale

                    Tenant Branding Config


                              │


                              ▼


                    Experience Rendering Layer


        ┌─────────────────────┼─────────────────────┐


        ▼                     ▼                     ▼


       UI Theme            Documents             Emails

4. Branding Configuration

Configuration :

brand_name ;
logo ;
favicon ;
primary_color ;
secondary_color ;
email_sender ;
custom_domain ;
report_cover ;
terminology.

5. Theming Rules

Règles :

contraste accessible ;
dimensions logo ;
palette validée ;
fallback ;
prévisualisation ;
validation avant publication.

6. Custom Domain

Support :

tenant.callibr.com ;
training.client.com.

Contrôles :

DNS ;
TLS ;
ownership verification ;
renewal certificates.

7. Branded Reports

Les rapports peuvent porter :

logo client ;
couverture ;
pied de page ;
mentions légales ;
style graphique.

8. Tenant Terminology

Exemples :

"Agent" peut devenir "Conseiller".

"Scenario" peut devenir "Cas de formation".

La terminologie est configurée par tenant.

9. Data Model

BrandingProfile
---------------

id

tenant_id

name

theme

assets

status

CustomDomain
------------

id

tenant_id

domain

tls_status

verification_status

TerminologyOverride
-------------------

id

tenant_id

source_term

target_term

10. API interne

Créer branding :

POST /branding/profiles

Publier branding :

POST /branding/profiles/{id}/publish

Vérifier domaine :

POST /branding/domains/{id}/verify

11. Décisions d'architecture (ADR)

ADR-J07-001
Le white label est déclaratif.

Décision :

Éviter les forks clients.

ADR-J07-002
Les thèmes sont validés.

Décision :

Préserver accessibilité et qualité.

ADR-J07-003
Les domaines personnalisés sont vérifiés.

Décision :

Garantir sécurité et propriété.

ADR-J07-004
La terminologie est tenant-scoped.

Décision :

Adapter l'expérience sans modifier le domaine.

12. Critères d'acceptation

White Label conforme lorsque :

un tenant peut publier une marque ;
les thèmes sont validés ;
les rapports reprennent la marque ;
les domaines personnalisés sont sécurisés ;
les termes sont substitués sans casser les APIs ;
le fallback Callibr existe toujours.

Décision majeure : Brandable SaaS Without Forks

Callibr devient personnalisable sans perdre son intégrité produit.
