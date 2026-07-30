"""Conversation Runtime — Orchestrator.

Assembles all domain objects into a ConversationContext,
delegates generation to LLMAdapter, and returns the result.
"""

from __future__ import annotations

from typing import Any

from callibr_contracts import (
    ConversationContext,
    ConversationMetadata,
    ConversationState,
    ModelRequest,
    PromptContext,
    RuleEvaluation,
    ScenarioExecutionPlan,
)


class ContextBuilder:
    def build_system_context(
        self,
        plan: ScenarioExecutionPlan | None = None,
        prompt_ctx: PromptContext | None = None,
        rule_eval: RuleEvaluation | None = None,
    ) -> str:
        parts: list[str] = []
        if prompt_ctx and prompt_ctx.system_prompt:
            parts.append(prompt_ctx.system_prompt)
        if prompt_ctx and prompt_ctx.conversation_rules:
            parts.append("\nRègles:\n" + prompt_ctx.conversation_rules)
        if rule_eval and rule_eval.blocked:
            parts.append("\nAttention: Certaines actions sont bloquées par les règles.")
        if rule_eval and rule_eval.total_score_delta:
            score_info = f"Score actuel: {rule_eval.total_score_delta:.0f}"
            parts.append(score_info)
        return "\n".join(parts)

    def assemble_context(
        self,
        plan: ScenarioExecutionPlan | None = None,
        prompt_ctx: PromptContext | None = None,
        rule_eval: RuleEvaluation | None = None,
        crm_context: dict[str, Any] | None = None,
        state: ConversationState | None = None,
        metadata: ConversationMetadata | None = None,
    ) -> ConversationContext:
        return ConversationContext(
            system_context=self.build_system_context(plan, prompt_ctx, rule_eval),
            persona_context=prompt_ctx or PromptContext(),
            scenario_context=plan.execution_context if plan else {},
            procedure_context=plan.execution_context if plan else {},
            rule_context=rule_eval or RuleEvaluation(results=[]),
            crm_context=crm_context or {},
            memory_context={
                "turn_count": len(state.turns) if state else 0,
                "last_turn": state.turns[-1].content if state and state.turns else "",
            },
            metadata=metadata or ConversationMetadata(),
            conversation_state=state,
        )

    def build_model_request(
        self,
        ctx: ConversationContext,
        user_message: str,
    ) -> ModelRequest:
        messages: list[dict[str, str]] = []

        persona = ctx.persona_context
        if persona.persona_prompt:
            messages.append({"role": "system", "content": persona.persona_prompt})

        if ctx.system_context:
            system_block = ctx.system_context
            if persona.scenario_context:
                system_block += f"\n\nContexte scénario: {persona.scenario_context}"
            if ctx.crm_context:
                system_block += f"\n\nContexte CRM: {ctx.crm_context}"
            if ctx.plan_context:
                system_block += f"\n\n{ctx.plan_context}"
            messages.append({"role": "system", "content": system_block})

        conv_state = ctx.conversation_state
        if conv_state:
            for turn in conv_state.turns:
                messages.append({"role": turn.role, "content": turn.content})

        messages.append({"role": "user", "content": user_message})

        return ModelRequest(
            messages=messages,
            system_context=ctx.system_context,
            persona_context=persona.persona_prompt,
            scenario_context=str(ctx.scenario_context),
            procedure_context=str(ctx.procedure_context),
            rule_context=str(ctx.rule_context),
            crm_context=str(ctx.crm_context),
            memory_context=str(ctx.memory_context),
        )
