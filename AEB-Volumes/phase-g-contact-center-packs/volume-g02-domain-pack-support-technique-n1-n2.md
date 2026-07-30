# Volume G02 — Domain Pack — Support Technique N1 / N2

> Extrait généré depuis `Architecture & Engineering Book (AEB).md` le 2026-07-27.

PHASE G — CONTACT CENTER BUSINESS PACKS
Volume G2
Domain Pack — Support Technique N1 / N2

Version : 1.0

Statut : Référence métier

Criticité : Critique

1. Vision

Le Support Technique est une simulation de résolution d'incidents.

L'agent ne doit pas seulement répondre.

Il doit :

investiguer ;
éliminer des hypothèses ;
interpréter des informations techniques ;
appliquer une procédure ;
résoudre ou escalader.

Le moteur IA doit pouvoir simuler un environnement technique crédible.

2. Objectifs pédagogiques

À la fin de la formation, un agent doit savoir :

qualifier un incident ;
identifier le symptôme principal ;
suivre un arbre de diagnostic ;
utiliser les outils disponibles ;
isoler la cause probable ;
proposer une solution adaptée ;
documenter correctement le ticket ;
décider d'une escalade si nécessaire.
3. Workflow global
Accueil

↓

Identification

↓

Qualification

↓

Collecte d'informations

↓

Diagnostic

↓

Tests

↓

Analyse

↓

Résolution

↓

Validation

↓

Documentation

↓

Clôture
4. Niveaux de support
Niveau 1

Responsabilités :

incidents simples ;
assistance utilisateur ;
configuration ;
procédures standard ;
FAQ.
Niveau 2

Responsabilités :

incidents complexes ;
analyse approfondie ;
corrélation d'événements ;
expertise produit ;
résolution avancée.
Niveau 3 (simulation)

Le N3 n'est généralement pas joué par l'apprenant.

Il représente :

l'équipe d'ingénierie ;
les développeurs ;
les constructeurs.

Le moteur simule les réponses du N3 lorsque cela est nécessaire.

5. Familles d'incidents

Le pack couvre plusieurs catégories.

Connectivité
pas de connexion
débit faible
perte intermittente
coupures
Authentification
mot de passe
MFA
compte bloqué
droits
Logiciel
erreur
plantage
lenteur
installation
Matériel
modem
routeur
téléphone
PC
imprimante
Cloud
API
service indisponible
synchronisation
stockage
6. Diagnostic Engine

Nouveau composant.

Le moteur maintient :

hypothèses ;
observations ;
tests réalisés ;
résultats ;
cause probable ;
résolution.

Il suit une logique déterministe.

7. Structure interne du diagnostic
Incident

↓

Hypothèses

↓

Tests

↓

Résultats

↓

Hypothèse retenue

↓

Solution

Le LLM ne décide jamais seul.

Le Diagnostic Engine valide la cohérence.

8. Arbres de diagnostic

Chaque incident possède un arbre.

Exemple.

Internet KO

↓

Voyants modem ?

↓

Oui

↓

Adresse IP ?

↓

Oui

↓

Ping ?

↓

Échec

↓

DNS ?

↓

Résolution impossible

↓

Incident DNS probable

Les arbres sont déclaratifs.

9. Procédure de diagnostic

Exemple YAML.

procedure: internet_down

steps:

- verify_identity

- identify_equipment

- check_leds

- reboot_modem

- wait_sync

- test_connection

- test_dns

- conclude

success:

- internet_restored

failure:

- escalation_level2
10. Outils simulés

L'agent dispose d'outils virtuels.

Exemples.

état modem ;
journal système ;
état réseau ;
test de ligne ;
vitesse ;
DNS ;
adresse IP ;
services cloud ;
monitoring.

Ces outils renvoient des données fictives cohérentes.

11. CRM Technique

Le CRM contient :

Client
abonnement
historique
incidents
Équipements
numéro de série
firmware
modèle
état
Réseau
statut
qualité
dernières mesures
Historique
tickets
remplacements
interventions
12. Actions disponibles

L'agent peut :

consulter les équipements ;
lancer un test ;
redémarrer virtuellement un équipement ;
ouvrir un ticket ;
programmer un technicien ;
changer une configuration ;
envoyer une documentation ;
escalader.
13. États émotionnels

Le comportement du client évolue.

Exemple.

