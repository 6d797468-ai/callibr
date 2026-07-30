# Audit Complet Callibr - AEB, Implementation et Trajectoire Enterprise

Date : 2026-07-28  
Produit : Callibr  
Reference architecturale interne : ATOS - AI Training Operating System  
Perimetre audite : AEB, volumes modulaires, plan d'implementation, code MVP actuel, tests, roadmap cible  
Niveau de lecture : Principal Architect / Consultant Senior SaaS, IA, plateformes distribuees

---

## 1. Synthese Executive

Callibr a franchi deux etapes majeures :

1. une etape architecturale tres avancee, avec un Architecture & Engineering Book couvrant les phases A a L ;
2. une etape d'execution initiale, avec une premiere tranche MVP executable autour de l'authentification demo, de la simulation SAV, des actions CRM et de l'audit de session.

Le diagnostic central est le suivant :

> Callibr dispose aujourd'hui d'une architecture cible de niveau Enterprise, mais son implementation est encore au stade fondation MVP. Cet ecart est normal a ce stade, mais il doit maintenant etre pilote par une matrice stricte de priorisation, de tracabilite et de preuves d'execution.

L'AEB est devenu une reference tres riche, proche d'un system design book complet. En revanche, le code actuel couvre surtout le noyau local et une verticale SAV simple. Les briques critiques du MVP pedagogique restent a stabiliser : evaluation detaillee, rapport de session, procedure engine, isolation tenant, tests PostgreSQL, roles/permissions, observabilite minimale et traçabilite documentaire vers le code.

### Verdict Global

| Axe | Evaluation | Commentaire |
| --- | ---: | --- |
| Reference architecturale AEB | 8.5 / 10 | Couverture tres large A-L, nombreux volumes, vision Enterprise claire. |
| Maintenabilite documentaire | 6.5 / 10 | Fort contenu, mais monolithe peu structure en vrais titres Markdown et quelques incoherences de numerotation. |
| MVP executable | 5.5 / 10 | Boucle locale fonctionnelle, mais evaluation/report/procedure et durcissement manquent encore. |
| Alignement architecture-code | 5.0 / 10 | Le squelette respecte l'AEB, mais la tracabilite n'est pas encore systematique. |
| Securite production | 2.5 / 10 | IAM volontairement MVP, pas pret production. |
| Data & persistence | 3.5 / 10 | Adapters PostgreSQL presents, mais integration et migrations non industrialisees. |
| IA/LLM Platform | 1.0 / 10 | Pas encore implementee, choix sain pour eviter de mettre le LLM trop tot. |
| Enterprise readiness | 2.0 / 10 | Vision documentee, implementation encore locale/MVP. |

### Position De Maturite

| Niveau | Etat actuel |
| --- | --- |
| Documentation d'architecture | Tres avancee, environ 85-90 % de la cible conceptuelle A-L. |
| Documentation exploitable par build/RAG | Moyenne, environ 60-70 %, a cause de la normalisation et de la structure Markdown restante. |
| MVP produit | Environ 40-45 % de la cible MVP fonctionnelle. |
| Plateforme Enterprise complete | Environ 5-8 % de la cible implementee. |
| Risque global | Moyen a eleve si l'on poursuit sans gouvernance de priorisation ; acceptable si l'on continue par vertical slices. |

---

## 2. Sources Et Elements Audites

### Documentation AEB

- `Architecture & Engineering Book (AEB).md`
- `AEB-Volumes/AEB-MASTER-INDEX.md`
- `AEB-Volumes/_indexes/NORMALIZATION-REPORT.md`
- index ADR, API, events, engines, data models, scenarios, traceability matrix
- volumes A a L

### Documentation Implementation

- `implementation/IMPLEMENTATION-INDEX.md`
- `implementation/STATUS.md`
- `implementation/implementation-manifest.json`
- `implementation/00-overview/CALLIBR-IMPLEMENTATION-MASTER-PLAN.md`
- `implementation/00-overview/MVP-SCOPE.md`
- `implementation/01-roadmap/DELIVERY-ROADMAP.md`
- `implementation/02-backlog/EPIC-BACKLOG.md`
- `implementation/03-sprints/*`
- `implementation/04-architecture-to-code/*`
- `implementation/05-delivery/DELIVERY-GOVERNANCE.md`
- `implementation/06-risks/RISK-REGISTER.md`
- `implementation/07-decisions/IMPLEMENTATION-DECISIONS.md`

