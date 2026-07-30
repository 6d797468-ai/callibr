# Volume A00-A02 — Fondations, vision, architecture et constitution engineering

> Extrait généré depuis `Architecture & Engineering Book (AEB).md` le 2026-07-27.

Architecture & Engineering Book (AEB)

Nom : Callibr 

Architecte developpeur : Nawfel Reghai

Projet : Callibr : AI Contact Center Simulator Platform (ACS Platform)

Version : 1.1 (Living Architecture)

Statut : Developpement — Phase I completee

Phases couvertes : A à L — Fondations, Architecture métier, Platform Core, Engineering Standards, AI Engineering, Delivery, Business Packs, AI Platform Enterprise, Product, Business & Data Platform, Enterprise Platform Services, Dev Platform & DevSecOps, Product & Architecture Governance

Note d'édition — 2026-07-27

Le document monolithique reste la source narrative principale.

Une répartition physique en volumes opérationnels a été générée dans :

AEB-Volumes/AEB-MASTER-INDEX.md

Nomenclature recommandée :

Callibr : nom produit et marque SaaS.

ATOS : nom interne architectural du noyau AI Training Operating System.

ACS Platform : appellation initiale historique du projet.

La Phase I a été complétée avec les volumes I05 à I10.

Table des matières de la Phase A
Volume A0 — Vision Produit
A0.1 Executive Summary
A0.2 Vision
A0.3 Mission
A0.4 Problématique du marché
A0.5 Positionnement
A0.6 Objectifs stratégiques
A0.7 Personas
A0.8 Proposition de valeur
A0.9 Business Model
A0.10 KPIs
A0.11 Roadmap Produit
A0.12 Contraintes
Volume A1 — Enterprise Architecture
Principes d'architecture
Bounded Contexts
Domaines fonctionnels
Architecture logique
Architecture physique
Architecture des données
Architecture IA
Architecture événementielle
Architecture temps réel
Architecture multi-tenant
Scalabilité
Sécurité
Observabilité
Volume A2 — Engineering Constitution
Principes de développement
Standards Python
Standards IA
Standards API
Standards DDD
Standards Tests
Standards Git
Standards Documentation
Definition of Done
Critères de qualité
Gouvernance
Volume A0 — Vision Produit
A0.1 Executive Summary
Nom du produit

AI Contact Center Simulator Platform (ACS Platform)

Description

L'ACS Platform est une plateforme SaaS de simulation intelligente destinée aux centres de contacts.

Elle permet :

l'onboarding des nouveaux agents ;
la formation continue ;
l'entraînement sur des scénarios complexes ;
l'évaluation automatique des performances ;
le coaching personnalisé ;
la mesure des compétences dans le temps.

Le système reproduit un environnement réaliste de centre de contacts en combinant :

un client simulé par IA ;
un CRM fictif interactif ;
des procédures métier configurables ;
un moteur de règles déterministe ;
une évaluation QA automatisée.
Objectif

Créer la plateforme de référence pour l'entraînement conversationnel assisté par IA dans les centres de contacts.

A0.2 Vision

Créer une plateforme où chaque entreprise peut reproduire fidèlement son environnement opérationnel afin que les agents s'entraînent sans risque avant de traiter de vrais clients.

La plateforme doit permettre :

de réduire le temps de montée en compétence ;
d'améliorer la qualité des interactions ;
de standardiser les pratiques ;
de diminuer les coûts de formation ;
d'accélérer les certifications internes.
A0.3 Mission

Transformer la formation des centres de contacts en remplaçant les jeux de rôle manuels par des simulations réalistes, mesurables et personnalisables.

A0.4 Problématique

Les entreprises rencontrent plusieurs difficultés :

formation coûteuse ;
disponibilité limitée des formateurs ;
qualité variable des jeux de rôle ;
difficulté à reproduire les cas complexes ;
manque de données objectives sur les compétences.

Conséquences :

faible qualité de service ;
durée d'onboarding élevée ;
erreurs de procédure ;
insatisfaction client ;
coûts opérationnels.
A0.5 Positionnement

L'ACS Platform n'est pas :

un chatbot ;
un assistant conversationnel ;
un CRM ;
un LMS traditionnel.

L'ACS Platform est un Simulation Operating System spécialisé dans les interactions client.

