from __future__ import annotations

from callibr_kernel import CallibrError

from callibr_planning.models import (
    CommunicationGoal,
    CommunicationIntent,
    PlanningContext,
    ResponseConstraint,
    ResponsePlan,
    ResponseTone,
    VoiceStyle,
)


class PlanningError(CallibrError):
    pass


class ResponsePlanner:
    """Produces a structured ResponsePlan from the current conversation context.

    The ResponsePlanner is fully deterministic — it applies rules based on
    the conversation stage, scenario context, and learner input. It does not
    call an LLM. The plan it produces is later verbalized by an LLM or a
    static renderer.

    This separation (planning → verbalization) allows:
    - Small models to produce high-quality replies (the decision is already made)
    - Full control over conversation flow
    - Testing planning logic independently of any LLM
    """

    def plan(self, context: PlanningContext) -> ResponsePlan:
        if context.current_stage == "opening":
            return self._plan_opening(context)
        elif context.current_stage == "discovery":
            return self._plan_discovery(context)
        elif context.current_stage == "handling":
            return self._plan_handling(context)
        elif context.current_stage == "objection":
            return self._plan_objection(context)
        elif context.current_stage == "closing":
            return self._plan_closing(context)
        elif context.current_stage == "evaluation":
            return self._plan_evaluation(context)
        else:
            return self._plan_fallback(context)

    def _plan_opening(self, context: PlanningContext) -> ResponsePlan:
        msg = context.learner_message.lower()
        if "bonjour" in msg or "bonsoir" in msg:
            intent = CommunicationIntent.acknowledge
            goals = [CommunicationGoal.reassure]
            tone = ResponseTone.warm
        else:
            intent = CommunicationIntent.probe_for_details
            goals = [CommunicationGoal.gather_info, CommunicationGoal.probe]
            tone = ResponseTone.professional

        return ResponsePlan(
            intent=intent,
            goals=goals,
            tone=tone,
            voice=VoiceStyle.warm,
            expected_outcome="learner provides initial context",
            constraints=ResponseConstraint(max_sentences=2, empathetic=True),
            procedure_step_id=context.procedure_step_id,
        )

    def _plan_discovery(self, context: PlanningContext) -> ResponsePlan:
        score = context.evaluation_score
        if score < 40:
            intent = CommunicationIntent.probe_for_details
            goals = [CommunicationGoal.probe, CommunicationGoal.gather_info]
            tone = ResponseTone.calm
        elif score < 70:
            intent = CommunicationIntent.confirm_understanding
            goals = [CommunicationGoal.confirm, CommunicationGoal.probe]
            tone = ResponseTone.neutral
        else:
            intent = CommunicationIntent.acknowledge
            goals = [CommunicationGoal.confirm]
            tone = ResponseTone.warm

        return ResponsePlan(
            intent=intent,
            goals=goals,
            tone=tone,
            voice=VoiceStyle.calm,
            expected_outcome="learner provides relevant case information",
            constraints=ResponseConstraint(max_sentences=2),
            procedure_step_id=context.procedure_step_id,
        )

    def _plan_handling(self, context: PlanningContext) -> ResponsePlan:
        intent = CommunicationIntent.propose_solution
        goals = [CommunicationGoal.propose, CommunicationGoal.explain]
        tone = ResponseTone.professional

        if context.detected_emotion in ("angry", "frustrated"):
            intent = CommunicationIntent.de_escalate
            goals = [CommunicationGoal.reassure, CommunicationGoal.apologize]
            tone = ResponseTone.empathetic

        return ResponsePlan(
            intent=intent,
            goals=goals,
            tone=tone,
            voice=VoiceStyle.professional,
            expected_outcome="learner applies correct procedure",
            constraints=ResponseConstraint(max_sentences=3),
            procedure_step_id=context.procedure_step_id,
        )

    def _plan_objection(self, context: PlanningContext) -> ResponsePlan:
        return ResponsePlan(
            intent=CommunicationIntent.handle_objection,
            goals=[CommunicationGoal.object, CommunicationGoal.challenge],
            tone=ResponseTone.firm,
            voice=VoiceStyle.calm,
            expected_outcome="learner handles objection professionally",
            constraints=ResponseConstraint(max_sentences=2),
            procedure_step_id=context.procedure_step_id,
        )

    def _plan_closing(self, context: PlanningContext) -> ResponsePlan:
        return ResponsePlan(
            intent=CommunicationIntent.close_conversation,
            goals=[CommunicationGoal.conclude, CommunicationGoal.confirm],
            tone=ResponseTone.warm,
            voice=VoiceStyle.warm,
            expected_outcome="conversation ends on a positive note",
            constraints=ResponseConstraint(max_sentences=3),
            procedure_step_id=context.procedure_step_id,
        )

    def _plan_evaluation(self, context: PlanningContext) -> ResponsePlan:
        return ResponsePlan(
            intent=CommunicationIntent.summarize,
            goals=[CommunicationGoal.praise, CommunicationGoal.conclude],
            tone=ResponseTone.warm,
            voice=VoiceStyle.warm,
            expected_outcome="learner receives coaching feedback",
            constraints=ResponseConstraint(max_sentences=4),
            procedure_step_id=context.procedure_step_id,
        )

    def _plan_fallback(self, context: PlanningContext) -> ResponsePlan:
        return ResponsePlan(
            intent=CommunicationIntent.redirect,
            goals=[CommunicationGoal.probe],
            tone=ResponseTone.neutral,
            voice=VoiceStyle.neutral,
            expected_outcome="conversation gets back on track",
            constraints=ResponseConstraint(max_sentences=2),
            procedure_step_id=context.procedure_step_id,
        )
