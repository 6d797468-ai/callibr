# ADR Registry

Mise à jour : 2026-07-27

Total ADR extraits : 287.

Statut : extraction automatique à valider par revue architecture.

## Index Par Phase

### Phase D

| ADR | Titre | Volume | Fichier | Ligne |
| --- | --- | --- | --- | --- |
| ADR-001 | Architecture Micro-Kernel | D01 | [phase-d/adr-001-d01-architecture-micro-kernel.md](phase-d/adr-001-d01-architecture-micro-kernel.md) | 10551 |
| ADR-002 | Event Sourcing | D01 | [phase-d/adr-002-d01-event-sourcing.md](phase-d/adr-002-d01-event-sourcing.md) | 10554 |
| ADR-003 | Hexagonal Architecture | D01 | [phase-d/adr-003-d01-hexagonal-architecture.md](phase-d/adr-003-d01-hexagonal-architecture.md) | 10557 |

### Phase E

| ADR | Titre | Volume | Fichier | Ligne |
| --- | --- | --- | --- | --- |
| ADR-021 | ↓ | E04 | [phase-e/adr-021-e04-adr.md](phase-e/adr-021-e04-adr.md) | 13828 |

### Phase F

| ADR | Titre | Volume | Fichier | Ligne |
| --- | --- | --- | --- | --- |
| ADR-0001 | ADR-0002 | F01 | [phase-f/adr-0001-f01-adr-0002.md](phase-f/adr-0001-f01-adr-0002.md) | 15332 |
| ADR-0002 | ADR-0003 | F01 | [phase-f/adr-0002-f01-adr-0003.md](phase-f/adr-0002-f01-adr-0003.md) | 15334 |
| ADR-0003 | ... | F01 | [phase-f/adr-0003-f01-adr.md](phase-f/adr-0003-f01-adr.md) | 15336 |

### Phase H

