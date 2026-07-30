"""Seed loader — loads the shared G1-SUPPORT-SAV demo catalogue.

Catalogue content
-----------------
Personas   : persona-sav-client-frustre-001
Procedures : proc-sav-retard-colis-001, proc-sav-erreur-facturation-001
Rules      : rule-identity-required, rule-escalation-after-two-fails
Scenarios  : sc-sav-retard-colis-v1, sc-sav-erreur-facturation-v1

Each loader is idempotent: it silently skips definitions that are already
present in the target store (identified by their ID).
"""

from __future__ import annotations

import logging
from typing import TYPE_CHECKING

from callibr_contracts import (
    PersonaCommunication,
    PersonaDefinition,
    PersonaMemoryProfile,
    PersonaMetadata,
    PersonaTrait,
    ProcedureDefinition,
    RuleAction,
    RuleCondition,
    RuleDefinition,
    RuleMetadata,
    ScenarioDefinition,
    ScenarioMetadata,
    ScenarioObjective,
    ScenarioReference,
    StepDefinition,
)
from callibr_kernel import CallibrError

if TYPE_CHECKING:
    from callibr_persona import PersonaService
    from callibr_procedure import ProcedureService
    from callibr_rule import RuleService
    from callibr_scenario import ScenarioService

log = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Persona catalogue
# ---------------------------------------------------------------------------

_PERSONAS: list[PersonaDefinition] = [
    PersonaDefinition(
        persona_id="persona-sav-client-frustre-001",
        name="Client SAV — Frustré Coopératif",
        description=(
            "Client exprimant une frustration modérée suite à un retard de livraison. "
            "Coopératif si l'agent fait preuve d'empathie et de réactivité."
        ),
        role="client",
        tone=["empathique", "direct"],
        traits=[
            PersonaTrait(trait_id="t-frustration", name="frustration", weight=0.7),
            PersonaTrait(trait_id="t-cooperation", name="coopération", weight=0.8),
            PersonaTrait(trait_id="t-patience", name="patience", weight=0.5),
        ],
        communication=PersonaCommunication(
            style="informel",
            verbosity="medium",
            language="fr",
        ),
        memory_profile=PersonaMemoryProfile(
            short_term=True,
            long_term=False,
            max_history_turns=6,
            summary_after_turns=20,
        ),
        metadata=PersonaMetadata(
            difficulty="beginner",
            tags=["sav", "retard", "client", "g1"],
            author="callibr-seed",
            description="Persona client G1-SUPPORT-SAV pour scénarios retard colis.",
        ),
    ),
    PersonaDefinition(
        persona_id="persona-sav-client-exigeant-001",
        name="Client SAV — Exigeant",
        description=(
            "Client exigeant qui réclame une résolution immédiate et un dédommagement. "
            "Peu patient, risque d'escalade si la réponse est trop vague."
        ),
        role="client",
        tone=["direct", "persuasif"],
        traits=[
            PersonaTrait(trait_id="t-exigence", name="exigence", weight=1.2),
            PersonaTrait(trait_id="t-impatience", name="impatience", weight=1.0),
            PersonaTrait(trait_id="t-frustration", name="frustration", weight=0.9),
        ],
        communication=PersonaCommunication(
            style="directif",
            verbosity="high",
            language="fr",
        ),
        metadata=PersonaMetadata(
            difficulty="intermediate",
            tags=["sav", "facturation", "client", "g1"],
            author="callibr-seed",
        ),
    ),
]


# ---------------------------------------------------------------------------
# Procedure catalogue
# ---------------------------------------------------------------------------