A0.6 Objectifs stratégiques
Court terme (MVP)
Simulations textuelles.
CRM simulé.
Évaluation automatique.
Catalogue de scénarios.
Multi-tenant.
Moyen terme
Simulation vocale temps réel.
Génération automatique de scénarios.
Coaching adaptatif.
Tableau de bord superviseur.
Long terme
IA coach en temps réel.
Certification automatique.
Marketplace de scénarios.
Multi-langues.
API partenaires.
A0.7 Personas
Agent

Objectif :

Améliorer ses compétences.

Attentes :

simulations réalistes ;
feedback immédiat ;
progression mesurable.
Formateur

Objectif :

Former plusieurs agents efficacement.

Attentes :

créer des scénarios ;
suivre les résultats ;
comparer les performances.
Superviseur

Objectif :

Garantir la qualité opérationnelle.

Attentes :

tableaux de bord ;
détection des lacunes ;
reporting.
Administrateur

Objectif :

Configurer la plateforme.

Attentes :

gestion des organisations ;
gestion des rôles ;
catalogue métier.
Entreprise

Objectif :

Réduire les coûts de formation.

Attentes :

ROI ;
qualité ;
conformité ;
statistiques.
A0.8 Proposition de valeur

L'ACS Platform combine dans une seule solution :

simulation IA ;
CRM fictif ;
procédures métier ;
évaluation QA ;
analytics ;
coaching.
A0.9 Business Model
SaaS B2B

Abonnement par :

organisation ;
nombre d'agents ;
nombre de simulations ;
modules activés.

Modules optionnels :

voix ;
analytics avancés ;
marketplace ;
API ;
SSO.
A0.10 KPIs
Produit
nombre de simulations ;
durée moyenne ;
taux de réussite ;
progression des compétences ;
réutilisation des scénarios.
Métier
réduction du temps d'onboarding ;
amélioration du score QA ;
réduction des erreurs de procédure ;
amélioration du FCR ;
satisfaction des formateurs.
Technique
latence médiane des réponses IA ;
disponibilité de la plateforme ;
taux d'erreurs API ;
coût moyen d'une simulation.
A0.11 Roadmap
Phase 1

POC

simulation texte ;
un scénario ;
un persona.
Phase 2

MVP

catalogue ;
CRM ;
QA ;
multi-tenant.
Phase 3

V1

voix ;
analytics ;
coaching.
Phase 4

Enterprise

SSO ;
haute disponibilité ;
marketplace ;
API publiques.
A0.12 Contraintes
Fonctionnelles
scénarios entièrement configurables ;
aucun métier codé en dur ;
personnalisation par entreprise.
Non fonctionnelles
multi-tenant ;
haute disponibilité ;
observabilité complète ;
sécurité dès la conception ;
architecture modulaire.
Volume A1 — Enterprise Architecture (Synthèse)

Les principes directeurs sont les suivants :

Architecture hexagonale (Ports & Adapters) pour isoler le domaine métier des technologies.
Domain-Driven Design (DDD) pour structurer les domaines (Simulation, CRM, QA, Utilisateurs, Catalogue, IA).
Event-Driven Architecture pour synchroniser les modules sans couplage fort.
Machine à états déterministe pour piloter les scénarios ; le LLM n'est jamais responsable des transitions.
LLM comme composant spécialisé : il incarne le client, génère des réponses ou des évaluations, mais ne contient pas les règles métier.
Multi-tenant avec isolation logique dès le MVP et possibilité d'évolution vers une isolation physique pour les grands comptes.
API-first : toutes les fonctionnalités sont exposées via des contrats versionnés.
Observabilité native : logs structurés, métriques, traces distribuées et audit métier.
Volume A2 — Engineering Constitution (Extraits fondateurs)
Principes non négociables
Une règle métier ne doit jamais dépendre d'un prompt.
Un scénario ne doit jamais être codé en dur.
Toute décision importante doit être traçable.
Chaque fonctionnalité doit être testable de manière déterministe.
Les composants IA doivent pouvoir être remplacés sans modifier le domaine métier.
Définition de terminé (Definition of Done)

Une fonctionnalité est considérée comme terminée uniquement si :

la spécification est validée ;
le code est implémenté ;
les tests automatisés passent ;
la documentation est à jour ;
les métriques et logs sont présents ;
les critères d'acceptation sont satisfaits.
Gouvernance

Toute évolution devra respecter la chaîne de preuve suivante :

Spécification → Implémentation → Tests → Déploiement → Utilisation → Impact métier

Aucune fonctionnalité ne sera considérée comme "réussie" tant que cette chaîne n'est pas complète.
