# Plan De Renumérotation Contrôlée Des Volumes

Mise à jour : 2026-07-27

## Objectif

Ce plan définit une renumérotation canonique recommandée sans modifier immédiatement le monolithe ni les fichiers existants.

L'objectif est de préserver la traçabilité historique tout en préparant une édition finale propre.

## Principes

- Le monolithe reste la source historique.
- Les fichiers existants restent stables jusqu'à validation humaine.
- Toute renumérotation doit produire une table de correspondance ancien identifiant -> nouvel identifiant.
- Les liens, ADR, index et matrices doivent être recalculés après renumérotation.

## Incohérences Détectées

| Zone | Problème | Risque | Action recommandée |
| --- | --- | --- | --- |
| Phase A | `A00-A02` est composite | Granularité insuffisante | Séparer en A00, A01, A02 |
| Phase B | Deux volumes `B04` | Ambiguïté de référence | Renommer le second en `B04b` ou `B05`, puis décaler B05-B10 |
| Phase G | Deux volumes `G06` | Ambiguïté de référence | Renommer le second en `G06b` ou `G07`, puis décaler G07-G20 |
| Phase G | Bilan mentionne G19 alors que Omnichannel est G20 | Incohérence éditoriale | Conserver G20 et corriger le bilan, ou renuméroter G00-G19 |
| Phase I | Product/Business et Data Platform partagent la même phase | Taxonomie hybride | Conserver I01-I20 ou scinder Data en Phase M dans une édition future |

## Mapping Canonique Recommandé — Phase A

| Actuel | Recommandé | Titre |
| --- | --- | --- |
| A00-A02 | A00 | Executive Foundation & Product Vision |
| A00-A02 | A01 | Enterprise Architecture Foundation |
| A00-A02 | A02 | Engineering Constitution |

## Mapping Canonique Recommandé — Phase B

Option retenue pour minimiser l'impact : suffixe stable.

| Actuel | Recommandé | Titre |
| --- | --- | --- |
| B04 | B04 | Customer Persona Engine & Emotion Engine |
| B04 partie 2 | B04B | Customer Persona Engine & Behavior Simulation Engine |
| B05 | B05 | Scenario Engine & Procedure Engine |
| B06 | B06 | Rule Engine & Decision Engine |
| B07 | B07 | CRM Runtime Engine |
| B08 | B08 | Conversation Runtime Engine |
| B09 | B09 | Evaluation & Quality Intelligence Engine |
| B10 | B10 | Analytics, Learning Intelligence & Coaching Platform |

Alternative stricte : renommer le second B04 en B05 et décaler B05-B10 vers B06-B11. Cette option est plus propre mais plus risquée pour les références existantes.

## Mapping Canonique Recommandé — Phase G

Option retenue pour minimiser l'impact : conserver G00 comme framework et utiliser G06B pour le second Back Office.

| Actuel | Recommandé | Titre |
| --- | --- | --- |
| G00 | G00 | Domain Pack Framework |
| G01 | G01 | Service Après-Vente |
| G02 | G02 | Support Technique N1/N2 |
| G03 | G03 | Télévente & Vente Conseil |
| G04 | G04 | Rétention & Fidélisation |
| G05 | G05 | Recouvrement |
| G06 | G06 | Back Office |
| G06 partie 2 | G06B | Back Office — Processus administratifs avancés |
| G07 | G07 | Conduite d'Activité & Dispatch |
| G08 | G08 | QA & Coaching |
| G09 | G09 | Workforce Management |
| G10 | G10 | Supervision Temps Réel |
| G11 | G11 | Customer Success |
| G12 | G12 | Help Desk ITIL |
| G13 | G13 | Incident & Problem Management |
| G14 | G14 | Banking Contact Center |
| G15 | G15 | Insurance Contact Center |
| G16 | G16 | Healthcare Contact Center |
| G17 | G17 | E-commerce & Retail |
| G18 | G18 | Public Services & Administration |
| G19 | G19 | Collections avancées & Contentieux |
| G20 | G20 | Omnichannel & Digital Engagement |

## Décision Recommandée

Pour l'édition actuelle : ne pas renommer les fichiers existants.

Pour l'édition finale PDF/site : afficher les suffixes `B04B` et `G06B` dans les index, tout en gardant les anciens chemins comme aliases.

## Étapes De Migration Futures

1. Valider ce plan avec l'architecte principal.
2. Générer un alias map machine-readable.
3. Mettre à jour l'index maître.
4. Générer les liens de redirection ou aliases.
5. Régénérer les index spécialisés.
6. Corriger le monolithe uniquement après gel éditorial.
