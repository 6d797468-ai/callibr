from __future__ import annotations

from collections.abc import Iterable

from callibr_contracts import ModelRequest, TokenUsage


class DeterministicTokenCounter:
    def __init__(
        self,
        *,
        characters_per_token: int = 4,
        message_overhead: int = 4,
    ) -> None:
        if characters_per_token <= 0:
            raise ValueError("characters_per_token must be positive")
        if message_overhead < 0:
            raise ValueError("message_overhead cannot be negative")

        self._characters_per_token = characters_per_token
        self._message_overhead = message_overhead

    def count(self, request: ModelRequest) -> TokenUsage:
        system_tokens = self._count_text(request.system_prompt)
        conversation_tokens = self._count_text(request.system_context)
        context_tokens = self._count_messages(request.messages)

        return TokenUsage(
            system_tokens=system_tokens,
            conversation_tokens=conversation_tokens,
            context_tokens=context_tokens,
            total_input_tokens=(
                system_tokens
                + conversation_tokens
                + context_tokens
            ),
        )

    def _count_text(self, value: str | None) -> int:
        if not value:
            return 0

        normalized = value.strip()
        if not normalized:
            return 0

        length = len(normalized)
        return max(
            1,
            (length + self._characters_per_token - 1)
            // self._characters_per_token,
        )

    def _count_messages(self, messages: Iterable[object]) -> int:
        total = 0

        for message in messages:
            if isinstance(message, dict):
                role = message.get("role", "")
                content = message.get("content", "")
            else:
                role = getattr(message, "role", "")
                content = getattr(message, "content", "")

            total += self._message_overhead
            total += self._count_text(str(role))
            total += self._count_text(str(content))

        return total
