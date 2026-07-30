# Volume G15 — Domain Pack — Insurance Contact Center

> Extrait généré depuis `Architecture & Engineering Book (AEB).md` le 2026-07-27.

PHASE G — CONTACT CENTER BUSINESS PACKS
Volume G15
Domain Pack — Insurance Contact Center

Version : 1.0

Statut : Enterprise Vertical

Criticité : Critique

1. Vision

Le Domain Pack Insurance simule les interactions entre un assuré et un centre de relation client d'une compagnie d'assurance.

Le moteur couvre :

souscription ;
gestion des contrats ;
déclaration de sinistre ;
indemnisation ;
assistance ;
résiliation ;
renouvellement ;
modifications contractuelles.

L'objectif est de former des conseillers capables de gérer des situations émotionnelles tout en appliquant les procédures de gestion des risques.

2. Objectifs pédagogiques

À la fin de la formation, le conseiller doit être capable de :

identifier correctement l'assuré ;
comprendre la situation ;
qualifier un sinistre ;
appliquer les garanties ;
expliquer les exclusions ;
déclencher les bonnes procédures ;
documenter le dossier.
3. Architecture fonctionnelle
Customer

↓

Authentication Engine

↓

Policy Engine

↓

Claims Engine

↓

Coverage Engine

↓

Fraud Detection Engine

↓

Compensation Engine

↓

QA Engine

Chaque moteur possède des responsabilités clairement définies.

4. Policy Engine

Le moteur gère le cycle de vie des contrats.

Il maintient :

contrats actifs ;
garanties ;
options ;
bénéficiaires ;
échéances ;
historique des modifications.

Toutes les données sont synthétiques.

5. Claims Engine

Le moteur pilote les sinistres.

Cycle de vie :

Déclaration

↓

Qualification

↓

Instruction

↓

Expertise

↓

Décision

↓

Indemnisation

↓

Clôture

Chaque transition est contrôlée.

6. Types d'assurance

Le moteur supporte notamment :

automobile ;
habitation ;
santé ;
prévoyance ;
responsabilité civile ;
voyage ;
protection juridique ;
assurance professionnelle.

Chaque produit possède ses propres règles.

7. Coverage Engine

Le moteur vérifie automatiquement :

garanties applicables ;
exclusions ;
franchises ;
plafonds ;
délais de carence ;
conditions particulières.

Le LLM ne décide jamais seul de la couverture.

8. Fraud Detection Engine

Le moteur calcule un score de risque à partir de facteurs simulés :

déclarations contradictoires ;
fréquence inhabituelle des sinistres ;
incohérences documentaires ;
chronologie suspecte ;
informations incomplètes.

Ce score influence le scénario sans constituer une preuve de fraude.

9. CRM Assurance

Le CRM simulé contient :

assuré ;
contrats ;
garanties ;
sinistres ;
pièces justificatives ;
correspondances ;
expertises ;
paiements simulés.

Toutes les données sont fictives.

10. Actions disponibles

Le conseiller peut :

ouvrir un dossier de sinistre ;
consulter un contrat ;
demander des justificatifs ;
planifier une expertise ;
transmettre à un gestionnaire spécialisé ;
informer l'assuré ;
clôturer le dossier lorsque les conditions sont réunies.

Toutes les actions sont historisées.

11. Gestion documentaire

Le moteur peut générer des documents synthétiques :

constat amiable ;
photos simulées ;
devis de réparation ;
factures ;
certificat médical fictif ;
rapport d'expertise ;
déclaration signée.

Le Workflow Engine vérifie la complétude du dossier.

12. Gestion émotionnelle

Le Persona Engine adapte le comportement de l'assuré.

Exemples :

stress après un accident ;
inquiétude face à une hospitalisation ;
colère après un refus d'indemnisation ;
impatience pendant une expertise.

Le niveau émotionnel évolue selon les réponses du conseiller.