### Code Et Runtime

- backend FastAPI : `apps/api`
- frontend Vite/React : `apps/frontend`
- packages contracts, kernel, persistence, telemetry
- platform identity
- engines scenario, simulation, CRM
- infrastructure PostgreSQL locale
- tests API et unitaires

---

## 3. Indicateurs Quantitatifs

### Documentation

| Indicateur | Valeur observee |
| --- | ---: |
| Lignes du monolithe AEB | 55 916 |
| Fichiers Markdown dans `AEB-Volumes` | 426 |
| Volumes detectes par rapport de normalisation | 124 |
| Volumes comptes par fichiers `volume-*.md` | 125 |
| ADR detectes | 287 |
| Endpoints API detectes dans l'AEB | 205 |
| Evenements detectes dans l'AEB | 112 |
| Engines/services detectes dans l'AEB | 1 022 |
| Modeles de donnees detectes dans l'AEB | 213 |
| Entrees scenario detectees | 169 |
| Documents implementation | 20 avant cet audit |

Note d'audit : l'ecart 124/125 vient probablement des doublons et volumes composites deja signales dans le rapport de normalisation.

### Code Et Runtime

| Indicateur | Valeur observee |
| --- | ---: |
| Fichiers projet audites hors dependances et build | 115 |
| Lignes applicatives/tests dans les zones actives | 3 363 |
| Endpoints FastAPI metier observes | 12 hors docs OpenAPI |
| Tests automatises observes | 34 passes lors de la derniere verification |
| Build frontend | OK lors de la derniere verification |
| Lint Python | OK lors de la derniere verification |
| Depot Git local detecte | Non detecte dans le workspace courant |

---

## 4. Etat Actuel Du Projet

### 4.1 Capacites Deja Executables

Le projet n'est plus seulement documentaire. Il dispose d'une premiere verticale locale utilisable :

- backend FastAPI minimal ;
- frontend Vite/React connecte a l'API ;
- Docker Compose local ;
- contexte tenant/user demo ;
- endpoint `/api/v1/auth/login` ;
- endpoint `/api/v1/me` ;
- token bearer signe pour le MVP ;
- hash de mot de passe PBKDF2 ;
- stores identite memoire et PostgreSQL ;
- endpoint `/api/v1/scenarios` ;
- demarrage de session de simulation ;
- envoi de messages de simulation ;
- moteur de simulation texte deterministe ;
- evaluation simple par regles ;
- moteur d'actions CRM simulees ;
- execution d'actions CRM depuis le frontend ;
- audit trail par session ;
- propagation `X-Trace-Id` ;
- schema PostgreSQL initial pour sessions, audit, tenants et users ;
- tests API et unitaires.

### 4.2 Parcours Produit Disponible

Le parcours actuellement disponible correspond a une demo locale :

1. l'utilisateur demo se connecte ou est connecte automatiquement ;
2. le frontend recupere la liste des scenarios ;
3. l'apprenant demarre une session SAV ;
4. le client simule envoie un message d'ouverture ;
5. l'apprenant repond ;
6. le moteur evalue le tour par mots-cles/comportements attendus ;
7. le client simule repond ;
8. l'apprenant peut executer des actions CRM ;
9. les evenements sont journalises dans l'audit trail ;
10. l'interface affiche le score et les traces principales.

Ce parcours est coherent avec une strategie de vertical slice. Il constitue une bonne base de demo interne, mais pas encore un MVP pedagogique complet.

### 4.3 Capacites Non Encore Maturees

Les capacites suivantes restent a developper ou durcir :

- rapport final de session ;
- evaluation detaillee par criteres, ponderations et preuves ;
- procedure engine ;
- persona engine explicite ;
- conversation engine separe du service de simulation ;
- end session / close session ;
- progression apprenant ;
- coaching structure ;
- dashboard historique ;
- roles et permissions ;
- isolation tenant sur toutes les lectures/mutations ;
- tests d'integration PostgreSQL ;
- migrations versionnees ;
- observabilite metrics/traces ;
- CI/CD ;
- registry de domain packs ;
- integration LLM derriere interface stable ;
- gouvernance de release.