| ADR | Titre | Volume | Fichier | Ligne |
| --- | --- | --- | --- | --- |
| ADR-H01-001 | Le LLM ne contient aucune logique métier critique. | H01 | [phase-h/adr-h01-001-h01-le-llm-ne-contient-aucune-logique-metier-critique.md](phase-h/adr-h01-001-h01-le-llm-ne-contient-aucune-logique-metier-critique.md) | 27930 |
| ADR-H01-002 | Tous les appels LLM passent par un Gateway unique. | H01 | [phase-h/adr-h01-002-h01-tous-les-appels-llm-passent-par-un-gateway-unique.md](phase-h/adr-h01-002-h01-tous-les-appels-llm-passent-par-un-gateway-unique.md) | 27938 |
| ADR-H01-003 | Les prompts sont générés dynamiquement. | H01 | [phase-h/adr-h01-003-h01-les-prompts-sont-generes-dynamiquement.md](phase-h/adr-h01-003-h01-les-prompts-sont-generes-dynamiquement.md) | 27946 |
| ADR-H01-004 | Les agents IA sont stateful. | H01 | [phase-h/adr-h01-004-h01-les-agents-ia-sont-stateful.md](phase-h/adr-h01-004-h01-les-agents-ia-sont-stateful.md) | 27954 |
| ADR-H02-001 | Un agent est une entité versionnée. | H02 | [phase-h/adr-h02-001-h02-un-agent-est-une-entite-versionnee.md](phase-h/adr-h02-001-h02-un-agent-est-une-entite-versionnee.md) | 28584 |
| ADR-H02-002 | Les agents sont stateful. | H02 | [phase-h/adr-h02-002-h02-les-agents-sont-stateful.md](phase-h/adr-h02-002-h02-les-agents-sont-stateful.md) | 28591 |
| ADR-H02-003 | Les outils sont contrôlés par permission. | H02 | [phase-h/adr-h02-003-h02-les-outils-sont-controles-par-permission.md](phase-h/adr-h02-003-h02-les-outils-sont-controles-par-permission.md) | 28598 |
| ADR-H02-004 | Les sessions sont totalement isolées. | H02 | [phase-h/adr-h02-004-h02-les-sessions-sont-totalement-isolees.md](phase-h/adr-h02-004-h02-les-sessions-sont-totalement-isolees.md) | 28605 |
| ADR-H03-001 | Les prompts sont des artefacts versionnés. | H03 | [phase-h/adr-h03-001-h03-les-prompts-sont-des-artefacts-versionnes.md](phase-h/adr-h03-001-h03-les-prompts-sont-des-artefacts-versionnes.md) | 29315 |
| ADR-H03-002 | Les prompts passent par un pipeline de déploiement. | H03 | [phase-h/adr-h03-002-h03-les-prompts-passent-par-un-pipeline-de-deploiement.md](phase-h/adr-h03-002-h03-les-prompts-passent-par-un-pipeline-de-deploiement.md) | 29322 |
| ADR-H03-003 | Les prompts sont composables. | H03 | [phase-h/adr-h03-003-h03-les-prompts-sont-composables.md](phase-h/adr-h03-003-h03-les-prompts-sont-composables.md) | 29329 |
| ADR-H03-004 | Les prompts sont mesurables. | H03 | [phase-h/adr-h03-004-h03-les-prompts-sont-mesurables.md](phase-h/adr-h03-004-h03-les-prompts-sont-mesurables.md) | 29336 |
| ADR-H04-001 | Aucun service applicatif ne contacte directement un LLM. | H04 | [phase-h/adr-h04-001-h04-aucun-service-applicatif-ne-contacte-directement-un-llm.md](phase-h/adr-h04-001-h04-aucun-service-applicatif-ne-contacte-directement-un-llm.md) | 30008 |
| ADR-H04-002 | Le choix du modèle est dynamique. | H04 | [phase-h/adr-h04-002-h04-le-choix-du-modele-est-dynamique.md](phase-h/adr-h04-002-h04-le-choix-du-modele-est-dynamique.md) | 30015 |
| ADR-H04-003 | Les politiques de routage sont configurables. | H04 | [phase-h/adr-h04-003-h04-les-politiques-de-routage-sont-configurables.md](phase-h/adr-h04-003-h04-les-politiques-de-routage-sont-configurables.md) | 30022 |
| ADR-H04-004 | Le coût IA est une métrique de premier niveau. | H04 | [phase-h/adr-h04-004-h04-le-cout-ia-est-une-metrique-de-premier-niveau.md](phase-h/adr-h04-004-h04-le-cout-ia-est-une-metrique-de-premier-niveau.md) | 30029 |
| ADR-H05-001 | La mémoire est composée de plusieurs couches. | H05 | [phase-h/adr-h05-001-h05-la-memoire-est-composee-de-plusieurs-couches.md](phase-h/adr-h05-001-h05-la-memoire-est-composee-de-plusieurs-couches.md) | 30738 |
| ADR-H05-002 | Le contexte envoyé au LLM est construit dynamiquement. | H05 | [phase-h/adr-h05-002-h05-le-contexte-envoye-au-llm-est-construit-dynamiquement.md](phase-h/adr-h05-002-h05-le-contexte-envoye-au-llm-est-construit-dynamiquement.md) | 30745 |
| ADR-H05-003 | La mémoire est isolée par tenant. | H05 | [phase-h/adr-h05-003-h05-la-memoire-est-isolee-par-tenant.md](phase-h/adr-h05-003-h05-la-memoire-est-isolee-par-tenant.md) | 30752 |
| ADR-H05-004 | Les connaissances métier passent par un mécanisme RAG. | H05 | [phase-h/adr-h05-004-h05-les-connaissances-metier-passent-par-un-mecanisme-rag.md](phase-h/adr-h05-004-h05-les-connaissances-metier-passent-par-un-mecanisme-rag.md) | 30759 |
| ADR-H06-001 | Les agents n'accèdent jamais directement aux systèmes. | H06 | [phase-h/adr-h06-001-h06-les-agents-n-accedent-jamais-directement-aux-systemes.md](phase-h/adr-h06-001-h06-les-agents-n-accedent-jamais-directement-aux-systemes.md) | 31503 |
| ADR-H06-002 | Les outils sont versionnés. | H06 | [phase-h/adr-h06-002-h06-les-outils-sont-versionnes.md](phase-h/adr-h06-002-h06-les-outils-sont-versionnes.md) | 31510 |
| ADR-H06-003 | Chaque action IA est auditable. | H06 | [phase-h/adr-h06-003-h06-chaque-action-ia-est-auditable.md](phase-h/adr-h06-003-h06-chaque-action-ia-est-auditable.md) | 31517 |
| ADR-H06-004 | Les permissions sont natives au runtime. | H06 | [phase-h/adr-h06-004-h06-les-permissions-sont-natives-au-runtime.md](phase-h/adr-h06-004-h06-les-permissions-sont-natives-au-runtime.md) | 31524 |
| ADR-H07-001 | Les agents sont spécialisés. | H07 | [phase-h/adr-h07-001-h07-les-agents-sont-specialises.md](phase-h/adr-h07-001-h07-les-agents-sont-specialises.md) | 32256 |
| ADR-H07-002 | Les communications passent par un protocole interne. | H07 | [phase-h/adr-h07-002-h07-les-communications-passent-par-un-protocole-interne.md](phase-h/adr-h07-002-h07-les-communications-passent-par-un-protocole-interne.md) | 32263 |
| ADR-H07-003 | L'orchestrateur contrôle les workflows. | H07 | [phase-h/adr-h07-003-h07-l-orchestrateur-controle-les-workflows.md](phase-h/adr-h07-003-h07-l-orchestrateur-controle-les-workflows.md) | 32270 |
| ADR-H07-004 | Les conflits sont arbitrés par des politiques. | H07 | [phase-h/adr-h07-004-h07-les-conflits-sont-arbitres-par-des-politiques.md](phase-h/adr-h07-004-h07-les-conflits-sont-arbitres-par-des-politiques.md) | 32277 |
| ADR-H08-001 | Toute entrée externe est considérée non fiable. | H08 | [phase-h/adr-h08-001-h08-toute-entree-externe-est-consideree-non-fiable.md](phase-h/adr-h08-001-h08-toute-entree-externe-est-consideree-non-fiable.md) | 33023 |
| ADR-H08-002 | Les actions IA nécessitent une validation. | H08 | [phase-h/adr-h08-002-h08-les-actions-ia-necessitent-une-validation.md](phase-h/adr-h08-002-h08-les-actions-ia-necessitent-une-validation.md) | 33030 |
| ADR-H08-003 | Les réponses critiques doivent être évaluées. | H08 | [phase-h/adr-h08-003-h08-les-reponses-critiques-doivent-etre-evaluees.md](phase-h/adr-h08-003-h08-les-reponses-critiques-doivent-etre-evaluees.md) | 33037 |
| ADR-H08-004 | La sécurité IA est une couche transverse. | H08 | [phase-h/adr-h08-004-h08-la-securite-ia-est-une-couche-transverse.md](phase-h/adr-h08-004-h08-la-securite-ia-est-une-couche-transverse.md) | 33044 |
| ADR-H09-001 | Toute évolution IA doit être mesurée. | H09 | [phase-h/adr-h09-001-h09-toute-evolution-ia-doit-etre-mesuree.md](phase-h/adr-h09-001-h09-toute-evolution-ia-doit-etre-mesuree.md) | 33786 |
| ADR-H09-002 | Les évaluations doivent être reproductibles. | H09 | [phase-h/adr-h09-002-h09-les-evaluations-doivent-etre-reproductibles.md](phase-h/adr-h09-002-h09-les-evaluations-doivent-etre-reproductibles.md) | 33793 |
| ADR-H09-003 | Les scores doivent être expliqués. | H09 | [phase-h/adr-h09-003-h09-les-scores-doivent-etre-expliques.md](phase-h/adr-h09-003-h09-les-scores-doivent-etre-expliques.md) | 33800 |
| ADR-H09-004 | Les humains restent une référence qualité. | H09 | [phase-h/adr-h09-004-h09-les-humains-restent-une-reference-qualite.md](phase-h/adr-h09-004-h09-les-humains-restent-une-reference-qualite.md) | 33807 |
| ADR-H10-001 | Toute exécution IA doit produire une trace. | H10 | [phase-h/adr-h10-001-h10-toute-execution-ia-doit-produire-une-trace.md](phase-h/adr-h10-001-h10-toute-execution-ia-doit-produire-une-trace.md) | 34512 |
| ADR-H10-002 | Les métriques IA sont différentes des métriques classiques. | H10 | [phase-h/adr-h10-002-h10-les-metriques-ia-sont-differentes-des-metriques-classiques.md](phase-h/adr-h10-002-h10-les-metriques-ia-sont-differentes-des-metriques-classiques.md) | 34519 |
| ADR-H10-003 | Les données sensibles doivent être protégées dans les logs. | H10 | [phase-h/adr-h10-003-h10-les-donnees-sensibles-doivent-etre-protegees-dans-les-logs.md](phase-h/adr-h10-003-h10-les-donnees-sensibles-doivent-etre-protegees-dans-les-logs.md) | 34526 |
| ADR-H10-004 | Les incidents IA doivent avoir une analyse causale. | H10 | [phase-h/adr-h10-004-h10-les-incidents-ia-doivent-avoir-une-analyse-causale.md](phase-h/adr-h10-004-h10-les-incidents-ia-doivent-avoir-une-analyse-causale.md) | 34533 |
| ADR-H11-001 | Aucun modèle n'est utilisé sans enregistrement. | H11 | [phase-h/adr-h11-001-h11-aucun-modele-n-est-utilise-sans-enregistrement.md](phase-h/adr-h11-001-h11-aucun-modele-n-est-utilise-sans-enregistrement.md) | 35309 |
| ADR-H11-002 | Toute version IA est immuable. | H11 | [phase-h/adr-h11-002-h11-toute-version-ia-est-immuable.md](phase-h/adr-h11-002-h11-toute-version-ia-est-immuable.md) | 35316 |
| ADR-H11-003 | Le déploiement nécessite une validation automatique. | H11 | [phase-h/adr-h11-003-h11-le-deploiement-necessite-une-validation-automatique.md](phase-h/adr-h11-003-h11-le-deploiement-necessite-une-validation-automatique.md) | 35323 |
| ADR-H11-004 | Les performances modèles sont suivies dans le temps. | H11 | [phase-h/adr-h11-004-h11-les-performances-modeles-sont-suivies-dans-le-temps.md](phase-h/adr-h11-004-h11-les-performances-modeles-sont-suivies-dans-le-temps.md) | 35330 |
| ADR-H12-001 | Chaque appel IA doit être facturable. | H12 | [phase-h/adr-h12-001-h12-chaque-appel-ia-doit-etre-facturable.md](phase-h/adr-h12-001-h12-chaque-appel-ia-doit-etre-facturable.md) | 36015 |
| ADR-H12-002 | Le coût influence le routage modèle. | H12 | [phase-h/adr-h12-002-h12-le-cout-influence-le-routage-modele.md](phase-h/adr-h12-002-h12-le-cout-influence-le-routage-modele.md) | 36022 |
| ADR-H12-003 | Les optimisations ne doivent pas dégrader la qualité. | H12 | [phase-h/adr-h12-003-h12-les-optimisations-ne-doivent-pas-degrader-la-qualite.md](phase-h/adr-h12-003-h12-les-optimisations-ne-doivent-pas-degrader-la-qualite.md) | 36029 |
| ADR-H12-004 | Les budgets sont des garde-fous opérationnels. | H12 | [phase-h/adr-h12-004-h12-les-budgets-sont-des-garde-fous-operationnels.md](phase-h/adr-h12-004-h12-les-budgets-sont-des-garde-fous-operationnels.md) | 36036 |
| ADR-H13-001 | Aucun système IA sans propriétaire identifié. | H13 | [phase-h/adr-h13-001-h13-aucun-systeme-ia-sans-proprietaire-identifie.md](phase-h/adr-h13-001-h13-aucun-systeme-ia-sans-proprietaire-identifie.md) | 36765 |
| ADR-H13-002 | Tout actif IA doit être enregistré. | H13 | [phase-h/adr-h13-002-h13-tout-actif-ia-doit-etre-enregistre.md](phase-h/adr-h13-002-h13-tout-actif-ia-doit-etre-enregistre.md) | 36772 |
| ADR-H13-003 | Le risque détermine le niveau de contrôle. | H13 | [phase-h/adr-h13-003-h13-le-risque-determine-le-niveau-de-controle.md](phase-h/adr-h13-003-h13-le-risque-determine-le-niveau-de-controle.md) | 36779 |
| ADR-H13-004 | La gouvernance accompagne tout le cycle de vie. | H13 | [phase-h/adr-h13-004-h13-la-gouvernance-accompagne-tout-le-cycle-de-vie.md](phase-h/adr-h13-004-h13-la-gouvernance-accompagne-tout-le-cycle-de-vie.md) | 36786 |
| ADR-H14-001 | Aucun agent n'a d'accès implicite. | H14 | [phase-h/adr-h14-001-h14-aucun-agent-n-a-d-acces-implicite.md](phase-h/adr-h14-001-h14-aucun-agent-n-a-d-acces-implicite.md) | 37588 |
| ADR-H14-002 | Les modèles externes sont considérés non fiables. | H14 | [phase-h/adr-h14-002-h14-les-modeles-externes-sont-consideres-non-fiables.md](phase-h/adr-h14-002-h14-les-modeles-externes-sont-consideres-non-fiables.md) | 37595 |
| ADR-H14-003 | Les données doivent être protégées avant traitement IA. | H14 | [phase-h/adr-h14-003-h14-les-donnees-doivent-etre-protegees-avant-traitement-ia.md](phase-h/adr-h14-003-h14-les-donnees-doivent-etre-protegees-avant-traitement-ia.md) | 37602 |
| ADR-H14-004 | L'identité agent est obligatoire. | H14 | [phase-h/adr-h14-004-h14-l-identite-agent-est-obligatoire.md](phase-h/adr-h14-004-h14-l-identite-agent-est-obligatoire.md) | 37609 |
| ADR-H15-001 | Toute IA critique doit avoir un plan d'exploitation. | H15 | [phase-h/adr-h15-001-h15-toute-ia-critique-doit-avoir-un-plan-d-exploitation.md](phase-h/adr-h15-001-h15-toute-ia-critique-doit-avoir-un-plan-d-exploitation.md) | 38317 |
| ADR-H15-002 | Les déploiements IA sont progressifs. | H15 | [phase-h/adr-h15-002-h15-les-deploiements-ia-sont-progressifs.md](phase-h/adr-h15-002-h15-les-deploiements-ia-sont-progressifs.md) | 38324 |
| ADR-H15-003 | La récupération est testée régulièrement. | H15 | [phase-h/adr-h15-003-h15-la-recuperation-est-testee-regulierement.md](phase-h/adr-h15-003-h15-la-recuperation-est-testee-regulierement.md) | 38331 |
| ADR-H15-004 | L'exploitation IA est automatisée au maximum. | H15 | [phase-h/adr-h15-004-h15-l-exploitation-ia-est-automatisee-au-maximum.md](phase-h/adr-h15-004-h15-l-exploitation-ia-est-automatisee-au-maximum.md) | 38338 |

### Phase I

