# Volume G16 — Domain Pack — Healthcare Contact Center

> Extrait généré depuis `Architecture & Engineering Book (AEB).md` le 2026-07-27.

PHASE G — CONTACT CENTER BUSINESS PACKS
Volume G16
Domain Pack — Healthcare Contact Center

Version : 1.0

Statut : Enterprise Vertical

Criticité : Critique

1. Vision

Le Domain Pack Healthcare simule le fonctionnement d'un centre de relation patient.

Il couvre :

prise de rendez-vous ;
accueil téléphonique hospitalier ;
assistance patient ;
coordination de soins ;
orientation ;
suivi administratif ;
mutuelles ;
télésecrétariat médical ;
centres de vaccination ;
laboratoires ;
centres d'imagerie.

Le moteur entraîne les agents à gérer correctement la relation patient tout en respectant la confidentialité et les procédures.

2. Objectifs pédagogiques

À la fin de la formation, le stagiaire doit être capable de :

identifier correctement un patient ;
comprendre la demande ;
appliquer les procédures administratives ;
orienter vers le bon service ;
reconnaître les situations nécessitant une escalade ;
protéger les données médicales ;
communiquer avec empathie.
3. Architecture fonctionnelle
Patient

↓

Identity Engine

↓

Appointment Engine

↓

Healthcare Workflow Engine

↓

Medical Triage Engine

↓

Privacy & Compliance Engine

↓

Care Coordination Engine

↓

QA Engine
4. Patient Identity Engine

Le moteur gère :

identité simulée ;
dossier administratif ;
couverture ;
historique de rendez-vous ;
préférences de communication.

Toutes les données sont synthétiques.

5. Appointment Engine

Le moteur simule :

prise de rendez-vous ;
modification ;
annulation ;
listes d'attente ;
disponibilité des praticiens ;
ressources médicales.

Le calendrier est entièrement fictif.

6. Care Coordination Engine

Le moteur suit :

rendez-vous ;
examens ;
prescriptions simulées ;
transferts administratifs ;
orientations.

Il ne prend jamais de décision médicale.

7. Medical Triage Engine

Le moteur classe les demandes.

Exemple :

Niveau	Description
T1	Information administrative
T2	Orientation médicale simple
T3	Situation urgente nécessitant transfert
T4	Situation critique nécessitant les services d'urgence

Le moteur ne fournit jamais de diagnostic.

Il identifie uniquement le niveau de traitement attendu.

8. Situations d'urgence

Le Persona Engine peut générer :

douleur thoracique ;
perte de connaissance ;
difficultés respiratoires ;
accident ;
enfant malade ;
réaction allergique.

Le rôle du conseiller est :

garder son calme ;
appliquer le protocole ;
orienter immédiatement vers les services d'urgence lorsque le scénario le prévoit.

Le système évalue le respect du protocole, pas la qualité d'un avis médical.

9. Confidentialité

Le Privacy Engine contrôle :

vérification d'identité ;
accès aux informations ;
confidentialité des échanges ;
journalisation des accès ;
partage d'informations.

Les règles sont paramétrables selon les réglementations locales.

10. CRM Santé simulé

Le CRM contient :

patient ;
rendez-vous ;
historique administratif ;
correspondances ;
examens planifiés ;
documents administratifs.

Aucune donnée médicale réelle n'est utilisée.

11. Actions disponibles

Le conseiller peut :

rechercher un patient ;
planifier un rendez-vous ;
déplacer un rendez-vous ;
annuler ;
transmettre un dossier administratif ;
contacter un service ;
escalader vers un professionnel habilité.

Toutes les actions sont enregistrées.

12. Gestion émotionnelle

Le Persona Engine adapte le comportement du patient.

Exemples :

anxieux ;
inquiet ;
âgé ;
parent stressé ;
en colère après une longue attente ;
confus.

L'évolution émotionnelle dépend de la qualité de la communication.