---

## 5. Comparaison AEB Cible vs Implementation Actuelle

### 5.1 Lecture Par Phases A-L

| Phase AEB | Cible Documentee | Etat Implementation | Ecart Principal |
| --- | --- | --- | --- |
| A - Fondations | Vision, principes, gouvernance, standards | Documentation tres avancee ; implementation plan initialise | Besoin d'une matrice de decision vivante et de criteres produit mesurables. |
| B - Architecture metier | DDD, SOE, Persona, Scenario, Rule, CRM, Conversation, Evaluation | Scenario, Simulation et CRM partiels ; evaluation simple | Conversation, persona, procedure, rule et evaluation restent a separer en engines dedies. |
| C - Platform Core | Kernel, event bus, multi-tenant, gateway, runtime infra | Kernel minimal, EventBus in-process, contexte tenant | Pas d'event sourcing, CQRS, outbox, gateway, SDK, runtime cloud. |
| D - Engineering Standards | Monorepo, qualite, tests, implementation blueprint | Monorepo, tests, lint, packages separes | Pas encore de CI, coverage gates, typing strict, policies automatiques. |
| E - AI Engineering | Prompt orchestration, RAG, LLMOps, validation IA | Non implemente, moteur deterministe local | Il manque LLM gateway, prompt engine, evaluation IA, sandbox, guardrails. |
| F - Delivery Operations | API, data model, frontend, runbook production | API locale, frontend, Docker Compose, schema PostgreSQL | Pas encore de runbook production, DR, packaging release, observabilite prod. |
| G - Domain Packs | 21/22 volumes contact center selon comptage | Seulement Support/SAV code avec 2 scenarios | Pas de domain pack registry, pas de packs WFM, supervision, ITIL, banking, etc. |
| H - AI Platform Enterprise | Multi-agents, router, sandbox, model registry | Non implemente | Phase Enterprise IA non commencee en code. |
| I - Product Business & Data Platform | Billing, marketplace, analytics, data lake, vector DB | Audit/session persistence initiale | Pas d'analytics, BI, feature store, vector DB, event store industriel. |
| J - Enterprise Platform Services | IAM, RBAC, tenants, billing, plugins, GDPR | IAM local demo, users/tenants stores | Pas de RBAC/ABAC, org/workspace, entitlements, GDPR, admin console. |
| K - Dev Platform / DevSecOps | CI/CD, GitOps, Docker, K8s, Terraform, SRE | Docker local, Makefile, lint/test/build | Pas de depot Git detecte, pas de CI/CD, K8s, IaC, SRE. |
| L - Governance | ADR, RFC, metrics, security/design review, release gates | Docs et decisions initiales | Pas encore de workflow de gouvernance executable ou gates automatises. |

### 5.2 Conclusion De Comparaison

L'AEB decrit une plateforme SaaS/AI Enterprise complete. L'implementation couvre actuellement :

- une base monorepo ;
- un backend local ;
- un frontend local ;
- une authentification demo ;
- une premiere verticale SAV ;
- un audit trail ;
- une persistence PostgreSQL initiale ;
- un premier niveau de tests.

Le coeur produit n'est donc pas absent ; il est a son premier niveau. La priorite n'est pas d'implementer toutes les phases A-L immediatement, mais de construire un MVP vertical solide qui respecte les invariants de l'AEB : tenant, audit, contrats, separation engines, testabilite et gouvernance.

---

## 6. Comparaison Avec Le Plan D'Implementation

### 6.1 Roadmap Sprint 00-12

