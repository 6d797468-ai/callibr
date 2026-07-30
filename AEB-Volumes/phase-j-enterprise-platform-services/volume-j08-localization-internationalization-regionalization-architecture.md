# Volume J08 — Localization, Internationalization & Regionalization Architecture

> Extrait généré depuis `Architecture & Engineering Book (AEB).md` le 2026-07-27.

PHASE J — ENTERPRISE PLATFORM SERVICES
Volume J08
Localization, Internationalization & Regionalization Architecture

Version : 1.0

Statut : Enterprise Globalization Foundation

Criticité : Élevée

1. Vision

Callibr doit pouvoir fonctionner dans plusieurs langues, pays, fuseaux horaires et cadres réglementaires.

La localisation couvre :

interface ;
contenu ;
scénarios ;
voix ;
rapports ;
dates ;
devises ;
formats ;
règles régionales.

2. Principe fondamental

La langue n'est pas seulement une traduction.

Elle influence :

ton ;
procédures ;
politesse ;
culture ;
conformité ;
modèles IA ;
évaluation QA.

3. Architecture globale

                    Locale Context


                         │


                         ▼


                    Localization Service


       ┌─────────────────┼─────────────────┐


       ▼                 ▼                 ▼


 Translations       Regional Rules      AI Locale Policy

4. Locale Context

Contexte :

language ;
country ;
timezone ;
currency ;
date_format ;
number_format ;
legal_region ;
voice_locale.

5. Translation Management

Les textes sont externalisés.

Règles :

clé stable ;
fallback ;
version ;
review ;
tenant override ;
contexte UI.

6. Content Localization

Les Domain Packs peuvent avoir :

variantes pays ;
terminologies ;
procédures locales ;
scripts ;
exemples ;
grilles QA.

7. AI Locale Policy

Définit :

modèle autorisé ;
langue réponse ;
registre ;
accent voix ;
règles culturelles ;
sécurité locale.

8. Timezone Correctness

Toutes les dates internes restent timezone-aware.

Affichage selon locale.

Calculs métier selon timezone tenant ou workspace.

9. Data Model

LocaleProfile
-------------

id

tenant_id

language

country

timezone

settings

TranslationKey
--------------

id

key

namespace

default_value

TranslationValue
----------------

id

key_id

locale

value

status

10. API interne

Lire traduction :

GET /localization/translations

Publier locale :

POST /localization/locales/{id}/publish

11. Décisions d'architecture (ADR)

ADR-J08-001
La localisation est une capacité plateforme.

Décision :

Éviter les traductions dispersées.

ADR-J08-002
Les contenus métier sont localisables.

Décision :

Adapter les formations aux marchés.

ADR-J08-003
L'IA respecte la locale.

Décision :

Préserver cohérence linguistique et culturelle.

ADR-J08-004
Les dates sont timezone-aware.

Décision :

Éviter les erreurs multi-régions.

12. Critères d'acceptation

Localization conforme lorsque :

les textes sont externalisés ;
les locales ont fallback ;
les Domain Packs supportent variantes régionales ;
les rapports utilisent les bons formats ;
les modèles IA respectent langue et culture ;
les dates restent correctes.

Décision majeure : Global-Ready Training Platform

Callibr devient déployable dans plusieurs régions sans refonte.
