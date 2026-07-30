# Volume G05 — Domain Pack — Recouvrement

> Extrait généré depuis `Architecture & Engineering Book (AEB).md` le 2026-07-27.

PHASE G — CONTACT CENTER BUSINESS PACKS
Volume G5
Domain Pack — Recouvrement

Version : 1.0

Statut : Référence métier

Criticité : Critique

1. Vision

Le Domain Pack Recouvrement simule des interactions entre un conseiller et un client présentant un retard de paiement.

Le but de la formation est de permettre à l'agent de :

comprendre la situation ;
négocier une solution adaptée ;
respecter la réglementation ;
préserver autant que possible la relation client ;
documenter les engagements.

Le moteur favorise une approche professionnelle et respectueuse.

2. Objectifs pédagogiques

À l'issue de la formation, l'agent doit être capable de :

identifier le dossier concerné ;
vérifier l'identité ;
expliquer clairement la situation financière ;
écouter les difficultés du client ;
proposer une solution adaptée aux règles de l'entreprise ;
formaliser un engagement ;
clôturer le dossier correctement.
3. Workflow métier
Accueil

↓

Vérification identité

↓

Présentation du dossier

↓

Compréhension de la situation

↓

Qualification financière

↓

Négociation

↓

Accord

↓

Formalisation

↓

Confirmation

↓

Clôture
4. Collection Engine

Le Collection Engine maintient un état structuré du dossier.

Il suit notamment :

montant dû ;
ancienneté de la dette ;
nombre d'échéances impayées ;
historique des paiements ;
promesses de paiement ;
niveau de risque ;
probabilité de recouvrement.

Le LLM conduit la conversation.

Le Collection Engine garantit la cohérence métier.

5. États du dossier
À jour

↓

Premier retard

↓

Retard confirmé

↓

Relance

↓

Négociation

↓

Engagement

↓

Paiement

ou

Nouvel impayé

ou

Escalade
6. Typologie des dossiers

Le moteur distingue plusieurs situations.

Retard ponctuel

Client habituellement fiable.

Difficulté temporaire

Perte d'emploi.

Maladie.

Retard de salaire.

Difficulté durable

Situation financière dégradée.

Contestation

Le client estime que la facture est incorrecte.

Refus volontaire

Le client refuse de payer malgré une dette reconnue.

Chaque cas implique une stratégie différente.

7. Personas
Persona	Description	Difficulté
Coopératif	Souhaite régulariser	★
Gêné	Difficultés financières	★★
Contestataire	Conteste la dette	★★
Méfiant	Ne fait pas confiance	★★
Colérique	Très tendu	★★★
Refus catégorique	Refuse tout dialogue	★★★
8. Qualification financière

Le moteur vérifie que l'agent cherche à comprendre :

origine de la difficulté ;
caractère temporaire ou durable ;
capacité de paiement ;
date possible de régularisation.

Ces informations conditionnent les solutions proposées.

9. Solutions possibles

Selon les règles métier, l'agent peut :

demander un paiement immédiat ;
proposer un échéancier ;
reporter une échéance ;
transférer vers un service spécialisé ;
enregistrer une promesse de paiement ;
suspendre temporairement certaines actions si la politique le prévoit.

Toutes les possibilités sont définies par configuration.

10. Politique de recouvrement

Exemple déclaratif.

collection_policy:

payment_plan:
  max_installments: 6

grace_period_days: 15

promise_to_pay:
  allowed: true

escalation_after:
  failed_promises: 2

legal_referral:
  enabled: true

Le moteur applique automatiquement ces règles.

11. CRM Recouvrement

Le CRM simulé expose notamment :

Client
identité ;
coordonnées ;
historique.
Contrats
contrat concerné ;
produits ;
statut.
Factures
numéro ;
montant ;
échéance ;
statut.
Paiements
historique ;
incidents ;
pénalités.
Promesses
date ;
montant ;
statut.
12. Actions CRM

L'agent peut :

consulter les factures ;
enregistrer une promesse de paiement ;
créer un échéancier ;
modifier une échéance (si autorisé) ;
ouvrir un dossier de contestation ;
transmettre au niveau supérieur ;
clôturer le dossier.

Toutes les actions sont historisées.