| Sprint | Objectif Planifie | Etat Actuel | Evaluation Audit |
| --- | --- | --- | --- |
| 00 | Bootstrap monorepo | Fait | Conforme. |
| 01 | Kernel minimal | Fait initial | Bon depart ; EventBus reste in-memory. |
| 02 | Identity & tenant context | Fait demo + login local | Conforme MVP, non production. |
| 03 | Session & conversation | Fait partiel | Session/chat disponibles, Conversation Engine non separe. |
| 04 | Scenario & persona | Fait partiel | Scenarios en memoire ; persona implicite dans donnees scenario. |
| 05 | CRM fictif | Fait partiel | Actions CRM simulees ; pas encore CRM data model complet. |
| 06 | Actions metier | Fait partiel | Actions presentes, mais procedure/policy incomplètes. |
| 07 | Procedure engine | Non commence | Fort ecart MVP. |
| 08 | Evaluation QA | Debut simple | Scoring basique ; manque scorecard detaillee et rapport. |
| 09 | Coaching feedback | Partiel | `next_best_actions` existe, coaching engine absent. |
| 10 | Dashboard minimal | Non commence | Historique/KPI non disponibles. |
| 11 | Observabilite & hardening | Partiel | Logs/trace id presents ; metrics/traces/alerts absents. |
| 12 | Release candidate MVP | Non commence | Conditionne par S07-S11. |

### 6.2 Milestones

| Milestone | Cible | Etat Audit |
| --- | --- | --- |
| M0 - Repository Ready | monorepo, backend, frontend, DB, Redis, tests, lint, compose | Majoritairement atteint, sauf Redis non exploite et absence Git/CI. |
| M1 - Simulation Loop | session, message, persona, scenario, timeline | Atteint partiellement ; persona/timeline doivent etre formalises. |
| M2 - Business Actions | CRM, action engine, procedure engine, event trail | CRM/action/audit partiels ; procedure manquant. |
| M3 - Learning Value | evaluation, feedback, rapport, progression | Debut seulement ; c'est le principal chantier produit. |
| M4 - MVP Release Candidate | obs, docs, seed demo, tests integration, packaging | Non atteint. |

### 6.3 Ecart Sur Le MVP Scope

| Element MVP | Statut | Commentaire |
| --- | --- | --- |
| Login minimal | Atteint | Login local + bearer token. |
| Tenant demo | Atteint partiel | Contexte present, isolation complete a durcir. |
| Scenario selection | Atteint | 2 scenarios SAV. |
| Simulation chat | Atteint | Moteur deterministe simple. |
| CRM panel | Atteint partiel | Actions disponibles, pas encore modele CRM generique. |
| Objectives/procedure panel | Non atteint | Besoin Procedure Engine + UI. |
| QA score | Atteint simple | Score global, pas scorecard detaillee. |
| Final report | Non atteint | Priorite immediate. |
| Tests | Atteint initial | 34 tests passes, integration DB a ajouter. |
| Local launch < 10 min | Probable | Docker/local ready, a documenter comme preuve. |

---

## 7. Architecture Technique Actuelle

### 7.1 Forces

- Separation initiale claire entre API, contracts, kernel, persistence, telemetry, identity et engines.
- FastAPI et Pydantic donnent une base saine pour contrats et OpenAPI.
- L'API utilise des response models, ce qui limite la derive implicite.
- Le kernel contient deja erreurs, IDs, temps, command bus et event bus.
- Le service de simulation depend de protocols de persistence, ce qui facilite memory/PostgreSQL.
- Les actions CRM encapsulent des preconditions metier utiles, par exemple identite requise avant ticket/remboursement.
- L'audit trail existe tot, ce qui est tres positif pour une plateforme d'apprentissage et de compliance.
- Les tests couvrent deja API, kernel, identity, persistence, telemetry, CRM et simulation.

### 7.2 Fragilites

- Les endpoints de lecture session, CRM actions et audit ne prennent pas encore le `TenantContext`, donc ils ne peuvent pas verifier l'isolation tenant.
- Le store `get(session_id)` ne requiert pas `tenant_id`, ce qui est insuffisant pour une plateforme SaaS multi-tenant.
- Le token est un JWT-like HMAC maison ; acceptable pour MVP local, pas pour production.
- Pas de refresh token, revocation, rotation de secrets, audience, issuer, key id ou session management.
- Le schema PostgreSQL est initialise par code et SQL local, mais pas par migrations versionnees.
- Les tests PostgreSQL via Docker Compose ne sont pas encore en place.
- Les engines conversation/persona/procedure/evaluation sont encore vides ou implicites.
- L'evaluation est dans `SimulationService`, ce qui deviendra vite trop couple.
- Les scenarios sont hardcodes en memoire ; le Domain Pack Framework n'est pas encore executable.
- Pas de CI/CD ni de depot Git detecte dans le workspace courant.

