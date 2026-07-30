# Volume G01 — Domain Pack — Service Après-Vente (SAV)

> Extrait généré depuis `Architecture & Engineering Book (AEB).md` le 2026-07-27.

PHASE G — CONTACT CENTER BUSINESS PACKS
Volume G1
Domain Pack — Service Après-Vente (SAV)

Version : 1.0

Statut : Référence métier

Criticité : Critique

1. Vision

Le Domain Pack SAV reproduit le fonctionnement d'un véritable service client.

Le stagiaire ne s'entraîne pas uniquement à répondre.

Il apprend à :

rassurer un client ;
appliquer une procédure ;
consulter un CRM ;
respecter les obligations légales ;
résoudre le problème ;
clôturer correctement l'interaction.

Le moteur IA doit reproduire un client réaliste.

2. Domaines couverts

Le pack SAV couvre notamment :

E-commerce
Télécom
Banque
Assurance
Énergie
Administration
Logiciels SaaS
Retail
Livraison
Transport

Le cœur du moteur reste identique.

Seules les connaissances changent.

3. Objectifs pédagogiques

À la fin d'une formation SAV, un agent doit être capable de :

accueillir le client ;
identifier la demande ;
vérifier l'identité ;
reformuler ;
diagnostiquer ;
appliquer la bonne procédure ;
proposer une solution adaptée ;
conclure correctement.
4. Workflow métier
Accueil

↓

Identification

↓

Qualification

↓

Diagnostic

↓

Recherche CRM

↓

Application procédure

↓

Résolution

↓

Validation client

↓

Clôture

↓

Synthèse

Ce workflow constitue la base de tous les scénarios SAV.

5. Familles de demandes

Le pack fournit une bibliothèque de demandes.

Informations
horaires
tarifs
garanties
modalités
livraison
Réclamations
retard
produit défectueux
erreur de facturation
mauvais produit
mauvaise prestation
Contrats
modification
suspension
résiliation
renouvellement
Paiements
remboursement
impayé
échéancier
Assistance
activation
configuration
suivi de dossier
6. Niveaux de difficulté

Trois niveaux.

Niveau 1

Simple.

Une seule demande.

Client calme.

Niveau 2

Deux demandes.

Client impatient.

Quelques objections.

Niveau 3

Multiples problèmes.

Client difficile.

Exceptions.

Escalade possible.

7. Typologie des clients

Le pack fournit une bibliothèque.

Persona	Difficulté
Calme	★
Pressé	★
Bavard	★★
Confus	★★
Mécontent	★★★
Agressif	★★★
Exigeant	★★★
Suspicieux	★★★
8. États émotionnels

Le moteur gère.

Neutre

↓

Frustré

↓

En colère

↓

Très en colère

↓

Calmé

↓

Satisfait

Les transitions dépendent :

du ton ;
des délais ;
des actions CRM ;
des erreurs de procédure.
9. Procédure standard

Checklist.

□ Salutation

□ Présentation

□ Vérification identité

□ Reformulation

□ Recherche CRM

□ Diagnostic

□ Solution

□ Validation

□ Conclusion

Chaque étape peut être obligatoire ou optionnelle selon le scénario.

10. CRM simulé

Le CRM expose des données réalistes.

Client
nom
prénom
date de naissance
téléphone
e-mail
adresse
Contrat
numéro
statut
ancienneté
offre
options
Historique
appels
tickets
remboursements
incidents
Produits
référence
garantie
état
livraison
11. Actions CRM

L'agent peut :

rechercher un client ;
vérifier l'identité ;
consulter le contrat ;
ouvrir un ticket ;
créer une réclamation ;
programmer un rappel ;
déclencher un remboursement fictif ;
appliquer un geste commercial ;
clôturer un dossier.

Toutes les actions sont simulées et historisées.

12. Procédures métiers

Chaque procédure est décrite sous forme déclarative.

Exemple :

procedure: refund_standard

mandatory_steps:
  - verify_identity
  - check_order
  - validate_eligibility
  - explain_conditions
  - confirm_refund

optional_steps:
  - commercial_gesture

blocking_rules:
  - identity_not_verified
  - order_not_found

success_conditions:
  - refund_created

