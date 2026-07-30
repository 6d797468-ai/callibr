# CAP-02 — CRM

Mise a jour : 2026-07-28

## Definition

Capacite de simuler des actions metier dans un CRM fictif pendant une session de simulation : recherche client, verification d'identite, creation de ticket, modification de dossier.

## Stabilite

Le CRM simule est un composant stable de la plateforme. Les actions metier evoluent, mais la capacite de simuler un CRM reste.

## AEB Volumes Concernes

- B07 — CRM Runtime Engine (CRE)

## Composants

| Composant | Emplacement | Statut |
| --- | --- | --- |
| CRM Runtime | `engines/crm/` | Actif |
| Customer Model | `engines/crm/` | Actif |
| Action Engine | `engines/crm/application/actions/` | Actif |
| CRM Event Trail | `engines/crm/` | Actif |

## Contrats

- `RunCrmActionCommand` -> execute une action CRM
- `CrmActionExecuted` -> evenement audit metier

## Actions Metier Supportees (MVP)

1. Recherche client
2. Verification d'identite
3. Creation de ticket
4. Consultation de dossier

## Criteres De Stabilite

Une feature CRM est terminee quand :

- Une action CRM peut etre executee dans une session
- L'action est tracée dans l'audit trail
- Les tests couvrent le cas d'usage