---

## 8. Audit Securite Et Multi-Tenant

### 8.1 Etat Actuel

Le projet possede une base IAM MVP :

- login email/password ;
- hash PBKDF2 ;
- bearer token signe ;
- tenant demo ;
- user demo ;
- roles dans les claims ;
- stores identite memory/PostgreSQL.

Cette base est suffisante pour une demo locale. Elle n'est pas suffisante pour une plateforme Enterprise.

### 8.2 Risques Majeurs

| Risque | Severite | Analyse |
| --- | --- | --- |
| Acces cross-tenant a une session | Haute | `session_id` suffit a lire une session/audit ; `tenant_id` n'est pas verifie sur tous les chemins. |
| Token maison | Haute | Implementation pedagogique, mais pas alignee avec les standards OIDC/JWT production. |
| Absence RBAC/ABAC effectif | Haute | Les roles existent dans le user, mais pas de policy enforcement. |
| Secrets locaux | Moyenne | `.env.example` contient des valeurs demo, normal, mais il faut une strategie secrets. |
| Audit non cloisonne par tenant sur read | Haute | Le store liste par aggregate sans filtre tenant. |

### 8.3 Recommandation Securite Prioritaire

Avant d'etendre les domaines fonctionnels, il faut introduire un invariant strict :

> Toute lecture ou mutation de ressource metier doit etre appelee avec `TenantContext` et verifier que `resource.tenant_id == context.tenant_id`.

Ce principe doit etre applique a :

- `get_simulation` ;
- `list_crm_actions` ;
- `execute_crm_action` ;
- `get_simulation_audit` ;
- futurs endpoints report, evaluation, dashboard et admin.

---

## 9. Audit Data, Persistence Et Audit Trail

### 9.1 Points Positifs

- Presence de stores memory et PostgreSQL.
- Schema initial pour `simulation_sessions`.
- Schema initial pour `audit_events`.
- Schema initial tenants/users.
- JSONB pour conserver la session complete.
- Index audit par aggregate et tenant.

### 9.2 Ecarts

- Pas de migration tool versionne type Alembic ou equivalent.
- Pas de tests d'integration PostgreSQL automatises.
- Pas de transaction de haut niveau autour session update + audit append + event publish.
- Pas d'outbox event.
- Pas de modele analytique des evaluations.
- Pas d'event store canonical.
- Pas de retention policy.
- Pas de lineage data.
- Pas de separation OLTP/analytics.

### 9.3 Priorite Data

Pour le MVP, il ne faut pas encore construire toute la Data Platform. Il faut plutot stabiliser trois choses :

1. persistence PostgreSQL verifiee par tests ;
2. schema de rapport/evaluation exploitable ;
3. audit tenant-safe et requetable pour l'interface.

---

## 10. Audit IA Et LLM Platform

### 10.1 Etat Actuel

L'implementation actuelle n'integre pas encore de LLM. C'est une decision saine pour le MVP, car elle evite de rendre instable une verticale produit encore jeune.

Le moteur de simulation est deterministe :

- evaluation par detection de comportements attendus ;
- reponse client selon score et tour ;
- next best actions simples ;
- scenario hardcode.

### 10.2 Ecarts Avec La Cible AEB

La cible AEB couvre :

- Prompt Engine ;
- Persona Engine ;
- Conversation Engine ;
- Evaluation Engine ;
- RAG ;
- guardrails ;
- memory ;
- agent orchestration ;
- LLM gateway ;
- model registry ;
- AI observability ;
- safety sandbox.

Aucune de ces briques n'est encore implementee comme plateforme IA Enterprise. Les concepts existent seulement en documentation et parfois sous forme de comportement implicite.

### 10.3 Recommandation IA

Ne pas connecter un LLM directement au frontend ou au `SimulationService`. Introduire d'abord une interface stable :

- `ConversationEngine`;
- `EvaluationEngine`;
- `PersonaRuntime`;
- `LLMProvider` ou `ModelGateway`;
- mode `deterministic` par defaut ;
- mode `llm` optionnel derriere configuration.

---

## 11. Audit Frontend Et Experience Produit

### 11.1 Points Positifs

