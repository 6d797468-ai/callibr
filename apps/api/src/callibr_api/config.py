from __future__ import annotations

import logging
import os
import sys

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

log = logging.getLogger(__name__)


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="CALLIBR_", env_file=".env", extra="ignore")

    env: str = "local"
    service_name: str = "callibr-api"
    api_host: str = "0.0.0.0"
    api_port: int = 8000
    cors_origins: list[str] = Field(
        default_factory=lambda: ["http://localhost:5173", "http://127.0.0.1:5173"]
    )
    persistence_backend: str = Field(default="memory")
    database_url: str = "postgresql+psycopg://callibr:callibr@localhost:5432/callibr"
    redis_url: str = "redis://localhost:6379/0"
    demo_tenant_id: str = Field(default="tenant_demo")
    demo_user_email: str = Field(default="learner@demo.callibr.local")
    demo_user_password: str = Field(default="callibr-demo")
    auth_secret: str = Field(default="change-me-local-dev-secret")
    auth_token_ttl_seconds: int = Field(default=3600, ge=60)
    openai_api_key: str | None = Field(default=None)
    openai_model: str = Field(default="gpt-4o-mini")
    ai_runtime_budget_enabled: bool = Field(default=False)
    ai_runtime_safety_enabled: bool = Field(default=False)
    ai_runtime_reduction_enabled: bool = Field(default=False)
    ai_runtime_routing_enabled: bool = Field(default=False)

    # Voice (non-CALLIBR_ prefix — accessed via os.environ or injected)
    mock_stt: bool = Field(default=True)
    mock_tts: bool = Field(default=True)


def get_settings() -> Settings:
    return Settings()


# ── Configuration Validation ────────────────────────────────


class ConfigError(Exception):
    def __init__(self, message: str, variable: str = "") -> None:
        self.variable = variable
        super().__init__(message)


class MissingVariableError(ConfigError):
    ...


class ConfigValidator:
    """Validates environment configuration at startup.

    Checks required variables are set, detects placeholder/default values,
    and ensures provider consistency (e.g. mock vs. real voice keys).
    In local/demo mode, missing secrets are auto-generated.
    """

    _DEFAULT_CREDENTIALS = {
        "CALLIBR_AUTH_SECRET": [
            "change-me-local-dev-secret",
            "CLAUSEC_WcskJE32UpK6GcWIO5lUbT76EkeO2Rlu",
        ],
    }

    def validate(self, settings: Settings | None = None) -> list[ConfigError]:
        import base64
        import os

        errors: list[ConfigError] = []
        if settings is None:
            settings = get_settings()

        # ── auth_secret: auto-generate in local mode ──────────
        if settings.auth_secret in self._DEFAULT_CREDENTIALS.get("CALLIBR_AUTH_SECRET", []):
            if settings.env == "local":
                new_secret = base64.b64encode(os.urandom(32)).decode()
                settings.auth_secret = new_secret
                log.info("CALLIBR_AUTH_SECRET auto-généré pour l'environnement local")
            else:
                errors.append(
                    MissingVariableError(
                        "CALLIBR_AUTH_SECRET utilise une valeur par défaut ou compromise. "
                        "Génère-en une nouvelle avec : openssl rand -base64 32",
                        variable="CALLIBR_AUTH_SECRET",
                    )
                )

        # ── At least one LLM provider must be configured ────────
        llm_providers = [
            ("CALLIBR_OPENAI_API_KEY", settings.openai_api_key),
        ]
        for env_var in ("OPENROUTER_API_KEY",):
            val = os.environ.get(env_var)
            if val:
                llm_providers.append((env_var, val))

        has_llm = any(bool(key) for _, key in llm_providers)
        if not has_llm and settings.env != "local":
            errors.append(
                MissingVariableError(
                    "Aucun fournisseur LLM configuré. Définis au moins "
                    "CALLIBR_OPENAI_API_KEY ou OPENROUTER_API_KEY.",
                )
            )

        # ── Voice: if mock is disabled, real API keys are required ──
        if not settings.mock_stt and not os.environ.get("DEEPGRAM_API_KEY"):
            errors.append(
                MissingVariableError(
                    "CALLIBR_MOCK_STT=false mais DEEPGRAM_API_KEY n'est pas défini.",
                    variable="DEEPGRAM_API_KEY",
                )
            )

        if not settings.mock_tts and not os.environ.get("ELEVENLABS_API_KEY"):
            errors.append(
                MissingVariableError(
                    "CALLIBR_MOCK_TTS=false mais ELEVENLABS_API_KEY n'est pas défini.",
                    variable="ELEVENLABS_API_KEY",
                )
            )

        return errors

    def validate_or_exit(self, settings: Settings | None = None) -> None:
        errors = self.validate(settings)
        if not errors:
            count = len(vars(settings or get_settings()))
            log.info("Configuration validée — %d variable(s) OK", count)
            return

        print("=" * 70, file=sys.stderr)
        print("  CONFIGURATION INVALIDE", file=sys.stderr)
        print("=" * 70, file=sys.stderr)
        for err in errors:
            var = f"  [{err.variable}] " if err.variable else "  "
            print(f"{var}{err}", file=sys.stderr)
        print(file=sys.stderr)
        print("  Corrige les erreurs ci-dessus puis relance l'application.", file=sys.stderr)
        print("=" * 70, file=sys.stderr)
        sys.exit(1)
