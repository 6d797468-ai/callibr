# Architecture & Engineering Book (AEB) — Master Index

Mise à jour : 2026-07-27

Produit : Callibr

Nom interne architectural : ATOS — AI Training Operating System

Source monolithique : `Architecture & Engineering Book (AEB).md`

Sauvegardes :

- `Architecture & Engineering Book (AEB).md.bak-20260727-avant-completion`
- `Architecture & Engineering Book (AEB).md.bak-20260727-avant-data-platform`
- `Architecture & Engineering Book (AEB).md.bak-20260727-avant-phase-j`
- `Architecture & Engineering Book (AEB).md.bak-20260727-avant-phase-k`
- `Architecture & Engineering Book (AEB).md.bak-20260727-avant-phase-l`

## Statut

Le document principal couvre désormais les phases A à L.

La répartition ci-dessous transforme le livre monolithique en volumes opérationnels lisibles, indexables et utilisables par des développeurs, architectes et agents IA.

## Diagnostic Principal

- Le fichier original était déjà très riche, mais physiquement monolithique et difficile à maintenir.
- La Phase I produit/business existante a été conservée en I01-I10, puis complétée par la Data Platform en I11-I20.
- La Phase J ajoute les services Enterprise transverses.
- La Phase K ajoute la plateforme de développement, DevSecOps et Platform Engineering.
- La Phase L ajoute la gouvernance produit, architecture, sécurité, audit et release gates.
- Le document mélange `Callibr`, `ACS Platform` et `ATOS`. La normalisation recommandée est : `Callibr` pour le produit, `ATOS` pour le noyau architectural interne, `ACS Platform` comme appellation initiale/historique.
- Certaines numérotations historiques restent à harmoniser lors d'une passe éditoriale : double `B4`, double `G6`, et dérive `G20` pour l'omnichannel alors que le bilan de Phase G mentionne G19.

## Gouvernance De Lecture

- Le monolithe reste la source canonique de continuité narrative.
- Les volumes séparés sont les unités de revue, d'implémentation, de RAG et de travail agentique.
- Toute décision structurante doit être reportée dans le volume concerné et, si elle change un choix existant, dans un ADR dédié.
- Toute extension future doit préserver le canevas : vision, principes, architecture, modèle de données, API interne, ADR, critères d'acceptation.

## Index Spécialisés

- [Rapport de normalisation éditoriale](_indexes/NORMALIZATION-REPORT.md)
- [Matrice de traçabilité des volumes](_indexes/TRACEABILITY-MATRIX.md)
- [Index ADR](_indexes/ADR-INDEX.md)
- [Registre ADR extrait](_adr/ADR-REGISTRY.md)
- [Index API](_indexes/API-INDEX.md)
- [Index événements](_indexes/EVENT-INDEX.md)
- [Index engines et services](_indexes/ENGINE-INDEX.md)
- [Index data models](_indexes/DATA-MODEL-INDEX.md)
- [Index catalogue scénarios](_indexes/SCENARIO-CATALOG-INDEX.md)
- [Plan de renumérotation contrôlée](_normalization/VOLUME-RENUMBERING-PLAN.md)
- [Manifests publication/RAG](_manifests/README.md)
- [Blueprint site documentaire](_publication/DOCUMENTATION-SITE-BLUEPRINT.md)
- [Blueprint ingestion RAG](_publication/RAG-INGESTION-BLUEPRINT.md)
- [Squelette navigation MkDocs](_publication/MKDOCS-NAV-SKELETON.md)

## Volumes

### Phase A — Fondations

- [A00-A02 — Fondations, vision produit, enterprise architecture et engineering constitution](phase-a-foundations/volume-a00-a02-foundations-vision-architecture-constitution.md)

### Phase B — Architecture métier