- Frontend React/Vite operationnel.
- Boucle de simulation disponible.
- Affichage scenarios/session/messages.
- Execution d'actions CRM depuis l'interface.
- Score et audit visibles.
- Connexion API deja effective.

### 11.2 Limites

- Experience encore demo, pas encore poste de travail apprenant complet.
- Login automatique utile pour developpement, mais a remplacer par flux clair.
- Pas de rapport de fin de session.
- Pas de panneau procedure/objectifs complet.
- Pas de dashboard historique.
- Pas de gestion fine des erreurs et etats vides.
- Pas encore de design system formalise.
- Pas d'accessibilite verifiee.

### 11.3 Priorite Frontend

La prochaine valeur produit visible doit etre :

- session report ;
- scorecard detaillee ;
- recommandations de coaching ;
- checklist procedure ;
- historique minimal des sessions.

---

## 12. Audit Documentation Et Gouvernance

### 12.1 Forces Documentaires

- L'AEB couvre A-L.
- Les volumes modulaires existent.
- Les index specialises existent.
- Le rapport de normalisation identifie deja les incoherences.
- Le plan d'implementation existe.
- Les sprints initiaux sont documentes.
- Les decisions d'implementation sont tracees.

### 12.2 Points A Corriger

| Probleme | Impact |
| --- | --- |
| Le monolithe AEB utilise tres peu de vrais titres Markdown | Navigation, publication, RAG et revue plus difficiles. |
| Doublons `B04` et `G06` | Ambiguite de reference et de tracabilite. |
| Phase A composite `A00-A02` | Granularite non homogene avec le reste des volumes. |
| Nomenclature Callibr / ATOS / ACS | Risque de confusion produit vs kernel vs historique. |
| Roadmap implementation partiellement depassee par le code | Risque de mauvais pilotage sprint. |
| Mapping architecture-code non enforce | Risque de derive entre l'AEB et l'implementation. |
| Pas de depot Git detecte | Faible traçabilite technique et gouvernance de changement. |

### 12.3 Recommandation Gouvernance

Creer une matrice vivante `AEB -> Implementation -> Tests -> Status` avec une ligne par capability :

- ID AEB ;
- volume source ;
- capability ;
- package/code owner ;
- status ;
- endpoints ;
- tests ;
- risques ;
- prochaine action.

Cette matrice doit devenir le principal outil de pilotage.

---

## 13. Risques Prioritaires

| ID | Risque | Severite | Probabilite | Impact | Mitigation |
| --- | --- | --- | --- | --- | --- |
| R-AUD-01 | Ecart entre ambition AEB et execution MVP | Haute | Haute | Dispersion, ralentissement | Piloter par vertical slices et gates MVP. |
| R-AUD-02 | Isolation tenant incomplete | Haute | Moyenne | Risque SaaS critique | Ajouter tenant checks dans services/stores/tests. |
| R-AUD-03 | Evaluation pedagogique trop faible | Haute | Haute | Valeur produit insuffisante | Prioriser scorecard, report, coaching. |
| R-AUD-04 | Persistence non industrialisee | Moyenne | Haute | Bugs runtime, perte confiance | Tests PostgreSQL + migrations. |
| R-AUD-05 | Engines implicites dans SimulationService | Moyenne | Haute | Couplage et dette technique | Extraire Evaluation/Procedure/Conversation progressivement. |
| R-AUD-06 | Documentation non executable | Moyenne | Haute | AEB difficile a utiliser par devs/agents | Traceability matrix et publication/RAG. |
| R-AUD-07 | Absence CI/CD/Git visible | Haute | Moyenne | Pas de controle qualite continu | Initialiser versioning + pipeline. |
| R-AUD-08 | LLM integre trop tot | Moyenne | Moyenne | Instabilite et couts | Garder deterministic mode, gateway plus tard. |
| R-AUD-09 | Domain packs non data-driven | Moyenne | Haute | Extension metier lente | Creer pack registry et format scenario. |
| R-AUD-10 | Frontend demo seulement | Moyenne | Haute | Difficultes de validation utilisateur | Construire report/procedure/dashboard. |

---

## 14. Constats D'Audit Priorises

### Finding 1 - Isolation Multi-Tenant Incomplete

