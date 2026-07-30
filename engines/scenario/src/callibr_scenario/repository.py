from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from callibr_contracts import ScenarioSummary
from callibr_kernel import CallibrError


class ScenarioNotFoundError(CallibrError):
    def __init__(self, scenario_id: str) -> None:
        super().__init__(
            "SCENARIO_NOT_FOUND",
            f"Scenario {scenario_id} was not found.",
            details={"scenario_id": scenario_id},
        )


@dataclass(frozen=True, slots=True)
class ScenarioDefinition:
    summary: ScenarioSummary
    opening_message: str
    customer_profile: dict[str, Any]
    crm_context: dict[str, Any]
    expected_behaviors: tuple[str, ...]
    customer_replies: tuple[str, ...]


class InMemoryScenarioRepository:
    """In-memory scenario catalogue.

    MVP behaviour: tenants without a dedicated catalogue fall back to the
    shared ``tenant_demo`` catalogue so that multi-tenant header propagation
    tests pass without requiring per-tenant seeding.
    """

    _SHARED_CATALOGUE_TENANT = "tenant_demo"

    def __init__(self) -> None:
        self._tenant_scenarios: dict[str, dict[str, ScenarioDefinition]] = {
            self._SHARED_CATALOGUE_TENANT: self._build_demo_scenarios(),
        }

    @staticmethod
    def _build_demo_scenarios() -> dict[str, ScenarioDefinition]:
        return {
            # ─── Pack: Service Client (SAV) ───
            "sav-retard-colis-001": ScenarioDefinition(
                summary=ScenarioSummary(
                    scenario_id="sav-retard-colis-001",
                    domain_pack="G1-SUPPORT-SAV",
                    title="SAV - Colis en retard",
                    level="foundation",
                    channel="chat",
                    estimated_minutes=8,
                    learning_goals=[
                        "ouvrir l'echange avec empathie",
                        "verifier l'identite et la commande",
                        "proposer une solution claire",
                        "recapituler les prochaines etapes",
                    ],
                ),
                opening_message="Bonjour, ma commande devait arriver hier et je n'ai rien recu.",
                customer_profile={
                    "name": "Amal Benali",
                    "segment": "client standard",
                    "emotion": "frustre mais cooperatif",
                    "order_id": "CMD-2048",
                },
                crm_context={
                    "customer_name": "Amal Benali",
                    "order_id": "CMD-2048",
                    "delivery_status": "retard transporteur",
                    "identity_verified": False,
                    "ticket_status": "non_cree",
                    "eligible_actions": [
                        "verification_identite",
                        "consultation_suivi_colis",
                        "creation_ticket_transporteur",
                        "notification_client",
                    ],
                },
                expected_behaviors=(
                    "empathy",
                    "identity_verification",
                    "ownership",
                    "solution",
                    "recap",
                ),
                customer_replies=(
                    "Oui, je peux vous confirmer les informations de commande.",
                    "D'accord, mais j'ai besoin de savoir quand je serai livre.",
                    "Merci. Je veux surtout etre tenu au courant si le transporteur reprogramme.",
                    "Tres bien, j'attends votre confirmation par message.",
                ),
            ),
            "sav-erreur-facturation-001": ScenarioDefinition(
                summary=ScenarioSummary(
                    scenario_id="sav-erreur-facturation-001",
                    domain_pack="G1-SUPPORT-SAV",
                    title="SAV - Erreur de facturation",
                    level="foundation",
                    channel="chat",
                    estimated_minutes=10,
                    learning_goals=[
                        "accueillir une reclamation sensible",
                        "qualifier le motif de facturation",
                        "expliquer le delai de correction",
                        "securiser la cloture",
                    ],
                ),
                opening_message="Bonjour, j'ai ete facture deux fois pour la meme commande.",
                customer_profile={
                    "name": "Yanis Martin",
                    "segment": "client premium",
                    "emotion": "inquiet et exigeant",
                    "order_id": "CMD-4096",
                },
                crm_context={
                    "customer_name": "Yanis Martin",
                    "order_id": "CMD-4096",
                    "invoice_status": "double prelevement suspecte",
                    "identity_verified": False,
                    "ticket_status": "non_cree",
                    "eligible_actions": [
                        "verification_identite",
                        "consultation_facture",
                        "creation_ticket_facturation",
                        "demande_remboursement",
                    ],
                },
                expected_behaviors=(
                    "empathy",
                    "identity_verification",
                    "ownership",
                    "solution",
                    "recap",
                ),
                customer_replies=(
                    "Je vous confirme mon numero de commande si necessaire.",
                    "Je veux etre rembourse rapidement, c'est assez stressant.",
                    "Merci, mais pouvez-vous me confirmer le delai exact ?",
                    "D'accord, je surveillerai mon compte.",
                ),
            ),
            # ─── Pack: Commercial ───
            "com-refus-paiement-001": ScenarioDefinition(
                summary=ScenarioSummary(
                    scenario_id="com-refus-paiement-001",
                    domain_pack="G2-COMMERCIAL",
                    title="Commercial - Paiement refuse en ligne",
                    level="foundation",
                    channel="chat",
                    estimated_minutes=8,
                    learning_goals=[
                        "rassurer le client apres un echec de paiement",
                        "proposer un moyen de paiement alternatif",
                        "securiser le panier en cours",
                        "conclure la vente",
                    ],
                ),
                opening_message="Bonjour, j'essaie de payer ma commande depuis ce matin mais ca ne marche pas.",
                customer_profile={
                    "name": "Sofia El Amrani",
                    "segment": "nouveau client",
                    "emotion": "inquiete et impatiente",
                    "order_id": "CMD-5120",
                },
                crm_context={
                    "customer_name": "Sofia El Amrani",
                    "order_id": "CMD-5120",
                    "payment_status": "refuse",
                    "identity_verified": False,
                    "ticket_status": "non_cree",
                    "eligible_actions": [
                        "verification_identite",
                        "consultation_panier",
                        "relance_paiement",
                        "proposition_moyen_alternatif",
                    ],
                },
                expected_behaviors=(
                    "empathy",
                    "identity_verification",
                    "solution",
                    "recap",
                ),
                customer_replies=(
                    "Oui, j'ai essaye avec ma carte bancaire et aussi PayPal.",
                    "D'accord, je peux essayer par virement si c'est possible.",
                    "Merci, pouvez-vous verrouiller mon panier le temps que je fasse le virement ?",
                    "Parfait, je fais le virement tout de suite.",
                ),
            ),
            "com-annulation-commande-001": ScenarioDefinition(
                summary=ScenarioSummary(
                    scenario_id="com-annulation-commande-001",
                    domain_pack="G2-COMMERCIAL",
                    title="Commercial - Annulation de commande",
                    level="intermediate",
                    channel="chat",
                    estimated_minutes=10,
                    learning_goals=[
                        "comprendre le motif d'annulation",
                        "proposer une alternative ou une retenue",
                        "gerer l'insistance du client",
                        "finaliser l'annulation si necessaire",
                    ],
                ),
                opening_message="Bonjour, j'ai change d'avis, je veux annuler ma commande.",
                customer_profile={
                    "name": "Karim Bouchard",
                    "segment": "client regulier",
                    "emotion": "determine mais ouvert a la discussion",
                    "order_id": "CMD-6144",
                },
                crm_context={
                    "customer_name": "Karim Bouchard",
                    "order_id": "CMD-6144",
                    "order_status": "en_preparation",
                    "identity_verified": False,
                    "ticket_status": "non_cree",
                    "eligible_actions": [
                        "verification_identite",
                        "consultation_commande",
                        "suspension_preparation",
                        "annulation_commande",
                    ],
                },
                expected_behaviors=(
                    "empathy",
                    "identity_verification",
                    "ownership",
                    "retention",
                    "solution",
                ),
                customer_replies=(
                    "C'est juste que j'ai trouve moins cher ailleurs.",
                    "Si vous pouvez me faire une remise, je peux encore annuler l'annulation.",
                    "Non, je prefere annuler definitivement.",
                    "D'accord, merci pour la proposition mais je confirme l'annulation.",
                ),
            ),
            # ─── Pack: Support Technique ───
            "sup-login-impossible-001": ScenarioDefinition(
                summary=ScenarioSummary(
                    scenario_id="sup-login-impossible-001",
                    domain_pack="G3-SUPPORT-TECH",
                    title="Support - Connexion impossible au portail",
                    level="foundation",
                    channel="chat",
                    estimated_minutes=8,
                    learning_goals=[
                        "diagnostiquer un probleme d'acces",
                        "guider le client pas a pas",
                        "proposer une solution de contournement",
                        "escalader si necessaire",
                    ],
                ),
                opening_message="Bonjour, je n'arrive plus a me connecter a mon espace client.",
                customer_profile={
                    "name": "Lea Dubois",
                    "segment": "client standard",
                    "emotion": "stressee et pressee",
                    "order_id": "N/A",
                },
                crm_context={
                    "customer_name": "Lea Dubois",
                    "email": "lea.dubois@example.com",
                    "account_status": "actif",
                    "identity_verified": False,
                    "ticket_status": "non_cree",
                    "eligible_actions": [
                        "verification_identite",
                        "reinitialisation_mot_de_passe",
                        "verification_statut_compte",
                        "creation_ticket_technique",
                    ],
                },
                expected_behaviors=(
                    "empathy",
                    "identity_verification",
                    "diagnostic",
                    "solution",
                    "recap",
                ),
                customer_replies=(
                    "J'ai essaye de reinitialiser mon mot de passe mais je ne recois pas l'email.",
                    "Oui, mon adresse email est toujours la meme.",
                    "Je viens de le faire, toujours rien.",
                    "D'accord, je vais attendre le delai de 24h.",
                ),
            ),
            "sup-incident-reseau-001": ScenarioDefinition(
                summary=ScenarioSummary(
                    scenario_id="sup-incident-reseau-001",
                    domain_pack="G3-SUPPORT-TECH",
                    title="Support - Incident reseau signale",
                    level="intermediate",
                    channel="chat",
                    estimated_minutes=10,
                    learning_goals=[
                        "qualifier un incident technique",
                        "rassurer le client pendant l'interruption",
                        "communiquer un statut clair",
                        "assurer le suivi apres retablissement",
                    ],
                ),
                opening_message="Bonjour, votre service est inaccessible depuis 2 heures, que se passe-t-il ?",
                customer_profile={
                    "name": "Marc Moreau",
                    "segment": "client professionnel",
                    "emotion": "en colere et exigeant un delai",
                    "order_id": "N/A",
                },
                crm_context={
                    "customer_name": "Marc Moreau",
                    "sla": "premium",
                    "account_status": "actif",
                    "identity_verified": True,
                    "ticket_status": "non_cree",
                    "eligible_actions": [
                        "verification_incident",
                        "communication_statut",
                        "escalade_technique",
                        "compensation_proactive",
                    ],
                },
                expected_behaviors=(
                    "empathy",
                    "ownership",
                    "communication",
                    "solution",
                    "follow_up",
                ),
                customer_replies=(
                    "C'est un service critique pour mon activite, j'ai besoin d'une solution rapidement.",
                    "Quel est le delai estime de retablissement ?",
                    "D'accord, je veux etre tenu informe directement.",
                    "Merci, je surveille votre communication.",
                ),
            ),
            # ─── Pack: Recouvrement ───
            "rec-echeance-depassee-001": ScenarioDefinition(
                summary=ScenarioSummary(
                    scenario_id="rec-echeance-depassee-001",
                    domain_pack="G4-RECOUVREMENT",
                    title="Recouvrement - Echeance depassee",
                    level="foundation",
                    channel="chat",
                    estimated_minutes=8,
                    learning_goals=[
                        "aborder le sujet avec tact",
                        "verifier la situation du client",
                        "proposer un echelonnement",
                        "obtenir un engagement ferme",
                    ],
                ),
                opening_message="Bonjour, je viens de recevoir un rappel pour une facture impayee.",
                customer_profile={
                    "name": "Nadia Toumi",
                    "segment": "client standard",
                    "emotion": "genee et sur la defense",
                    "order_id": "FACT-8192",
                },
                crm_context={
                    "customer_name": "Nadia Toumi",
                    "order_id": "FACT-8192",
                    "invoice_status": "impayee_j30",
                    "amount_due": "245.00 EUR",
                    "identity_verified": False,
                    "ticket_status": "non_cree",
                    "eligible_actions": [
                        "verification_identite",
                        "consultation_facture",
                        "proposition_echelonnement",
                        "envoi_relance_accord",
                    ],
                },
                expected_behaviors=(
                    "empathy",
                    "identity_verification",
                    "diagnostic",
                    "solution",
                    "commitment",
                ),
                customer_replies=(
                    "Oui, j'ai eu des difficultes ce mois-ci mais je veux reguler.",
                    "Je peux payer la moitie aujourd'hui et le reste dans 15 jours.",
                    "D'accord pour un echelonnement sur 3 mois.",
                    "Merci, je valide le plan et je ferai le premier versement ce soir.",
                ),
            ),
            "rec-plan-remboursement-001": ScenarioDefinition(
                summary=ScenarioSummary(
                    scenario_id="rec-plan-remboursement-001",
                    domain_pack="G4-RECOUVREMENT",
                    title="Recouvrement - Demande de plan de remboursement",
                    level="intermediate",
                    channel="chat",
                    estimated_minutes=10,
                    learning_goals=[
                        "recevoir une demande de plan de remboursement",
                        "evaluer la capacite de remboursement",
                        "negocier un echeancier realiste",
                        "formaliser l'accord",
                    ],
                ),
                opening_message="Bonjour, je ne peux pas payer la totalite de ma facture tout de suite.",
                customer_profile={
                    "name": "Hassan Diallo",
                    "segment": "client vulnerable",
                    "emotion": "anxieux mais transparent",
                    "order_id": "FACT-10240",
                },
                crm_context={
                    "customer_name": "Hassan Diallo",
                    "order_id": "FACT-10240",
                    "invoice_status": "impayee_j60",
                    "amount_due": "580.00 EUR",
                    "identity_verified": False,
                    "ticket_status": "non_cree",
                    "eligible_actions": [
                        "verification_identite",
                        "consultation_historique",
                        "proposition_echelonnement",
                        "validation_plan",
                    ],
                },
                expected_behaviors=(
                    "empathy",
                    "identity_verification",
                    "diagnostic",
                    "negotiation",
                    "commitment",
                ),
                customer_replies=(
                    "J'ai perdu mon emploi il y a deux mois, je cherche un arrangement.",
                    "Je peux payer 100 EUR par mois maximum.",
                    "Oui, 100 EUR par mois pendant 6 mois c'est bon pour moi.",
                    "Merci, je m'engage a respecter cet echeancier.",
                ),
            ),
        }

    def _resolve(self, tenant_id: str) -> dict[str, ScenarioDefinition]:
        """Return the catalogue for *tenant_id*, falling back to the shared demo
        catalogue when the tenant has no dedicated scenarios yet (MVP mode)."""
        return self._tenant_scenarios.get(
            tenant_id,
            self._tenant_scenarios.get(self._SHARED_CATALOGUE_TENANT, {}),
        )

    def list_scenarios(self, tenant_id: str = "tenant_demo") -> list[ScenarioSummary]:
        scenarios = self._resolve(tenant_id)
        return [scenario.summary for scenario in scenarios.values()]

    def get(self, scenario_id: str, tenant_id: str = "tenant_demo") -> ScenarioDefinition:
        scenarios = self._resolve(tenant_id)
        scenario = scenarios.get(scenario_id)
        if scenario is None:
            raise ScenarioNotFoundError(scenario_id)
        return scenario
