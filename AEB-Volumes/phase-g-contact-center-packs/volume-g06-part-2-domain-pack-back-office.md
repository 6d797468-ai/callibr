# Volume G06 (partie 2) — Domain Pack — Back Office

> Extrait généré depuis `Architecture & Engineering Book (AEB).md` le 2026-07-27.

PHASE G — CONTACT CENTER BUSINESS PACKS
Volume G6
Domain Pack — Back Office

Version : 1.0

Statut : Référence métier

Criticité : Critique

1. Vision

Le Domain Pack Back Office simule le traitement complet d'un dossier métier.

L'objectif n'est plus la conversation.

L'objectif est la prise de décision conforme.

Le stagiaire apprend à :

analyser ;
contrôler ;
vérifier ;
décider ;
documenter.

Le Workflow Engine pilote l'ensemble du processus.

2. Objectifs pédagogiques

À la fin de la formation, l'agent doit savoir :

analyser un dossier complet ;
vérifier les justificatifs ;
détecter les incohérences ;
appliquer une procédure ;
décider d'une validation, d'un rejet ou d'une demande de complément ;
documenter sa décision.
3. Workflow global
Réception dossier

↓

Contrôle de complétude

↓

Contrôle documentaire

↓

Contrôle métier

↓

Analyse des risques

↓

Décision

↓

Documentation

↓

Notification

↓

Archivage
4. Workflow Engine

Le Workflow Engine maintient :

état du dossier ;
pièces reçues ;
règles appliquées ;
anomalies détectées ;
décisions prises ;
historique complet.

Le moteur est déterministe.

Le LLM ne décide jamais seul.

5. Cycle de vie d'un dossier
Nouveau

↓

En attente

↓

Analyse

↓

Contrôle

↓

Décision

↓

Validation

ou

Rejet

ou

Complément demandé

↓

Clôturé
6. Types de dossiers

Le moteur supporte notamment :

ouverture de compte ;
modification de contrat ;
changement d'adresse ;
remboursement ;
réclamation ;
création de compte client ;
vérification documentaire ;
validation d'un devis ;
mise à jour de données.

Chaque type possède son workflow.

7. Documents simulés

Le moteur peut générer :

carte d'identité ;
passeport ;
permis de conduire ;
justificatif de domicile ;
facture ;
contrat ;
devis ;
RIB ;
certificat ;
formulaire.

Les documents sont fictifs.

8. Contrôle documentaire

Chaque document est vérifié selon :

présence ;
lisibilité ;
cohérence ;
date de validité ;
conformité.

Les règles sont déclaratives.

9. Règles métier

Exemple.

rule:

customer_age:

minimum: 18

required_documents:

- identity

- proof_of_address

decision:

approve

Les règles sont séparées du moteur.

10. Détection d'anomalies

Le Workflow Engine détecte :

document manquant ;
date expirée ;
incohérence d'identité ;
doublon ;
information contradictoire ;
valeur hors seuil.

Les anomalies alimentent le score qualité.

11. CRM Back Office

Le CRM expose :

Dossier
identifiant ;
statut ;
date de création ;
priorité.
Documents
liste ;
validation ;
historique.
Historique
traitements ;
commentaires ;
décisions.
12. Actions disponibles

L'agent peut :

ouvrir un dossier ;
consulter les documents ;
demander un complément ;
valider un document ;
rejeter un document ;
approuver un dossier ;
refuser un dossier ;
transmettre à un superviseur.

Toutes les actions sont historisées.

13. Files de travail

Le Workflow Engine gère plusieurs files :

nouveaux dossiers ;
dossiers incomplets ;
dossiers urgents ;
dossiers en attente ;
dossiers rejetés ;
dossiers à réexaminer.

Chaque dossier possède une priorité.

14. Priorisation

Exemple.

priority:

urgent

↓

high

↓

normal

↓

low

Les règles de priorité sont configurables.