- [B01 — Domain Driven Design (DDD)](phase-b-business-architecture/volume-b01-domain-driven-design-ddd.md)
- [B02 — Simulation Operating Engine (SOE)](phase-b-business-architecture/volume-b02-simulation-operating-engine-soe.md)
- [B03 — AI Runtime Architecture & Prompt Orchestration Engine (POE)](phase-b-business-architecture/volume-b03-ai-runtime-architecture-prompt-orchestration-engine-poe.md)
- [B04 — Customer Persona Engine & Emotion Engine](phase-b-business-architecture/volume-b04-customer-persona-engine-emotion-engine.md)
- [B04 (partie 2) — Customer Persona Engine & Behavior Simulation Engine (BSE)](phase-b-business-architecture/volume-b04-part-2-customer-persona-engine-behavior-simulation-engine-bse.md)
- [B05 — Scenario Engine & Procedure Engine](phase-b-business-architecture/volume-b05-scenario-engine-procedure-engine.md)
- [B06 — Rule Engine & Decision Engine](phase-b-business-architecture/volume-b06-rule-engine-decision-engine.md)
- [B07 — CRM Runtime Engine (CRE)](phase-b-business-architecture/volume-b07-crm-runtime-engine-cre.md)
- [B08 — Conversation Runtime Engine (CoRE)](phase-b-business-architecture/volume-b08-conversation-runtime-engine-core.md)
- [B09 — Evaluation & Quality Intelligence Engine (EQI)](phase-b-business-architecture/volume-b09-evaluation-quality-intelligence-engine-eqi.md)
- [B10 — Analytics, Learning Intelligence & Coaching Platform (ALICP)](phase-b-business-architecture/volume-b10-analytics-learning-intelligence-coaching-platform-alicp.md)

### Phase C — Platform Core Architecture

- [C01 — AI Training Operating System (ATOS) Kernel](phase-c-platform-core/volume-c01-ai-training-operating-system-atos-kernel.md)
- [C02 — Event Bus, Event Sourcing & CQRS](phase-c-platform-core/volume-c02-event-bus-event-sourcing-cqrs.md)
- [C03 — Enterprise Multi-Tenant SaaS Architecture](phase-c-platform-core/volume-c03-enterprise-multi-tenant-saas-architecture.md)
- [C04 — API Gateway, Integration Platform & SDK](phase-c-platform-core/volume-c04-api-gateway-integration-platform-sdk.md)
- [C05 — Runtime Infrastructure, Platform Engineering & Cloud Architecture](phase-c-platform-core/volume-c05-runtime-infrastructure-platform-engineering-cloud-architecture.md)

### Phase D — Engineering Standards & Implementation Blueprint

- [D01 — Monorepo, Code Organization & Engineering Standards](phase-d-engineering-standards/volume-d01-monorepo-code-organization-engineering-standards.md)
- [D02 — Engineering Quality, Testing, DevSecOps & Governance](phase-d-engineering-standards/volume-d02-engineering-quality-testing-devsecops-governance.md)
- [D03 — Engine Implementation Blueprint](phase-d-engineering-standards/volume-d03-engine-implementation-blueprint.md)

### Phase E — AI Engineering & Autonomous Development

- [E01 — AI Engineering Framework & Prompt Orchestration](phase-e-ai-engineering/volume-e01-ai-engineering-framework-prompt-orchestration.md)
- [E02 — OpenCode Development Playbook (Master Prompt)](phase-e-ai-engineering/volume-e02-opencode-development-playbook-master-prompt.md)
- [E03 — AI Coding Governance & Autonomous Development Lifecycle](phase-e-ai-engineering/volume-e03-ai-coding-governance-autonomous-development-lifecycle.md)
- [E04 — Engineering Knowledge Base & RAG Architecture](phase-e-ai-engineering/volume-e04-engineering-knowledge-base-rag-architecture.md)
- [E05 — LLMOps, AI Runtime & Cost Optimization](phase-e-ai-engineering/volume-e05-llmops-ai-runtime-cost-optimization.md)
- [E06 — AI Validation, Benchmarking & Continuous Improvement Framework](phase-e-ai-engineering/volume-e06-ai-validation-benchmarking-continuous-improvement-framework.md)

### Phase F — Delivery, Implementation & Enterprise Operations

