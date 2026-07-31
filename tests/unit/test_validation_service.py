from __future__ import annotations

from callibr_planning import (
    CommunicationGoal,
    CommunicationIntent,
    ResponseConstraint,
    ResponsePlan,
    ResponseTone,
    ResponseValidator,
    ValidationResult,
    ValidationViolation,
    VoiceStyle,
)


def _plan(
    intent: CommunicationIntent = CommunicationIntent.acknowledge,
    goals: list[CommunicationGoal] | None = None,
    tone: ResponseTone = ResponseTone.professional,
    max_sentences: int = 3,
    min_sentences: int = 1,
    language: str = "fr",
    must_avoid: list[str] | None = None,
    must_include: list[str] | None = None,
    no_technical_terms: bool = False,
    empathetic: bool = False,
) -> ResponsePlan:
    return ResponsePlan(
        intent=intent,
        goals=goals or [CommunicationGoal.confirm],
        tone=tone,
        voice=VoiceStyle.professional,
        expected_outcome="test",
        constraints=ResponseConstraint(
            max_sentences=max_sentences,
            min_sentences=min_sentences,
            language=language,
            no_technical_terms=no_technical_terms,
            empathetic=empathetic,
            must_avoid=must_avoid or [],
            must_include=must_include or [],
        ),
    )


class TestSentenceCount:
    def test_valid_sentence_count(self) -> None:
        validator = ResponseValidator()
        plan = _plan(max_sentences=3, min_sentences=1, tone=ResponseTone.neutral)
        result = validator.validate("Bonjour Monsieur. Comment puis-je vous aider ?", plan)
        assert result.valid
        assert result.score == 1.0

    def test_too_many_sentences(self) -> None:
        validator = ResponseValidator()
        plan = _plan(max_sentences=2, tone=ResponseTone.neutral)
        text = "Bonjour. Comment puis-je vous aider ?. Avez-vous votre numero de commande ?."
        result = validator.validate(text, plan)
        assert not result.valid
        assert any(v.code == "max_sentences" for v in result.violations)
        assert result.regenerate

    def test_too_few_sentences(self) -> None:
        validator = ResponseValidator()
        plan = _plan(min_sentences=2, max_sentences=3, tone=ResponseTone.neutral)
        result = validator.validate("Bonjour.", plan)
        assert not result.valid
        assert any(v.code == "min_sentences" for v in result.violations)

    def test_exact_sentence_count(self) -> None:
        validator = ResponseValidator()
        plan = _plan(min_sentences=2, max_sentences=2, tone=ResponseTone.neutral)
        result = validator.validate("Bonjour Monsieur. Comment puis-je vous aider ?", plan)
        assert result.valid


class TestLanguage:
    def test_detects_french(self) -> None:
        validator = ResponseValidator()
        plan = _plan(language="fr", tone=ResponseTone.neutral)
        result = validator.validate("Bonjour, je suis desole pour le probleme. Nous allons trouver une solution.", plan)
        assert result.valid

    def test_rejects_english(self) -> None:
        validator = ResponseValidator()
        plan = _plan(language="fr", tone=ResponseTone.neutral)
        result = validator.validate("Hello, I am sorry for the problem. We will find a solution.", plan)
        assert not result.valid
        assert any(v.code == "wrong_language" for v in result.violations)

    def test_empty_text_language(self) -> None:
        validator = ResponseValidator()
        plan = _plan(language="fr", tone=ResponseTone.neutral)
        result = validator.validate("", plan)
        assert not result.valid
        assert any(v.code == "wrong_language" for v in result.violations)


class TestForbiddenPhrases:
    def test_no_forbidden_phrases(self) -> None:
        validator = ResponseValidator()
        plan = _plan(must_avoid=["annulation", "remboursement"], tone=ResponseTone.neutral)
        result = validator.validate("Je vais verifier votre commande.", plan)
        assert result.valid

    def test_detects_forbidden_phrase(self) -> None:
        validator = ResponseValidator()
        plan = _plan(must_avoid=["annulation"], tone=ResponseTone.neutral)
        result = validator.validate("Je vais proceder a l'annulation.", plan)
        assert not result.valid
        assert any(v.code == "forbidden_phrase" for v in result.violations)

    def test_empty_forbidden_list(self) -> None:
        validator = ResponseValidator()
        plan = _plan(tone=ResponseTone.neutral)
        result = validator.validate("Je vais verifier votre commande Monsieur.", plan)
        assert result.valid


class TestRequiredPhrases:
    def test_contains_required_phrase(self) -> None:
        validator = ResponseValidator()
        plan = _plan(must_include=["commande"], tone=ResponseTone.neutral)
        result = validator.validate("Pouvez-vous me donner votre numero de commande ?", plan)
        assert result.valid

    def test_missing_required_phrase(self) -> None:
        validator = ResponseValidator()
        plan = _plan(must_include=["remboursement"], tone=ResponseTone.neutral)
        result = validator.validate("Je vais verifier votre compte.", plan)
        assert not result.valid
        assert any(v.code == "missing_required_phrase" for v in result.violations)


