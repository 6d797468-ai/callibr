from callibr_contracts import RuleDefinition


class InMemoryRuleStore:
    def __init__(self) -> None:
        self._definitions: dict[str, RuleDefinition] = {}

    def save(self, definition: RuleDefinition) -> None:
        self._definitions[definition.rule_id] = definition

    def get(self, rule_id: str) -> RuleDefinition | None:
        return self._definitions.get(rule_id)

    def list(self) -> list[RuleDefinition]:
        return list(self._definitions.values())


class PostgresRuleStore:
    def __init__(self, database_url: str) -> None:
        from callibr_persistence.postgres import normalize_psycopg_url

        self._database_url = normalize_psycopg_url(database_url)

    def save(self, definition: RuleDefinition) -> None:
        from psycopg import connect
        from psycopg.types.json import Jsonb

        with connect(self._database_url) as connection:
            connection.execute(
                """
                INSERT INTO rules (rule_id, payload, updated_at)
                VALUES (%s, %s, now())
                ON CONFLICT (rule_id) DO UPDATE 
                SET payload = EXCLUDED.payload, updated_at = now();
                """,
                (
                    definition.rule_id,
                    Jsonb(definition.model_dump(mode="json")),
                ),
            )

    def get(self, rule_id: str) -> RuleDefinition | None:
        from psycopg import connect
        from psycopg.rows import dict_row

        with connect(self._database_url, row_factory=dict_row) as connection:
            row = connection.execute(
                "SELECT payload FROM rules WHERE rule_id = %s",
                (rule_id,),
            ).fetchone()

        if row:
            return RuleDefinition.model_validate(row["payload"])
        return None

    def list(self) -> list[RuleDefinition]:
        from psycopg import connect
        from psycopg.rows import dict_row

        with connect(self._database_url, row_factory=dict_row) as connection:
            rows = connection.execute("SELECT payload FROM rules ORDER BY rule_id").fetchall()

        return [RuleDefinition.model_validate(row["payload"]) for row in rows]
