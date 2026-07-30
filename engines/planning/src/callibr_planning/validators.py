from __future__ import annotations

import re
from typing import Any

from pydantic import BaseModel, Field

from callibr_planning.models import (
    CommunicationIntent,
    ResponsePlan,
    ResponseTone,
)


class ValidationViolation(BaseModel):
    code: str
    message: str
    severity: str = "error"  # error | warning
    details: dict[str, Any] = Field(default_factory=dict)


class ValidationResult(BaseModel):
    valid: bool
    score: float  # 0.0 - 1.0
    violations: list[ValidationViolation] = Field(default_factory=list)
    regenerate: bool = False

    def merge(self, other: ValidationResult) -> ValidationResult:
        all_violations = self.violations + other.violations
        valid = self.valid and other.valid
        score = min(self.score, other.score)
        regenerate = self.regenerate or other.regenerate
        return ValidationResult(
            valid=valid,
            score=score,
            violations=all_violations,
            regenerate=regenerate,
        )


# French language detection — common French words (3+ chars to avoid EN/FR ambiguity)
_FRENCH_MARKERS: list[str] = [
    "les", "des", "ces", "mes", "tes", "ses", "nos", "vos",
    "elle", "avec", "pour", "sur", "sous", "chez", "entre",
    "bonjour", "merci", "monsieur", "madame",
    "commande", "numero", "client", "probleme",
    "compris", "daccord",
    "parce", "donc", "enfin", "voila",
    "egalement", "toujours", "jamais", "souvent",
]

# Tone-specific positive markers
_TONE_MARKERS: dict[ResponseTone, list[str]] = {
    ResponseTone.calm: [
        "compris", "entendu", "bien", "daccord", "je vois",
        "pas d'inquietude", "tranquillement", "pas de souci",
    ],
    ResponseTone.empathetic: [
        "comprends", "desole", "desolee", "navre", "navree",
        "je comprends", "je vois que", "j'imagine", "ca doit etre",
        "toute mon attention", "je suis la pour",
    ],
    ResponseTone.professional: [
        "confirmer", "verifier", "procedure", "prise en charge",
        "souhaitez-vous", "je vous propose", "solution",
    ],
    ResponseTone.warm: [
        "bonjour", "merci", "ravi", "ravie", "avec plaisir",
        "content", "contente", "super", "excellent",
    ],
    ResponseTone.firm: [
        "doit", "devons", "necessaire", "obligatoire",
        "je dois vous demander", "il est important",
    ],
    ResponseTone.urgent: [
        "immediatement", "urgence", "rapidement", "des que possible",
        "dans les plus brefs delais", "en priorite",
    ],
    ResponseTone.friendly: [
        "sans probleme", "bien sur", "pas de souci",
        "je vous en prie", "avec plaisir",
    ],
    ResponseTone.neutral: [],
}

# Intent-specific required patterns
_INTENT_PATTERNS: dict[CommunicationIntent, list[str]] = {
    CommunicationIntent.apologize: ["desol", "navr", "excuse", "regret"],
    CommunicationIntent.reassure_customer: ["rassur", "tranquill", "inquiet", "confiance"],
    CommunicationIntent.ask_for_info: ["?$", "pourriez", "pouvez", "avoir"],
    CommunicationIntent.propose_solution: ["propos", "solution", "pouvons", "suggestion"],
    CommunicationIntent.confirm_understanding: ["compris", "entendu", "bien", "recu", "merci"],
    CommunicationIntent.close_conversation: ["merci", "bonne journ", "a bientot", "ravi"],
    CommunicationIntent.de_escalate: ["rassur", "comprend", "desol", "solution", "calm"],
    CommunicationIntent.handle_objection: [
        "comprend", "cependant", "neanmoins", "voyons", "permet",
    ],
    CommunicationIntent.summarize: ["recapitul", "resum", "voici", "done", "donc"],
}


def _count_sentences(text: str) -> int:
    text = text.strip()
    if not text:
        return 0
    text = text.replace("\n", " ")
    text = re.sub(r"[.!?]+", ".", text)
    sentences = [s.strip() for s in text.split(".") if s.strip()]
    return len(sentences)


def _detect_language(text: str) -> str:
    words = set(re.findall(r"\b[a-zA-Z'-]+\b", text.lower()))
    if not words:
        return "unknown"
    matches = sum(1 for marker in _FRENCH_MARKERS if marker in words)
    ratio = matches / len(words)
    return "fr" if ratio >= 0.10 else "unknown"


