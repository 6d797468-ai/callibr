# Volume G03 — Domain Pack — Télévente & Vente Conseil

> Extrait généré depuis `Architecture & Engineering Book (AEB).md` le 2026-07-27.

PHASE G — CONTACT CENTER BUSINESS PACKS
Volume G3
Domain Pack — Télévente & Vente Conseil

Version : 1.0

Statut : Référence métier

Criticité : Critique

1. Vision

Le Domain Pack Télévente transforme ATOS en une plateforme d'entraînement commercial.

L'objectif n'est pas de pousser le stagiaire à vendre à tout prix.

L'objectif est de former un conseiller capable de :

comprendre le client ;
proposer une solution adaptée ;
argumenter avec pertinence ;
respecter les règles de conformité ;
conclure de manière professionnelle.

Le moteur valorise la qualité de la démarche autant que le résultat.

2. Objectifs pédagogiques

À la fin de la formation, l'agent doit être capable de :

créer un climat de confiance ;
découvrir les besoins explicites et implicites ;
qualifier le prospect ;
présenter une offre adaptée ;
traiter les objections ;
détecter les opportunités de vente additionnelle ;
conclure ou planifier une relance.
3. Workflow commercial
Accueil

↓

Création du contact

↓

Découverte

↓

Qualification

↓

Présentation de la solution

↓

Argumentation

↓

Traitement des objections

↓

Closing

↓

Confirmation

↓

Clôture
4. Sales Engine

Le Sales Engine maintient un état structuré de l'entretien.

Il suit notamment :

le niveau d'intérêt ;
les besoins identifiés ;
les objections ;
les motivations d'achat ;
les freins ;
la probabilité de conversion ;
la prochaine meilleure action (Next Best Action).

Le LLM anime la conversation.

Le Sales Engine valide la logique commerciale.

5. État interne
Prospect

↓

Qualification

↓

Découverte

↓

Opportunité

↓

Argumentation

↓

Objections

↓

Décision

↓

Vente

ou

Relance

ou

Abandon
6. Qualification

Le moteur vérifie que l'agent identifie :

le contexte ;
le besoin principal ;
le budget (si pertinent) ;
le délai de décision ;
le décideur ;
les contraintes.

Ces éléments sont configurables selon le secteur.

7. Personas commerciaux

Le pack fournit plusieurs profils.

Persona	Description	Difficulté
Curieux	Veut comprendre	★
Pressé	Peu de temps	★
Comparateur	Compare plusieurs offres	★★
Méfiant	Craint un engagement	★★
Négociateur	Cherche une remise	★★★
Indécis	Hésite longtemps	★★★
Expert	Connaît bien le produit	★★★
Décideur exigeant	Attentes élevées	★★★
8. Motivations d'achat

Le moteur identifie des motivations telles que :

prix ;
qualité ;
rapidité ;
sécurité ;
simplicité ;
innovation ;
image de marque ;
accompagnement.

Un même client peut en avoir plusieurs.

9. Objections

Bibliothèque standard :

trop cher ;
je dois réfléchir ;
j'ai déjà un fournisseur ;
je n'ai pas le temps ;
envoyez-moi une documentation ;
je dois consulter mon responsable ;
ce n'est pas une priorité.

Chaque objection possède des réponses attendues.

10. CRM commercial

Le CRM simulé comprend :

Prospect
identité ;
entreprise (B2B) ;
secteur ;
historique des contacts ;
statut commercial.
Opportunité
produit visé ;
valeur estimée ;
probabilité de conversion ;
étape du pipeline ;
date de relance.
Historique
appels ;
e-mails ;
démonstrations ;
devis ;
commandes.
11. Actions CRM

L'agent peut :

créer un prospect ;
mettre à jour une opportunité ;
planifier une relance ;
générer un devis fictif ;
envoyer une brochure ;
enregistrer une note ;
clôturer l'opportunité.
12. Arbre de décision commerciale

Exemple simplifié :

Besoin identifié ?

↓

Non

↓

Continuer la découverte

↓

Oui

↓

Offre adaptée ?

↓

Oui

↓

Présenter les bénéfices

↓

Objection ?

↓

Oui

↓

Traiter

↓

Closing
13. Vente additionnelle

Le moteur détecte les opportunités de :