_PROCEDURES: list[ProcedureDefinition] = [
    ProcedureDefinition(
        procedure_id="proc-sav-retard-colis-001",
        name="SAV — Traitement retard colis",
        version="1.0.0",
        description="Checklist obligatoire pour l'agent SAV traitant un retard de livraison.",
        steps=[
            StepDefinition(
                step_id="s-accueil",
                title="Accueil empathique",
                type="greeting",
                description="Saluer le client et reconnaître sa gêne.",
                expected_actions=["saluer_client", "exprimer_empathie"],
                order=1,
            ),
            StepDefinition(
                step_id="s-identite",
                title="Vérification identité",
                type="verification",
                description="Demander et valider le numéro de commande.",
                expected_actions=["demander_numero_commande", "verification_identite"],
                order=2,
            ),
            StepDefinition(
                step_id="s-suivi",
                title="Consultation suivi colis",
                type="discovery",
                description="Interroger le transporteur et communiquer l'état.",
                expected_actions=["consultation_suivi_colis"],
                order=3,
            ),
            StepDefinition(
                step_id="s-solution",
                title="Proposition de solution",
                type="solution",
                description="Proposer un nouveau délai ou un réenvoi.",
                expected_actions=["proposer_solution", "creation_ticket_transporteur"],
                order=4,
            ),
            StepDefinition(
                step_id="s-cloture",
                title="Récapitulatif et clôture",
                type="closing",
                description="Résumer les actions et envoyer la confirmation au client.",
                expected_actions=["notification_client", "recapituler_echanges"],
                order=5,
            ),
        ],
    ),
    ProcedureDefinition(
        procedure_id="proc-sav-erreur-facturation-001",
        name="SAV — Traitement erreur de facturation",
        version="1.0.0",
        description="Checklist pour l'agent SAV traitant une erreur de facturation.",
        steps=[
            StepDefinition(
                step_id="s-accueil",
                title="Accueil empathique",
                type="greeting",
                description="Saluer le client et reconnaître l'anomalie.",
                expected_actions=["saluer_client", "exprimer_empathie"],
                order=1,
            ),
            StepDefinition(
                step_id="s-identite",
                title="Vérification identité et facture",
                type="verification",
                description="Valider identité et numéro de facture.",
                expected_actions=["verification_identite", "demander_numero_facture"],
                order=2,
            ),
            StepDefinition(
                step_id="s-analyse",
                title="Analyse facturation",
                type="discovery",
                description="Analyser le montant facturé vs attendu.",
                expected_actions=["analyse_facture", "consultation_historique_paiement"],
                order=3,
            ),
            StepDefinition(
                step_id="s-correction",
                title="Correction et avoir",
                type="solution",
                description="Créer un avoir ou corriger la facture.",
                expected_actions=["creation_avoir", "correction_facturation"],
                order=4,
            ),
            StepDefinition(
                step_id="s-cloture",
                title="Confirmation client",
                type="closing",
                description="Confirmer la correction et envoyer la nouvelle facture.",
                expected_actions=["notification_client", "envoi_facture_corrigee"],
                order=5,
            ),
        ],
    ),
]


# ---------------------------------------------------------------------------
# Rule catalogue
# ---------------------------------------------------------------------------

_RULES: list[RuleDefinition] = [
    RuleDefinition(
        rule_id="rule-identity-required",
        name="Vérification identité obligatoire",
        description=(
            "Bloque toute action sensible (ticket, notification) si l'identité "
            "du client n'a pas été vérifiée au préalable."
        ),
        priority=10,
        enabled=True,
        status="active",
        conditions=[
            RuleCondition(
                condition_id="c-identity-not-verified",
                type="equals",
                field="identity_verified",
                value=False,
                label="Identité non vérifiée",
            )
        ],
        actions=[
            RuleAction(
                action_id="a-block-sensitive",
                type="block_transition",
                target="sensitive_action",
                label="Bloquer action sensible",
            )
        ],
        metadata=RuleMetadata(
            tags=["sav", "security", "identity"],
            category="security",
            author="callibr-seed",
        ),
    ),
    RuleDefinition(
        rule_id="rule-escalation-after-two-fails",
        name="Escalade après deux échecs de solution",
        description="Déclenche un événement d'escalade si deux solutions ont été proposées sans résolution.",
        priority=20,
        enabled=True,
        status="active",
        conditions=[
            RuleCondition(
                condition_id="c-failed-solutions",
                type="greater_than",
                field="failed_solution_count",
                value=1,
                label="Plus d'un échec de solution",
            )
        ],
        actions=[
            RuleAction(
                action_id="a-emit-escalation",
                type="emit_event",
                target="escalation.required",
                label="Émettre événement escalade",
            )
        ],
        metadata=RuleMetadata(
            tags=["sav", "escalation"],
            category="workflow",
            author="callibr-seed",
        ),
    ),
]