Severite : Haute  
Impact : securite SaaS, conformite, confiance Enterprise

Constat : plusieurs endpoints recuperent une session ou un audit uniquement par `session_id`, sans `TenantContext`. Le store de session expose egalement `get(session_id)` sans filtre tenant.

Recommandation :

- modifier les signatures service/store vers `get(session_id, tenant_id)` ou ajouter `assert_session_access`;
- passer `TenantContext` a tous les endpoints session/action/audit ;
- ajouter des tests cross-tenant explicites.

### Finding 2 - Evaluation Et Rapport MVP Non Complets

Severite : Haute  
Impact : valeur pedagogique centrale

Constat : le score actuel est utile pour une demo, mais il ne suffit pas a produire une experience d'apprentissage professionnelle.

Recommandation :

- creer `EvaluationCriterion`, `EvaluationScorecard`, `SessionReport`;
- separer `EvaluationEngine`;
- exposer `/api/v1/simulations/{session_id}/report`;
- afficher rapport, preuves, points forts, axes de progres, coaching.

### Finding 3 - Procedure Engine Manquant

Severite : Haute  
Impact : alignement metier contact center

Constat : les actions CRM existent, mais les obligations procedurelles ne sont pas gerees comme checklist, regles ou state machine.

Recommandation :

- introduire `ProcedureDefinition`, `ProcedureStep`, `ProcedureState`;
- rattacher procedure au scenario ;
- evaluer completion et violations ;
- afficher procedure dans le frontend.

### Finding 4 - Gouvernance Document-Code Insuffisamment Mecanisee

Severite : Moyenne a Haute  
Impact : derive architecture/execution

Constat : l'AEB contient une cible tres large, mais l'implementation ne dispose pas encore d'une matrice executable de couverture.

Recommandation :

- creer une traceability matrix implementation ;
- lier chaque sprint aux volumes AEB ;
- associer chaque capability a ses endpoints/tests ;
- mettre a jour l'index implementation apres chaque sprint.

### Finding 5 - Persistence PostgreSQL A Durcir

Severite : Moyenne  
Impact : fiabilite runtime

Constat : les stores PostgreSQL existent, mais les migrations et tests d'integration ne sont pas encore industrialises.

Recommandation :

- ajouter tests Docker Compose PostgreSQL ;
- versionner les migrations ;
- verifier tenant queries et indexes ;
- definir strategie transaction/outbox.

### Finding 6 - Securite IAM Locale Seulement

Severite : Haute pour production, acceptable pour MVP local  
Impact : Enterprise readiness

Constat : l'IAM est un MVP local avec token signe maison et roles non appliques par policy.

Recommandation :

- conserver pour demo ;
- ajouter policy service RBAC minimal ;
- preparer futur OIDC/SAML/SCIM ;
- gerer refresh/revocation plus tard.

### Finding 7 - Domain Packs Non Executables Comme Packs

Severite : Moyenne  
Impact : scalabilite metier

Constat : les volumes G sont riches, mais le code contient seulement deux scenarios SAV hardcodes.

Recommandation :

- definir un format pack YAML/JSON versionne ;
- creer `DomainPackRegistry`;
- charger scenarios/procedures/actions/personas depuis fichiers ;
- tester le pack G01 avant d'etendre G02-G20.

### Finding 8 - Dev Platform Non Encore En Place

Severite : Moyenne a Haute  
Impact : industrialisation

Constat : Makefile, tests et Docker existent, mais pas de Git detecte, pas de CI/CD, pas de coverage gates.

Recommandation :

- initialiser ou connecter le depot Git ;
- ajouter pipeline lint/test/build ;
- ajouter coverage ;
- ajouter release checklist.

---

## 15. Plan De Redressement Et De Developpement Recommande

### Horizon 0-2 Semaines - Stabiliser Le MVP Pedagogique

Priorite 1 : Evaluation et rapport

- ajouter contrats d'evaluation detaillee ;
- creer `EvaluationEngine` minimal ;
- generer `SessionReport` ;
- endpoint report ;
- UI rapport.

Priorite 2 : Isolation tenant

- passer `TenantContext` partout ;
- filtrer session/audit par tenant ;
- tests cross-tenant.

Priorite 3 : Procedure Engine minimal

