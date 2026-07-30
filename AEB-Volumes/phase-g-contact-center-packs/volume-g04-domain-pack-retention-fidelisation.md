# Volume G04 — Domain Pack — Rétention & Fidélisation

> Extrait généré depuis `Architecture & Engineering Book (AEB).md` le 2026-07-27.

PHASE G — CONTACT CENTER BUSINESS PACKS
Volume G4
Domain Pack — Rétention & Fidélisation

Version : 1.0

Statut : Référence métier

Criticité : Critique

1. Vision

Le Domain Pack Rétention simule les interactions avec des clients qui envisagent de :

résilier un contrat ;
changer de fournisseur ;
réduire leurs services ;
exprimer une forte insatisfaction.

L'objectif est de former les agents à préserver la relation tout en respectant les politiques de l'entreprise.

2. Objectifs pédagogiques

À la fin de la formation, l'agent doit être capable de :

identifier le véritable motif de départ ;
distinguer les causes émotionnelles des causes rationnelles ;
évaluer le risque de résiliation ;
proposer une solution adaptée ;
négocier dans les limites de ses autorisations ;
conclure avec transparence, que le client reste ou parte.
3. Workflow métier
Accueil

↓

Identification

↓

Expression du problème

↓

Analyse des causes

↓

Évaluation du risque

↓

Recherche de solutions

↓

Négociation

↓

Décision

↓

Confirmation

↓

Clôture
4. Retention Engine

Le moteur maintient plusieurs états :

niveau de satisfaction ;
niveau de frustration ;
intention de départ ;
sensibilité au prix ;
confiance envers la marque ;
probabilité de rétention ;
historique des concessions.

Il met à jour ces états après chaque échange.

5. État interne
Client fidèle

↓

Insatisfaction

↓

Intention de départ

↓

Négociation

↓

Décision

↓

Conservation

ou

Résiliation
6. Causes de résiliation

Le moteur distingue notamment :

Prix
augmentation tarifaire ;
concurrent moins cher.
Qualité
incidents répétés ;
mauvaise qualité de service.
Relation
mauvaise expérience ;
absence de suivi.
Produit
fonctionnalités insuffisantes ;
besoins qui ont évolué.
Personnel
déménagement ;
changement d'activité ;
fermeture d'entreprise.

Ces causes peuvent être combinées.

7. Personas spécifiques
Persona	Description	Difficulté
Déçu	Plusieurs mauvaises expériences	★★
Opportuniste	Cherche une meilleure offre	★★
Irrité	Veut partir immédiatement	★★★
Loyal mais frustré	Longue ancienneté	★★★
Calculateur	Compare toutes les offres	★★★
Décision déjà prise	Très difficile à retenir	★★★
8. Analyse des causes

Le moteur vérifie que l'agent :

écoute sans interrompre ;
reformule correctement ;
identifie la cause principale ;
distingue les symptômes des causes profondes.

Une proposition faite avant cette analyse est considérée comme prématurée.

9. Catalogue d'actions

Selon les règles métier, l'agent peut :

proposer une remise ;
changer d'offre ;
offrir un mois gratuit ;
supprimer des frais ;
planifier un rappel ;
transférer vers une équipe spécialisée ;
accepter la résiliation.

Chaque action possède des limites définies par le Domain Pack.

10. Politique commerciale

Les règles sont déclaratives.

Exemple :

commercial_policy:

discount:
  max_percentage: 15

free_months:
  max: 2

gift:
  allowed: false

escalation:
  required_after: 2_failed_attempts

Le moteur applique ces règles automatiquement.

11. CRM Fidélisation

Le CRM expose notamment :

Contrat
ancienneté ;
formule ;
historique des renouvellements.
Valeur client
dépenses ;
produits détenus ;
incidents passés.
Historique
réclamations ;
gestes commerciaux ;
tentatives de rétention.
12. Actions CRM

L'agent peut :

consulter la valeur client ;
consulter les gestes précédents ;
appliquer une remise autorisée ;
modifier l'abonnement ;
planifier un rappel ;
créer une demande d'exception ;
enregistrer une résiliation.