# ---------------------------------------------------------------------------
# Scenario Engine catalogue
# ---------------------------------------------------------------------------

_SCENARIOS: list[ScenarioDefinition] = [
    ScenarioDefinition(
        scenario_id="sc-sav-retard-colis-v1",
        name="SAV — Colis en retard (Conversation Runtime)",
        version="1.0.0",
        status="active",
        reference=ScenarioReference(
            procedure_id="proc-sav-retard-colis-001",
            persona_id="persona-sav-client-frustre-001",
            rule_ids=["rule-identity-required", "rule-escalation-after-two-fails"],
            crm_context_key="sav-retard",
        ),
        objectives=[
            ScenarioObjective(
                objective_id="obj-resolution",
                label="Résoudre le problème de retard",
                description="Le client obtient une date de livraison ou un réenvoi.",
                success_criteria=["ticket_transporteur_cree", "client_notifie"],
            ),
            ScenarioObjective(
                objective_id="obj-satisfaction",
                label="Maintenir la satisfaction client",
                description="Le client quitte l'échange rassuré.",
                success_criteria=["empathie_exprimee", "solution_proposee"],
            ),
        ],
        metadata=ScenarioMetadata(
            difficulty="beginner",
            estimated_minutes=8,
            tags=["sav", "retard", "g1", "conversation"],
            author="callibr-seed",
            description="Scénario conversation complète pour le Conversation Runtime.",
        ),
    ),
    ScenarioDefinition(
        scenario_id="sc-sav-erreur-facturation-v1",
        name="SAV — Erreur de facturation (Conversation Runtime)",
        version="1.0.0",
        status="active",
        reference=ScenarioReference(
            procedure_id="proc-sav-erreur-facturation-001",
            persona_id="persona-sav-client-exigeant-001",
            rule_ids=["rule-identity-required"],
            crm_context_key="sav-facturation",
        ),
        objectives=[
            ScenarioObjective(
                objective_id="obj-correction",
                label="Corriger la facturation",
                description="La facture erronée est corrigée et un avoir est émis.",
                success_criteria=["avoir_cree", "facture_corrigee_envoyee"],
            ),
        ],
        metadata=ScenarioMetadata(
            difficulty="intermediate",
            estimated_minutes=10,
            tags=["sav", "facturation", "g1", "conversation"],
            author="callibr-seed",
            description="Scénario conversation pour erreur de facturation — persona exigeant.",
        ),
    ),
]


# ---------------------------------------------------------------------------
# G2-COMMERCIAL catalogue
# ---------------------------------------------------------------------------

_PERSONAS_COM: list[PersonaDefinition] = [
    PersonaDefinition(
        persona_id="persona-com-client-inquiet-001",
        name="Client Commercial — Inquiet",
        description="Nouveau client rencontrant un problème de paiement en ligne. Besoin d'être rassuré et guidé.",
        role="client",
        tone=["neutre", "empathique"],
        traits=[
            PersonaTrait(trait_id="t-anxiete", name="anxiété", weight=0.8),
            PersonaTrait(trait_id="t-cooperation", name="coopération", weight=0.9),
            PersonaTrait(trait_id="t-impatience", name="impatience", weight=0.4),
        ],
        communication=PersonaCommunication(style="informel", verbosity="medium", language="fr"),
        memory_profile=PersonaMemoryProfile(short_term=True, long_term=False, max_history_turns=6, summary_after_turns=20),
        metadata=PersonaMetadata(difficulty="beginner", tags=["commercial", "paiement", "g2"], author="callibr-seed"),
    ),
    PersonaDefinition(
        persona_id="persona-com-client-retracteur-001",
        name="Client Commercial — Rétracteur",
        description="Client régulier qui souhaite annuler une commande. Ouvert à la discussion si une alternative intéressante est proposée.",
        role="client",
        tone=["direct", "empathique"],
        traits=[
            PersonaTrait(trait_id="t-assertivite", name="assertivité", weight=0.7),
            PersonaTrait(trait_id="t-collaboration", name="collaboration", weight=0.8),
            PersonaTrait(trait_id="t-satisfaction", name="satisfaction", weight=0.6),
        ],
        communication=PersonaCommunication(style="directif", verbosity="medium", language="fr"),
        memory_profile=PersonaMemoryProfile(short_term=True, long_term=False, max_history_turns=6, summary_after_turns=20),
        metadata=PersonaMetadata(difficulty="intermediate", tags=["commercial", "annulation", "g2"], author="callibr-seed"),
    ),
]