13. Bibliothèque de scénarios
ID	Scénario	Niveau
COL-001	Premier retard	1
COL-002	Retard de salaire	1
COL-003	Demande d'échéancier	2
COL-004	Contestation de facture	2
COL-005	Refus de paiement	3
COL-006	Multiples impayés	3
COL-007	Promesse non tenue	3
COL-008	Escalade contentieuse	3
14. Engagements

Le moteur suit :

la date promise ;
le montant promis ;
le respect des engagements ;
les promesses antérieures.

Une nouvelle promesse est évaluée à la lumière de l'historique.

15. Conformité

Le moteur vérifie notamment :

respect du ton professionnel ;
absence de menace inappropriée ;
exactitude des informations communiquées ;
respect des procédures internes ;
transparence sur les conséquences possibles.

Les règles précises dépendent du pays et du secteur. Elles sont configurables dans le Domain Pack.

16. Évaluation QA

Critères indicatifs.

Critère	Pondération
Vérification identité	15 %
Qualité de l'écoute	20 %
Qualification financière	20 %
Négociation	15 %
Respect des procédures	15 %
Documentation	10 %
Clôture	5 %
17. KPI métier

Le pack calcule notamment :

taux d'engagement obtenu ;
qualité de la qualification financière ;
pertinence des solutions proposées ;
respect des procédures ;
qualité documentaire ;
progression de l'apprenant.

Le KPI ne récompense pas uniquement le paiement immédiat.

18. Coach IA

Le Coach peut analyser :

les informations financières non explorées ;
les solutions qui auraient pu être proposées ;
les formulations à améliorer ;
les risques de non-conformité ;
la qualité de la négociation.

Le retour est centré sur les compétences observables.

19. Jeux de données

Le pack fournit :

clients fictifs ;
contrats ;
factures ;
historiques de paiement ;
promesses de paiement ;
règles de recouvrement ;
profils financiers synthétiques.

Toutes les données sont générées artificiellement.

20. Extensions sectorielles

Le même moteur peut être utilisé pour :

télécommunications ;
énergie ;
banques ;
assurances ;
établissements de crédit ;
e-commerce ;
services publics ;
abonnements numériques.

Chaque secteur fournit ses politiques de recouvrement et ses scénarios.

21. Décisions d'architecture (ADR)

Ce volume formalise les principes suivants :

Le Collection Engine pilote la logique métier du recouvrement.
Les politiques de paiement sont déclaratives.
Les engagements du client sont historisés.
Les règles de conformité sont configurables.
Le moteur distingue incapacité de paiement et refus de paiement.
22. Critères d'acceptation

Le Domain Pack Recouvrement est considéré conforme lorsque :

les scénarios couvrent les principales situations d'impayés ;
les politiques de paiement sont appliquées automatiquement ;
les personas produisent des comportements réalistes ;
les engagements sont suivis par le Collection Engine ;
les évaluations QA sont cohérentes avec les procédures métier.
🏛️ Décision d'architecture majeure : Ethical Collection Architecture (ECA)

Je recommande une Ethical Collection Architecture.

Le moteur de simulation ne cherche pas à maximiser la pression exercée sur le client. Il entraîne les agents à adopter une démarche conforme, respectueuse et documentée, tout en atteignant les objectifs opérationnels fixés par l'entreprise.

Cette architecture sépare clairement :

la simulation conversationnelle (LLM) ;
la logique métier (Collection Engine) ;
les politiques de recouvrement (configuration) ;
l'évaluation qualité (QA Engine).

Cette séparation facilite l'adaptation aux réglementations locales et aux politiques propres à chaque organisation.

📘 Prochaine étape : G6 — Domain Pack Back Office

Le prochain volume portera sur un métier souvent absent des simulateurs classiques mais essentiel dans les centres de contacts modernes :

traitement des dossiers sans contact direct avec le client ;
vérification documentaire ;
validation et rejet de demandes ;
gestion des files de travail (work queues) ;
application de règles métier ;
détection des anomalies ;
collaboration avec les équipes Front Office.

Ce volume introduira un Workflow Engine, chargé de simuler le traitement de dossiers, les transitions d'état, les contrôles de conformité et les files de traitement, afin d'entraîner les collaborateurs Back Office sur des processus complets plutôt que sur des conversations.