13. Bibliothèque de scénarios
ID	Scénario	Niveau
INS-001	Changement d'adresse	1
INS-002	Déclaration de bris de glace	1
INS-003	Accident automobile	2
INS-004	Dégât des eaux	2
INS-005	Refus de garantie	3
INS-006	Suspicion de fraude	3
INS-007	Sinistre complexe multi-garanties	3
INS-008	Gestion de catastrophe naturelle	3
14. KPI métier

Le moteur calcule notamment :

délai moyen d'ouverture de dossier ;
qualité de qualification ;
exactitude de l'application des garanties ;
qualité documentaire ;
satisfaction simulée ;
délai simulé de traitement.
15. Évaluation QA
Critère	Pondération
Authentification	10 %
Qualification du besoin	20 %
Application des garanties	25 %
Communication et empathie	20 %
Documentation	15 %
Conformité	10 %

Le poids accordé à l'empathie est plus important que dans plusieurs autres Domain Packs.

16. Jeux de données

Le pack comprend :

contrats synthétiques ;
assurés fictifs ;
historiques de sinistres ;
garanties ;
expertises ;
documents simulés ;
profils de risque.

Toutes les données sont générées artificiellement.

17. Architecture interne
Authentication Engine

↓

Policy Engine

↓

Claims Engine

↓

Coverage Engine

↓

Fraud Engine

↓

Compensation Engine

↓

Analytics

Chaque composant peut évoluer indépendamment.

18. Intégration avec les autres moteurs

Le Domain Pack Insurance échange avec :

Conversation Engine pour les échanges avec l'assuré ;
Workflow Engine pour le cycle de vie des dossiers ;
Back Office Engine pour l'instruction documentaire ;
QA Engine pour l'évaluation ;
Learning Platform pour les parcours pédagogiques ;
Reporting Platform pour les KPI.

Cette architecture favorise la réutilisation des moteurs transverses.

19. Décisions d'architecture (ADR)

Ce volume formalise les principes suivants :

Les contrats et les sinistres sont deux objets métier distincts.
Les règles de couverture sont déclaratives et versionnées.
Le moteur de fraude fournit un score explicable sans conclure automatiquement à une fraude.
Les documents sont gérés par le Workflow Engine.
Toutes les décisions sont historisées et auditables.
20. Critères d'acceptation

Le Domain Pack Insurance est considéré conforme lorsque :

les workflows de souscription et de sinistre sont respectés ;
les garanties sont appliquées de manière cohérente ;
les scénarios reproduisent des situations réalistes ;
les évaluations distinguent les compétences relationnelles et métier ;
les dossiers sont complets et traçables.
🏛️ Décision d'architecture majeure : Insurance Lifecycle Simulation Architecture (ILSA)

Je recommande une Insurance Lifecycle Simulation Architecture (ILSA).

Le moteur modélise deux cycles de vie indépendants mais liés : le cycle du contrat et le cycle du sinistre. Cette séparation simplifie l'évolution des produits d'assurance, permet de mutualiser des composants avec d'autres secteurs réglementés et garantit une meilleure traçabilité des décisions.

Le LLM reste un moteur de simulation conversationnelle et d'explication, tandis que les décisions relatives aux garanties, aux workflows et aux règles métier sont prises par des moteurs déterministes configurables.

📘 État d'avancement

Après ce volume :

✅ G1 à G15 terminés (15 Domain Packs sur 20).
📘 Il reste 5 volumes pour achever la Phase G :
G16 — Healthcare Contact Center
G17 — E-commerce & Retail
G18 — Public Services & Administration
G19 — Collections avancées & Contentieux
G20 — Omnichannel & Digital Engagement

Une fois ces cinq volumes finalisés, nous entamerons la Phase H — AI Platform Enterprise, qui constituera le cœur architectural de l'orchestration des modèles LLM, des agents IA, des outils, des prompts et de la gouvernance de l'intelligence artificielle à l'échelle de la plateforme.
