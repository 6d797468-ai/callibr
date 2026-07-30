from callibr_contracts import ScenarioDefinition


class InMemoryScenarioDefinitionStore:
    def __init__(self) -> None:
        self._definitions: dict[str, ScenarioDefinition] = {}

    def save(self, definition: ScenarioDefinition) -> None:
        self._definitions[definition.scenario_id] = definition

    def get(self, scenario_id: str) -> ScenarioDefinition | None:
        return self._definitions.get(scenario_id)

    def list(self) -> list[ScenarioDefinition]:
        return list(self._definitions.values())


class PostgresScenarioDefinitionStore:
    def __init__(self, database_url: str) -> None:
        from callibr_persistence.postgres import normalize_psycopg_url

        self._database_url = normalize_psycopg_url(database_url)

    def save(self, definition: ScenarioDefinition) -> None:
        from psycopg import connect
        from psycopg.types.json import Jsonb

        with connect(self._database_url) as connection:
            connection.execute(
                """
                INSERT INTO scenario_definitions (scenario_id, payload, updated_at)
                VALUES (%s, %s, now())
                ON CONFLICT (scenario_id) DO UPDATE 
                SET payload = EXCLUDED.payload, updated_at = now();
                """,
                (
                    definition.scenario_id,
                    Jsonb(definition.model_dump(mode="json")),
                ),
            )

    def get(self, scenario_id: str) -> ScenarioDefinition | None:
        from psycopg import connect
        from psycopg.rows import dict_row

        with connect(self._database_url, row_factory=dict_row) as connection:
            row = connection.execute(
                "SELECT payload FROM scenario_definitions WHERE scenario_id = %s",
                (scenario_id,),
            ).fetchone()

        if row:
            return ScenarioDefinition.model_validate(row["payload"])
        return None

    def list(self) -> list[ScenarioDefinition]:
        from psycopg import connect
        from psycopg.rows import dict_row

        with connect(self._database_url, row_factory=dict_row) as connection:
            rows = connection.execute(
                "SELECT payload FROM scenario_definitions ORDER BY scenario_id"
            ).fetchall()

        return [ScenarioDefinition.model_validate(row["payload"]) for row in rows]