def _check_sentence_count(
    text: str, min_sentences: int, max_sentences: int
) -> ValidationResult:
    count = _count_sentences(text)
    violations: list[ValidationViolation] = []
    if count < min_sentences:
        violations.append(
            ValidationViolation(
                code="min_sentences",
                message=f"Minimum {min_sentences} phrases requises, trouve {count}",
                severity="error",
                details={"expected": min_sentences, "actual": count},
            )
        )
    if count > max_sentences:
        violations.append(
            ValidationViolation(
                code="max_sentences",
                message=f"Maximum {max_sentences} phrases autorisees, trouve {count}",
                severity="error",
                details={"expected": max_sentences, "actual": count},
            )
        )
    valid = len(violations) == 0
    return ValidationResult(
        valid=valid,
        score=1.0 if valid else 0.3,
        violations=violations,
        regenerate=not valid,
    )


def _check_language(text: str, expected: str) -> ValidationResult:
    detected = _detect_language(text)
    if expected == "fr" and detected == "unknown":
        return ValidationResult(
            valid=False,
            score=0.4,
            violations=[
                ValidationViolation(
                    code="wrong_language",
                    message="Le texte ne semble pas etre en francais",
                    details={"expected": expected, "detected": detected},
                )
            ],
            regenerate=True,
        )
    return ValidationResult(valid=True, score=1.0)


def _check_forbidden_phrases(
    text: str, forbidden: list[str]
) -> ValidationResult:
    if not forbidden:
        return ValidationResult(valid=True, score=1.0)
    text_lower = text.lower()
    violations: list[ValidationViolation] = []
    for phrase in forbidden:
        if phrase.lower() in text_lower:
            violations.append(
                ValidationViolation(
                    code="forbidden_phrase",
                    message=f"Expression interdite detectee : '{phrase}'",
                    severity="error",
                    details={"phrase": phrase},
                )
            )
    valid = len(violations) == 0
    return ValidationResult(
        valid=valid,
        score=0.0 if violations else 1.0,
        violations=violations,
        regenerate=valid is False,
    )


def _check_required_phrases(
    text: str, required: list[str]
) -> ValidationResult:
    if not required:
        return ValidationResult(valid=True, score=1.0)
    text_lower = text.lower()
    violations: list[ValidationViolation] = []
    for phrase in required:
        if phrase.lower() not in text_lower:
            violations.append(
                ValidationViolation(
                    code="missing_required_phrase",
                    message=f"Expression requise manquante : '{phrase}'",
                    severity="warning",
                    details={"phrase": phrase},
                )
            )
    valid = len(violations) == 0
    return ValidationResult(
        valid=valid,
        score=0.6 if violations else 1.0,
        violations=violations,
        regenerate=False,
    )


def _check_tone(text: str, tone: ResponseTone) -> ValidationResult:
    markers = _TONE_MARKERS.get(tone, [])
    if not markers:
        return ValidationResult(valid=True, score=1.0)
    text_lower = text.lower()
    found = sum(1 for m in markers if m in text_lower)
    ratio = found / len(markers)
    if ratio < 0.15:
        return ValidationResult(
            valid=False,
            score=0.3,
            violations=[
                ValidationViolation(
                    code="wrong_tone",
                    message=f"Ton '{tone.value}' non respecte",
                    severity="warning",
                    details={
                        "expected_tone": tone.value,
                        "markers_found": found,
                        "markers_total": len(markers),
                    },
                )
            ],
            regenerate=False,
        )
    return ValidationResult(valid=True, score=1.0)


def _check_technical_terms(text: str, no_technical_terms: bool) -> ValidationResult:
    if not no_technical_terms:
        return ValidationResult(valid=True, score=1.0)
    technical_patterns = [
        r"\bAPI\b", r"\bJSON\b", r"\bREST\b", r"\bHTTP\b", r"\bSQL\b",
        r"\bDNS\b", r"\bIP\b", r"\bSSL\b", r"\bSSH\b", r"\bHTTPS\b",
        r"\bendpoint\b", r"\bpayload\b", r"\bwebhook\b", r"\bcache\b",
        r"\bCRUD\b", r"\bDAO\b", r"\bORM\b", r"\bDDL\b",
        r"\bauthentification\b", r"\bjwt\b", r"\boauth\b",
        r"\bcontainer\b", r"\bdocker\b",
        r"\bkubernetes\b", r"\bdeploiement continu\b",
    ]
    text_lower = text.lower()
    violations: list[ValidationViolation] = []
    for pattern in technical_patterns:
        compiled = re.compile(pattern)
        if compiled.search(text_lower):
            violations.append(
                ValidationViolation(
                    code="technical_term",
                    message=f"Terme technique detecte : {pattern}",
                    severity="warning",
                    details={"pattern": pattern},
                )
            )
    valid = len(violations) == 0
    return ValidationResult(
        valid=valid,
        score=0.5 if violations else 1.0,
        violations=violations,
        regenerate=False,
    )


