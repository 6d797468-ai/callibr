from __future__ import annotations

import logging
import re

from callibr_contracts import ModelRequest, ModelResponse, SafetyResult

log = logging.getLogger(__name__)

PII_PATTERNS: list[re.Pattern[str]] = [
    re.compile(r"\b\d{3}-\d{2}-\d{4}\b"),
    re.compile(r"\b\d{16}\b"),
    re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b"),
]

ROLE_OVERRIDE_PATTERNS: list[re.Pattern[str]] = [
    re.compile(r"(?i)(ignore|override|disregard).*(system|instruction|constraint)"),
    re.compile(r"(?i)you are (not |no longer )?(a(n)? )?(assistant|ai|bot)"),
]

PROHIBITED_CONTENT: list[re.Pattern[str]] = [
    re.compile(r"(?i)(hate speech|racial slur|explicit violence)"),
]


class DeterministicSafetyValidator:
    def validate_input(self, request: ModelRequest) -> SafetyResult:
        for msg in request.messages:
            content = msg.get("content", "")
            if not content.strip():
                return SafetyResult(
                    is_safe=False,
                    reason="Empty message content is not allowed.",
                    flagged_categories=["empty_content"],
                )

            for pattern in PROHIBITED_CONTENT:
                if pattern.search(content):
                    return SafetyResult(
                        is_safe=False,
                        reason=f"Prohibited content detected: {pattern.pattern}",
                        flagged_categories=["prohibited_content"],
                    )

            for pattern in ROLE_OVERRIDE_PATTERNS:
                if pattern.search(content):
                    return SafetyResult(
                        is_safe=False,
                        reason="Role override attempt detected.",
                        flagged_categories=["role_override_attempt"],
                    )

        return SafetyResult(is_safe=True)

    def validate_output(self, response: ModelResponse) -> SafetyResult:
        content = response.content
        if not content.strip():
            return SafetyResult(
                is_safe=False,
                reason="Empty response content is not allowed.",
                flagged_categories=["empty_content"],
            )

        for pattern in PII_PATTERNS:
            if pattern.search(content):
                return SafetyResult(
                    is_safe=False,
                    reason="PII detected in output.",
                    flagged_categories=["pii_leak"],
                )

        for pattern in PROHIBITED_CONTENT:
            if pattern.search(content):
                return SafetyResult(
                    is_safe=False,
                    reason=f"Prohibited content detected in output: {pattern.pattern}",
                    flagged_categories=["prohibited_content"],
                )

        return SafetyResult(is_safe=True)
