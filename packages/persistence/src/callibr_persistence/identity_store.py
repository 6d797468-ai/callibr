from __future__ import annotations

from typing import Protocol

from callibr_contracts import IdentityUserRecord, TenantInfo

from callibr_persistence.postgres import normalize_psycopg_url


class IdentityStore(Protocol):
    def save_tenant(self, tenant: TenantInfo) -> None: ...

    def get_tenant(self, tenant_id: str) -> TenantInfo | None: ...

    def save_user(self, user: IdentityUserRecord) -> None: ...

    def get_user_by_email(self, tenant_id: str, email: str) -> IdentityUserRecord | None: ...

    def get_user(self, tenant_id: str, user_id: str) -> IdentityUserRecord | None: ...


class InMemoryIdentityStore:
    def __init__(self) -> None:
        self._tenants: dict[str, TenantInfo] = {}
        self._users: dict[tuple[str, str], IdentityUserRecord] = {}

    def save_tenant(self, tenant: TenantInfo) -> None:
        self._tenants[tenant.tenant_id] = tenant

    def get_tenant(self, tenant_id: str) -> TenantInfo | None:
        return self._tenants.get(tenant_id)

    def save_user(self, user: IdentityUserRecord) -> None:
        self._users[(user.tenant_id, user.user_id)] = user

    def get_user_by_email(self, tenant_id: str, email: str) -> IdentityUserRecord | None:
        normalized_email = email.strip().lower()
        return next(
            (
                user
                for user in self._users.values()
                if user.tenant_id == tenant_id and user.email.lower() == normalized_email
            ),
            None,
        )

    def get_user(self, tenant_id: str, user_id: str) -> IdentityUserRecord | None:
        return self._users.get((tenant_id, user_id))


class PostgresIdentityStore:
    def __init__(self, database_url: str) -> None:
        self._database_url = normalize_psycopg_url(database_url)

    def init_schema(self) -> None:
        from psycopg import connect

        with connect(self._database_url) as connection:
            connection.execute(
                """
                create table if not exists tenants (
                    tenant_id text primary key,
                    name text not null,
                    environment text not null,
                    created_at timestamptz not null default now()
                );
                """
            )
            connection.execute(
                """
                create table if not exists identity_users (
                    tenant_id text not null references tenants (tenant_id),
                    user_id text not null,
                    email text not null,
                    display_name text not null,
                    roles jsonb not null,
                    password_hash text not null,
                    is_active boolean not null default true,
                    created_at timestamptz not null default now(),
                    updated_at timestamptz not null default now(),
                    primary key (tenant_id, user_id)
                );
                """
            )
            connection.execute(
                """
                create unique index if not exists identity_users_tenant_email_idx
                    on identity_users (tenant_id, lower(email));
                """
            )

    def save_tenant(self, tenant: TenantInfo) -> None:
        from psycopg import connect

        with connect(self._database_url) as connection:
            connection.execute(
                """
                insert into tenants (tenant_id, name, environment)
                values (%s, %s, %s)
                on conflict (tenant_id) do update set
                    name = excluded.name,
                    environment = excluded.environment;
                """,
                (tenant.tenant_id, tenant.name, tenant.environment),
            )

    def get_tenant(self, tenant_id: str) -> TenantInfo | None:
        from psycopg import connect
        from psycopg.rows import dict_row

        with connect(self._database_url, row_factory=dict_row) as connection:
            row = connection.execute(
                "select tenant_id, name, environment from tenants where tenant_id = %s",
                (tenant_id,),
            ).fetchone()
        if row is None:
            return None
        return TenantInfo.model_validate(row)

    def save_user(self, user: IdentityUserRecord) -> None:
        from psycopg import connect
        from psycopg.types.json import Jsonb

        with connect(self._database_url) as connection:
            connection.execute(
                """
                insert into identity_users (
                    tenant_id,
                    user_id,
                    email,
                    display_name,
                    roles,
                    password_hash,
                    is_active
                )
                values (%s, %s, %s, %s, %s, %s, %s)
                on conflict (tenant_id, user_id) do update set
                    email = excluded.email,
                    display_name = excluded.display_name,
                    roles = excluded.roles,
                    password_hash = excluded.password_hash,
                    is_active = excluded.is_active,
                    updated_at = now();
                """,
                (
                    user.tenant_id,
                    user.user_id,
                    user.email,
                    user.display_name,
                    Jsonb(user.roles),
                    user.password_hash,
                    user.is_active,
                ),
            )

    def get_user_by_email(self, tenant_id: str, email: str) -> IdentityUserRecord | None:
        from psycopg import connect
        from psycopg.rows import dict_row

        with connect(self._database_url, row_factory=dict_row) as connection:
            row = connection.execute(
                """
                select tenant_id, user_id, email, display_name, roles, password_hash, is_active
                from identity_users
                where tenant_id = %s and lower(email) = lower(%s)
                """,
                (tenant_id, email),
            ).fetchone()
        if row is None:
            return None
        return IdentityUserRecord.model_validate(row)

    def get_user(self, tenant_id: str, user_id: str) -> IdentityUserRecord | None:
        from psycopg import connect
        from psycopg.rows import dict_row

        with connect(self._database_url, row_factory=dict_row) as connection:
            row = connection.execute(
                """
                select tenant_id, user_id, email, display_name, roles, password_hash, is_active
                from identity_users
                where tenant_id = %s and user_id = %s
                """,
                (tenant_id, user_id),
            ).fetchone()
        if row is None:
            return None
        return IdentityUserRecord.model_validate(row)
