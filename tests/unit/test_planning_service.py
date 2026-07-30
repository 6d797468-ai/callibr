from __future__ import annotations

from callibr_planning import (
    CommunicationGoal,
    CommunicationIntent,
    PlanningContext,
    ResponsePlanner,
    ResponseTone,
)


def _make_context(
    stage: str = "opening",
    learner_message: str = "",
    score: int = 50,
    emotion: str = "neutral",
    turn_count: int = 1,
) -> PlanningContext:
    return PlanningContext(
        scenario_id="sav-retard-colis-001",
        persona_id="persona_sav_01",
        procedure_id="proc_sav_01",
        procedure_step_id="step_opening_01",
        current_stage=stage,
        learner_message=learner_message,
        last_customer_message="Bonjour, je vous remercie de m'avoir contacté.",
        evaluation_score=score,
        turn_count=turn_count,
        detected_emotion=emotion,
    )


def test_opening_greeting_produces_acknowledge_intent() -> None:
    planner = ResponsePlanner()
    context = _make_context(learner_message="Bonjour, je vous appelle au sujet de ma commande.")
    plan = planner.plan(context)
    assert plan.intent == CommunicationIntent.acknowledge
    assert CommunicationGoal.reassure in plan.goals
    assert plan.tone == ResponseTone.warm


def test_opening_no_greeting_probes_for_details() -> None:
    planner = ResponsePlanner()
    context = _make_context(learner_message="Je veux parler de mon compte.")
    plan = planner.plan(context)
    assert plan.intent == CommunicationIntent.probe_for_details
    assert CommunicationGoal.gather_info in plan.goals


def test_discovery_low_score_probes() -> None:
    planner = ResponsePlanner()
    context = _make_context(stage="discovery", score=30)
    plan = planner.plan(context)
    assert plan.intent == CommunicationIntent.probe_for_details
    assert plan.tone == ResponseTone.calm


def test_discovery_mid_score_confirms() -> None:
    planner = ResponsePlanner()
    context = _make_context(stage="discovery", score=55)
    plan = planner.plan(context)
    assert plan.intent == CommunicationIntent.confirm_understanding
    assert plan.tone == ResponseTone.neutral


def test_discovery_high_score_acknowledges() -> None:
    planner = ResponsePlanner()
    context = _make_context(stage="discovery", score=85)
    plan = planner.plan(context)
    assert plan.intent == CommunicationIntent.acknowledge
    assert plan.tone == ResponseTone.warm


def test_handling_normal_proposes_solution() -> None:
    planner = ResponsePlanner()
    context = _make_context(stage="handling", score=60)
    plan = planner.plan(context)
    assert plan.intent == CommunicationIntent.propose_solution
    assert plan.tone == ResponseTone.professional


def test_handling_angry_emotion_de_escalates() -> None:
    planner = ResponsePlanner()
    context = _make_context(stage="handling", score=40, emotion="angry")
    plan = planner.plan(context)
    assert plan.intent == CommunicationIntent.de_escalate
    assert plan.tone == ResponseTone.empathetic


def test_handling_frustrated_emotion_de_escalates() -> None:
    planner = ResponsePlanner()
    context = _make_context(stage="handling", score=40, emotion="frustrated")
    plan = planner.plan(context)
    assert plan.intent == CommunicationIntent.de_escalate
    assert ResponseTone.empathetic in [plan.tone]


def test_objection_handles_objection() -> None:
    planner = ResponsePlanner()
    context = _make_context(stage="objection", score=50)
    plan = planner.plan(context)
    assert plan.intent == CommunicationIntent.handle_objection
    assert CommunicationGoal.challenge in plan.goals
    assert plan.tone == ResponseTone.firm


def test_closing_warm_and_conclusive() -> None:
    planner = ResponsePlanner()
    context = _make_context(stage="closing", score=80)
    plan = planner.plan(context)
    assert plan.intent == CommunicationIntent.close_conversation
    assert CommunicationGoal.conclude in plan.goals
    assert plan.tone == ResponseTone.warm


def test_evaluation_praises_and_concludes() -> None:
    planner = ResponsePlanner()
    context = _make_context(stage="evaluation", score=90)
    plan = planner.plan(context)
    assert plan.intent == CommunicationIntent.summarize
    assert CommunicationGoal.praise in plan.goals
    assert plan.constraints.max_sentences == 4


def test_fallback_redirects() -> None:
    planner = ResponsePlanner()
    context = _make_context(stage="unknown_stage")
    plan = planner.plan(context)
    assert plan.intent == CommunicationIntent.redirect
    assert CommunicationGoal.probe in plan.goals
    assert plan.tone == ResponseTone.neutral


def test_plan_always_has_procedure_step_id() -> None:
    planner = ResponsePlanner()
    context = _make_context(stage="closing")
    plan = planner.plan(context)
    assert plan.procedure_step_id == "step_opening_01"


def test_opening_constraints_empathetic() -> None:
    planner = ResponsePlanner()
    context = _make_context(learner_message="Bonjour!")
    plan = planner.plan(context)
    assert plan.constraints.empathetic is True
    assert plan.constraints.max_sentences == 2


def test_handling_constraints_max_3_sentences() -> None:
    planner = ResponsePlanner()
    context = _make_context(stage="handling")
    plan = planner.plan(context)
    assert plan.constraints.max_sentences == 3