| ADR | Titre | Volume | Fichier | Ligne |
| --- | --- | --- | --- | --- |
| ADR-I01-001 | Le produit est piloté par la valeur utilisateur. | I01 | [phase-i/adr-i01-001-i01-le-produit-est-pilote-par-la-valeur-utilisateur.md](phase-i/adr-i01-001-i01-le-produit-est-pilote-par-la-valeur-utilisateur.md) | 39005 |
| ADR-I01-002 | Chaque domaine produit possède un propriétaire. | I01 | [phase-i/adr-i01-002-i01-chaque-domaine-produit-possede-un-proprietaire.md](phase-i/adr-i01-002-i01-chaque-domaine-produit-possede-un-proprietaire.md) | 39012 |
| ADR-I01-003 | Les décisions produit sont basées sur les données. | I01 | [phase-i/adr-i01-003-i01-les-decisions-produit-sont-basees-sur-les-donnees.md](phase-i/adr-i01-003-i01-les-decisions-produit-sont-basees-sur-les-donnees.md) | 39019 |
| ADR-I01-004 | Les releases suivent un cycle contrôlé. | I01 | [phase-i/adr-i01-004-i01-les-releases-suivent-un-cycle-controle.md](phase-i/adr-i01-004-i01-les-releases-suivent-un-cycle-controle.md) | 39026 |
| ADR-I02-001 | Le tenant est une frontière de sécurité. | I02 | [phase-i/adr-i02-001-i02-le-tenant-est-une-frontiere-de-securite.md](phase-i/adr-i02-001-i02-le-tenant-est-une-frontiere-de-securite.md) | 39830 |
| ADR-I02-002 | L'identité tenant est propagée partout. | I02 | [phase-i/adr-i02-002-i02-l-identite-tenant-est-propagee-partout.md](phase-i/adr-i02-002-i02-l-identite-tenant-est-propagee-partout.md) | 39837 |
| ADR-I02-003 | L'architecture supporte plusieurs niveaux d'isolation. | I02 | [phase-i/adr-i02-003-i02-l-architecture-supporte-plusieurs-niveaux-d-isolation.md](phase-i/adr-i02-003-i02-l-architecture-supporte-plusieurs-niveaux-d-isolation.md) | 39844 |
| ADR-I02-004 | Les ressources sont gouvernées par tenant. | I02 | [phase-i/adr-i02-004-i02-les-ressources-sont-gouvernees-par-tenant.md](phase-i/adr-i02-004-i02-les-ressources-sont-gouvernees-par-tenant.md) | 39851 |
| ADR-I03-001 | Le client possède un cycle de vie complet. | I03 | [phase-i/adr-i03-001-i03-le-client-possede-un-cycle-de-vie-complet.md](phase-i/adr-i03-001-i03-le-client-possede-un-cycle-de-vie-complet.md) | 40555 |
| ADR-I03-002 | La valeur doit être mesurée. | I03 | [phase-i/adr-i03-002-i03-la-valeur-doit-etre-mesuree.md](phase-i/adr-i03-002-i03-la-valeur-doit-etre-mesuree.md) | 40562 |
| ADR-I03-003 | Le churn doit être anticipé. | I03 | [phase-i/adr-i03-003-i03-le-churn-doit-etre-anticipe.md](phase-i/adr-i03-003-i03-le-churn-doit-etre-anticipe.md) | 40569 |
| ADR-I03-004 | Le Customer Success utilise les données produit. | I03 | [phase-i/adr-i03-004-i03-le-customer-success-utilise-les-donnees-produit.md](phase-i/adr-i03-004-i03-le-customer-success-utilise-les-donnees-produit.md) | 40576 |
| ADR-I04-001 | Le billing est découplé du produit. | I04 | [phase-i/adr-i04-001-i04-le-billing-est-decouple-du-produit.md](phase-i/adr-i04-001-i04-le-billing-est-decouple-du-produit.md) | 41394 |
| ADR-I04-002 | Toute consommation doit être mesurable. | I04 | [phase-i/adr-i04-002-i04-toute-consommation-doit-etre-mesurable.md](phase-i/adr-i04-002-i04-toute-consommation-doit-etre-mesurable.md) | 41401 |
| ADR-I04-003 | Les droits produit dépendent des entitlements. | I04 | [phase-i/adr-i04-003-i04-les-droits-produit-dependent-des-entitlements.md](phase-i/adr-i04-003-i04-les-droits-produit-dependent-des-entitlements.md) | 41408 |
| ADR-I04-004 | Les fournisseurs de paiement sont abstraits. | I04 | [phase-i/adr-i04-004-i04-les-fournisseurs-de-paiement-sont-abstraits.md](phase-i/adr-i04-004-i04-les-fournisseurs-de-paiement-sont-abstraits.md) | 41415 |
| ADR-I05-001 | Les intégrations sont des produits techniques versionnés. | I05 | [phase-i/adr-i05-001-i05-les-integrations-sont-des-produits-techniques-versionnes.md](phase-i/adr-i05-001-i05-les-integrations-sont-des-produits-techniques-versionnes.md) | 42140 |
| ADR-I05-002 | Le modèle canonique protège le domaine. | I05 | [phase-i/adr-i05-002-i05-le-modele-canonique-protege-le-domaine.md](phase-i/adr-i05-002-i05-le-modele-canonique-protege-le-domaine.md) | 42147 |
| ADR-I05-003 | Toutes les synchronisations sont observables. | I05 | [phase-i/adr-i05-003-i05-toutes-les-synchronisations-sont-observables.md](phase-i/adr-i05-003-i05-toutes-les-synchronisations-sont-observables.md) | 42154 |
| ADR-I05-004 | Les webhooks sont signés, rejouables et idempotents. | I05 | [phase-i/adr-i05-004-i05-les-webhooks-sont-signes-rejouables-et-idempotents.md](phase-i/adr-i05-004-i05-les-webhooks-sont-signes-rejouables-et-idempotents.md) | 42161 |
| ADR-I06-001 | L'API est un produit. | I06 | [phase-i/adr-i06-001-i06-l-api-est-un-produit.md](phase-i/adr-i06-001-i06-l-api-est-un-produit.md) | 42746 |
| ADR-I06-002 | OpenAPI est la source de vérité. | I06 | [phase-i/adr-i06-002-i06-openapi-est-la-source-de-verite.md](phase-i/adr-i06-002-i06-openapi-est-la-source-de-verite.md) | 42753 |
| ADR-I06-003 | La compatibilité ascendante est obligatoire. | I06 | [phase-i/adr-i06-003-i06-la-compatibilite-ascendante-est-obligatoire.md](phase-i/adr-i06-003-i06-la-compatibilite-ascendante-est-obligatoire.md) | 42760 |
| ADR-I06-004 | L'API Gateway applique les politiques transverses. | I06 | [phase-i/adr-i06-004-i06-l-api-gateway-applique-les-politiques-transverses.md](phase-i/adr-i06-004-i06-l-api-gateway-applique-les-politiques-transverses.md) | 42767 |
| ADR-I07-001 | Toute extension est décrite par un manifest. | I07 | [phase-i/adr-i07-001-i07-toute-extension-est-decrite-par-un-manifest.md](phase-i/adr-i07-001-i07-toute-extension-est-decrite-par-un-manifest.md) | 43267 |
| ADR-I07-002 | La marketplace applique une certification. | I07 | [phase-i/adr-i07-002-i07-la-marketplace-applique-une-certification.md](phase-i/adr-i07-002-i07-la-marketplace-applique-une-certification.md) | 43274 |
| ADR-I07-003 | Les permissions sont explicites. | I07 | [phase-i/adr-i07-003-i07-les-permissions-sont-explicites.md](phase-i/adr-i07-003-i07-les-permissions-sont-explicites.md) | 43281 |
| ADR-I07-004 | Les extensions sont versionnées et rollbackables. | I07 | [phase-i/adr-i07-004-i07-les-extensions-sont-versionnees-et-rollbackables.md](phase-i/adr-i07-004-i07-les-extensions-sont-versionnees-et-rollbackables.md) | 43288 |
| ADR-I08-001 | Les partenaires sont des organisations autonomes. | I08 | [phase-i/adr-i08-001-i08-les-partenaires-sont-des-organisations-autonomes.md](phase-i/adr-i08-001-i08-les-partenaires-sont-des-organisations-autonomes.md) | 43782 |
| ADR-I08-002 | L'accès délégué est limité, justifié et audité. | I08 | [phase-i/adr-i08-002-i08-l-acces-delegue-est-limite-justifie-et-audite.md](phase-i/adr-i08-002-i08-l-acces-delegue-est-limite-justifie-et-audite.md) | 43789 |
| ADR-I08-003 | La certification contrôle la qualité écosystème. | I08 | [phase-i/adr-i08-003-i08-la-certification-controle-la-qualite-ecosysteme.md](phase-i/adr-i08-003-i08-la-certification-controle-la-qualite-ecosysteme.md) | 43796 |
| ADR-I08-004 | Les revenus partenaires sont mesurables. | I08 | [phase-i/adr-i08-004-i08-les-revenus-partenaires-sont-mesurables.md](phase-i/adr-i08-004-i08-les-revenus-partenaires-sont-mesurables.md) | 43803 |
| ADR-I09-001 | Le revenu est piloté par une métrique de valeur. | I09 | [phase-i/adr-i09-001-i09-le-revenu-est-pilote-par-une-metrique-de-valeur.md](phase-i/adr-i09-001-i09-le-revenu-est-pilote-par-une-metrique-de-valeur.md) | 44365 |
| ADR-I09-002 | Quote-to-cash est un flux gouverné. | I09 | [phase-i/adr-i09-002-i09-quote-to-cash-est-un-flux-gouverne.md](phase-i/adr-i09-002-i09-quote-to-cash-est-un-flux-gouverne.md) | 44372 |
| ADR-I09-003 | Usage et revenu sont reliés par événement. | I09 | [phase-i/adr-i09-003-i09-usage-et-revenu-sont-relies-par-evenement.md](phase-i/adr-i09-003-i09-usage-et-revenu-sont-relies-par-evenement.md) | 44379 |
| ADR-I09-004 | RevOps possède une source de vérité. | I09 | [phase-i/adr-i09-004-i09-revops-possede-une-source-de-verite.md](phase-i/adr-i09-004-i09-revops-possede-une-source-de-verite.md) | 44386 |
| ADR-I10-001 | La croissance est pilotée par événements. | I10 | [phase-i/adr-i10-001-i10-la-croissance-est-pilotee-par-evenements.md](phase-i/adr-i10-001-i10-la-croissance-est-pilotee-par-evenements.md) | 44930 |
| ADR-I10-002 | L'expérimentation est gouvernée. | I10 | [phase-i/adr-i10-002-i10-l-experimentation-est-gouvernee.md](phase-i/adr-i10-002-i10-l-experimentation-est-gouvernee.md) | 44937 |
| ADR-I10-003 | La croissance respecte la confiance Enterprise. | I10 | [phase-i/adr-i10-003-i10-la-croissance-respecte-la-confiance-enterprise.md](phase-i/adr-i10-003-i10-la-croissance-respecte-la-confiance-enterprise.md) | 44944 |
| ADR-I10-004 | Les boucles marketplace et partenaires font partie du growth. | I10 | [phase-i/adr-i10-004-i10-les-boucles-marketplace-et-partenaires-font-partie-du-growth.md](phase-i/adr-i10-004-i10-les-boucles-marketplace-et-partenaires-font-partie-du-growth.md) | 44951 |
| ADR-I11-001 | Les événements métiers sont la base de la Data Platform. | I11 | [phase-i/adr-i11-001-i11-les-evenements-metiers-sont-la-base-de-la-data-platform.md](phase-i/adr-i11-001-i11-les-evenements-metiers-sont-la-base-de-la-data-platform.md) | 45428 |
| ADR-I11-002 | Tous les événements ont une enveloppe canonique. | I11 | [phase-i/adr-i11-002-i11-tous-les-evenements-ont-une-enveloppe-canonique.md](phase-i/adr-i11-002-i11-tous-les-evenements-ont-une-enveloppe-canonique.md) | 45435 |
| ADR-I11-003 | Le replay est une capacité de plateforme. | I11 | [phase-i/adr-i11-003-i11-le-replay-est-une-capacite-de-plateforme.md](phase-i/adr-i11-003-i11-le-replay-est-une-capacite-de-plateforme.md) | 45442 |
| ADR-I11-004 | Les schémas d'événements sont gouvernés. | I11 | [phase-i/adr-i11-004-i11-les-schemas-d-evenements-sont-gouvernes.md](phase-i/adr-i11-004-i11-les-schemas-d-evenements-sont-gouvernes.md) | 45449 |
| ADR-I12-001 | Les KPI sont définis comme des contrats. | I12 | [phase-i/adr-i12-001-i12-les-kpi-sont-definis-comme-des-contrats.md](phase-i/adr-i12-001-i12-les-kpi-sont-definis-comme-des-contrats.md) | 45774 |
| ADR-I12-002 | Le Semantic Layer est obligatoire. | I12 | [phase-i/adr-i12-002-i12-le-semantic-layer-est-obligatoire.md](phase-i/adr-i12-002-i12-le-semantic-layer-est-obligatoire.md) | 45781 |
| ADR-I12-003 | Les benchmarks inter-tenants sont anonymisés. | I12 | [phase-i/adr-i12-003-i12-les-benchmarks-inter-tenants-sont-anonymises.md](phase-i/adr-i12-003-i12-les-benchmarks-inter-tenants-sont-anonymises.md) | 45788 |
| ADR-I12-004 | Les dashboards consomment des métriques gouvernées. | I12 | [phase-i/adr-i12-004-i12-les-dashboards-consomment-des-metriques-gouvernees.md](phase-i/adr-i12-004-i12-les-dashboards-consomment-des-metriques-gouvernees.md) | 45795 |
| ADR-I13-001 | Les bases transactionnelles ne servent pas de warehouse. | I13 | [phase-i/adr-i13-001-i13-les-bases-transactionnelles-ne-servent-pas-de-warehouse.md](phase-i/adr-i13-001-i13-les-bases-transactionnelles-ne-servent-pas-de-warehouse.md) | 46085 |
| ADR-I13-002 | Les datasets sont des produits. | I13 | [phase-i/adr-i13-002-i13-les-datasets-sont-des-produits.md](phase-i/adr-i13-002-i13-les-datasets-sont-des-produits.md) | 46092 |
| ADR-I13-003 | Le stockage analytique supporte schema evolution. | I13 | [phase-i/adr-i13-003-i13-le-stockage-analytique-supporte-schema-evolution.md](phase-i/adr-i13-003-i13-le-stockage-analytique-supporte-schema-evolution.md) | 46099 |
| ADR-I13-004 | Le coût data est attribuable. | I13 | [phase-i/adr-i13-004-i13-le-cout-data-est-attribuable.md](phase-i/adr-i13-004-i13-le-cout-data-est-attribuable.md) | 46106 |
| ADR-I14-001 | Les features IA sont gouvernées. | I14 | [phase-i/adr-i14-001-i14-les-features-ia-sont-gouvernees.md](phase-i/adr-i14-001-i14-les-features-ia-sont-gouvernees.md) | 46391 |
| ADR-I14-002 | Offline et online stores sont séparés. | I14 | [phase-i/adr-i14-002-i14-offline-et-online-stores-sont-separes.md](phase-i/adr-i14-002-i14-offline-et-online-stores-sont-separes.md) | 46398 |
| ADR-I14-003 | La correction temporelle est obligatoire. | I14 | [phase-i/adr-i14-003-i14-la-correction-temporelle-est-obligatoire.md](phase-i/adr-i14-003-i14-la-correction-temporelle-est-obligatoire.md) | 46405 |
| ADR-I14-004 | Le drift est surveillé. | I14 | [phase-i/adr-i14-004-i14-le-drift-est-surveille.md](phase-i/adr-i14-004-i14-le-drift-est-surveille.md) | 46412 |
| ADR-I15-001 | La recherche sémantique est multi-tenant par conception. | I15 | [phase-i/adr-i15-001-i15-la-recherche-semantique-est-multi-tenant-par-conception.md](phase-i/adr-i15-001-i15-la-recherche-semantique-est-multi-tenant-par-conception.md) | 46707 |
| ADR-I15-002 | Chaque chunk est traçable jusqu'à sa source. | I15 | [phase-i/adr-i15-002-i15-chaque-chunk-est-tracable-jusqu-a-sa-source.md](phase-i/adr-i15-002-i15-chaque-chunk-est-tracable-jusqu-a-sa-source.md) | 46714 |
| ADR-I15-003 | Le retrieval est évalué automatiquement. | I15 | [phase-i/adr-i15-003-i15-le-retrieval-est-evalue-automatiquement.md](phase-i/adr-i15-003-i15-le-retrieval-est-evalue-automatiquement.md) | 46721 |
| ADR-I15-004 | Les embeddings sont versionnés. | I15 | [phase-i/adr-i15-004-i15-les-embeddings-sont-versionnes.md](phase-i/adr-i15-004-i15-les-embeddings-sont-versionnes.md) | 46728 |
| ADR-I16-001 | Les concepts métier sont modélisés dans un graphe. | I16 | [phase-i/adr-i16-001-i16-les-concepts-metier-sont-modelises-dans-un-graphe.md](phase-i/adr-i16-001-i16-les-concepts-metier-sont-modelises-dans-un-graphe.md) | 47001 |
| ADR-I16-002 | Le graphe distingue ontologie globale et extensions tenant. | I16 | [phase-i/adr-i16-002-i16-le-graphe-distingue-ontologie-globale-et-extensions-tenant.md](phase-i/adr-i16-002-i16-le-graphe-distingue-ontologie-globale-et-extensions-tenant.md) | 47008 |
| ADR-I16-003 | Le graphe complète le RAG vectoriel. | I16 | [phase-i/adr-i16-003-i16-le-graphe-complete-le-rag-vectoriel.md](phase-i/adr-i16-003-i16-le-graphe-complete-le-rag-vectoriel.md) | 47015 |
| ADR-I16-004 | Le raisonnement doit rester explicable. | I16 | [phase-i/adr-i16-004-i16-le-raisonnement-doit-rester-explicable.md](phase-i/adr-i16-004-i16-le-raisonnement-doit-rester-explicable.md) | 47022 |
| ADR-I17-001 | La gouvernance data est intégrée à la plateforme. | I17 | [phase-i/adr-i17-001-i17-la-gouvernance-data-est-integree-a-la-plateforme.md](phase-i/adr-i17-001-i17-la-gouvernance-data-est-integree-a-la-plateforme.md) | 47261 |
| ADR-I17-002 | Chaque asset possède un owner. | I17 | [phase-i/adr-i17-002-i17-chaque-asset-possede-un-owner.md](phase-i/adr-i17-002-i17-chaque-asset-possede-un-owner.md) | 47268 |
| ADR-I17-003 | La classification contrôle les usages. | I17 | [phase-i/adr-i17-003-i17-la-classification-controle-les-usages.md](phase-i/adr-i17-003-i17-la-classification-controle-les-usages.md) | 47275 |
| ADR-I17-004 | La qualité bloque les publications critiques. | I17 | [phase-i/adr-i17-004-i17-la-qualite-bloque-les-publications-critiques.md](phase-i/adr-i17-004-i17-la-qualite-bloque-les-publications-critiques.md) | 47282 |
| ADR-I18-001 | L'audit est append-only. | I18 | [phase-i/adr-i18-001-i18-l-audit-est-append-only.md](phase-i/adr-i18-001-i18-l-audit-est-append-only.md) | 47537 |
| ADR-I18-002 | Le lineage est graphe. | I18 | [phase-i/adr-i18-002-i18-le-lineage-est-graphe.md](phase-i/adr-i18-002-i18-le-lineage-est-graphe.md) | 47544 |
| ADR-I18-003 | Les preuves IA sont conservées. | I18 | [phase-i/adr-i18-003-i18-les-preuves-ia-sont-conservees.md](phase-i/adr-i18-003-i18-les-preuves-ia-sont-conservees.md) | 47551 |
| ADR-I18-004 | Les rapports conformité sont générables. | I18 | [phase-i/adr-i18-004-i18-les-rapports-conformite-sont-generables.md](phase-i/adr-i18-004-i18-les-rapports-conformite-sont-generables.md) | 47558 |
| ADR-I19-001 | Les rapports dérivent de métriques gouvernées. | I19 | [phase-i/adr-i19-001-i19-les-rapports-derivent-de-metriques-gouvernees.md](phase-i/adr-i19-001-i19-les-rapports-derivent-de-metriques-gouvernees.md) | 47779 |
| ADR-I19-002 | La narration IA est séparée du calcul. | I19 | [phase-i/adr-i19-002-i19-la-narration-ia-est-separee-du-calcul.md](phase-i/adr-i19-002-i19-la-narration-ia-est-separee-du-calcul.md) | 47786 |
| ADR-I19-003 | Les rapports sont versionnés. | I19 | [phase-i/adr-i19-003-i19-les-rapports-sont-versionnes.md](phase-i/adr-i19-003-i19-les-rapports-sont-versionnes.md) | 47793 |
| ADR-I19-004 | Les audiences contrôlent les vues. | I19 | [phase-i/adr-i19-004-i19-les-audiences-controlent-les-vues.md](phase-i/adr-i19-004-i19-les-audiences-controlent-les-vues.md) | 47800 |
| ADR-I20-001 | Le streaming est séparé du batch. | I20 | [phase-i/adr-i20-001-i20-le-streaming-est-separe-du-batch.md](phase-i/adr-i20-001-i20-le-streaming-est-separe-du-batch.md) | 48047 |
| ADR-I20-002 | Les garanties sont choisies par cas d'usage. | I20 | [phase-i/adr-i20-002-i20-les-garanties-sont-choisies-par-cas-d-usage.md](phase-i/adr-i20-002-i20-les-garanties-sont-choisies-par-cas-d-usage.md) | 48054 |
| ADR-I20-003 | Les vues temps réel sont dérivées d'événements. | I20 | [phase-i/adr-i20-003-i20-les-vues-temps-reel-sont-derivees-d-evenements.md](phase-i/adr-i20-003-i20-les-vues-temps-reel-sont-derivees-d-evenements.md) | 48061 |
| ADR-I20-004 | Les alertes sont gouvernées. | I20 | [phase-i/adr-i20-004-i20-les-alertes-sont-gouvernees.md](phase-i/adr-i20-004-i20-les-alertes-sont-gouvernees.md) | 48068 |