Cross-sell ;
Up-sell ;
Bundle.

Il n'encourage ces propositions que lorsqu'elles sont pertinentes pour le besoin exprimé.

14. Conformité

Le moteur contrôle :

absence de promesse trompeuse ;
respect des conditions de vente ;
transparence sur les engagements ;
conformité réglementaire propre au secteur.

Une vente obtenue par une information incorrecte est considérée comme un échec.

15. Bibliothèque de scénarios

Exemples.

ID	Scénario	Niveau
SALES-001	Vente d'une offre Internet	1
SALES-002	Changement de forfait	1
SALES-003	Vente avec comparaison concurrente	2
SALES-004	Prospect indécis	2
SALES-005	Négociation tarifaire	2
SALES-006	Vente B2B	3
SALES-007	Vente avec décideurs multiples	3
SALES-008	Vente complexe avec relance	3
16. Évaluation QA

Critères indicatifs.

Critère	Pondération
Accueil	10 %
Découverte	20 %
Qualification	15 %
Argumentation	20 %
Traitement des objections	15 %
Closing	10 %
Conformité	10 %

Le score final combine qualité de la démarche et résultat.

17. KPI métier

Le pack calcule notamment :

taux de conversion simulé ;
taux de qualification complète ;
nombre moyen d'objections traitées ;
opportunités de cross-sell détectées ;
qualité du closing ;
durée moyenne d'entretien ;
progression commerciale.
18. Coach commercial

Le Coach IA peut fournir :

une analyse de la découverte ;
les questions oubliées ;
les arguments les plus efficaces ;
les objections mal traitées ;
des pistes d'amélioration personnalisées.

Le débriefing met l'accent sur les compétences, pas uniquement sur le résultat.

19. Jeux de données

Le pack fournit :

prospects B2C ;
entreprises B2B ;
catalogues d'offres ;
produits ;
remises autorisées ;
campagnes commerciales ;
historiques d'interactions.

Toutes les données sont synthétiques et cohérentes.

20. Extensions sectorielles

Le même moteur peut être adapté à :

télécommunications ;
assurances ;
banques ;
énergie ;
logiciels SaaS ;
automobile ;
immobilier ;
formation.

Chaque secteur apporte ses offres, ses règles et ses scénarios.

21. Décisions d'architecture (ADR)

Ce volume formalise les principes suivants :

Le Sales Engine pilote la logique commerciale.
Les objections sont déclaratives et versionnées.
Les règles de conformité sont configurables.
Les opportunités commerciales sont évaluées indépendamment du LLM.
Les CRM commerciaux utilisent les mêmes contrats que les autres Domain Packs.
22. Critères d'acceptation

Le Domain Pack Télévente est considéré conforme lorsque :

les scénarios couvrent les principales étapes du cycle de vente ;
les personas commerciaux produisent des comportements variés ;
les règles de conformité sont appliquées ;
les opportunités de vente sont correctement identifiées ;
les évaluations distinguent clairement la qualité de la démarche du résultat obtenu.
🏛️ Décision d'architecture majeure : Opportunity-Driven Sales Architecture (ODSA)

Pour la télévente, je recommande une Opportunity-Driven Sales Architecture.

Le moteur ne juge pas uniquement si une vente a été conclue. Il analyse l'ensemble du processus commercial : découverte, qualification, argumentation, traitement des objections, conformité et capacité à identifier des opportunités pertinentes.

Cette approche permet d'entraîner des conseillers à développer des compétences durables plutôt qu'à rechercher un résultat immédiat.

📘 Prochaine étape : G4 — Domain Pack Rétention & Fidélisation

Le prochain volume abordera un domaine où la vente n'est plus l'objectif principal. L'enjeu sera de préserver la relation client :

analyse des motifs de résiliation ;
détection du risque de départ (churn) ;
techniques de rétention ;
négociation et gestes commerciaux ;
limites des pouvoirs de l'agent ;
escalade vers les équipes spécialisées ;
conformité et transparence ;
calcul d'un Retention Score et d'une probabilité de fidélisation.

Ce volume introduira un Retention Engine, chargé d'évaluer le risque de départ du client, l'efficacité des actions proposées et l'équilibre entre satisfaction client et préservation des intérêts de l'entreprise.
