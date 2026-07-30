# Volume J05 — Plugin & Extension Runtime Architecture

> Extrait généré depuis `Architecture & Engineering Book (AEB).md` le 2026-07-27.

PHASE J — ENTERPRISE PLATFORM SERVICES
Volume J05
Plugin & Extension Runtime Architecture

Version : 1.0

Statut : Enterprise Extensibility Foundation

Criticité : Critique

1. Vision

Le Plugin & Extension Runtime permet d'étendre Callibr sans modifier le noyau.

Extensions possibles :

connecteurs ;
domain packs ;
agents IA ;
outils ;
dashboards ;
reports ;
actions CRM ;
workflows ;
prompts.

2. Principe fondamental

Une extension est du code ou de la configuration non native.

Elle doit donc être isolée, limitée, observable et révocable.

3. Architecture globale

                    Extension Package


                           │


                           ▼


                     Extension Registry


        ┌──────────────────┼──────────────────┐


        ▼                  ▼                  ▼


 Sandbox Runtime      Permission Model     Lifecycle Manager

4. Extension Manifest

Chaque extension déclare :

id ;
type ;
version ;
publisher ;
permissions ;
entrypoints ;
dependencies ;
compatible_platform ;
configuration_schema.

5. Runtime Isolation

Isolation par :

process ;
container ;
tenant boundary ;
permission scopes ;
network policy ;
resource quotas.

6. Lifecycle

Cycle :

uploaded ;
validated ;
approved ;
installed ;
enabled ;
disabled ;
upgraded ;
removed.

7. Permission Model

Une extension demande :

API scopes ;
data scopes ;
tool scopes ;
event subscriptions ;
network access ;
secret access.

8. Extension Hooks

Hooks :

on_install ;
on_enable ;
on_disable ;
on_event ;
on_uninstall ;
on_upgrade.

9. Data Model

ExtensionPackage
----------------

id

type

version

publisher_id

manifest

signature

ExtensionInstallation
---------------------

id

tenant_id

package_id

status

config

ExtensionPermissionGrant
------------------------

id

installation_id

permission

approved_by

10. API interne

Installer extension :

POST /extensions/install

Activer :

POST /extensions/{id}/enable

Désactiver :

POST /extensions/{id}/disable

11. Décisions d'architecture (ADR)

ADR-J05-001
Toute extension possède un manifest.

Décision :

Rendre installation, sécurité et compatibilité vérifiables.

ADR-J05-002
Le runtime est isolé.

Décision :

Limiter le rayon d'impact.

ADR-J05-003
Les permissions sont explicites.

Décision :

Interdire les privilèges implicites.

ADR-J05-004
Les extensions sont révocables.

Décision :

Permettre réponse rapide à incident.

12. Critères d'acceptation

Plugin Runtime conforme lorsque :

les manifests sont validés ;
les extensions sont isolées ;
les permissions sont approuvées ;
les hooks sont audités ;
les quotas sont appliqués ;
les extensions peuvent être désactivées sans casser le noyau.

Décision majeure : Extensible Core, Governed Runtime

Callibr devient extensible sans devenir incontrôlable.
