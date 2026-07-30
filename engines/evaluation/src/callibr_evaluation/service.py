from __future__ import annotations

import unicodedata
from dataclasses import dataclass
from datetime import datetime

from callibr_contracts import (
    AuditRecord,
    EvaluationCriterionResult,
    SessionReport,
    SimulationEvaluation,
    SimulationSession,
)
from callibr_kernel import utc_now
from callibr_scenario import ScenarioDefinition


@dataclass(frozen=True, slots=True)
class CriterionDefinition:
    criterion_id: str
    label: str
    needles: tuple[str, ...]
    passed_feedback: str
    missed_feedback: str
    next_best_action: str
    max_score: int = 20


class EvaluationService:
    def __init__(self) -> None:
        self._criteria = {
            "empathy": CriterionDefinition(
                criterion_id="empathy",
                label="Empathie et reconnaissance de la situation",
                needles=("desole", "navre", "comprends", "excuse", "regret"),
                passed_feedback="L'apprenant reconnait la gene client.",
                missed_feedback="L'empathie explicite est insuffisante.",
                next_best_action="Reformuler la gene client avec une phrase d'empathie courte.",
            ),
            "identity_verification": CriterionDefinition(
                criterion_id="identity_verification",
                label="Verification client",
                needles=("identite", "numero", "commande", "email", "nom"),
                passed_feedback="L'apprenant demande ou utilise un identifiant client.",
                missed_feedback="La verification client est absente.",
                next_best_action="Demander le numero de commande ou un identifiant client.",
            ),
            "ownership": CriterionDefinition(
                criterion_id="ownership",
                label="Prise en charge",
                needles=("je vais", "nous allons", "verifier", "prendre en charge", "regarder"),
                passed_feedback="L'apprenant annonce une prise en charge claire.",
                missed_feedback="La prise en charge reste trop floue.",
                next_best_action="Dire clairement quelle verification va etre faite.",
            ),
            "solution": CriterionDefinition(
                criterion_id="solution",
                label="Orientation solution",
                needles=(
                    "solution",
                    "remboursement",
                    "renvoi",
                    "livraison",
                    "delai",
                    "ticket",
                    "transporteur",
                ),
                passed_feedback="L'apprenant propose une action ou un delai concret.",
                missed_feedback="La solution ou le delai n'est pas assez precise.",
                next_best_action="Proposer l'action SAV adaptee et un delai concret.",
            ),
            "recap": CriterionDefinition(
                criterion_id="recap",
                label="Recapitulatif et prochaine etape",
                needles=("recap", "resume", "confirme", "prochaine etape", "suivi"),
                passed_feedback="L'apprenant securise la suite de l'echange.",
                missed_feedback="La prochaine etape n'est pas assez securisee.",
                next_best_action="Terminer par un recapitulatif et le canal de suivi.",
            ),
        }

    def evaluate_turn(
        self,
        content: str,
        scenario: ScenarioDefinition,
    ) -> SimulationEvaluation:
        normalized = self._normalize(content)
        criteria = [
            self._evaluate_criterion(self._criteria[behavior], normalized)
            for behavior in scenario.expected_behaviors
            if behavior in self._criteria
        ]
        max_score = sum(criterion.max_score for criterion in criteria) or 100
        raw_score = sum(criterion.score for criterion in criteria)
        score = min(100, round(raw_score * 100 / max_score))
        strengths = [criterion.feedback for criterion in criteria if criterion.status == "passed"]
        risks = [criterion.feedback for criterion in criteria if criterion.status == "missed"]
        next_best_actions = [
            self._criteria[criterion.criterion_id].next_best_action
            for criterion in criteria
            if criterion.status == "missed"
        ]
        return SimulationEvaluation(
            score=score,
            max_score=100,
            criteria=criteria,
            strengths=strengths,
            risks=risks[:3],
            next_best_actions=next_best_actions[:2],
        )

    def build_session_report(
        self,
        session: SimulationSession,
        audit_records: list[AuditRecord],
    ) -> SessionReport:
        generated_at = utc_now()
        completed_at = session.completed_at
        duration_end = completed_at or self._last_activity_at(session) or generated_at
        duration_seconds = max(0, int((duration_end - session.started_at).total_seconds()))
        evaluation = session.evaluation or SimulationEvaluation(score=0)
        return SessionReport(
            session_id=session.session_id,
            tenant_id=session.tenant_id,
            learner_id=session.learner_id,
            scenario=session.scenario,
            status=session.status,
            generated_at=generated_at,
            started_at=session.started_at,
            completed_at=completed_at,
            duration_seconds=duration_seconds,
            message_count=len(session.messages),
            learner_message_count=self._count_messages(session, "learner"),
            customer_message_count=self._count_messages(session, "customer"),
            crm_action_count=len(session.crm_actions),
            audit_event_count=len(audit_records),
            final_score=evaluation.score,
            max_score=evaluation.max_score,
            criteria=evaluation.criteria,
            strengths=evaluation.strengths,
            risks=evaluation.risks,
            next_best_actions=evaluation.next_best_actions,
            crm_actions=session.crm_actions,
        )

    def _evaluate_criterion(
        self,
        definition: CriterionDefinition,
        normalized_content: str,
    ) -> EvaluationCriterionResult:
        evidence = [needle for needle in definition.needles if needle in normalized_content]
        passed = bool(evidence)
        return EvaluationCriterionResult(
            criterion_id=definition.criterion_id,
            label=definition.label,
            status="passed" if passed else "missed",
            score=definition.max_score if passed else 0,
            max_score=definition.max_score,
            evidence=evidence,
            feedback=definition.passed_feedback if passed else definition.missed_feedback,
        )

    @staticmethod
    def _normalize(text: str) -> str:
        ascii_text = unicodedata.normalize("NFKD", text).encode("ascii", "ignore").decode()
        return ascii_text.lower()

    @staticmethod
    def _count_messages(session: SimulationSession, role: str) -> int:
        return sum(1 for message in session.messages if message.role == role)

    @staticmethod
    def _last_activity_at(session: SimulationSession) -> datetime | None:
        if not session.messages:
            return None
        return max(message.at for message in session.messages)