13. Bibliothèque de scénarios
ID	Scénario	Niveau
HC-001	Prise de rendez-vous	1
HC-002	Modification d'un rendez-vous	1
HC-003	Patient anxieux	2
HC-004	Orientation vers un spécialiste	2
HC-005	Situation urgente	3
HC-006	Gestion d'un parcours complexe	3
HC-007	Coordination multi-services	3
HC-008	Centre hospitalier saturé	3
14. KPI métier

Le moteur calcule notamment :

délai moyen de prise en charge ;
taux de rendez-vous correctement planifiés ;
qualité de l'orientation ;
respect des protocoles ;
satisfaction simulée du patient ;
qualité de la communication.
15. Évaluation QA
Critère	Pondération
Vérification d'identité	10 %
Compréhension du besoin	20 %
Respect des procédures	20 %
Orientation appropriée	20 %
Communication et empathie	20 %
Documentation	10 %
16. Jeux de données

Le pack comprend :

patients fictifs ;
rendez-vous simulés ;
établissements ;
spécialités médicales ;
plannings ;
documents administratifs.

Toutes les données sont synthétiques.

17. Architecture interne
Identity Engine

↓

Appointment Engine

↓

Workflow Engine

↓

Medical Triage Engine

↓

Privacy Engine

↓

Care Coordination Engine

↓

Analytics

Chaque moteur reste indépendant.

18. Intégration avec les autres moteurs

Le Domain Pack Healthcare échange avec :

Conversation Engine pour les interactions ;
Workflow Engine pour les processus administratifs ;
QA Engine pour l'évaluation ;
Learning Platform pour les recommandations pédagogiques ;
Reporting Platform pour les indicateurs ;
Scheduling Engine pour la simulation des agendas.
19. Décisions d'architecture (ADR)

Ce volume formalise les principes suivants :

Le moteur ne produit jamais de diagnostic médical.
Les décisions médicales sont hors du périmètre de la plateforme.
Les situations critiques déclenchent des protocoles déterministes.
Les données patients sont exclusivement synthétiques.
Les règles de confidentialité sont configurables et auditables.
20. Critères d'acceptation

Le Domain Pack Healthcare est considéré conforme lorsque :

les scénarios respectent les limites du rôle du conseiller ;
les protocoles d'orientation sont correctement appliqués ;
la confidentialité est systématiquement contrôlée ;
les évaluations distinguent compétences administratives et relationnelles ;
les données restent entièrement fictives.
🏛️ Décision d'architecture majeure : Healthcare Safety Simulation Architecture (HSSA)

Je recommande une Healthcare Safety Simulation Architecture (HSSA).

Le principe fondamental est une séparation stricte entre :

la simulation conversationnelle, assurée par le LLM ;
les décisions de processus, gérées par des moteurs déterministes ;
les décisions médicales, qui sont explicitement exclues du périmètre.

Le LLM peut expliquer une procédure, rassurer un patient ou guider un parcours administratif, mais il ne fournit jamais de diagnostic, de traitement ou de décision clinique.

Cette architecture permet de créer des scénarios réalistes tout en maintenant un niveau élevé de sécurité et de conformité.

📘 État d'avancement

Après ce volume :

✅ G1 à G16 terminés (16 Domain Packs sur 20).
📘 Il reste 4 volumes pour achever la Phase G :
G17 — E-commerce & Retail
G18 — Public Services & Administration
G19 — Collections avancées & Contentieux
G20 — Omnichannel & Digital Engagement

Une fois la Phase G terminée, nous passerons à la Phase H — AI Platform Enterprise, qui marquera une évolution majeure de l'Architecture & Engineering Book. Nous quitterons les domaines métier pour concevoir l'infrastructure technique de la plateforme : Agent Runtime, Prompt Compiler, LLM Gateway, Tool Calling, Memory Engine, Safety Layer, AI Governance et orchestration multi-agents. Cette phase constituera le cœur de votre future plateforme SaaS Enterprise de simulation par IA.