class TestTone:
    def test_detects_calm_tone(self) -> None:
        validator = ResponseValidator()
        plan = _plan(tone=ResponseTone.calm)
        result = validator.validate("J'ai bien compris votre situation. Pas d'inquietude, je vais m'en occuper Monsieur.", plan)
        assert result.valid

    def test_detects_empathetic_tone(self) -> None:
        validator = ResponseValidator()
        plan = _plan(tone=ResponseTone.empathetic)
        result = validator.validate("Je comprends votre mecontentement. Je suis desole pour ce desagrement Monsieur.", plan)
        assert result.valid

    def test_wrong_tone(self) -> None:
        validator = ResponseValidator()
        plan = _plan(tone=ResponseTone.warm)
        result = validator.validate("Le dossier doit etre complete selon la procedure et les regles Madame.", plan)
        assert not result.valid
        assert any(v.code == "wrong_tone" for v in result.violations)


class TestTechnicalTerms:
    def test_no_technical_terms_allowed(self) -> None:
        validator = ResponseValidator()
        plan = _plan(no_technical_terms=False, tone=ResponseTone.neutral)
        result = validator.validate("L'API renvoie une erreur 500. Contactez le support Monsieur.", plan)
        assert result.valid

    def test_detects_technical_term(self) -> None:
        validator = ResponseValidator()
        plan = _plan(no_technical_terms=True, tone=ResponseTone.neutral)
        result = validator.validate("Nous allons verifier le endpoint API. Je vous rappelle des que possible Monsieur.", plan)
        assert not result.valid
        assert any(v.code == "technical_term" for v in result.violations)


class TestEmpathetic:
    def test_empathetic_response(self) -> None:
        validator = ResponseValidator()
        plan = _plan(empathetic=True, tone=ResponseTone.neutral)
        result = validator.validate("Je comprends votre frustration. Je suis desole pour ce probleme.", plan)
        assert result.valid

    def test_missing_empathy(self) -> None:
        validator = ResponseValidator()
        plan = _plan(empathetic=True, tone=ResponseTone.neutral)
        result = validator.validate("Voici votre numero de commande. Bonne journee.", plan)
        assert not result.valid
        assert any(v.code == "missing_empathy" for v in result.violations)
        assert result.regenerate


class TestIntent:
    def test_apologize_intent(self) -> None:
        validator = ResponseValidator()
        plan = _plan(intent=CommunicationIntent.apologize, tone=ResponseTone.neutral)
        result = validator.validate("Je suis vraiment desole pour ce desagrement Madame.", plan)
        assert result.valid

    def test_wrong_intent(self) -> None:
        validator = ResponseValidator()
        plan = _plan(intent=CommunicationIntent.propose_solution, tone=ResponseTone.neutral)
        result = validator.validate("Bonjour Madame, comment allez-vous ?", plan)
        assert not result.valid
        assert any(v.code == "wrong_intent" for v in result.violations)
        assert result.regenerate


class TestHallucination:
    def test_no_hallucination(self) -> None:
        validator = ResponseValidator()
        plan = _plan(tone=ResponseTone.neutral)
        result = validator.validate("Je vais verifier votre dossier Madame.", plan)
        assert result.valid

    def test_unverified_date(self) -> None:
        validator = ResponseValidator()
        plan = ResponsePlan(
            intent=CommunicationIntent.acknowledge,
            goals=[CommunicationGoal.confirm],
            tone=ResponseTone.neutral,
            voice=VoiceStyle.neutral,
            constraints=ResponseConstraint(),
            expected_outcome="test",
            context_variables={"customer_name": "Dupont"},
        )
        result = validator.validate("Votre commande sera livree le 15/03/2027. Merci Monsieur.", plan)
        assert not result.valid
        assert any(v.code == "unverified_date" for v in result.violations)


class TestMerge:
    def test_merge_all_valid(self) -> None:
        v1 = _make_result(valid=True, score=1.0)
        v2 = _make_result(valid=True, score=1.0)
        merged = v1.merge(v2)
        assert merged.valid
        assert merged.score == 1.0
        assert len(merged.violations) == 0

    def test_merge_with_violations(self) -> None:
        from callibr_planning import ValidationResult
        v1 = ValidationResult(
            valid=True,
            score=1.0,
            violations=[
                ValidationViolation(code="a", message="A"),
            ],
        )
        v2 = ValidationResult(
            valid=False,
            score=0.3,
            regenerate=True,
            violations=[
                ValidationViolation(code="b", message="B"),
            ],
        )
        merged = v1.merge(v2)
        assert not merged.valid
        assert merged.score == 0.3
        assert len(merged.violations) == 2
        assert merged.regenerate


def _make_result(valid: bool, score: float) -> ValidationResult:
    return ValidationResult(valid=valid, score=score)
