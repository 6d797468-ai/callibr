from callibr_contracts import ProcedureDefinition, ProcedureExecution


class InMemoryProcedureStore:
    def __init__(self) -> None:
        self._definitions: dict[str, ProcedureDefinition] = {}
        self._executions: dict[str, ProcedureExecution] = {}

    def save_definition(self, definition: ProcedureDefinition) -> None:
        self._definitions[definition.procedure_id] = definition

    def get_definition(self, procedure_id: str) -> ProcedureDefinition | None:
        return self._definitions.get(procedure_id)

    def list_definitions(self) -> list[ProcedureDefinition]:
        return list(self._definitions.values())

    def save_execution(self, execution: ProcedureExecution) -> None:
        self._executions[execution.execution_id] = execution

    def get_execution(self, execution_id: str) -> ProcedureExecution | None:
        return self._executions.get(execution_id)


class PostgresProcedureStore:
    def __init__(self, database_url: str) -> None:
        from callibr_persistence.postgres import normalize_psycopg_url

        self._database_url = normalize_psycopg_url(database_url)

    def save_definition(self, definition: ProcedureDefinition) -> None:
        from psycopg import connect
        from psycopg.types.json import Jsonb

        with connect(self._database_url) as connection:
            connection.execute(
                """
                INSERT INTO procedures (procedure_id, payload, updated_at)
                VALUES (%s, %s, now())
                ON CONFLICT (procedure_id) DO UPDATE 
                SET payload = EXCLUDED.payload, updated_at = now();
                """,
                (
                    definition.procedure_id,
                    Jsonb(definition.model_dump(mode="json")),
                ),
            )

    def get_definition(self, procedure_id: str) -> ProcedureDefinition | None:
        from psycopg import connect
        from psycopg.rows import dict_row

        with connect(self._database_url, row_factory=dict_row) as connection:
            row = connection.execute(
                "SELECT payload FROM procedures WHERE procedure_id = %s",
                (procedure_id,),
            ).fetchone()

        if row:
            return ProcedureDefinition.model_validate(row["payload"])
        return None

    def list_definitions(self) -> list[ProcedureDefinition]:
        from psycopg import connect
        from psycopg.rows import dict_row

        with connect(self._database_url, row_factory=dict_row) as connection:
            rows = connection.execute(
                "SELECT payload FROM procedures ORDER BY procedure_id"
            ).fetchall()

        return [ProcedureDefinition.model_validate(row["payload"]) for row in rows]

    def save_execution(self, execution: ProcedureExecution) -> None:
        from psycopg import connect
        from psycopg.types.json import Jsonb

        with connect(self._database_url) as connection:
            connection.execute(
                """
                INSERT INTO procedure_executions (execution_id, payload, updated_at)
                VALUES (%s, %s, now())
                ON CONFLICT (execution_id) DO UPDATE 
                SET payload = EXCLUDED.payload, updated_at = now();
                """,
                (
                    execution.execution_id,
                    Jsonb(execution.model_dump(mode="json")),
                ),
            )

    def get_execution(self, execution_id: str) -> ProcedureExecution | None:
        from psycopg import connect
        from psycopg.rows import dict_row

        with connect(self._database_url, row_factory=dict_row) as connection:
            row = connection.execute(
                "SELECT payload FROM procedure_executions WHERE execution_id = %s",
                (execution_id,),
            ).fetchone()

        if row:
            return ProcedureExecution.model_validate(row["payload"])
        return None

    def list_executions(self, procedure_id: str) -> list[ProcedureExecution]:
        from psycopg import connect
        from psycopg.rows import dict_row

        with connect(self._database_url, row_factory=dict_row) as connection:
            rows = connection.execute(
                "SELECT payload FROM procedure_executions WHERE payload->>'procedure_id' = %s ORDER BY execution_id",
                (procedure_id,),
            ).fetchall()

        return [ProcedureExecution.model_validate(row["payload"]) for row in rows]