_PROCEDURES_COM: list[ProcedureDefinition] = [
    ProcedureDefinition(
        procedure_id="proc-com-refus-paiement-001",
        name="Commercial — Traitement refus de paiement",
        version="1.0.0",
        description="Checklist pour l'agent commercial traitant un refus de paiement en ligne.",
        steps=[
            StepDefinition(step_id="s-accueil", title="Accueil rassurant", type="greeting", description="Rassurer le client sur son panier.", expected_actions=["saluer_client", "rassurer_panier"], order=1),
            StepDefinition(step_id="s-identite", title="Vérification commande", type="verification", description="Valider l'identité et le numéro de commande.", expected_actions=["verification_identite", "consulter_panier"], order=2),
            StepDefinition(step_id="s-diagnostic", title="Diagnostic paiement", type="discovery", description="Comprendre la raison du refus.", expected_actions=["analyser_echec_paiement"], order=3),
            StepDefinition(step_id="s-solution", title="Proposition alternative", type="solution", description="Proposer un autre moyen de paiement.", expected_actions=["proposer_moyen_alternatif", "securiser_panier"], order=4),
            StepDefinition(step_id="s-cloture", title="Confirmation et suivi", type="closing", description="Confirmer la solution et le suivi.", expected_actions=["confirmer_solution", "envoyer_recapitulatif"], order=5),
        ],
    ),
    ProcedureDefinition(
        procedure_id="proc-com-annulation-commande-001",
        name="Commercial — Traitement annulation commande",
        version="1.0.0",
        description="Checklist pour l'agent commercial traitant une demande d'annulation.",
        steps=[
            StepDefinition(step_id="s-accueil", title="Accueil et compréhension", type="greeting", description="Comprendre le motif d'annulation.", expected_actions=["saluer_client", "comprendre_motif"], order=1),
            StepDefinition(step_id="s-identite", title="Vérification commande", type="verification", description="Valider la commande concernée.", expected_actions=["verification_identite", "consulter_commande"], order=2),
            StepDefinition(step_id="s-retention", title="Tentative de rétention", type="solution", description="Proposer une alternative pour conserver le client.", expected_actions=["proposer_remise", "proposer_alternative"], order=3),
            StepDefinition(step_id="s-annulation", title="Annulation si confirmée", type="custom", description="Finaliser l'annulation si le client insiste.", expected_actions=["annuler_commande", "confirmer_annulation"], order=4),
            StepDefinition(step_id="s-cloture", title="Récapitulatif", type="closing", description="Résumer les actions effectuées.", expected_actions=["recapituler", "envoyer_confirmation"], order=5),
        ],
    ),
]

# ---------------------------------------------------------------------------
# G3-SUPPORT-TECH catalogue
# ---------------------------------------------------------------------------