- [F01 — Monorepo Blueprint & Repository Architecture](phase-f-delivery-operations/volume-f01-monorepo-blueprint-repository-architecture.md)
- [F02 — API Contracts & Communication Architecture](phase-f-delivery-operations/volume-f02-api-contracts-communication-architecture.md)
- [F03 — PostgreSQL Enterprise Data Model](phase-f-delivery-operations/volume-f03-postgresql-enterprise-data-model.md)
- [F04 — Frontend Architecture & Design System](phase-f-delivery-operations/volume-f04-frontend-architecture-design-system.md)
- [F05 — Implementation Roadmap & Sprint Execution Plan](phase-f-delivery-operations/volume-f05-implementation-roadmap-sprint-execution-plan.md)
- [F06 — Production Runbook & Enterprise Operations](phase-f-delivery-operations/volume-f06-production-runbook-enterprise-operations.md)

### Phase G — Contact Center Business Packs

- [G00 — Domain Pack Framework](phase-g-contact-center-packs/volume-g00-domain-pack-framework.md)
- [G01 — Domain Pack — Service Après-Vente (SAV)](phase-g-contact-center-packs/volume-g01-domain-pack-service-apres-vente-sav.md)
- [G02 — Domain Pack — Support Technique N1 / N2](phase-g-contact-center-packs/volume-g02-domain-pack-support-technique-n1-n2.md)
- [G03 — Domain Pack — Télévente & Vente Conseil](phase-g-contact-center-packs/volume-g03-domain-pack-televente-vente-conseil.md)
- [G04 — Domain Pack — Rétention & Fidélisation](phase-g-contact-center-packs/volume-g04-domain-pack-retention-fidelisation.md)
- [G05 — Domain Pack — Recouvrement](phase-g-contact-center-packs/volume-g05-domain-pack-recouvrement.md)
- [G06 — Domain Pack — Back Office](phase-g-contact-center-packs/volume-g06-domain-pack-back-office.md)
- [G06 (partie 2) — Domain Pack — Back Office](phase-g-contact-center-packs/volume-g06-part-2-domain-pack-back-office.md)
- [G07 — Domain Pack — Conduite d'Activité & Dispatch](phase-g-contact-center-packs/volume-g07-domain-pack-conduite-d-activite-dispatch.md)
- [G08 — Domain Pack — Assurance Qualité (QA) & Coaching](phase-g-contact-center-packs/volume-g08-domain-pack-assurance-qualite-qa-coaching.md)
- [G09 — Domain Pack — Workforce Management (WFM)](phase-g-contact-center-packs/volume-g09-domain-pack-workforce-management-wfm.md)
- [G10 — Domain Pack — Supervision Temps Réel (Real-Time Command Center)](phase-g-contact-center-packs/volume-g10-domain-pack-supervision-temps-reel-real-time-command-center.md)
- [G11 — Domain Pack — Customer Success](phase-g-contact-center-packs/volume-g11-domain-pack-customer-success.md)
- [G12 — Domain Pack — Help Desk ITIL](phase-g-contact-center-packs/volume-g12-domain-pack-help-desk-itil.md)
- [G13 — Domain Pack — Incident & Problem Management](phase-g-contact-center-packs/volume-g13-domain-pack-incident-problem-management.md)
- [G14 — Domain Pack — Banking Contact Center](phase-g-contact-center-packs/volume-g14-domain-pack-banking-contact-center.md)
- [G15 — Domain Pack — Insurance Contact Center](phase-g-contact-center-packs/volume-g15-domain-pack-insurance-contact-center.md)
- [G16 — Domain Pack — Healthcare Contact Center](phase-g-contact-center-packs/volume-g16-domain-pack-healthcare-contact-center.md)
- [G17 — Domain Pack — E-commerce & Retail](phase-g-contact-center-packs/volume-g17-domain-pack-e-commerce-retail.md)
- [G18 — Domain Pack — Public Services & Administration](phase-g-contact-center-packs/volume-g18-domain-pack-public-services-administration.md)
- [G19 — Domain Pack — Collections avancées & Contentieux](phase-g-contact-center-packs/volume-g19-domain-pack-collections-avancees-contentieux.md)
- [G20 — Domain Pack — Omnichannel & Digital Engagement](phase-g-contact-center-packs/volume-g20-domain-pack-omnichannel-digital-engagement.md)

### Phase H — AI Platform Enterprise

- [H01 — AI Platform Core Architecture](phase-h-ai-platform-enterprise/volume-h01-ai-platform-core-architecture.md)
- [H02 — Agent Runtime Architecture](phase-h-ai-platform-enterprise/volume-h02-agent-runtime-architecture.md)
- [H03 — Prompt Engineering Platform Architecture](phase-h-ai-platform-enterprise/volume-h03-prompt-engineering-platform-architecture.md)
- [H04 — LLM Gateway & Model Routing Architecture](phase-h-ai-platform-enterprise/volume-h04-llm-gateway-model-routing-architecture.md)
- [H05 — Memory & Context Architecture](phase-h-ai-platform-enterprise/volume-h05-memory-context-architecture.md)
- [H06 — Tool Calling Platform Architecture](phase-h-ai-platform-enterprise/volume-h06-tool-calling-platform-architecture.md)
- [H07 — Multi-Agent Orchestration Architecture](phase-h-ai-platform-enterprise/volume-h07-multi-agent-orchestration-architecture.md)
- [H08 — AI Safety & Guardrails Architecture](phase-h-ai-platform-enterprise/volume-h08-ai-safety-guardrails-architecture.md)
- [H09 — Evaluation & Benchmarking Engine Architecture](phase-h-ai-platform-enterprise/volume-h09-evaluation-benchmarking-engine-architecture.md)
- [H10 — AI Observability Platform Architecture](phase-h-ai-platform-enterprise/volume-h10-ai-observability-platform-architecture.md)
- [H11 — Model Registry & MLOps Architecture](phase-h-ai-platform-enterprise/volume-h11-model-registry-mlops-architecture.md)
- [H12 — AI Cost Optimization Architecture](phase-h-ai-platform-enterprise/volume-h12-ai-cost-optimization-architecture.md)
- [H13 — Enterprise AI Governance Architecture](phase-h-ai-platform-enterprise/volume-h13-enterprise-ai-governance-architecture.md)
- [H14 — AI Security Architecture](phase-h-ai-platform-enterprise/volume-h14-ai-security-architecture.md)
- [H15 — Production AI Operations Architecture](phase-h-ai-platform-enterprise/volume-h15-production-ai-operations-architecture.md)

### Phase I — Enterprise Product, Business & Data Platform

- [I01 — Product Operating Model Architecture](phase-i-product-business-data-platform/volume-i01-product-operating-model-architecture.md)
- [I02 — SaaS Multi-Tenant Architecture](phase-i-product-business-data-platform/volume-i02-saas-multi-tenant-architecture.md)
- [I03 — Customer Lifecycle Architecture](phase-i-product-business-data-platform/volume-i03-customer-lifecycle-architecture.md)
- [I04 — Billing & Subscription Platform Architecture](phase-i-product-business-data-platform/volume-i04-billing-subscription-platform-architecture.md)
- [I05 — Enterprise Integration Platform Architecture](phase-i-product-business-data-platform/volume-i05-enterprise-integration-platform-architecture.md)
- [I06 — API Ecosystem Architecture](phase-i-product-business-data-platform/volume-i06-api-ecosystem-architecture.md)
- [I07 — Marketplace Architecture](phase-i-product-business-data-platform/volume-i07-marketplace-architecture.md)
- [I08 — Partner Platform Architecture](phase-i-product-business-data-platform/volume-i08-partner-platform-architecture.md)
- [I09 — Revenue Architecture](phase-i-product-business-data-platform/volume-i09-revenue-architecture.md)
- [I10 — Growth Engine Architecture](phase-i-product-business-data-platform/volume-i10-growth-engine-architecture.md)
- [I11 — Event Store, Data Contracts & Canonical Event Model Architecture](phase-i-product-business-data-platform/volume-i11-event-store-data-contracts-canonical-event-model-architecture.md)
- [I12 — Analytics, BI & Decision Intelligence Platform Architecture](phase-i-product-business-data-platform/volume-i12-analytics-bi-decision-intelligence-platform-architecture.md)
- [I13 — Lakehouse, Warehouse & Data Product Architecture](phase-i-product-business-data-platform/volume-i13-lakehouse-warehouse-data-product-architecture.md)
- [I14 — Feature Store & ML Data Platform Architecture](phase-i-product-business-data-platform/volume-i14-feature-store-ml-data-platform-architecture.md)
- [I15 — Vector Database, Embeddings & Semantic Retrieval Architecture](phase-i-product-business-data-platform/volume-i15-vector-database-embeddings-semantic-retrieval-architecture.md)
- [I16 — Knowledge Graph & Semantic Layer Architecture](phase-i-product-business-data-platform/volume-i16-knowledge-graph-semantic-layer-architecture.md)
- [I17 — Data Governance, Privacy & Quality Architecture](phase-i-product-business-data-platform/volume-i17-data-governance-privacy-quality-architecture.md)
- [I18 — Audit, Lineage & Compliance Data Architecture](phase-i-product-business-data-platform/volume-i18-audit-lineage-compliance-data-architecture.md)
- [I19 — KPI, Reporting & Executive Intelligence Architecture](phase-i-product-business-data-platform/volume-i19-kpi-reporting-executive-intelligence-architecture.md)
- [I20 — Real-Time Data Streaming & Operational Intelligence Architecture](phase-i-product-business-data-platform/volume-i20-real-time-data-streaming-operational-intelligence-architecture.md)

### Phase J — Enterprise Platform Services

- [J01 — Identity & Access Management Architecture](phase-j-enterprise-platform-services/volume-j01-identity-access-management-architecture.md)
- [J02 — RBAC, ABAC & Policy Enforcement Architecture](phase-j-enterprise-platform-services/volume-j02-rbac-abac-policy-enforcement-architecture.md)
- [J03 — Organization, Tenant & Workspace Control Plane Architecture](phase-j-enterprise-platform-services/volume-j03-organization-tenant-workspace-control-plane-architecture.md)
- [J04 — Subscription, Entitlement & Plan Enforcement Architecture](phase-j-enterprise-platform-services/volume-j04-subscription-entitlement-plan-enforcement-architecture.md)
- [J05 — Plugin & Extension Runtime Architecture](phase-j-enterprise-platform-services/volume-j05-plugin-extension-runtime-architecture.md)
- [J06 — Marketplace Runtime & Installation Governance Architecture](phase-j-enterprise-platform-services/volume-j06-marketplace-runtime-installation-governance-architecture.md)
- [J07 — White Label, Branding & Tenant Experience Architecture](phase-j-enterprise-platform-services/volume-j07-white-label-branding-tenant-experience-architecture.md)
- [J08 — Localization, Internationalization & Regionalization Architecture](phase-j-enterprise-platform-services/volume-j08-localization-internationalization-regionalization-architecture.md)
- [J09 — Compliance, GDPR & Data Rights Architecture](phase-j-enterprise-platform-services/volume-j09-compliance-gdpr-data-rights-architecture.md)
- [J10 — API Management, Developer Portal & Gateway Governance Architecture](phase-j-enterprise-platform-services/volume-j10-api-management-developer-portal-gateway-governance-architecture.md)
- [J11 — Enterprise Integration Hub & Connector Operations Architecture](phase-j-enterprise-platform-services/volume-j11-enterprise-integration-hub-connector-operations-architecture.md)
- [J12 — Notification, Communication & Messaging Platform Architecture](phase-j-enterprise-platform-services/volume-j12-notification-communication-messaging-platform-architecture.md)
- [J13 — Admin Console, Audit Operations & Enterprise Governance Portal Architecture](phase-j-enterprise-platform-services/volume-j13-admin-console-audit-operations-enterprise-governance-portal-architecture.md)
- [J14 — Configuration, Feature Flags & Remote Policy Management Architecture](phase-j-enterprise-platform-services/volume-j14-configuration-feature-flags-remote-policy-management-architecture.md)
- [J15 — Platform Service Reliability, SLO & Enterprise SLA Architecture](phase-j-enterprise-platform-services/volume-j15-platform-service-reliability-slo-enterprise-sla-architecture.md)

### Phase K — Dev Platform, DevSecOps & Platform Engineering

- [K01 — Developer Platform & DevSecOps Operating Model Architecture](phase-k-dev-platform-devsecops/volume-k01-developer-platform-devsecops-operating-model-architecture.md)
- [K02 — CI/CD Pipeline Architecture](phase-k-dev-platform-devsecops/volume-k02-ci-cd-pipeline-architecture.md)
- [K03 — GitOps, Environment Promotion & Configuration Drift Architecture](phase-k-dev-platform-devsecops/volume-k03-gitops-environment-promotion-configuration-drift-architecture.md)
- [K04 — Containers, Docker & Software Supply Chain Security Architecture](phase-k-dev-platform-devsecops/volume-k04-containers-docker-software-supply-chain-security-architecture.md)
- [K05 — Kubernetes Runtime & Service Platform Architecture](phase-k-dev-platform-devsecops/volume-k05-kubernetes-runtime-service-platform-architecture.md)
- [K06 — Infrastructure as Code, Terraform & Cloud Foundation Architecture](phase-k-dev-platform-devsecops/volume-k06-infrastructure-as-code-terraform-cloud-foundation-architecture.md)
- [K07 — Observability, Monitoring & SRE Architecture](phase-k-dev-platform-devsecops/volume-k07-observability-monitoring-sre-architecture.md)
- [K08 — Disaster Recovery, Backup & Business Continuity Architecture](phase-k-dev-platform-devsecops/volume-k08-disaster-recovery-backup-business-continuity-architecture.md)
- [K09 — Performance, Scalability & Capacity Engineering Architecture](phase-k-dev-platform-devsecops/volume-k09-performance-scalability-capacity-engineering-architecture.md)
- [K10 — Release Management, Change Control & Production Readiness Architecture](phase-k-dev-platform-devsecops/volume-k10-release-management-change-control-production-readiness-architecture.md)

### Phase L — Product Governance, Architecture Governance & Enterprise Operations

- [L01 — ADR Lifecycle & Architecture Decision Records Governance Architecture](phase-l-product-architecture-governance/volume-l01-adr-lifecycle-architecture-decision-records-governance-architecture.md)
- [L02 — RFC, Design Proposal & Collaborative Decision Process Architecture](phase-l-product-architecture-governance/volume-l02-rfc-design-proposal-collaborative-decision-process-architecture.md)
- [L03 — Product Governance, Portfolio & Roadmap Operating Model Architecture](phase-l-product-architecture-governance/volume-l03-product-governance-portfolio-roadmap-operating-model-architecture.md)
- [L04 — Product Metrics, OKR & Outcome Measurement Architecture](phase-l-product-architecture-governance/volume-l04-product-metrics-okr-outcome-measurement-architecture.md)
- [L05 — Architecture Governance, Standards & Review Board Architecture](phase-l-product-architecture-governance/volume-l05-architecture-governance-standards-review-board-architecture.md)
- [L06 — Technical Debt, Lifecycle & Deprecation Management Architecture](phase-l-product-architecture-governance/volume-l06-technical-debt-lifecycle-deprecation-management-architecture.md)
- [L07 — Security Review, Threat Modeling & Risk Acceptance Architecture](phase-l-product-architecture-governance/volume-l07-security-review-threat-modeling-risk-acceptance-architecture.md)
- [L08 — Design Review, UX Governance & Accessibility Architecture](phase-l-product-architecture-governance/volume-l08-design-review-ux-governance-accessibility-architecture.md)
- [L09 — Audit Framework, Control Evidence & Enterprise Assurance Architecture](phase-l-product-architecture-governance/volume-l09-audit-framework-control-evidence-enterprise-assurance-architecture.md)
- [L10 — Release Gates, Enterprise Readiness & Operating Review Architecture](phase-l-product-architecture-governance/volume-l10-release-gates-enterprise-readiness-operating-review-architecture.md)

## Prochaine Passe Recommandée

1. Normaliser les titres Markdown du monolithe avec de vrais niveaux `#`, `##`, `###`.
2. Harmoniser la numérotation B et G sans supprimer l'historique.
3. Extraire les ADR dans un répertoire dédié `adr/`.
4. Transformer les exemples YAML/JSON en blocs de code Markdown.
5. Ajouter une matrice de traçabilité entre volumes, ADR, domaines, APIs et composants Python.
6. Ajouter les index spécialisés : APIs, événements, moteurs, modèles de données, policies, contrôles.
7. Préparer une version publication : PDF, site documentaire ou base RAG.