- ajouter checklist procedure ;
- relier procedure au scenario ;
- afficher completion.

Priorite 4 : Tests d'integration persistence

- lancer PostgreSQL via Docker Compose ;
- verifier sessions, audit, users ;
- tester reconnection et schema init.

### Horizon 2-6 Semaines - Passer De Demo A MVP Produit

- extraire `ConversationEngine`;
- formaliser `PersonaRuntime`;
- creer `DomainPackRegistry`;
- charger scenarios SAV depuis fichiers ;
- ajouter historique sessions ;
- ajouter dashboard KPI minimal ;
- ajouter RBAC/policy enforcement simple ;
- ajouter OpenTelemetry ou instrumentation minimale ;
- ajouter CI lint/test/build ;
- documenter runbook local.

### Horizon 6-12 Semaines - Preparer La Plateforme SaaS

- migrations versionnees ;
- org/tenant/workspace model ;
- admin minimal ;
- audit tenant-safe requetable ;
- event outbox ;
- API versioning ;
- seed data manager ;
- feature flags ;
- premiers SLO ;
- release candidate MVP.

### Horizon 3-6 Mois - Entrer Dans L'Enterprise Platform

- LLM Gateway ;
- Prompt/Persona/Conversation/Evaluation engines separes ;
- RAG documentaire AEB ;
- analytics learning ;
- model evaluation ;
- RBAC/ABAC avance ;
- GDPR/data rights ;
- marketplace/plugins ;
- CI/CD/GitOps ;
- K8s/Terraform si besoin cloud.

---

## 16. Recommandation D'Ordonnancement Immediat

L'ordre recommande des prochains sprints est :

| Ordre | Sprint Recommande | Objectif | Pourquoi maintenant |
| --- | --- | --- | --- |
| 1 | S06 - Evaluation & Report | Donner une valeur pedagogique claire | C'est le coeur produit du MVP. |
| 2 | S07 - Tenant Safety & PostgreSQL Tests | Rendre la base SaaS fiable | Evite une dette de securite structurante. |
| 3 | S08 - Procedure Engine | Connecter CRM, scenario et qualite metier | Indispensable contact center. |
| 4 | S09 - Domain Pack Registry | Sortir les scenarios du code | Ouvre l'extension G01 puis G02-G20. |
| 5 | S10 - Dashboard & History | Montrer progression et pilotage | Cree la valeur manager/coach. |
| 6 | S11 - Observability & CI | Industrialiser | Prepare release candidate. |

Cette sequence respecte la cible AEB sans tomber dans l'implementation prematuree de toute la plateforme Enterprise.

---

## 17. Definition Of Done Proposee Pour Le Prochain Palier

Le prochain palier doit etre considere termine uniquement si :

- une session peut etre terminee explicitement ;
- un rapport de session est genere ;
- le rapport contient score global, criteres, preuves, recommandations ;
- les actions CRM sont prises en compte dans l'evaluation ;
- une procedure scenario est affichee et evaluee ;
- toutes les lectures session/audit sont tenant-safe ;
- les tests unitaires et API passent ;
- au moins un test PostgreSQL passe ;
- l'index implementation est mis a jour ;
- les capabilities implementees sont mappees vers les volumes AEB.

---

## 18. Conclusion

Callibr est dans une situation saine pour un projet ambitieux : la vision est largement formalisee, les fondations techniques existent, et une premiere verticale produit tourne deja localement.

Le risque principal n'est pas un manque d'architecture. Le risque principal est maintenant l'exces de surface cible par rapport a la capacite d'execution immediate. Il faut donc piloter le projet par increments verticaux, chacun apportant une valeur produit mesurable et renforcant un invariant Enterprise.

La trajectoire recommandee est claire :

1. finir le MVP pedagogique SAV ;
2. securiser tenant/persistence/audit ;
3. rendre les domain packs executables ;
4. extraire progressivement les engines ;
5. seulement ensuite brancher les briques IA/LLM Enterprise ;
6. industrialiser DevSecOps, data platform et gouvernance.

En suivant cet ordre, Callibr peut evoluer d'une demo locale prometteuse vers une plateforme SaaS/AI Enterprise sans renier l'ambition de l'AEB.