_PERSONAS_TECH: list[PersonaDefinition] = [
    PersonaDefinition(
        persona_id="persona-tech-client-stresse-001",
        name="Client Support — Stressé",
        description="Client bloqué sur son espace client, stressé car pressé par le temps.",
        role="client",
        tone=["neutre", "direct"],
        traits=[
            PersonaTrait(trait_id="t-anxiete", name="anxiété", weight=0.8),
            PersonaTrait(trait_id="t-impatience", name="impatience", weight=0.7),
            PersonaTrait(trait_id="t-patience", name="patience", weight=0.3),
        ],
        communication=PersonaCommunication(style="directif", verbosity="low", language="fr"),
        memory_profile=PersonaMemoryProfile(short_term=True, long_term=False, max_history_turns=6, summary_after_turns=20),
        metadata=PersonaMetadata(difficulty="beginner", tags=["support", "connexion", "g3"], author="callibr-seed"),
    ),
    PersonaDefinition(
        persona_id="persona-tech-client-urgent-001",
        name="Client Support — Urgent et en colère",
        description="Client professionnel impacté par une interruption de service, exigeant une résolution immédiate.",
        role="client",
        tone=["direct", "persuasif"],
        traits=[
            PersonaTrait(trait_id="t-frustration", name="frustration", weight=1.0),
            PersonaTrait(trait_id="t-exigence", name="exigence", weight=1.1),
            PersonaTrait(trait_id="t-impatience", name="impatience", weight=0.9),
        ],
        communication=PersonaCommunication(style="directif", verbosity="high", language="fr"),
        memory_profile=PersonaMemoryProfile(short_term=True, long_term=False, max_history_turns=6, summary_after_turns=20),
        metadata=PersonaMetadata(difficulty="intermediate", tags=["support", "incident", "g3"], author="callibr-seed"),
    ),
]

_PROCEDURES_TECH: list[ProcedureDefinition] = [
    ProcedureDefinition(
        procedure_id="proc-sup-login-impossible-001",
        name="Support — Dépannage connexion portail",
        version="1.0.0",
        description="Checklist pour diagnostiquer et résoudre un problème de connexion.",
        steps=[
            StepDefinition(step_id="s-accueil", title="Accueil et calme", type="greeting", description="Rassurer le client.", expected_actions=["saluer_client", "exprimer_comprehension"], order=1),
            StepDefinition(step_id="s-identite", title="Identification client", type="verification", description="Confirmer l'identité.", expected_actions=["verification_identite"], order=2),
            StepDefinition(step_id="s-diagnostic", title="Diagnostic accès", type="discovery", description="Vérifier les causes possibles.", expected_actions=["verifier_statut_compte", "verifier_email"], order=3),
            StepDefinition(step_id="s-solution", title="Réinitialisation", type="solution", description="Proposer réinitialisation et contournement.", expected_actions=["reinitialiser_mot_de_passe", "solution_contournement"], order=4),
            StepDefinition(step_id="s-cloture", title="Validation et suivi", type="closing", description="Confirmer le rétablissement.", expected_actions=["confirmer_acces", "recapituler_etapes", "creation_ticket_si_besoin"], order=5),
        ],
    ),
    ProcedureDefinition(
        procedure_id="proc-sup-incident-reseau-001",
        name="Support — Gestion incident réseau",
        version="1.0.0",
        description="Checklist pour gérer un incident réseau signalé par un client professionnel.",
        steps=[
            StepDefinition(step_id="s-accueil", title="Accueil sous pression", type="greeting", description="Accueillir le client en colère.", expected_actions=["saluer_client", "reconnaitre_impact"], order=1),
            StepDefinition(step_id="s-statut", title="Vérification incident", type="discovery", description="Vérifier l'état de l'incident.", expected_actions=["verifier_incident_connu", "consulter_statut_service"], order=2),
            StepDefinition(step_id="s-communication", title="Communication statut", type="solution", description="Informer le client clairement.", expected_actions=["communiquer_statut", "donner_delai_estime"], order=3),
            StepDefinition(step_id="s-escalade", title="Escalade si nécessaire", type="escalation", description="Escalader si besoin.", expected_actions=["escalade_technique", "compensation_proactive"], order=4),
            StepDefinition(step_id="s-cloture", title="Suivi et clôture", type="closing", description="Assurer le suivi.", expected_actions=["confirmer_suivi", "proposer_compensation", "recapituler"], order=5),
        ],
    ),
]

# ---------------------------------------------------------------------------
# G4-RECOUVREMENT catalogue
# ---------------------------------------------------------------------------

