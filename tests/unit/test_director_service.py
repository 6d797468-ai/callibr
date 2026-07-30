from __future__ import annotations

from callibr_director import (
    ConversationDirector,
    ConversationStage,
    DirectorCommand,
    DirectorContext,
)


def _make_context(
    stage: ConversationStage = ConversationStage.opening,
    learner_message_count: int = 0,
    score: int = 50,
    turn_count: int = 0,
) -> DirectorContext:
    return DirectorContext(
        session_id="sim_test_001",
        tenant_id="tenant_demo",
        scenario_id="sav-retard-colis-001",
        persona_id="persona_sav_01",
        stage=stage,
        turn_count=turn_count,
        learner_message_count=learner_message_count,
        current_score=score,
    )


def test_opening_asks_for_details_before_min_turns() -> None:
    director = ConversationDirector()
    context = _make_context(learner_message_count=0)
    decision = director.decide(context)
    assert decision.command == DirectorCommand.ask_for_details
    assert decision.next_stage == ConversationStage.opening


def test_opening_advances_to_discovery_after_min_turns() -> None:
    director = ConversationDirector()
    context = _make_context(learner_message_count=2)
    decision = director.decide(context)
    assert decision.command == DirectorCommand.conclude_turn
    assert decision.next_stage == ConversationStage.discovery


def test_discovery_provides_hint_when_struggling() -> None:
    director = ConversationDirector()
    context = _make_context(
        stage=ConversationStage.discovery,
        learner_message_count=3,
        score=30,
    )
    decision = director.decide(context)
    assert decision.command == DirectorCommand.provide_hint
    assert decision.difficulty_delta == -1


def test_discovery_advances_to_objection_when_high_score() -> None:
    director = ConversationDirector()
    context = _make_context(
        stage=ConversationStage.discovery,
        learner_message_count=3,
        score=75,
    )
    decision = director.decide(context)
    assert decision.next_stage == ConversationStage.objection
    assert decision.difficulty_delta == 1


def test_discovery_advances_to_handling_when_mid_score() -> None:
    director = ConversationDirector()
    context = _make_context(
        stage=ConversationStage.discovery,
        learner_message_count=3,
        score=55,
    )
    decision = director.decide(context)
    assert decision.next_stage == ConversationStage.handling
    assert decision.difficulty_delta == 0


def test_discovery_continues_before_min_turns() -> None:
    director = ConversationDirector()
    context = _make_context(
        stage=ConversationStage.discovery,
        learner_message_count=1,
    )
    decision = director.decide(context)
    assert decision.command == DirectorCommand.ask_for_details
    assert decision.next_stage == ConversationStage.discovery


def test_handling_advances_to_objection_when_high_score() -> None:
    director = ConversationDirector()
    context = _make_context(
        stage=ConversationStage.handling,
        learner_message_count=4,
        score=70,
    )
    decision = director.decide(context)
    assert decision.next_stage == ConversationStage.objection
    assert decision.command == DirectorCommand.introduce_objection
    assert decision.difficulty_delta == 1


def test_handling_advances_to_closing_when_low_score() -> None:
    director = ConversationDirector()
    context = _make_context(
        stage=ConversationStage.handling,
        learner_message_count=4,
        score=50,
    )
    decision = director.decide(context)
    assert decision.next_stage == ConversationStage.closing


def test_handling_provides_hint_when_struggling() -> None:
    director = ConversationDirector()
    context = _make_context(
        stage=ConversationStage.handling,
        learner_message_count=2,
        score=35,
    )
    decision = director.decide(context)
    assert decision.command == DirectorCommand.provide_hint
    assert decision.difficulty_delta == -1


def test_handling_continues_normally() -> None:
    director = ConversationDirector()
    context = _make_context(
        stage=ConversationStage.handling,
        learner_message_count=2,
        score=60,
    )
    decision = director.decide(context)
    assert decision.command == DirectorCommand.speak
    assert decision.next_stage == ConversationStage.handling


def test_objection_advances_to_closing() -> None:
    director = ConversationDirector()
    context = _make_context(
        stage=ConversationStage.objection,
        learner_message_count=2,
    )
    decision = director.decide(context)
    assert decision.next_stage == ConversationStage.closing
    assert decision.command == DirectorCommand.conclude_turn


def test_objection_continues_before_min_turns() -> None:
    director = ConversationDirector()
    context = _make_context(
        stage=ConversationStage.objection,
        learner_message_count=0,
    )
    decision = director.decide(context)
    assert decision.command == DirectorCommand.speak
    assert decision.next_stage == ConversationStage.objection


def test_closing_advances_to_evaluation() -> None:
    director = ConversationDirector()
    context = _make_context(
        stage=ConversationStage.closing,
        learner_message_count=3,
    )
    decision = director.decide(context)
    assert decision.next_stage == ConversationStage.evaluation
    assert decision.command == DirectorCommand.congratulate
    assert decision.wait_for_learner is True


def test_closing_continues_before_min_turns() -> None:
    director = ConversationDirector()
    context = _make_context(
        stage=ConversationStage.closing,
        learner_message_count=0,
    )
    decision = director.decide(context)
    assert decision.command == DirectorCommand.speak
    assert decision.next_stage == ConversationStage.closing


def test_evaluation_ends_session() -> None:
    director = ConversationDirector()
    context = _make_context(
        stage=ConversationStage.evaluation,
        learner_message_count=2,
    )
    decision = director.decide(context)
    assert decision.next_stage == ConversationStage.completed
    assert decision.command == DirectorCommand.end_session
    assert decision.wait_for_learner is False


def test_completed_stage_ends_session() -> None:
    director = ConversationDirector()
    context = _make_context(stage=ConversationStage.completed)
    decision = director.decide(context)
    assert decision.command == DirectorCommand.end_session
    assert decision.wait_for_learner is False


def test_fallback_stage_uses_handling() -> None:
    director = ConversationDirector()
    context = _make_context(stage=ConversationStage.opening)
    # bypass the normal decider dispatch to test _decide_fallback directly
    decision = director._decide_fallback(context)
    assert decision.command == DirectorCommand.speak
    assert decision.next_stage == ConversationStage.handling