### Phase J

| ADR | Titre | Volume | Fichier | Ligne |
| --- | --- | --- | --- | --- |
| ADR-J01-001 | L'identité est fédérable. | J01 | [phase-j/adr-j01-001-j01-l-identite-est-federable.md](phase-j/adr-j01-001-j01-l-identite-est-federable.md) | 48401 |
| ADR-J01-002 | Les sessions portent le contexte tenant. | J01 | [phase-j/adr-j01-002-j01-les-sessions-portent-le-contexte-tenant.md](phase-j/adr-j01-002-j01-les-sessions-portent-le-contexte-tenant.md) | 48408 |
| ADR-J01-003 | Les comptes de service sont séparés des utilisateurs humains. | J01 | [phase-j/adr-j01-003-j01-les-comptes-de-service-sont-separes-des-utilisateurs-humains.md](phase-j/adr-j01-003-j01-les-comptes-de-service-sont-separes-des-utilisateurs-humains.md) | 48415 |
| ADR-J01-004 | Le MFA est piloté par politique. | J01 | [phase-j/adr-j01-004-j01-le-mfa-est-pilote-par-politique.md](phase-j/adr-j01-004-j01-le-mfa-est-pilote-par-politique.md) | 48422 |
| ADR-J02-001 | RBAC et ABAC sont combinés. | J02 | [phase-j/adr-j02-001-j02-rbac-et-abac-sont-combines.md](phase-j/adr-j02-001-j02-rbac-et-abac-sont-combines.md) | 48646 |
| ADR-J02-002 | Le Policy Decision Point est central. | J02 | [phase-j/adr-j02-002-j02-le-policy-decision-point-est-central.md](phase-j/adr-j02-002-j02-le-policy-decision-point-est-central.md) | 48653 |
| ADR-J02-003 | Deny by default. | J02 | [phase-j/adr-j02-003-j02-deny-by-default.md](phase-j/adr-j02-003-j02-deny-by-default.md) | 48660 |
| ADR-J02-004 | Les décisions sont auditées. | J02 | [phase-j/adr-j02-004-j02-les-decisions-sont-auditees.md](phase-j/adr-j02-004-j02-les-decisions-sont-auditees.md) | 48667 |
| ADR-J03-001 | Le tenant est la frontière de sécurité. | J03 | [phase-j/adr-j03-001-j03-le-tenant-est-la-frontiere-de-securite.md](phase-j/adr-j03-001-j03-le-tenant-est-la-frontiere-de-securite.md) | 48875 |
| ADR-J03-002 | La configuration suit une hiérarchie contrôlée. | J03 | [phase-j/adr-j03-002-j03-la-configuration-suit-une-hierarchie-controlee.md](phase-j/adr-j03-002-j03-la-configuration-suit-une-hierarchie-controlee.md) | 48882 |
| ADR-J03-003 | Les workspaces sont des frontières opérationnelles. | J03 | [phase-j/adr-j03-003-j03-les-workspaces-sont-des-frontieres-operationnelles.md](phase-j/adr-j03-003-j03-les-workspaces-sont-des-frontieres-operationnelles.md) | 48889 |
| ADR-J03-004 | Le lifecycle est explicite. | J03 | [phase-j/adr-j03-004-j03-le-lifecycle-est-explicite.md](phase-j/adr-j03-004-j03-le-lifecycle-est-explicite.md) | 48896 |
| ADR-J04-001 | Les entitlements sont séparés du billing. | J04 | [phase-j/adr-j04-001-j04-les-entitlements-sont-separes-du-billing.md](phase-j/adr-j04-001-j04-les-entitlements-sont-separes-du-billing.md) | 49078 |
| ADR-J04-002 | Les quotas sont appliqués par points d'exécution. | J04 | [phase-j/adr-j04-002-j04-les-quotas-sont-appliques-par-points-d-execution.md](phase-j/adr-j04-002-j04-les-quotas-sont-appliques-par-points-d-execution.md) | 49085 |
| ADR-J04-003 | Les dépassements produisent des événements. | J04 | [phase-j/adr-j04-003-j04-les-depassements-produisent-des-evenements.md](phase-j/adr-j04-003-j04-les-depassements-produisent-des-evenements.md) | 49092 |
| ADR-J04-004 | Les plans sont versionnés. | J04 | [phase-j/adr-j04-004-j04-les-plans-sont-versionnes.md](phase-j/adr-j04-004-j04-les-plans-sont-versionnes.md) | 49099 |
| ADR-J05-001 | Toute extension possède un manifest. | J05 | [phase-j/adr-j05-001-j05-toute-extension-possede-un-manifest.md](phase-j/adr-j05-001-j05-toute-extension-possede-un-manifest.md) | 49292 |
| ADR-J05-002 | Le runtime est isolé. | J05 | [phase-j/adr-j05-002-j05-le-runtime-est-isole.md](phase-j/adr-j05-002-j05-le-runtime-est-isole.md) | 49299 |
| ADR-J05-003 | Les permissions sont explicites. | J05 | [phase-j/adr-j05-003-j05-les-permissions-sont-explicites.md](phase-j/adr-j05-003-j05-les-permissions-sont-explicites.md) | 49306 |
| ADR-J05-004 | Les extensions sont révocables. | J05 | [phase-j/adr-j05-004-j05-les-extensions-sont-revocables.md](phase-j/adr-j05-004-j05-les-extensions-sont-revocables.md) | 49313 |
| ADR-J06-001 | L'installation marketplace est gouvernée. | J06 | [phase-j/adr-j06-001-j06-l-installation-marketplace-est-gouvernee.md](phase-j/adr-j06-001-j06-l-installation-marketplace-est-gouvernee.md) | 49488 |
| ADR-J06-002 | La compatibilité est calculée avant installation. | J06 | [phase-j/adr-j06-002-j06-la-compatibilite-est-calculee-avant-installation.md](phase-j/adr-j06-002-j06-la-compatibilite-est-calculee-avant-installation.md) | 49495 |
| ADR-J06-003 | Le rollback est obligatoire. | J06 | [phase-j/adr-j06-003-j06-le-rollback-est-obligatoire.md](phase-j/adr-j06-003-j06-le-rollback-est-obligatoire.md) | 49502 |
| ADR-J06-004 | Les installations sont tenant-scoped. | J06 | [phase-j/adr-j06-004-j06-les-installations-sont-tenant-scoped.md](phase-j/adr-j06-004-j06-les-installations-sont-tenant-scoped.md) | 49509 |
| ADR-J07-001 | Le white label est déclaratif. | J07 | [phase-j/adr-j07-001-j07-le-white-label-est-declaratif.md](phase-j/adr-j07-001-j07-le-white-label-est-declaratif.md) | 49701 |
| ADR-J07-002 | Les thèmes sont validés. | J07 | [phase-j/adr-j07-002-j07-les-themes-sont-valides.md](phase-j/adr-j07-002-j07-les-themes-sont-valides.md) | 49708 |
| ADR-J07-003 | Les domaines personnalisés sont vérifiés. | J07 | [phase-j/adr-j07-003-j07-les-domaines-personnalises-sont-verifies.md](phase-j/adr-j07-003-j07-les-domaines-personnalises-sont-verifies.md) | 49715 |
| ADR-J07-004 | La terminologie est tenant-scoped. | J07 | [phase-j/adr-j07-004-j07-la-terminologie-est-tenant-scoped.md](phase-j/adr-j07-004-j07-la-terminologie-est-tenant-scoped.md) | 49722 |
| ADR-J08-001 | La localisation est une capacité plateforme. | J08 | [phase-j/adr-j08-001-j08-la-localisation-est-une-capacite-plateforme.md](phase-j/adr-j08-001-j08-la-localisation-est-une-capacite-plateforme.md) | 49915 |
| ADR-J08-002 | Les contenus métier sont localisables. | J08 | [phase-j/adr-j08-002-j08-les-contenus-metier-sont-localisables.md](phase-j/adr-j08-002-j08-les-contenus-metier-sont-localisables.md) | 49922 |
| ADR-J08-003 | L'IA respecte la locale. | J08 | [phase-j/adr-j08-003-j08-l-ia-respecte-la-locale.md](phase-j/adr-j08-003-j08-l-ia-respecte-la-locale.md) | 49929 |
| ADR-J08-004 | Les dates sont timezone-aware. | J08 | [phase-j/adr-j08-004-j08-les-dates-sont-timezone-aware.md](phase-j/adr-j08-004-j08-les-dates-sont-timezone-aware.md) | 49936 |
| ADR-J09-001 | Les droits RGPD sont workflow-driven. | J09 | [phase-j/adr-j09-001-j09-les-droits-rgpd-sont-workflow-driven.md](phase-j/adr-j09-001-j09-les-droits-rgpd-sont-workflow-driven.md) | 50129 |
| ADR-J09-002 | La rétention est policy-driven. | J09 | [phase-j/adr-j09-002-j09-la-retention-est-policy-driven.md](phase-j/adr-j09-002-j09-la-retention-est-policy-driven.md) | 50136 |
| ADR-J09-003 | La résidence des données est contrôlée. | J09 | [phase-j/adr-j09-003-j09-la-residence-des-donnees-est-controlee.md](phase-j/adr-j09-003-j09-la-residence-des-donnees-est-controlee.md) | 50143 |
| ADR-J09-004 | Chaque action conformité produit une preuve. | J09 | [phase-j/adr-j09-004-j09-chaque-action-conformite-produit-une-preuve.md](phase-j/adr-j09-004-j09-chaque-action-conformite-produit-une-preuve.md) | 50150 |
| ADR-J10-001 | Les APIs sont packagées en produits. | J10 | [phase-j/adr-j10-001-j10-les-apis-sont-packagees-en-produits.md](phase-j/adr-j10-001-j10-les-apis-sont-packagees-en-produits.md) | 50327 |
| ADR-J10-002 | Le Gateway applique les politiques. | J10 | [phase-j/adr-j10-002-j10-le-gateway-applique-les-politiques.md](phase-j/adr-j10-002-j10-le-gateway-applique-les-politiques.md) | 50334 |
| ADR-J10-003 | Le portail développeur est obligatoire. | J10 | [phase-j/adr-j10-003-j10-le-portail-developpeur-est-obligatoire.md](phase-j/adr-j10-003-j10-le-portail-developpeur-est-obligatoire.md) | 50341 |
| ADR-J10-004 | Les dépréciations sont gouvernées. | J10 | [phase-j/adr-j10-004-j10-les-depreciations-sont-gouvernees.md](phase-j/adr-j10-004-j10-les-depreciations-sont-gouvernees.md) | 50348 |
| ADR-J11-001 | Les connecteurs ont une couche opérations. | J11 | [phase-j/adr-j11-001-j11-les-connecteurs-ont-une-couche-operations.md](phase-j/adr-j11-001-j11-les-connecteurs-ont-une-couche-operations.md) | 50506 |
| ADR-J11-002 | Les mappings sont versionnés. | J11 | [phase-j/adr-j11-002-j11-les-mappings-sont-versionnes.md](phase-j/adr-j11-002-j11-les-mappings-sont-versionnes.md) | 50513 |
| ADR-J11-003 | Les erreurs sont classifiées. | J11 | [phase-j/adr-j11-003-j11-les-erreurs-sont-classifiees.md](phase-j/adr-j11-003-j11-les-erreurs-sont-classifiees.md) | 50520 |
| ADR-J11-004 | Les runbooks sont intégrés. | J11 | [phase-j/adr-j11-004-j11-les-runbooks-sont-integres.md](phase-j/adr-j11-004-j11-les-runbooks-sont-integres.md) | 50527 |
| ADR-J12-001 | Les notifications sont event-driven. | J12 | [phase-j/adr-j12-001-j12-les-notifications-sont-event-driven.md](phase-j/adr-j12-001-j12-les-notifications-sont-event-driven.md) | 50707 |
| ADR-J12-002 | Les templates sont versionnés. | J12 | [phase-j/adr-j12-002-j12-les-templates-sont-versionnes.md](phase-j/adr-j12-002-j12-les-templates-sont-versionnes.md) | 50714 |
| ADR-J12-003 | Les préférences utilisateur sont respectées. | J12 | [phase-j/adr-j12-003-j12-les-preferences-utilisateur-sont-respectees.md](phase-j/adr-j12-003-j12-les-preferences-utilisateur-sont-respectees.md) | 50721 |
| ADR-J12-004 | Les notifications critiques contournent les silences selon policy. | J12 | [phase-j/adr-j12-004-j12-les-notifications-critiques-contournent-les-silences-selon-policy.md](phase-j/adr-j12-004-j12-les-notifications-critiques-contournent-les-silences-selon-policy.md) | 50728 |
| ADR-J13-001 | Aucune opération admin hors API. | J13 | [phase-j/adr-j13-001-j13-aucune-operation-admin-hors-api.md](phase-j/adr-j13-001-j13-aucune-operation-admin-hors-api.md) | 50891 |
| ADR-J13-002 | Les actions sensibles exigent approbation. | J13 | [phase-j/adr-j13-002-j13-les-actions-sensibles-exigent-approbation.md](phase-j/adr-j13-002-j13-les-actions-sensibles-exigent-approbation.md) | 50898 |
| ADR-J13-003 | Break glass est contrôlé. | J13 | [phase-j/adr-j13-003-j13-break-glass-est-controle.md](phase-j/adr-j13-003-j13-break-glass-est-controle.md) | 50905 |
| ADR-J13-004 | L'audit est consultable par rôle. | J13 | [phase-j/adr-j13-004-j13-l-audit-est-consultable-par-role.md](phase-j/adr-j13-004-j13-l-audit-est-consultable-par-role.md) | 50912 |
| ADR-J14-001 | La configuration est versionnée. | J14 | [phase-j/adr-j14-001-j14-la-configuration-est-versionnee.md](phase-j/adr-j14-001-j14-la-configuration-est-versionnee.md) | 51092 |
| ADR-J14-002 | Les flags sont typés par usage. | J14 | [phase-j/adr-j14-002-j14-les-flags-sont-types-par-usage.md](phase-j/adr-j14-002-j14-les-flags-sont-types-par-usage.md) | 51099 |
| ADR-J14-003 | Les kill switches sont prioritaires. | J14 | [phase-j/adr-j14-003-j14-les-kill-switches-sont-prioritaires.md](phase-j/adr-j14-003-j14-les-kill-switches-sont-prioritaires.md) | 51106 |
| ADR-J14-004 | La configuration est évaluée par contexte. | J14 | [phase-j/adr-j14-004-j14-la-configuration-est-evaluee-par-contexte.md](phase-j/adr-j14-004-j14-la-configuration-est-evaluee-par-contexte.md) | 51113 |
| ADR-J15-001 | Chaque service critique possède un SLO. | J15 | [phase-j/adr-j15-001-j15-chaque-service-critique-possede-un-slo.md](phase-j/adr-j15-001-j15-chaque-service-critique-possede-un-slo.md) | 51314 |
| ADR-J15-002 | Les SLA dérivent des SLO. | J15 | [phase-j/adr-j15-002-j15-les-sla-derivent-des-slo.md](phase-j/adr-j15-002-j15-les-sla-derivent-des-slo.md) | 51321 |
| ADR-J15-003 | Les modes dégradés sont conçus. | J15 | [phase-j/adr-j15-003-j15-les-modes-degrades-sont-concus.md](phase-j/adr-j15-003-j15-les-modes-degrades-sont-concus.md) | 51328 |
| ADR-J15-004 | Les incidents produisent postmortem et actions. | J15 | [phase-j/adr-j15-004-j15-les-incidents-produisent-postmortem-et-actions.md](phase-j/adr-j15-004-j15-les-incidents-produisent-postmortem-et-actions.md) | 51335 |