_PERSONAS_REC: list[PersonaDefinition] = [
    PersonaDefinition(
        persona_id="persona-rec-client-embarrasse-001",
        name="Client Recouvrement — Embarrassé",
        description="Client qui a reçu un rappel et est gêné par sa situation. Besoin de tact et de solutions.",
        role="client",
        tone=["formel", "neutre"],
        traits=[
            PersonaTrait(trait_id="t-anxiete", name="anxiété", weight=0.7),
            PersonaTrait(trait_id="t-cooperation", name="coopération", weight=0.8),
            PersonaTrait(trait_id="t-rigueur", name="rigueur", weight=0.5),
        ],
        communication=PersonaCommunication(style="consultatif", verbosity="medium", language="fr"),
        memory_profile=PersonaMemoryProfile(short_term=True, long_term=False, max_history_turns=6, summary_after_turns=20),
        metadata=PersonaMetadata(difficulty="beginner", tags=["recouvrement", "echeance", "g4"], author="callibr-seed"),
    ),
    PersonaDefinition(
        persona_id="persona-rec-client-vulnerable-001",
        name="Client Recouvrement — Vulnérable",
        description="Client en situation de fragilité financière qui demande un plan de remboursement. Honnête mais anxieux.",
        role="client",
        tone=["formel", "direct"],
        traits=[
            PersonaTrait(trait_id="t-anxiete", name="anxiété", weight=0.8),
            PersonaTrait(trait_id="t-cooperation", name="coopération", weight=1.0),
            PersonaTrait(trait_id="t-frustration", name="frustration", weight=0.5),
        ],
        communication=PersonaCommunication(style="consultatif", verbosity="medium", language="fr"),
        memory_profile=PersonaMemoryProfile(short_term=True, long_term=False, max_history_turns=8, summary_after_turns=20),
        metadata=PersonaMetadata(difficulty="intermediate", tags=["recouvrement", "plan", "g4"], author="callibr-seed"),
    ),
]

_PROCEDURES_REC: list[ProcedureDefinition] = [
    ProcedureDefinition(
        procedure_id="proc-rec-echeance-depassee-001",
        name="Recouvrement — Gestion échéance dépassée",
        version="1.0.0",
        description="Checklist pour gérer un client en retard de paiement.",
        steps=[
            StepDefinition(step_id="s-accueil", title="Accueil avec tact", type="greeting", description="Aborder le sujet avec tact.", expected_actions=["saluer_client", "introduire_sujet_avec_tact"], order=1),
            StepDefinition(step_id="s-identite", title="Vérification facture", type="verification", description="Valider la facture concernée.", expected_actions=["verification_identite", "consulter_facture"], order=2),
            StepDefinition(step_id="s-diagnostic", title="Compréhension situation", type="discovery", description="Comprendre la situation du client.", expected_actions=["ecouter_client", "comprendre_difficultes"], order=3),
            StepDefinition(step_id="s-solution", title="Proposition échelonnement", type="solution", description="Proposer un plan adapté.", expected_actions=["proposer_echelonnement", "definir_mensualites"], order=4),
            StepDefinition(step_id="s-cloture", title="Engagement et clôture", type="closing", description="Obtenir un engagement.", expected_actions=["obtenir_engagement", "envoyer_accord", "planifier_rappel"], order=5),
        ],
    ),
    ProcedureDefinition(
        procedure_id="proc-rec-plan-remboursement-001",
        name="Recouvrement — Mise en place plan de remboursement",
        version="1.0.0",
        description="Checklist pour mettre en place un plan de remboursement personnalisé.",
        steps=[
            StepDefinition(step_id="s-accueil", title="Accueil empathique", type="greeting", description="Recevoir la demande avec empathie.", expected_actions=["saluer_client", "reconnaitre_demarche"], order=1),
            StepDefinition(step_id="s-identite", title="Vérification dossier", type="verification", description="Consulter l'historique.", expected_actions=["verification_identite", "consulter_historique_paiements"], order=2),
            StepDefinition(step_id="s-evaluation", title="Évaluation capacité", type="discovery", description="Évaluer la capacité de remboursement.", expected_actions=["evaluer_capacite", "definir_montant_mensuel"], order=3),
            StepDefinition(step_id="s-negociation", title="Négociation échéancier", type="solution", description="Négocier un échéancier réaliste.", expected_actions=["negocier_echeancier", "valider_mensualites"], order=4),
            StepDefinition(step_id="s-cloture", title="Formalisation accord", type="closing", description="Formaliser et envoyer l'accord.", expected_actions=["formaliser_accord", "envoyer_convention", "planifier_prelevement"], order=5),
        ],
    ),
]