15. Bibliothèque de scénarios
ID	Scénario	Niveau
BO-001	Changement d'adresse	1
BO-002	Dossier incomplet	1
BO-003	Justificatif expiré	2
BO-004	Informations contradictoires	2
BO-005	Validation complexe	3
BO-006	Dossier multi-documents	3
BO-007	Suspicion d'anomalie	3
BO-008	Décision exceptionnelle	3
16. Machine à états

Chaque workflow est défini par une machine à états.

Exemple.

NEW

↓

PENDING_REVIEW

↓

UNDER_ANALYSIS

↓

APPROVED

ou

REJECTED

ou

WAITING_DOCUMENT

Les transitions sont contrôlées.

17. Évaluation QA

Critères indicatifs.

Critère	Pondération
Contrôle documentaire	20 %
Respect de la procédure	20 %
Exactitude de l'analyse	20 %
Qualité de la décision	20 %
Documentation	10 %
Gestion des priorités	10 %
18. KPI métier

Le pack calcule notamment :

taux de décisions correctes ;
taux d'erreurs de validation ;
temps moyen de traitement ;
dossiers traités par heure (simulation) ;
taux de complétude ;
qualité documentaire.
19. Jeux de données

Le pack fournit :

100 000 dossiers fictifs ;
500 000 documents synthétiques ;
historiques de traitement ;
modèles de formulaires ;
politiques de validation ;
règles métier.

Toutes les données sont artificielles.

20. Extensions sectorielles

Le Workflow Engine peut être adapté à :

banque ;
assurance ;
mutuelle ;
administration ;
RH ;
immobilier ;
santé ;
logistique.

Les workflows changent.

Le moteur reste identique.

21. Collaboration Front / Back Office

Le moteur simule également les échanges entre équipes.

Exemples :

retour d'un dossier au Front Office ;
demande d'informations complémentaires ;
validation par un superviseur ;
escalade vers une équipe spécialisée.

Cette collaboration est modélisée comme des événements et des changements d'état.

22. Décisions d'architecture (ADR)

Ce volume formalise les principes suivants :

Le Workflow Engine pilote les transitions d'état des dossiers.
Les règles métier sont déclaratives et versionnées.
Les décisions sont entièrement traçables.
Les documents sont des objets métier indépendants.
Les scénarios sont reproductibles grâce à des jeux de données synthétiques.
23. Critères d'acceptation

Le Domain Pack Back Office est considéré conforme lorsque :

les workflows couvrent les principaux cas métier ;
les règles de validation sont appliquées automatiquement ;
les anomalies sont détectées de manière cohérente ;
les décisions sont justifiées et documentées ;
les benchmarks de traitement sont reproductibles.
🏛️ Décision d'architecture majeure : Workflow-Driven Decision Architecture (WDDA)

Je recommande une Workflow-Driven Decision Architecture.

Le Workflow Engine est responsable des états, des règles et des décisions. Le LLM intervient pour générer des dossiers réalistes, expliquer les situations, produire des commentaires ou simuler des échanges entre équipes, mais il ne remplace jamais le moteur de règles.

Cette séparation apporte :

des décisions cohérentes et auditables ;
une forte réutilisabilité des workflows entre secteurs ;
une adaptation simple à de nouvelles politiques métier ;
une meilleure conformité réglementaire.
📘 Prochaine étape : G7 — Domain Pack Conduite d'Activité & Dispatch

Le prochain volume introduira un domaine orienté pilotage opérationnel avec un Dispatch Engine. Il couvrira :

affectation dynamique des interventions et des tâches ;
gestion des files d'attente et des priorités ;
planification des techniciens ou équipes terrain ;
optimisation des ressources ;
gestion des incidents en temps réel ;
replanification et gestion des imprévus ;
simulation de SLA, KPI opérationnels et contraintes de capacité.

Ce moteur permettra d'entraîner des coordinateurs et superviseurs à prendre des décisions sous contrainte, en équilibrant satisfaction client, respect des engagements de service et utilisation optimale des ressources.