### Phase K

| ADR | Titre | Volume | Fichier | Ligne |
| --- | --- | --- | --- | --- |
| ADR-K01-001 | La Developer Platform est un produit interne. | K01 | [phase-k/adr-k01-001-k01-la-developer-platform-est-un-produit-interne.md](phase-k/adr-k01-001-k01-la-developer-platform-est-un-produit-interne.md) | 51630 |
| ADR-K01-002 | Les Golden Paths sont obligatoires pour les nouveaux composants. | K01 | [phase-k/adr-k01-002-k01-les-golden-paths-sont-obligatoires-pour-les-nouveaux-composants.md](phase-k/adr-k01-002-k01-les-golden-paths-sont-obligatoires-pour-les-nouveaux-composants.md) | 51637 |
| ADR-K01-003 | La sécurité est intégrée au pipeline. | K01 | [phase-k/adr-k01-003-k01-la-securite-est-integree-au-pipeline.md](phase-k/adr-k01-003-k01-la-securite-est-integree-au-pipeline.md) | 51644 |
| ADR-K01-004 | Le catalogue de services est source de vérité. | K01 | [phase-k/adr-k01-004-k01-le-catalogue-de-services-est-source-de-verite.md](phase-k/adr-k01-004-k01-le-catalogue-de-services-est-source-de-verite.md) | 51651 |
| ADR-K02-001 | Le pipeline est la voie unique de livraison. | K02 | [phase-k/adr-k02-001-k02-le-pipeline-est-la-voie-unique-de-livraison.md](phase-k/adr-k02-001-k02-le-pipeline-est-la-voie-unique-de-livraison.md) | 51862 |
| ADR-K02-002 | Les quality gates bloquent la promotion. | K02 | [phase-k/adr-k02-002-k02-les-quality-gates-bloquent-la-promotion.md](phase-k/adr-k02-002-k02-les-quality-gates-bloquent-la-promotion.md) | 51869 |
| ADR-K02-003 | Les artefacts sont promus sans rebuild. | K02 | [phase-k/adr-k02-003-k02-les-artefacts-sont-promus-sans-rebuild.md](phase-k/adr-k02-003-k02-les-artefacts-sont-promus-sans-rebuild.md) | 51876 |
| ADR-K02-004 | Les pipelines sont versionnés. | K02 | [phase-k/adr-k02-004-k02-les-pipelines-sont-versionnes.md](phase-k/adr-k02-004-k02-les-pipelines-sont-versionnes.md) | 51883 |
| ADR-K03-001 | Git est la source de vérité des environnements. | K03 | [phase-k/adr-k03-001-k03-git-est-la-source-de-verite-des-environnements.md](phase-k/adr-k03-001-k03-git-est-la-source-de-verite-des-environnements.md) | 52064 |
| ADR-K03-002 | Les promotions suivent un flux contrôlé. | K03 | [phase-k/adr-k03-002-k03-les-promotions-suivent-un-flux-controle.md](phase-k/adr-k03-002-k03-les-promotions-suivent-un-flux-controle.md) | 52071 |
| ADR-K03-003 | Le drift est détecté. | K03 | [phase-k/adr-k03-003-k03-le-drift-est-detecte.md](phase-k/adr-k03-003-k03-le-drift-est-detecte.md) | 52078 |
| ADR-K03-004 | Les secrets ne sont pas stockés en clair. | K03 | [phase-k/adr-k03-004-k03-les-secrets-ne-sont-pas-stockes-en-clair.md](phase-k/adr-k03-004-k03-les-secrets-ne-sont-pas-stockes-en-clair.md) | 52085 |
| ADR-K04-001 | Les images sont immuables. | K04 | [phase-k/adr-k04-001-k04-les-images-sont-immuables.md](phase-k/adr-k04-001-k04-les-images-sont-immuables.md) | 52279 |
| ADR-K04-002 | Les SBOM sont obligatoires. | K04 | [phase-k/adr-k04-002-k04-les-sbom-sont-obligatoires.md](phase-k/adr-k04-002-k04-les-sbom-sont-obligatoires.md) | 52286 |
| ADR-K04-003 | Les images production sont signées. | K04 | [phase-k/adr-k04-003-k04-les-images-production-sont-signees.md](phase-k/adr-k04-003-k04-les-images-production-sont-signees.md) | 52293 |
| ADR-K04-004 | Les vulnérabilités critiques bloquent la promotion. | K04 | [phase-k/adr-k04-004-k04-les-vulnerabilites-critiques-bloquent-la-promotion.md](phase-k/adr-k04-004-k04-les-vulnerabilites-critiques-bloquent-la-promotion.md) | 52300 |
| ADR-K05-001 | Kubernetes est le runtime production recommandé. | K05 | [phase-k/adr-k05-001-k05-kubernetes-est-le-runtime-production-recommande.md](phase-k/adr-k05-001-k05-kubernetes-est-le-runtime-production-recommande.md) | 52484 |
| ADR-K05-002 | Les namespaces isolent les responsabilités. | K05 | [phase-k/adr-k05-002-k05-les-namespaces-isolent-les-responsabilites.md](phase-k/adr-k05-002-k05-les-namespaces-isolent-les-responsabilites.md) | 52491 |
| ADR-K05-003 | Les network policies sont restrictives. | K05 | [phase-k/adr-k05-003-k05-les-network-policies-sont-restrictives.md](phase-k/adr-k05-003-k05-les-network-policies-sont-restrictives.md) | 52498 |
| ADR-K05-004 | Chaque workload déclare ses ressources. | K05 | [phase-k/adr-k05-004-k05-chaque-workload-declare-ses-ressources.md](phase-k/adr-k05-004-k05-chaque-workload-declare-ses-ressources.md) | 52505 |
| ADR-K06-001 | Terraform est le standard IaC principal. | K06 | [phase-k/adr-k06-001-k06-terraform-est-le-standard-iac-principal.md](phase-k/adr-k06-001-k06-terraform-est-le-standard-iac-principal.md) | 52684 |
| ADR-K06-002 | Les states sont isolés par environnement. | K06 | [phase-k/adr-k06-002-k06-les-states-sont-isoles-par-environnement.md](phase-k/adr-k06-002-k06-les-states-sont-isoles-par-environnement.md) | 52691 |
| ADR-K06-003 | Policy as Code bloque les ressources non conformes. | K06 | [phase-k/adr-k06-003-k06-policy-as-code-bloque-les-ressources-non-conformes.md](phase-k/adr-k06-003-k06-policy-as-code-bloque-les-ressources-non-conformes.md) | 52698 |
| ADR-K06-004 | Le drift est surveillé. | K06 | [phase-k/adr-k06-004-k06-le-drift-est-surveille.md](phase-k/adr-k06-004-k06-le-drift-est-surveille.md) | 52705 |
| ADR-K07-001 | OpenTelemetry est le standard de tracing. | K07 | [phase-k/adr-k07-001-k07-opentelemetry-est-le-standard-de-tracing.md](phase-k/adr-k07-001-k07-opentelemetry-est-le-standard-de-tracing.md) | 52898 |
| ADR-K07-002 | Les alertes critiques sont liées à des runbooks. | K07 | [phase-k/adr-k07-002-k07-les-alertes-critiques-sont-liees-a-des-runbooks.md](phase-k/adr-k07-002-k07-les-alertes-critiques-sont-liees-a-des-runbooks.md) | 52905 |
| ADR-K07-003 | Les SLO pilotent l'alerting. | K07 | [phase-k/adr-k07-003-k07-les-slo-pilotent-l-alerting.md](phase-k/adr-k07-003-k07-les-slo-pilotent-l-alerting.md) | 52912 |
| ADR-K07-004 | Les données sensibles sont exclues des logs. | K07 | [phase-k/adr-k07-004-k07-les-donnees-sensibles-sont-exclues-des-logs.md](phase-k/adr-k07-004-k07-les-donnees-sensibles-sont-exclues-des-logs.md) | 52919 |
| ADR-K08-001 | Les backups sont automatisés et testés. | K08 | [phase-k/adr-k08-001-k08-les-backups-sont-automatises-et-testes.md](phase-k/adr-k08-001-k08-les-backups-sont-automatises-et-testes.md) | 53099 |
| ADR-K08-002 | Les objectifs RPO/RTO sont définis par criticité. | K08 | [phase-k/adr-k08-002-k08-les-objectifs-rpo-rto-sont-definis-par-criticite.md](phase-k/adr-k08-002-k08-les-objectifs-rpo-rto-sont-definis-par-criticite.md) | 53106 |
| ADR-K08-003 | La restauration tenant est supportée. | K08 | [phase-k/adr-k08-003-k08-la-restauration-tenant-est-supportee.md](phase-k/adr-k08-003-k08-la-restauration-tenant-est-supportee.md) | 53113 |
| ADR-K08-004 | Les DR drills sont obligatoires. | K08 | [phase-k/adr-k08-004-k08-les-dr-drills-sont-obligatoires.md](phase-k/adr-k08-004-k08-les-dr-drills-sont-obligatoires.md) | 53120 |
| ADR-K09-001 | Chaque service critique possède un budget performance. | K09 | [phase-k/adr-k09-001-k09-chaque-service-critique-possede-un-budget-performance.md](phase-k/adr-k09-001-k09-chaque-service-critique-possede-un-budget-performance.md) | 53311 |
| ADR-K09-002 | Les tests de charge font partie de la release. | K09 | [phase-k/adr-k09-002-k09-les-tests-de-charge-font-partie-de-la-release.md](phase-k/adr-k09-002-k09-les-tests-de-charge-font-partie-de-la-release.md) | 53318 |
| ADR-K09-003 | Le noisy neighbor est testé. | K09 | [phase-k/adr-k09-003-k09-le-noisy-neighbor-est-teste.md](phase-k/adr-k09-003-k09-le-noisy-neighbor-est-teste.md) | 53325 |
| ADR-K09-004 | Le capacity planning est continu. | K09 | [phase-k/adr-k09-004-k09-le-capacity-planning-est-continu.md](phase-k/adr-k09-004-k09-le-capacity-planning-est-continu.md) | 53332 |
| ADR-K10-001 | Les releases sont gouvernées. | K10 | [phase-k/adr-k10-001-k10-les-releases-sont-gouvernees.md](phase-k/adr-k10-001-k10-les-releases-sont-gouvernees.md) | 53530 |
| ADR-K10-002 | Les changements IA suivent le même contrôle que le code. | K10 | [phase-k/adr-k10-002-k10-les-changements-ia-suivent-le-meme-controle-que-le-code.md](phase-k/adr-k10-002-k10-les-changements-ia-suivent-le-meme-controle-que-le-code.md) | 53537 |
| ADR-K10-003 | Les rollouts progressifs sont préférés. | K10 | [phase-k/adr-k10-003-k10-les-rollouts-progressifs-sont-preferes.md](phase-k/adr-k10-003-k10-les-rollouts-progressifs-sont-preferes.md) | 53544 |
| ADR-K10-004 | Chaque release possède un plan rollback. | K10 | [phase-k/adr-k10-004-k10-chaque-release-possede-un-plan-rollback.md](phase-k/adr-k10-004-k10-chaque-release-possede-un-plan-rollback.md) | 53551 |

