from callibr_contracts import PersonaDefinition


class InMemoryPersonaDefinitionStore:
    def __init__(self) -> None:
        self._definitions: dict[str, PersonaDefinition] = {}

    def save(self, definition: PersonaDefinition) -> None:
        self._definitions[definition.persona_id] = definition

    def get(self, persona_id: str) -> PersonaDefinition | None:
        return self._definitions.get(persona_id)

    def list(self) -> list[PersonaDefinition]:
        return list(self._definitions.values())


class PostgresPersonaDefinitionStore:
    def __init__(self, database_url: str) -> None:
        from callibr_persistence.postgres import normalize_psycopg_url

        self._database_url = normalize_psycopg_url(database_url)

    def save(self, definition: PersonaDefinition) -> None:
        from psycopg import connect
        from psycopg.types.json import Jsonb

        with connect(self._database_url) as connection:
            connection.execute(
                """
                INSERT INTO persona_definitions (persona_id, payload, updated_at)
                VALUES (%s, %s, now())
                ON CONFLICT (persona_id) DO UPDATE 
                SET payload = EXCLUDED.payload, updated_at = now();
                """,
                (
                    definition.persona_id,
                    Jsonb(definition.model_dump(mode="json")),
                ),
            )

    def get(self, persona_id: str) -> PersonaDefinition | None:
        from psycopg import connect
        from psycopg.rows import dict_row

        with connect(self._database_url, row_factory=dict_row) as connection:
            row = connection.execute(
                "SELECT payload FROM persona_definitions WHERE persona_id = %s",
                (persona_id,),
            ).fetchone()

        if row:
            return PersonaDefinition.model_validate(row["payload"])
        return None

    def list(self) -> list[PersonaDefinition]:
        from psycopg import connect
        from psycopg.rows import dict_row

        with connect(self._database_url, row_factory=dict_row) as connection:
            rows = connection.execute(
                "SELECT payload FROM persona_definitions ORDER BY persona_id"
            ).fetchall()

        return [PersonaDefinition.model_validate(row["payload"]) for row in rows]
