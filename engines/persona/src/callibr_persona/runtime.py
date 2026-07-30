from __future__ import annotations

from callibr_contracts import (
    PersonaDefinition,
    PersonaRuntime,
    PromptContext,
)
from callibr_kernel import utc_now


def build_runtime(definition: PersonaDefinition) -> PersonaRuntime:
    return PersonaRuntime(
        definition=definition,
        active_traits=list(definition.traits),
        active_objectives=list(definition.objectives),
        active_constraints=list(definition.constraints),
        memory_state={
            "short_term": definition.memory_profile.short_term,
            "long_term": definition.memory_profile.long_term,
            "max_history_turns": definition.memory_profile.max_history_turns,
            "summary_after_turns": definition.memory_profile.summary_after_turns,
        },
        built_at=utc_now().isoformat(),
    )


def build_prompt_context(
    persona_runtime: PersonaRuntime,
    crm_context: dict | None = None,
    scenario_context: dict | None = None,
    procedure_context: dict | None = None,
    evaluation_context: dict | None = None,
    extra: dict | None = None,
) -> PromptContext:
    d = persona_runtime.definition
    tone_str = ", ".join(d.tone) if d.tone else "neutre"
    traits_str = ", ".join(t.name for t in persona_runtime.active_traits)
    objectives_str = "; ".join(
        f"{o.label}: {o.description}" for o in persona_runtime.active_objectives
    )
    constraints_str = "; ".join(
        f"{c.label}: {c.description}" for c in persona_runtime.active_constraints
    )

    persona_prompt = (
        f"Tu es {d.name} ({d.role}).\n"
        f"Ton rôle : {d.description}\n"
        f"Ton ton : {tone_str}\n"
        f"Tes traits : {traits_str}\n"
        f"Objectifs : {objectives_str}\n"
        f"Contraintes : {constraints_str}\n"
        f"Style : {d.communication.style} ({d.communication.verbosity})"
    )

    rules_parts = ["Respecte le scénario en cours."]
    for c in persona_runtime.active_constraints:
        rules_parts.append(c.description)
    conversation_rules = "\n".join(rules_parts)

    return PromptContext(
        system_prompt=f"Tu es un assistant conversationnel spécialisé dans le rôle de {d.role}.",
        persona_prompt=persona_prompt,
        conversation_rules=conversation_rules,
        crm_context=crm_context or {},
        scenario_context=scenario_context or {},
        procedure_context=procedure_context or {},
        evaluation_context=evaluation_context or {},
        extra=extra or {},
    )