Le moteur vérifie le respect de cette procédure.

13. Bibliothèque de scénarios

Le pack inclut une première série de scénarios.

ID	Scénario	Niveau
SAV-001	Colis en retard	1
SAV-002	Produit défectueux	1
SAV-003	Erreur de facturation	2
SAV-004	Demande de remboursement	2
SAV-005	Résiliation difficile	3
SAV-006	Double réclamation	3
SAV-007	Client agressif	3
SAV-008	Escalade superviseur	3
14. Conditions de réussite

Une simulation est réussie si :

identité vérifiée ;
procédure respectée ;
demande résolue ou correctement orientée ;
communication professionnelle ;
clôture conforme.
15. Conditions d'échec

Exemples :

oubli de vérification d'identité ;
information erronée ;
promesse non autorisée ;
absence de reformulation ;
non-respect des règles de conformité ;
mauvaise clôture.
16. Évaluation QA

Critères indicatifs.

Critère	Pondération
Accueil	10 %
Écoute active	15 %
Empathie	15 %
Vérification d'identité	15 %
Respect de la procédure	20 %
Exactitude des informations	15 %
Clôture	10 %

Les pondérations restent configurables.

17. KPI métier

Le pack calcule notamment :

taux de réussite des simulations ;
score QA moyen ;
durée moyenne de traitement simulée ;
taux de résolution au premier contact (FCR simulé) ;
taux d'escalade ;
nombre moyen d'erreurs de procédure ;
progression de l'apprenant.
18. Prompts spécialisés

Le pack fournit des prompts versionnés pour :

le client IA ;
le coach IA ;
l'évaluateur QA ;
le moteur émotionnel ;
le moteur de connaissances ;
le générateur de débriefing.

Ces prompts héritent du Framework défini en Phase C et des contrats de Phase F.

19. Jeux de données

Le pack inclut des données fictives :

10 000 clients ;
5 000 contrats ;
25 000 commandes ;
15 000 tickets ;
3 000 remboursements ;
catalogue produits ;
historique d'interactions.

Toutes les données sont anonymes et générées artificiellement.

20. Benchmarks

Le pack est livré avec :

scénarios de validation ;
conversations de référence ;
scores attendus ;
tests de régression métier.

Ces benchmarks garantissent que les évolutions du moteur n'altèrent pas la qualité des simulations.

21. Décisions d'architecture (ADR)

Ce volume formalise les principes suivants :

Les procédures SAV sont déclaratives et versionnées.
Le CRM est simulé mais cohérent.
Les scénarios sont indépendants du moteur.
Les critères QA sont configurables.
Les données de démonstration sont entièrement synthétiques.
22. Critères d'acceptation

Le Domain Pack SAV est considéré conforme lorsque :

les scénarios couvrent les principaux cas d'usage ;
les procédures sont validées ;
les personas produisent des comportements crédibles ;
les évaluations QA sont cohérentes ;
les benchmarks sont reproductibles.
🏛️ Décision d'architecture majeure : Procedure-Driven Simulation

Pour le SAV, je recommande une approche Procedure-Driven Simulation.

Le LLM n'est pas seul à décider de la qualité de la conversation. Il est encadré par :

une machine à états ;
des procédures déclaratives ;
un CRM simulé ;
des règles métier ;
un moteur d'évaluation indépendant.

Ainsi, la simulation mesure à la fois la qualité de la communication et le respect des processus opérationnels, ce qui la rapproche des pratiques réelles des centres de contacts.

📘 Prochaine étape : G2 — Domain Pack Support Technique N1 / N2

Le prochain volume couvrira le support technique avec :

arbres de diagnostic ;
base de connaissances technique ;
procédures d'investigation ;
incidents, pannes et escalades ;
outils simulés (tests de ligne, état des services, journaux, équipements) ;
raisonnement guidé ;
critères QA spécifiques au support ;
simulation de tickets multi-niveaux ;
scénarios de résolution au premier contact et d'escalade vers le niveau 2.

Ce volume introduira également un Diagnostic Engine, capable de suivre les étapes d'investigation de l'agent et de vérifier qu'il applique une démarche de résolution méthodique plutôt que de répondre au hasard.
