from __future__ import annotations

from callibr_kernel import CallibrError

from callibr_director.models import (
    ConversationStage,
    DirectorCommand,
    DirectorContext,
    DirectorDecision,
)


class DirectorError(CallibrError):
    pass


# Stage transitions: minimum turns before moving to next stage
_STAGE_MIN_TURNS = {
    ConversationStage.opening: 1,
    ConversationStage.discovery: 2,
    ConversationStage.handling: 3,
    ConversationStage.objection: 1,
    ConversationStage.closing: 2,
    ConversationStage.evaluation: 1,
}


class ConversationDirector:
    """Orchestrates a full conversation session.

    The ConversationDirector owns the session flow:
    - Which stage the conversation is in
    - When to progress to the next stage
    - How to adapt difficulty based on learner performance
    - When to introduce objections or provide hints
    - When to end the session

    It operates independently of any LLM. The Response Planner then
    translates each DirectorDecision into a structured communication plan.
    """

    def decide(self, context: DirectorContext) -> DirectorDecision:
        if context.stage == ConversationStage.completed:
            return DirectorDecision(
                command=DirectorCommand.end_session,
                next_stage=ConversationStage.completed,
                reason="Session already completed",
                wait_for_learner=False,
            )

        stage_decider = {
            ConversationStage.opening: self._decide_opening,
            ConversationStage.discovery: self._decide_discovery,
            ConversationStage.handling: self._decide_handling,
            ConversationStage.objection: self._decide_objection,
            ConversationStage.closing: self._decide_closing,
            ConversationStage.evaluation: self._decide_evaluation,
        }

        decider = stage_decider.get(context.stage)
        if decider is None:
            return self._decide_fallback(context)

        return decider(context)

    def _min_turns_for_stage(self, stage: ConversationStage) -> int:
        return _STAGE_MIN_TURNS.get(stage, 1)

    def _should_advance(
        self, context: DirectorContext, stage: ConversationStage
    ) -> bool:
        return context.learner_message_count >= self._min_turns_for_stage(stage)

    def _next_stage(self, current: ConversationStage) -> ConversationStage:
        stages = list(ConversationStage)
        try:
            idx = stages.index(current)
            return stages[min(idx + 1, len(stages) - 1)]
        except ValueError:
            return ConversationStage.completed

    def _decide_opening(self, context: DirectorContext) -> DirectorDecision:
        if self._should_advance(context, ConversationStage.opening):
            return DirectorDecision(
                command=DirectorCommand.conclude_turn,
                next_stage=ConversationStage.discovery,
                reason="Opening complete, moving to discovery",
            )
        return DirectorDecision(
            command=DirectorCommand.ask_for_details,
            next_stage=ConversationStage.opening,
            reason="Gathering initial information",
        )

    def _decide_discovery(self, context: DirectorContext) -> DirectorDecision:
        score = context.current_score
        if score < 40 and context.learner_message_count >= 3:
            return DirectorDecision(
                command=DirectorCommand.provide_hint,
                next_stage=ConversationStage.discovery,
                reason="Learner struggling, providing hint",
                difficulty_delta=-1,
            )
        if self._should_advance(context, ConversationStage.discovery):
            next_stage = ConversationStage.handling
            cmd = DirectorCommand.conclude_turn
            if score >= 70:
                next_stage = ConversationStage.objection
                cmd = DirectorCommand.introduce_objection
            return DirectorDecision(
                command=cmd,
                next_stage=next_stage,
                reason=f"Discovery complete (score={score})",
                difficulty_delta=1 if score >= 70 else 0,
            )
        return DirectorDecision(
            command=DirectorCommand.ask_for_details,
            next_stage=ConversationStage.discovery,
            reason="Continuing discovery phase",
        )

    def _decide_handling(self, context: DirectorContext) -> DirectorDecision:
        if self._should_advance(context, ConversationStage.handling):
            if context.current_score >= 60:
                return DirectorDecision(
                    command=DirectorCommand.introduce_objection,
                    next_stage=ConversationStage.objection,
                    reason="Learner handling well, introducing objection",
                    difficulty_delta=1,
                )
            return DirectorDecision(
                command=DirectorCommand.conclude_turn,
                next_stage=ConversationStage.closing,
                reason="Handling phase complete",
            )
        if context.current_score < 40:
            return DirectorDecision(
                command=DirectorCommand.provide_hint,
                next_stage=ConversationStage.handling,
                reason="Learner needs support in handling phase",
                difficulty_delta=-1,
            )
        return DirectorDecision(
            command=DirectorCommand.speak,
            next_stage=ConversationStage.handling,
            reason="Continuing handling phase",
        )

    def _decide_objection(self, context: DirectorContext) -> DirectorDecision:
        if self._should_advance(context, ConversationStage.objection):
            return DirectorDecision(
                command=DirectorCommand.conclude_turn,
                next_stage=ConversationStage.closing,
                reason="Objection handled, moving to close",
            )
        return DirectorDecision(
            command=DirectorCommand.speak,
            next_stage=ConversationStage.objection,
            reason="Maintaining objection pressure",
        )

    def _decide_closing(self, context: DirectorContext) -> DirectorDecision:
        if self._should_advance(context, ConversationStage.closing):
            return DirectorDecision(
                command=DirectorCommand.congratulate,
                next_stage=ConversationStage.evaluation,
                reason="Session complete, entering evaluation",
                wait_for_learner=True,
            )
        return DirectorDecision(
            command=DirectorCommand.speak,
            next_stage=ConversationStage.closing,
            reason="Wrapping up conversation",
        )

    def _decide_evaluation(self, context: DirectorContext) -> DirectorDecision:
        return DirectorDecision(
            command=DirectorCommand.end_session,
            next_stage=ConversationStage.completed,
            reason="Evaluation complete, ending session",
            wait_for_learner=False,
        )

    def _decide_fallback(self, context: DirectorContext) -> DirectorDecision:
        return DirectorDecision(
            command=DirectorCommand.speak,
            next_stage=ConversationStage.handling,
            reason="Fallback: continuing conversation",
        )
