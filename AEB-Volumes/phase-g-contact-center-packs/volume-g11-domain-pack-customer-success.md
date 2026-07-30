# Volume G11 — Domain Pack — Customer Success

> Extrait généré depuis `Architecture & Engineering Book (AEB).md` le 2026-07-27.

PHASE G — CONTACT CENTER BUSINESS PACKS
Volume G11
Domain Pack — Customer Success

Version : 1.0

Statut : Enterprise Core

Criticité : Très élevée

1. Vision

Le Domain Pack Customer Success simule le travail d'un Customer Success Manager (CSM), chargé d'accompagner les clients tout au long de leur cycle de vie.

Le moteur couvre :

onboarding ;
adoption ;
accompagnement ;
suivi ;
renouvellement ;
expansion commerciale ;
prévention du churn.

L'objectif pédagogique est d'apprendre à créer de la valeur durable pour le client.

2. Objectifs pédagogiques

À la fin de la formation, l'apprenant doit être capable de :

conduire un entretien de découverte ;
comprendre les objectifs du client ;
définir un plan de succès ;
suivre les indicateurs d'adoption ;
détecter les risques de churn ;
proposer des actions adaptées.
3. Cycle de vie client
Prospect

↓

Client

↓

Onboarding

↓

Adoption

↓

Activation

↓

Utilisation

↓

Expansion

↓

Renouvellement

↓

Ambassadeur

Chaque étape possède ses propres objectifs et critères de réussite.

4. Customer Success Engine

Le moteur maintient un Success Profile pour chaque client.

Il regroupe :

objectifs métier ;
niveau d'adoption ;
utilisateurs actifs ;
incidents ouverts ;
satisfaction ;
risques ;
opportunités d'expansion.
5. Success Score

Le moteur calcule un score global.

Exemple :

success_score:

usage: 25

adoption: 20

health: 20

support: 15

engagement: 10

renewal_probability: 10

Le score est recalculé après chaque interaction.

6. Customer Health Engine

Le moteur suit notamment :

fréquence d'utilisation ;
fonctionnalités utilisées ;
nombre d'utilisateurs actifs ;
tickets ouverts ;
satisfaction ;
NPS ;
temps depuis la dernière connexion.

Ces indicateurs alimentent le Health Score.

7. Détection des risques

Le moteur identifie automatiquement :

baisse d'utilisation ;
absence d'activité ;
faible adoption ;
incidents répétés ;
faible engagement ;
retard de paiement ;
baisse de satisfaction.

Chaque risque possède un niveau de criticité.

8. Plan de succès

Le CSM construit un plan comprenant :

objectifs ;
échéances ;
actions ;
responsables ;
indicateurs de réussite.

Le moteur vérifie la cohérence du plan.

9. Actions disponibles

Le stagiaire peut :

planifier un rendez-vous ;
envoyer des ressources ;
proposer une formation ;
ouvrir un ticket ;
organiser un atelier ;
mettre en place un plan de remédiation ;
proposer une montée en gamme.

Toutes les actions sont historisées.

10. Détection d'opportunités

Le moteur identifie des opportunités telles que :

ajout d'utilisateurs ;
nouvelles licences ;
modules complémentaires ;
montée de gamme ;
renouvellement anticipé.

Ces suggestions sont fondées sur le contexte simulé et non sur des règles figées.

11. Gestion du churn

Le Customer Success Engine estime une probabilité de churn à partir de plusieurs facteurs :

satisfaction ;
fréquence d'utilisation ;
incidents ;
ancienneté ;
engagement ;
évolution des usages.

Cette estimation sert à adapter les scénarios, sans constituer une prédiction absolue.

12. Bibliothèque de scénarios
ID	Scénario	Niveau
CS-001	Onboarding standard	1
CS-002	Faible adoption	1
CS-003	Client inactif	2
CS-004	Risque de churn	2
CS-005	Renouvellement difficile	3
CS-006	Expansion complexe	3
CS-007	Compte stratégique	3
CS-008	Gestion d'un client Enterprise	3
13. CRM Customer Success

Le CRM expose :

compte client ;
objectifs ;
utilisateurs ;
licences ;
historique ;
réunions ;
plans d'action ;
Health Score ;
Success Score.
14. KPI métier

Le pack calcule notamment :

taux d'adoption ;
taux d'activation ;
taux de renouvellement simulé ;
évolution du Health Score ;
progression des plans de succès ;
satisfaction simulée.
15. Évaluation QA

Critères indicatifs.

Critère	Pondération
Compréhension des objectifs client	20 %
Qualité du plan de succès	20 %
Détection des risques	20 %
Communication	15 %
Pertinence des recommandations	15 %
Documentation	10 %
16. Jeux de données

Le pack fournit :

comptes clients synthétiques ;
profils d'utilisation ;
historiques d'activité ;
plans de succès ;
incidents ;
données d'engagement.

Toutes les données sont artificielles.

17. Architecture interne
Customer Profile Engine

↓

Health Engine

↓

Risk Engine

↓

Success Planning Engine

↓

Expansion Engine

↓

Analytics

Chaque composant est indépendant.

18. Intégration avec les autres moteurs

Le Customer Success Engine échange avec :

CRM Simulator pour les informations client ;
Conversation Engine pour les rendez-vous et échanges ;
QA Engine pour les compétences relationnelles ;
Learning Platform pour recommander des parcours ciblés ;
Reporting Platform pour le suivi des KPI.
19. Décisions d'architecture (ADR)

Ce volume formalise les principes suivants :

Le Success Score est composé de plusieurs indicateurs indépendants.
Les risques sont calculés à partir d'événements observables.
Les plans de succès sont versionnés et historisés.
Les recommandations restent explicables et traçables.
Le moteur est générique et réutilisable pour différents secteurs.
20. Critères d'acceptation

Le Domain Pack Customer Success est considéré conforme lorsque :

les profils clients évoluent de manière cohérente au fil des interactions ;
les scénarios reproduisent des situations réalistes d'adoption et de renouvellement ;
les plans de succès peuvent être suivis et évalués ;
les recommandations sont adaptées au contexte ;
les indicateurs reflètent l'évolution du client simulé.
🏛️ Décision d'architecture majeure : Customer Lifecycle Intelligence Architecture (CLIA)

Je recommande une Customer Lifecycle Intelligence Architecture (CLIA).

Le Customer Success Engine devient le gestionnaire du cycle de vie du client. Il ne se limite pas à suivre des indicateurs : il maintient un modèle évolutif de la relation client, permettant de simuler l'impact des décisions du Customer Success Manager sur l'adoption, la satisfaction et la fidélisation.

Cette architecture est particulièrement adaptée à une plateforme SaaS de formation, car elle permet de créer des scénarios riches et progressifs, où les conséquences d'une interaction peuvent influencer les suivantes.

📘 État d'avancement

Après ce volume :

✅ G1 à G11 terminés (11 Domain Packs sur 20).
📘 Il reste 9 volumes pour achever la Phase G :
G12 — Help Desk ITIL
G13 — Incident & Problem Management
G14 — Banking Contact Center
G15 — Insurance Contact Center
G16 — Healthcare Contact Center
G17 — E-commerce & Retail
G18 — Public Services & Administration
G19 — Collections avancées & Contentieux
G20 — Omnichannel & Digital Engagement

Une fois ces neuf volumes terminés, nous passerons à la Phase H — AI Platform Enterprise, qui constituera le cœur technique de l'orchestration des agents IA, des prompts, des outils et des modèles LLM de la plateforme.