Calme

↓

Inquiet

↓

Frustré

↓

En colère

↓

Rassuré

↓

Satisfait

Une démarche claire et pédagogique réduit généralement la frustration.

14. Escalade

Le moteur détermine :

si une escalade est justifiée ;
si elle intervient au bon moment ;
si le ticket contient les informations nécessaires.

Une escalade prématurée ou injustifiée est pénalisée.

15. Documentation du ticket

L'agent doit compléter :

symptôme ;
contexte ;
tests effectués ;
résultat ;
hypothèse retenue ;
solution ;
action suivante.

Le moteur vérifie la complétude.

16. Bibliothèque de scénarios

Exemples.

ID	Scénario	Niveau
TECH-001	Plus d'Internet	1
TECH-002	Wi-Fi instable	1
TECH-003	Erreur de connexion SaaS	2
TECH-004	Compte bloqué	2
TECH-005	Synchronisation impossible	2
TECH-006	Panne intermittente	3
TECH-007	Incident multi-services	3
TECH-008	Escalade N2	3
17. Évaluation QA

Critères indicatifs.

Critère	Pondération
Accueil	5 %
Qualification	15 %
Collecte d'informations	15 %
Respect du diagnostic	25 %
Communication	15 %
Résolution	15 %
Documentation	10 %

Les critères peuvent être adaptés selon le domaine.

18. KPI métier

Le pack calcule notamment :

taux de résolution au premier contact (FCR simulé) ;
temps moyen de diagnostic ;
nombre moyen d'hypothèses testées ;
taux d'escalade ;
qualité de la documentation ;
taux d'erreurs de procédure ;
progression technique de l'apprenant.
19. Jeux de données

Le pack fournit des données synthétiques :

10 000 clients ;
30 000 équipements ;
200 modèles d'appareils ;
500 incidents types ;
5 000 tickets historiques ;
états réseau simulés ;
journaux techniques fictifs.
20. Extensions par secteur

Le même moteur peut être spécialisé pour :

opérateur télécom ;
fournisseur d'accès Internet ;
éditeur SaaS ;
hébergeur Cloud ;
fabricant de matériel ;
entreprise énergétique ;
logiciels métiers.

Seuls les arbres de diagnostic, les outils simulés et les connaissances changent.

21. Décisions d'architecture (ADR)

Ce volume formalise les principes suivants :

Le raisonnement technique est piloté par le Diagnostic Engine.
Les arbres de diagnostic sont déclaratifs et versionnés.
Les outils simulés répondent via des contrats stables.
Le CRM technique est indépendant du moteur conversationnel.
Les scénarios séparent clairement les responsabilités N1, N2 et N3.
22. Critères d'acceptation

Le Domain Pack Support Technique est considéré conforme lorsque :

les arbres de diagnostic couvrent les incidents ciblés ;
les outils simulés produisent des résultats cohérents ;
les scénarios permettent de distinguer résolution et escalade ;
la qualité de la documentation est évaluée ;
les benchmarks techniques sont reproductibles.
🏛️ Décision d'architecture majeure : Guided Diagnostic Architecture (GDA)

Pour le support technique, je recommande une Guided Diagnostic Architecture.

Le LLM conserve son rôle conversationnel, mais le raisonnement métier est encadré par un moteur de diagnostic déterministe. Les hypothèses, les tests et les conclusions sont validés par des règles déclaratives plutôt que laissés à l'interprétation du modèle.

Cette séparation améliore :

la cohérence des simulations ;
la reproductibilité des évaluations ;
la facilité de maintenance des procédures ;
l'adaptation à différents secteurs techniques.
📘 Prochaine étape : G3 — Domain Pack Télévente & Vente Conseil

Le prochain volume décrira un domaine très différent, centré sur la performance commerciale :

qualification du besoin ;
découverte des attentes du client ;
argumentation et traitement des objections ;
vente additionnelle (cross-sell) et montée en gamme (up-sell) ;
techniques de closing ;
conformité commerciale ;
indicateurs de conversion ;
coaching commercial ;
personas orientés vente ;
simulation d'objectifs, de quotas et de campagnes.

Ce volume introduira également un Sales Engine, chargé de suivre la progression de l'entretien commercial, les opportunités détectées et les probabilités de conversion afin d'évaluer la qualité de la démarche de vente au-delà du simple résultat final.