### Phase L

| ADR | Titre | Volume | Fichier | Ligne |
| --- | --- | --- | --- | --- |
| ADR-L01-001 | Les décisions structurantes exigent un ADR. | L01 | [phase-l/adr-l01-001-l01-les-decisions-structurantes-exigent-un-adr.md](phase-l/adr-l01-001-l01-les-decisions-structurantes-exigent-un-adr.md) | 53839 |
| ADR-L01-002 | Les ADR sont immuables après acceptation. | L01 | [phase-l/adr-l01-002-l01-les-adr-sont-immuables-apres-acceptation.md](phase-l/adr-l01-002-l01-les-adr-sont-immuables-apres-acceptation.md) | 53846 |
| ADR-L01-003 | Le registry ADR est interrogeable. | L01 | [phase-l/adr-l01-003-l01-le-registry-adr-est-interrogeable.md](phase-l/adr-l01-003-l01-le-registry-adr-est-interrogeable.md) | 53853 |
| ADR-L01-004 | Les exceptions aux standards expirent. | L01 | [phase-l/adr-l01-004-l01-les-exceptions-aux-standards-expirent.md](phase-l/adr-l01-004-l01-les-exceptions-aux-standards-expirent.md) | 53860 |
| ADR-L02-001 | Le RFC précède les changements complexes. | L02 | [phase-l/adr-l02-001-l02-le-rfc-precede-les-changements-complexes.md](phase-l/adr-l02-001-l02-le-rfc-precede-les-changements-complexes.md) | 54066 |
| ADR-L02-002 | Les impacts sont explicitement évalués. | L02 | [phase-l/adr-l02-002-l02-les-impacts-sont-explicitement-evalues.md](phase-l/adr-l02-002-l02-les-impacts-sont-explicitement-evalues.md) | 54073 |
| ADR-L02-003 | Le RFC peut produire PRD, ADR ou backlog. | L02 | [phase-l/adr-l02-003-l02-le-rfc-peut-produire-prd-adr-ou-backlog.md](phase-l/adr-l02-003-l02-le-rfc-peut-produire-prd-adr-ou-backlog.md) | 54080 |
| ADR-L02-004 | Les fenêtres de feedback sont limitées. | L02 | [phase-l/adr-l02-004-l02-les-fenetres-de-feedback-sont-limitees.md](phase-l/adr-l02-004-l02-les-fenetres-de-feedback-sont-limitees.md) | 54087 |
| ADR-L03-001 | La roadmap est pilotée par outcomes. | L03 | [phase-l/adr-l03-001-l03-la-roadmap-est-pilotee-par-outcomes.md](phase-l/adr-l03-001-l03-la-roadmap-est-pilotee-par-outcomes.md) | 54288 |
| ADR-L03-002 | Les initiatives appartiennent à un portefeuille. | L03 | [phase-l/adr-l03-002-l03-les-initiatives-appartiennent-a-un-portefeuille.md](phase-l/adr-l03-002-l03-les-initiatives-appartiennent-a-un-portefeuille.md) | 54295 |
| ADR-L03-003 | Les décisions produit sont tracées. | L03 | [phase-l/adr-l03-003-l03-les-decisions-produit-sont-tracees.md](phase-l/adr-l03-003-l03-les-decisions-produit-sont-tracees.md) | 54302 |
| ADR-L03-004 | La dette et la sécurité sont des catégories d'investissement. | L03 | [phase-l/adr-l03-004-l03-la-dette-et-la-securite-sont-des-categories-d-investissement.md](phase-l/adr-l03-004-l03-la-dette-et-la-securite-sont-des-categories-d-investissement.md) | 54309 |
| ADR-L04-001 | Les métriques produit ont un owner. | L04 | [phase-l/adr-l04-001-l04-les-metriques-produit-ont-un-owner.md](phase-l/adr-l04-001-l04-les-metriques-produit-ont-un-owner.md) | 54510 |
| ADR-L04-002 | Les OKR sont liés aux métriques gouvernées. | L04 | [phase-l/adr-l04-002-l04-les-okr-sont-lies-aux-metriques-gouvernees.md](phase-l/adr-l04-002-l04-les-okr-sont-lies-aux-metriques-gouvernees.md) | 54517 |
| ADR-L04-003 | Chaque métrique critique a des guardrails. | L04 | [phase-l/adr-l04-003-l04-chaque-metrique-critique-a-des-guardrails.md](phase-l/adr-l04-003-l04-chaque-metrique-critique-a-des-guardrails.md) | 54524 |
| ADR-L04-004 | Les expérimentations ont des règles de décision. | L04 | [phase-l/adr-l04-004-l04-les-experimentations-ont-des-regles-de-decision.md](phase-l/adr-l04-004-l04-les-experimentations-ont-des-regles-de-decision.md) | 54531 |
| ADR-L05-001 | Les standards sont catalogués. | L05 | [phase-l/adr-l05-001-l05-les-standards-sont-catalogues.md](phase-l/adr-l05-001-l05-les-standards-sont-catalogues.md) | 54728 |
| ADR-L05-002 | Les exceptions expirent. | L05 | [phase-l/adr-l05-002-l05-les-exceptions-expirent.md](phase-l/adr-l05-002-l05-les-exceptions-expirent.md) | 54735 |
| ADR-L05-003 | Le Technology Radar guide les choix. | L05 | [phase-l/adr-l05-003-l05-le-technology-radar-guide-les-choix.md](phase-l/adr-l05-003-l05-le-technology-radar-guide-les-choix.md) | 54742 |
| ADR-L05-004 | Les revues sont proportionnelles au risque. | L05 | [phase-l/adr-l05-004-l05-les-revues-sont-proportionnelles-au-risque.md](phase-l/adr-l05-004-l05-les-revues-sont-proportionnelles-au-risque.md) | 54749 |
| ADR-L06-001 | La dette technique est enregistrée. | L06 | [phase-l/adr-l06-001-l06-la-dette-technique-est-enregistree.md](phase-l/adr-l06-001-l06-la-dette-technique-est-enregistree.md) | 54947 |
| ADR-L06-002 | Chaque dette possède owner et score. | L06 | [phase-l/adr-l06-002-l06-chaque-dette-possede-owner-et-score.md](phase-l/adr-l06-002-l06-chaque-dette-possede-owner-et-score.md) | 54954 |
| ADR-L06-003 | La dépréciation suit un lifecycle. | L06 | [phase-l/adr-l06-003-l06-la-depreciation-suit-un-lifecycle.md](phase-l/adr-l06-003-l06-la-depreciation-suit-un-lifecycle.md) | 54961 |
| ADR-L06-004 | Les assets IA ont aussi une dette. | L06 | [phase-l/adr-l06-004-l06-les-assets-ia-ont-aussi-une-dette.md](phase-l/adr-l06-004-l06-les-assets-ia-ont-aussi-une-dette.md) | 54968 |
| ADR-L07-001 | Les changements sensibles exigent threat model. | L07 | [phase-l/adr-l07-001-l07-les-changements-sensibles-exigent-threat-model.md](phase-l/adr-l07-001-l07-les-changements-sensibles-exigent-threat-model.md) | 55149 |
| ADR-L07-002 | Les risques acceptés expirent. | L07 | [phase-l/adr-l07-002-l07-les-risques-acceptes-expirent.md](phase-l/adr-l07-002-l07-les-risques-acceptes-expirent.md) | 55156 |
| ADR-L07-003 | Les gates sécurité sont intégrés à la delivery. | L07 | [phase-l/adr-l07-003-l07-les-gates-securite-sont-integres-a-la-delivery.md](phase-l/adr-l07-003-l07-les-gates-securite-sont-integres-a-la-delivery.md) | 55163 |
| ADR-L07-004 | Les findings critiques bloquent la release. | L07 | [phase-l/adr-l07-004-l07-les-findings-critiques-bloquent-la-release.md](phase-l/adr-l07-004-l07-les-findings-critiques-bloquent-la-release.md) | 55170 |
| ADR-L08-001 | Les workflows critiques exigent Design Review. | L08 | [phase-l/adr-l08-001-l08-les-workflows-critiques-exigent-design-review.md](phase-l/adr-l08-001-l08-les-workflows-critiques-exigent-design-review.md) | 55355 |
| ADR-L08-002 | Le design system est versionné. | L08 | [phase-l/adr-l08-002-l08-le-design-system-est-versionne.md](phase-l/adr-l08-002-l08-le-design-system-est-versionne.md) | 55362 |
| ADR-L08-003 | L'accessibilité est un gate. | L08 | [phase-l/adr-l08-003-l08-l-accessibilite-est-un-gate.md](phase-l/adr-l08-003-l08-l-accessibilite-est-un-gate.md) | 55369 |
| ADR-L08-004 | Les métriques UX alimentent la roadmap. | L08 | [phase-l/adr-l08-004-l08-les-metriques-ux-alimentent-la-roadmap.md](phase-l/adr-l08-004-l08-les-metriques-ux-alimentent-la-roadmap.md) | 55376 |
| ADR-L09-001 | Les contrôles sont catalogués. | L09 | [phase-l/adr-l09-001-l09-les-controles-sont-catalogues.md](phase-l/adr-l09-001-l09-les-controles-sont-catalogues.md) | 55569 |
| ADR-L09-002 | Les preuves sont collectées automatiquement quand possible. | L09 | [phase-l/adr-l09-002-l09-les-preuves-sont-collectees-automatiquement-quand-possible.md](phase-l/adr-l09-002-l09-les-preuves-sont-collectees-automatiquement-quand-possible.md) | 55576 |
| ADR-L09-003 | Les contrôles sont mappés aux frameworks. | L09 | [phase-l/adr-l09-003-l09-les-controles-sont-mappes-aux-frameworks.md](phase-l/adr-l09-003-l09-les-controles-sont-mappes-aux-frameworks.md) | 55583 |
| ADR-L09-004 | Les exceptions sont liées aux contrôles. | L09 | [phase-l/adr-l09-004-l09-les-exceptions-sont-liees-aux-controles.md](phase-l/adr-l09-004-l09-les-exceptions-sont-liees-aux-controles.md) | 55590 |
| ADR-L10-001 | Les releases critiques passent par gates. | L10 | [phase-l/adr-l10-001-l10-les-releases-critiques-passent-par-gates.md](phase-l/adr-l10-001-l10-les-releases-critiques-passent-par-gates.md) | 55826 |
| ADR-L10-002 | Chaque gate exige une preuve. | L10 | [phase-l/adr-l10-002-l10-chaque-gate-exige-une-preuve.md](phase-l/adr-l10-002-l10-chaque-gate-exige-une-preuve.md) | 55833 |
| ADR-L10-003 | Les changements IA ont un AI Gate. | L10 | [phase-l/adr-l10-003-l10-les-changements-ia-ont-un-ai-gate.md](phase-l/adr-l10-003-l10-les-changements-ia-ont-un-ai-gate.md) | 55840 |
| ADR-L10-004 | Les décisions conditionnelles sont suivies. | L10 | [phase-l/adr-l10-004-l10-les-decisions-conditionnelles-sont-suivies.md](phase-l/adr-l10-004-l10-les-decisions-conditionnelles-sont-suivies.md) | 55847 |
