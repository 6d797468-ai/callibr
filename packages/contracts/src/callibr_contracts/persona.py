from __future__ import annotations

from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field

ToneStyle = Literal[
    "professionnel",
    "empathique",
    "structuré",
    "direct",
    "pédagogique",
    "formel",
    "informel",
    "enthousiaste",
    "neutre",
    "persuasif",
]
TraitName = Literal[
    # Traits agent
    "écoute",
    "curiosité",
    "pédagogie",
    "assertivité",
    "patience",
    "adaptabilité",
    "rigueur",
    "créativité",
    "leadership",
    "collaboration",
    # Traits client
    "frustration",
    "coopération",
    "exigence",
    "anxiété",
    "satisfaction",
    "impatience",
]
CommunicationStyle = Literal["consultatif", "directif", "collaboratif", "informel"]
VerbosityLevel = Literal["low", "medium", "high"]
SupportedLanguage = Literal["fr", "en", "de", "es", "it"]
Difficulty = Literal["beginner", "intermediate", "advanced", "expert"]


class PersonaMemoryProfile(BaseModel):
    model_config = ConfigDict(frozen=True)

    short_term: bool = True
    long_term: bool = False
    max_history_turns: int = Field(default=10, ge=1)
    summary_after_turns: int = Field(default=20, ge=1)


class PersonaConstraint(BaseModel):
    model_config = ConfigDict(frozen=True)

    constraint_id: str
    label: str
    description: str = ""


class PersonaObjective(BaseModel):
    model_config = ConfigDict(frozen=True)

    objective_id: str
    label: str
    description: str = ""
    priority: int = Field(default=1, ge=1)


class PersonaTrait(BaseModel):
    model_config = ConfigDict(frozen=True)

    trait_id: str
    name: TraitName
    weight: float = Field(default=1.0, ge=0.0, le=2.0)


class PersonaCommunication(BaseModel):
    model_config = ConfigDict(frozen=True)

    style: CommunicationStyle = "consultatif"
    verbosity: VerbosityLevel = "medium"
    language: SupportedLanguage = "fr"


class PersonaMetadata(BaseModel):
    model_config = ConfigDict(frozen=True)

    difficulty: Difficulty = "intermediate"
    tags: list[str] = Field(default_factory=list)
    author: str = ""
    description: str = ""


class PersonaDefinition(BaseModel):
    model_config = ConfigDict(frozen=True)

    persona_id: str
    version: str = "1.0.0"
    name: str
    description: str = ""
    role: str = ""
    tone: list[ToneStyle] = Field(default_factory=list)
    traits: list[PersonaTrait] = Field(default_factory=list)
    communication: PersonaCommunication = Field(default_factory=PersonaCommunication)
    objectives: list[PersonaObjective] = Field(default_factory=list)
    constraints: list[PersonaConstraint] = Field(default_factory=list)
    memory_profile: PersonaMemoryProfile = Field(default_factory=PersonaMemoryProfile)
    metadata: PersonaMetadata = Field(default_factory=PersonaMetadata)


class PersonaRuntime(BaseModel):
    model_config = ConfigDict(frozen=True)

    definition: PersonaDefinition
    active_traits: list[PersonaTrait] = Field(default_factory=list)
    active_objectives: list[PersonaObjective] = Field(default_factory=list)
    active_constraints: list[PersonaConstraint] = Field(default_factory=list)
    memory_state: dict[str, Any] = Field(default_factory=dict)
    built_at: str = ""


class ValidatePersonaResult(BaseModel):
    model_config = ConfigDict(frozen=True)

    valid: bool
    errors: list[str] = Field(default_factory=list)
    warnings: list[str] = Field(default_factory=list)


class PromptContext(BaseModel):
    model_config = ConfigDict(frozen=True)

    system_prompt: str = ""
    persona_prompt: str = ""
    conversation_rules: str = ""
    crm_context: dict[str, Any] = Field(default_factory=dict)
    scenario_context: dict[str, Any] = Field(default_factory=dict)
    procedure_context: dict[str, Any] = Field(default_factory=dict)
    evaluation_context: dict[str, Any] = Field(default_factory=dict)
    extra: dict[str, Any] = Field(default_factory=dict)