_SCENARIOS_COM: list[ScenarioDefinition] = [
    ScenarioDefinition(
        scenario_id="sc-com-refus-paiement-v1",
        name="Commercial — Paiement refusé (Conversation Runtime)",
        version="1.0.0", status="active",
        reference=ScenarioReference(procedure_id="proc-com-refus-paiement-001", persona_id="persona-com-client-inquiet-001", rule_ids=["rule-identity-required"], crm_context_key="com-paiement"),
        objectives=[ScenarioObjective(objective_id="obj-paiement", label="Finaliser le paiement", description="Le client parvient à payer par un autre moyen.", success_criteria=["paiement_effectue", "panier_securise"])],
        metadata=ScenarioMetadata(difficulty="beginner", estimated_minutes=8, tags=["commercial", "paiement", "g2", "conversation"], author="callibr-seed"),
    ),
    ScenarioDefinition(
        scenario_id="sc-com-annulation-commande-v1",
        name="Commercial — Annulation commande (Conversation Runtime)",
        version="1.0.0", status="active",
        reference=ScenarioReference(procedure_id="proc-com-annulation-commande-001", persona_id="persona-com-client-retracteur-001", rule_ids=["rule-identity-required"], crm_context_key="com-annulation"),
        objectives=[ScenarioObjective(objective_id="obj-retention", label="Fidéliser le client", description="Le client repart avec une offre ou une solution.", success_criteria=["client_fidelise", "commande_conservee_ou_annulee_proprement"])],
        metadata=ScenarioMetadata(difficulty="intermediate", estimated_minutes=10, tags=["commercial", "annulation", "g2", "conversation"], author="callibr-seed"),
    ),
]

_SCENARIOS_TECH: list[ScenarioDefinition] = [
    ScenarioDefinition(
        scenario_id="sc-sup-login-impossible-v1",
        name="Support — Connexion impossible (Conversation Runtime)",
        version="1.0.0", status="active",
        reference=ScenarioReference(procedure_id="proc-sup-login-impossible-001", persona_id="persona-tech-client-stresse-001", rule_ids=["rule-identity-required"], crm_context_key="sup-login"),
        objectives=[ScenarioObjective(objective_id="obj-acces", label="Rétablir l'accès", description="Le client peut se reconnecter.", success_criteria=["mot_de_passe_reinitialise", "client_reconnecte"])],
        metadata=ScenarioMetadata(difficulty="beginner", estimated_minutes=8, tags=["support", "connexion", "g3", "conversation"], author="callibr-seed"),
    ),
    ScenarioDefinition(
        scenario_id="sc-sup-incident-reseau-v1",
        name="Support — Incident réseau (Conversation Runtime)",
        version="1.0.0", status="active",
        reference=ScenarioReference(procedure_id="proc-sup-incident-reseau-001", persona_id="persona-tech-client-urgent-001", rule_ids=["rule-identity-required", "rule-escalation-after-two-fails"], crm_context_key="sup-incident"),
        objectives=[ScenarioObjective(objective_id="obj-communication", label="Communiquer et rassurer", description="Le client est informé et rassuré.", success_criteria=["statut_communique", "client_rassure", "escalade_si_besoin"])],
        metadata=ScenarioMetadata(difficulty="intermediate", estimated_minutes=10, tags=["support", "incident", "g3", "conversation"], author="callibr-seed"),
    ),
]