Toutes les décisions sont simulées et tracées.

13. Bibliothèque de scénarios
ID	Scénario	Niveau
RET-001	Hausse tarifaire	1
RET-002	Client concurrent	1
RET-003	Qualité de service insuffisante	2
RET-004	Client fidèle très mécontent	2
RET-005	Menace de résiliation immédiate	3
RET-006	Négociation complexe	3
RET-007	Multi-produits	3
RET-008	Résiliation inévitable	3
14. Cas particuliers

Le moteur distingue :

client récupérable ;
client hésitant ;
client irrécupérable.

L'agent est évalué sur sa capacité à reconnaître ces situations.

Forcer une rétention lorsqu'elle n'est plus réaliste est pénalisé.

15. Évaluation QA

Critères indicatifs.

Critère	Pondération
Écoute active	20 %
Empathie	20 %
Analyse du besoin	20 %
Proposition adaptée	15 %
Respect des règles commerciales	15 %
Clôture	10 %
16. KPI métier

Le pack calcule notamment :

taux de rétention simulé ;
qualité de la découverte des causes ;
pertinence des offres proposées ;
taux de concessions inutiles ;
qualité de la négociation ;
progression de l'apprenant.
17. Retention Score

Le Retention Engine calcule un score basé sur :

compréhension du problème ;
qualité de la communication ;
pertinence des solutions ;
respect des limites commerciales ;
évolution de l'intention de départ.

Le score ne dépend pas uniquement du fait que le client reste.

18. Coach IA

Le Coach peut indiquer :

quelles causes n'ont pas été explorées ;
quelles concessions étaient prématurées ;
quelles questions auraient permis de mieux comprendre le client ;
quels arguments étaient les plus adaptés.
19. Jeux de données

Le pack fournit :

contrats fictifs ;
historiques de fidélité ;
campagnes de rétention ;
offres promotionnelles ;
règles d'éligibilité ;
profils de clients à risque.

Toutes les données sont synthétiques.

20. Extensions sectorielles

Le moteur peut être adapté à :

télécommunications ;
assurances ;
banques ;
énergie ;
abonnements SaaS ;
plateformes de streaming ;
salles de sport ;
presse numérique.
21. Décisions d'architecture (ADR)

Ce volume formalise les principes suivants :

Le Retention Engine pilote l'évaluation du risque de départ.
Les politiques commerciales sont entièrement déclaratives.
Les limites de négociation sont configurables par secteur.
Les concessions sont historisées et prises en compte dans l'évaluation.
Le résultat final ne constitue pas l'unique critère de réussite.
22. Critères d'acceptation

Le Domain Pack Rétention est considéré conforme lorsque :

les scénarios couvrent les principaux motifs de départ ;
les politiques commerciales sont appliquées automatiquement ;
les personas présentent des comportements variés ;
les évaluations distinguent clairement qualité de la démarche et issue de la négociation ;
les benchmarks de rétention sont reproductibles.
🏛️ Décision d'architecture majeure : Retention Intelligence Architecture (RIA)

Je recommande une Retention Intelligence Architecture.

Le moteur ne cherche pas à maximiser artificiellement le taux de rétention. Il cherche à entraîner l'agent à prendre la bonne décision au bon moment, dans le respect des intérêts du client et des règles de l'entreprise.

Cette approche favorise des comportements réalistes et mesurables, tout en évitant de récompenser des négociations inappropriées ou des concessions excessives.

📘 Prochaine étape : G5 — Domain Pack Recouvrement

Le prochain volume couvrira un domaine où les contraintes réglementaires et relationnelles sont particulièrement fortes :

qualification des impayés ;
promesses de paiement ;
négociation d'échéanciers ;
gestion des refus ;
obligations légales et conformité ;
suivi des engagements ;
profils de débiteurs ;
indicateurs de performance du recouvrement.

Ce volume introduira un Collection Engine, chargé de suivre l'évolution de la situation financière simulée, les engagements pris par le client et la conformité des actions de l'agent, afin d'entraîner des pratiques de recouvrement professionnelles, respectueuses et conformes aux politiques applicables.
