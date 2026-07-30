"""Tests d'intégration — S15 Persistance PostgreSQL pour le Seed."""

from __future__ import annotations

from unittest.mock import MagicMock, patch

import pytest
from callibr_contracts import (
    PersonaDefinition,
    ProcedureDefinition,
    RuleDefinition,
    ScenarioDefinition,
)
from callibr_persistence.persona_store import PostgresPersonaDefinitionStore
from callibr_persistence.procedure_store import PostgresProcedureStore
from callibr_persistence.rule_store import PostgresRuleStore
from callibr_persistence.scenario_store import PostgresScenarioDefinitionStore


@pytest.fixture
def mock_db():
    with patch("psycopg.connect") as mock_connect:
        mock_conn = MagicMock()
        mock_connect.return_value.__enter__.return_value = mock_conn
        yield mock_conn


def test_postgres_persona_store_upsert(mock_db) -> None:
    store = PostgresPersonaDefinitionStore("postgres://dummy")

    # 1. Insert
    def1 = PersonaDefinition(persona_id="p1", name="Test Persona 1", role="Role", traits=[])
    store.save(def1)

    assert mock_db.execute.call_count == 1
    args, kwargs = mock_db.execute.call_args
    assert "INSERT INTO persona_definitions" in args[0]

    # 2. Get
    mock_db.execute.return_value.fetchone.return_value = {"payload": def1.model_dump(mode="json")}
    fetched = store.get("p1")
    assert fetched is not None
    assert fetched.name == "Test Persona 1"

    # 3. List
    mock_db.execute.return_value.fetchall.return_value = [{"payload": def1.model_dump(mode="json")}]
    lst = store.list()
    assert len(lst) == 1
    assert lst[0].persona_id == "p1"


def test_postgres_procedure_store_upsert(mock_db) -> None:
    store = PostgresProcedureStore("postgres://dummy")
    pdef = ProcedureDefinition(procedure_id="proc1", name="Proc 1 Name", title="Proc 1", steps=[])
    store.save_definition(pdef)

    assert mock_db.execute.call_count == 1

    mock_db.execute.return_value.fetchone.return_value = {"payload": pdef.model_dump(mode="json")}
    assert store.get_definition("proc1") is not None

    mock_db.execute.return_value.fetchall.return_value = [{"payload": pdef.model_dump(mode="json")}]
    assert len(store.list_definitions()) == 1


def test_postgres_rule_store_upsert(mock_db) -> None:
    store = PostgresRuleStore("postgres://dummy")
    rdef = RuleDefinition(rule_id="r1", name="Rule 1 Name", title="Rule 1", description="Desc")
    store.save(rdef)

    assert mock_db.execute.call_count == 1

    mock_db.execute.return_value.fetchone.return_value = {"payload": rdef.model_dump(mode="json")}
    assert store.get("r1") is not None

    mock_db.execute.return_value.fetchall.return_value = [{"payload": rdef.model_dump(mode="json")}]
    assert len(store.list()) == 1


def test_postgres_scenario_store_upsert(mock_db) -> None:
    store = PostgresScenarioDefinitionStore("postgres://dummy")

    from callibr_contracts import ScenarioReference

    ref = ScenarioReference(procedure_id="p1", persona_id="per1", initial_state={})

    sdef = ScenarioDefinition(
        scenario_id="s1",
        domain_pack="pack1",
        name="Name",
        title="Title",
        level="foundation",
        channel="chat",
        estimated_minutes=5,
        learning_goals=[],
        reference=ref,
    )

    store.save(sdef)
    assert mock_db.execute.call_count == 1

    mock_db.execute.return_value.fetchone.return_value = {"payload": sdef.model_dump(mode="json")}
    assert store.get("s1") is not None

    mock_db.execute.return_value.fetchall.return_value = [{"payload": sdef.model_dump(mode="json")}]
    assert len(store.list()) == 1