_SCENARIOS_REC: list[ScenarioDefinition] = [
    ScenarioDefinition(
        scenario_id="sc-rec-echeance-depassee-v1",
        name="Recouvrement — Échéance dépassée (Conversation Runtime)",
        version="1.0.0", status="active",
        reference=ScenarioReference(procedure_id="proc-rec-echeance-depassee-001", persona_id="persona-rec-client-embarrasse-001", rule_ids=["rule-identity-required"], crm_context_key="rec-echeance"),
        objectives=[ScenarioObjective(objective_id="obj-plan", label="Mettre en place un plan", description="Un plan d'apurement est accepté.", success_criteria=["echelonnement_propose", "accord_client_obtenu"])],
        metadata=ScenarioMetadata(difficulty="beginner", estimated_minutes=8, tags=["recouvrement", "echeance", "g4", "conversation"], author="callibr-seed"),
    ),
    ScenarioDefinition(
        scenario_id="sc-rec-plan-remboursement-v1",
        name="Recouvrement — Plan de remboursement (Conversation Runtime)",
        version="1.0.0", status="active",
        reference=ScenarioReference(procedure_id="proc-rec-plan-remboursement-001", persona_id="persona-rec-client-vulnerable-001", rule_ids=["rule-identity-required"], crm_context_key="rec-plan"),
        objectives=[ScenarioObjective(objective_id="obj-accord", label="Formaliser l'accord", description="Un plan de remboursement est signé.", success_criteria=["plan_remboursement_valide", "convention_envoyee"])],
        metadata=ScenarioMetadata(difficulty="intermediate", estimated_minutes=10, tags=["recouvrement", "plan", "g4", "conversation"], author="callibr-seed"),
    ),
]


# ---------------------------------------------------------------------------
# Extend main catalogues with pack-specific content
# ---------------------------------------------------------------------------

_PERSONAS.extend(_PERSONAS_COM)
_PERSONAS.extend(_PERSONAS_TECH)
_PERSONAS.extend(_PERSONAS_REC)
_PROCEDURES.extend(_PROCEDURES_COM)
_PROCEDURES.extend(_PROCEDURES_TECH)
_PROCEDURES.extend(_PROCEDURES_REC)
_SCENARIOS.extend(_SCENARIOS_COM)
_SCENARIOS.extend(_SCENARIOS_TECH)
_SCENARIOS.extend(_SCENARIOS_REC)

# ---------------------------------------------------------------------------
# Loader
# ---------------------------------------------------------------------------


def load_demo_catalogue(
    persona_service: PersonaService,
    procedure_service: ProcedureService,
    rule_service: RuleService,
    scenario_service: ScenarioService,
) -> None:
    """Seed all reference data into the in-memory stores.

    Idempotent: already-defined entities are silently skipped.
    """
    _seed_personas(persona_service)
    _seed_procedures(procedure_service)
    _seed_rules(rule_service)
    _seed_scenarios(scenario_service)
    log.info(
        "callibr_seed: demo catalogue loaded — %d personas, %d procedures, %d rules, %d scenarios",
        len(_PERSONAS),
        len(_PROCEDURES),
        len(_RULES),
        len(_SCENARIOS),
    )


def _seed_personas(service: PersonaService) -> None:
    for definition in _PERSONAS:
        try:
            service.define(definition)
            log.debug("seed: persona '%s' registered", definition.persona_id)
        except CallibrError as exc:
            if exc.code == "INVALID_PERSONA":
                log.warning("seed: persona '%s' skipped — %s", definition.persona_id, exc.message)
            else:
                raise


def _seed_procedures(service: ProcedureService) -> None:
    for definition in _PROCEDURES:
        try:
            service.define(definition)
            log.debug("seed: procedure '%s' registered", definition.procedure_id)
        except CallibrError as exc:
            if exc.code == "INVALID_PROCEDURE":
                log.warning(
                    "seed: procedure '%s' skipped — %s", definition.procedure_id, exc.message
                )
            else:
                raise


def _seed_rules(service: RuleService) -> None:
    for definition in _RULES:
        try:
            service.define(definition)
            log.debug("seed: rule '%s' registered", definition.rule_id)
        except CallibrError as exc:
            if exc.code in ("INVALID_RULE", "HANDLER_ALREADY_REGISTERED"):
                log.warning("seed: rule '%s' skipped — %s", definition.rule_id, exc.message)
            else:
                raise


def _seed_scenarios(service: ScenarioService) -> None:
    for definition in _SCENARIOS:
        try:
            service.define(definition)
            log.debug("seed: scenario '%s' registered", definition.scenario_id)
        except CallibrError as exc:
            if exc.code == "INVALID_SCENARIO":
                log.warning("seed: scenario '%s' skipped — %s", definition.scenario_id, exc.message)
            else:
                raise
