# Volume G14 — Domain Pack — Banking Contact Center

> Extrait généré depuis `Architecture & Engineering Book (AEB).md` le 2026-07-27.

PHASE G — CONTACT CENTER BUSINESS PACKS
Volume G14
Domain Pack — Banking Contact Center

Version : 1.0

Statut : Enterprise Vertical

Criticité : Critique

1. Vision

Le Domain Pack Banking simule les interactions d'un centre de relation client bancaire.

Il couvre :

banque de détail ;

banque en ligne ;

cartes bancaires ;

paiements ;

virements ;

sécurité ;

KYC ;

fraude ;

réclamations financières ;

assistance digitale.

L'objectif est de former les agents à gérer des interactions sensibles, réglementées et fortement orientées confiance.

2. Objectifs pédagogiques

À la fin de la formation, l'agent doit être capable de :

authentifier un client ;

protéger les données bancaires ;

traiter une demande de paiement ;

gérer une carte perdue ou volée ;

détecter un risque de fraude ;

respecter les règles de conformité ;

documenter l'opération.

3. Architecture fonctionnelle
Client Request
        ↓
Authentication Engine
        ↓
Banking Workflow Engine
        ↓
Fraud & Risk Engine
        ↓
Compliance Engine
        ↓
Resolution Engine
        ↓
Audit & QA
4. Banking Workflow Engine

Le moteur gère les processus bancaires simulés :

consultation de compte ;

opposition carte ;

virement ;

changement de plafond ;

réclamation ;

contestation d'opération ;

mise à jour des coordonnées ;

activation de services digitaux.

Toutes les opérations sont fictives mais cohérentes.

5. Authentification

Avant toute action sensible, le moteur exige une authentification.

Exemple :

authentication:
  required_for:
    - account_balance
    - transfer
    - card_block
    - personal_data_update

  methods:
    - date_of_birth
    - last_transaction
    - one_time_code

Une authentification incomplète bloque l'opération.

6. Niveaux de sensibilité

Niveau

	

Exemple




Faible

	

Horaires d'agence




Moyen

	

Consultation de compte




Élevé

	

Changement de coordonnées




Critique

	

Virement / Opposition carte

Les contrôles augmentent avec la sensibilité.

7. Fraud & Risk Engine

Le moteur évalue le risque de fraude à partir de :

comportement inhabituel ;

localisation incohérente ;

montant atypique ;

fréquence des opérations ;

historique du client.

Le score de risque influence les scénarios.

8. Détection de fraude

Le système peut générer :

transaction inconnue ;

carte utilisée à l'étranger ;

tentatives multiples ;

phishing simulé ;

usurpation d'identité ;

prise de contrôle de compte.

L'agent doit appliquer la bonne procédure.

9. Compliance Engine

Le moteur vérifie notamment :

respect du secret bancaire ;

protection des données personnelles ;

authentification correcte ;

absence de divulgation d'informations sensibles ;

traçabilité des actions.

Les règles sont configurables selon le pays.

10. CRM bancaire

Le CRM simulé contient :

profils clients ;

comptes ;

cartes ;

bénéficiaires ;

historiques d'opérations ;

alertes de sécurité ;

incidents.

Toutes les données sont synthétiques.

11. Actions disponibles

L'agent peut :

consulter un compte (si autorisé) ;

bloquer une carte ;

débloquer un accès ;

enregistrer une contestation ;

initier un rappel sécurisé ;

mettre à jour certaines informations ;

escalader vers la cellule fraude.

Chaque action est journalisée.

12. Bibliothèque de scénarios

ID

	

Scénario

	

Niveau




BANK-001

	

Consultation de solde

	

1




BANK-002

	

Mot de passe oublié

	

1




BANK-003

	

Carte perdue

	

2




BANK-004

	

Transaction contestée

	

2




BANK-005

	

Tentative de fraude

	

3




BANK-006

	

Phishing simulé

	

3




BANK-007

	

Virement sensible

	

3




BANK-008

	

Incident de sécurité majeur

	

3

13. Évaluation QA

Critères indicatifs.

Critère

	

Pondération




Authentification

	

20 %




Conformité

	

20 %




Exactitude des informations

	

20 %




Gestion du risque

	

15 %




Communication

	

15 %




Documentation

	

10 %

La conformité est aussi importante que la relation client.

14. KPI métier

Le pack calcule notamment :

taux d'authentification correcte ;

taux de détection de fraude ;

taux d'erreurs de conformité ;

temps moyen de traitement ;

qualité de la documentation ;

satisfaction simulée.

15. Jeux de données

Le pack fournit :

clients fictifs ;

comptes synthétiques ;

cartes simulées ;

historiques d'opérations ;

alertes fraude ;

profils de risque.

Aucune donnée réelle n'est utilisée.

16. Architecture interne
Authentication Engine
        ↓
Authorization Engine
        ↓
Fraud Engine
        ↓
Compliance Engine
        ↓
Resolution Engine
        ↓
Audit Engine

Chaque composant est indépendant et testable.

17. Intégration avec les autres moteurs

Le Domain Pack Banking échange avec :

Conversation Engine pour les interactions client ;

QA Engine pour l'évaluation ;

Workflow Engine pour les processus ;

Learning Platform pour les parcours de formation ;

Reporting Platform pour les KPI.

Cette séparation permet d'ajouter d'autres produits bancaires sans modifier le cœur de la plateforme.

18. Décisions d'architecture (ADR)

Ce volume formalise les principes suivants :

L'authentification est obligatoire avant toute opération sensible.

Les contrôles de conformité sont indépendants du LLM.

Le moteur de fraude fournit un score de risque explicable.

Toutes les actions sont auditables et historisées.

Les données utilisées en simulation sont exclusivement synthétiques.

19. Critères d'acceptation

Le Domain Pack Banking est considéré conforme lorsque :

les opérations sensibles sont correctement protégées ;

les scénarios de fraude déclenchent les procédures adaptées ;

les évaluations QA prennent en compte la conformité et la sécurité ;

les journaux d'audit sont complets ;

les résultats sont reproductibles.

🏛️ Décision d'architecture majeure : Secure Financial Interaction Architecture (SFIA)

Je recommande une Secure Financial Interaction Architecture (SFIA).

Le principe central est que la sécurité et la conformité priment sur la fluidité de la conversation. Le LLM peut expliquer, rassurer et guider, mais il ne peut jamais contourner les contrôles d'authentification, d'autorisation ou de conformité.

Cette architecture apporte :

une simulation crédible des centres de relation bancaire ;

une forte traçabilité des opérations ;

une adaptation aux exigences réglementaires locales ;

une base réutilisable pour d'autres secteurs fortement réglementés.

📘 État d'avancement

Après ce volume :

✅ G1 à G14 terminés (14 Domain Packs sur 20).

📘 Il reste 6 volumes pour achever la Phase G :

G15 — Insurance Contact Center

G16 — Healthcare Contact Center

G17 — E-commerce & Retail

G18 — Public Services & Administration

G19 — Collections avancées & Contentieux

G20 — Omnichannel & Digital Engagement

Une fois ces six volumes terminés, nous entrerons dans la Phase H — AI Platform Enterprise, qui décrira l'orchestration complète des agents IA, du Prompt Compiler, du LLM Gateway, du Tool Calling, du registre de modèles et des mécanismes de sécurité et de gouvernance de l'intelligence artificielle de la plateforme.