def _check_empathetic(text: str, empathetic: bool) -> ValidationResult:
    if not empathetic:
        return ValidationResult(valid=True, score=1.0)
    text_lower = text.lower()
    empathy_markers = [
        "comprend", "desol", "navr", "excuse",
        "rassur", "j'imagine", "je vois",
        "frustrant", "genant", "inquiet",
    ]
    found = sum(1 for m in empathy_markers if m in text_lower)
    if found == 0:
        return ValidationResult(
            valid=False,
            score=0.3,
            violations=[
                ValidationViolation(
                    code="missing_empathy",
                    message="Reponse empathique attendue mais absente",
                    severity="error",
                    details={"markers_found": found},
                )
            ],
            regenerate=True,
        )
    return ValidationResult(valid=True, score=1.0)


def _check_intent(text: str, intent: CommunicationIntent) -> ValidationResult:
    patterns = _INTENT_PATTERNS.get(intent, [])
    if not patterns:
        return ValidationResult(valid=True, score=1.0)
    text_lower = text.lower()
    found = any(re.search(p, text_lower) for p in patterns)
    if not found:
        return ValidationResult(
            valid=False,
            score=0.4,
            violations=[
                ValidationViolation(
                    code="wrong_intent",
                    message=f"Intention '{intent.value}' non detectee dans la reponse",
                    severity="error",
                    details={"expected_intent": intent.value, "patterns": patterns},
                )
            ],
            regenerate=True,
        )
    return ValidationResult(valid=True, score=1.0)


def _check_hallucination(
    text: str, context_variables: dict[str, Any]
) -> ValidationResult:
    """Basic hallucination check: no specific numbers, dates, or names
    that don't appear in the context variables."""
    if not context_variables:
        return ValidationResult(valid=True, score=1.0)

    # Extract known values from context
    known_values: set[str] = set()
    for v in context_variables.values():
        if isinstance(v, str):
            known_values.add(v.lower())
        elif isinstance(v, (int, float)):
            known_values.add(str(v))

    # Check for specific patterns that could be hallucinated
    text_lower = text.lower()
    violations: list[ValidationViolation] = []

    # Check for unverified dates
    date_pattern = re.compile(r"\b\d{1,2}[/-]\d{1,2}[/-]\d{2,4}\b")
    for match in date_pattern.finditer(text_lower):
        date_val = match.group()
        if date_val not in known_values and date_val not in {
            "01/01/2024", "01/01/2025", "01/01/2026"
        }:
            violations.append(
                ValidationViolation(
                    code="unverified_date",
                    message=f"Date non verifiable dans le contexte : {date_val}",
                    severity="warning",
                    details={"value": date_val},
                )
            )

    # Check for unverified monetary amounts
    amount_pattern = re.compile(r"\b\d+[.,]?\d*\s*(€|euros|EUR)\b")
    for match in amount_pattern.finditer(text_lower):
        amount = match.group()
        if amount not in known_values:
            violations.append(
                ValidationViolation(
                    code="unverified_amount",
                    message=f"Montant non verifiable dans le contexte : {amount}",
                    severity="warning",
                    details={"value": amount},
                )
            )

    if violations:
        return ValidationResult(
            valid=False,
            score=0.7,
            violations=violations,
            regenerate=False,
        )
    return ValidationResult(valid=True, score=1.0)


class ResponseValidator:
    """Deterministic validator that checks LLM output against the ResponsePlan.

    Uses only rule-based checks — no LLM calls. Designed to be fast,
    explainable, and testable.
    """

    def validate(
        self,
        text: str,
        plan: ResponsePlan,
    ) -> ValidationResult:
        result = ValidationResult(valid=True, score=1.0)

        constraints = plan.constraints

        checks = [
            _check_sentence_count(text, constraints.min_sentences, constraints.max_sentences),
            _check_language(text, constraints.language),
            _check_forbidden_phrases(text, constraints.must_avoid),
            _check_required_phrases(text, constraints.must_include),
            _check_tone(text, plan.tone),
            _check_technical_terms(text, constraints.no_technical_terms),
            _check_empathetic(text, constraints.empathetic),
            _check_intent(text, plan.intent),
            _check_hallucination(text, plan.context_variables),
        ]

        for check in checks:
            result = result.merge(check)

        return result
