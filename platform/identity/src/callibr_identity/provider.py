from __future__ import annotations

from callibr_contracts import (
    AuthenticatedUser,
    AuthToken,
    IdentityUserRecord,
    LoginRequest,
    TenantInfo,
)
from callibr_kernel import TenantContext
from callibr_persistence import IdentityStore, InMemoryIdentityStore

from callibr_identity.security import (
    AuthenticationFailedError,
    InvalidTokenError,
    decode_token,
    encode_token,
    hash_password,
    verify_password,
)


class DemoIdentityProvider:
    def __init__(
        self,
        *,
        tenant_id: str = "tenant_demo",
        environment: str = "local",
        demo_user_email: str = "learner@demo.callibr.local",
        demo_user_password: str = "callibr-demo",
        auth_secret: str = "change-me-local-dev-secret",
        token_ttl_seconds: int = 3600,
        identity_store: IdentityStore | None = None,
    ) -> None:
        self._auth_secret = auth_secret
        self._token_ttl_seconds = token_ttl_seconds
        self._identity_store = identity_store or InMemoryIdentityStore()
        self._tenant = TenantInfo(
            tenant_id=tenant_id,
            name="Callibr Demo Tenant",
            environment=environment,
        )
        self._seed_demo_user(demo_user_email, demo_user_password)

    def current_tenant(self) -> TenantInfo:
        return self._tenant

    def authenticate(self, context: TenantContext) -> AuthenticatedUser:
        user_id = context.user_id or "learner_demo"
        user = self._identity_store.get_user(context.tenant_id, user_id)
        if user is not None:
            return self._to_authenticated_user(user, context.trace_id)

        return AuthenticatedUser(
            tenant_id=context.tenant_id,
            user_id=user_id,
            email=f"{user_id}@demo.callibr.local",
            display_name=self._display_name(user_id),
            roles=["agent", "learner"],
            trace_id=context.trace_id or "-",
        )

    def login(self, request: LoginRequest, trace_id: str) -> AuthToken:
        user = self._identity_store.get_user_by_email(request.tenant_id, request.email)
        if user is None or not user.is_active:
            raise AuthenticationFailedError()
        if not verify_password(request.password, user.password_hash):
            raise AuthenticationFailedError()

        authenticated_user = self._to_authenticated_user(user, trace_id)
        token = encode_token(
            {
                "tenant_id": user.tenant_id,
                "user_id": user.user_id,
                "email": user.email,
                "roles": user.roles,
            },
            secret=self._auth_secret,
            ttl_seconds=self._token_ttl_seconds,
        )
        return AuthToken(
            access_token=token,
            expires_in=self._token_ttl_seconds,
            user=authenticated_user,
        )

    def authenticate_token(self, token: str, trace_id: str) -> AuthenticatedUser:
        claims = decode_token(token, secret=self._auth_secret)
        tenant_id = claims.get("tenant_id")
        user_id = claims.get("user_id")
        if not isinstance(tenant_id, str) or not isinstance(user_id, str):
            raise InvalidTokenError("missing subject")
        user = self._identity_store.get_user(tenant_id, user_id)
        if user is None or not user.is_active:
            raise InvalidTokenError("unknown user")
        return self._to_authenticated_user(user, trace_id)

    def _seed_demo_user(self, demo_user_email: str, demo_user_password: str) -> None:
        self._identity_store.save_tenant(self._tenant)
        user = self._identity_store.get_user_by_email(self._tenant.tenant_id, demo_user_email)
        if user is not None:
            return
        self._identity_store.save_user(
            IdentityUserRecord(
                tenant_id=self._tenant.tenant_id,
                user_id="learner_demo",
                email=demo_user_email.strip().lower(),
                display_name="Learner Demo",
                roles=["agent", "learner"],
                password_hash=hash_password(demo_user_password),
                is_active=True,
            )
        )

    @staticmethod
    def _to_authenticated_user(
        user: IdentityUserRecord,
        trace_id: str | None,
    ) -> AuthenticatedUser:
        return AuthenticatedUser(
            tenant_id=user.tenant_id,
            user_id=user.user_id,
            email=user.email,
            display_name=user.display_name,
            roles=user.roles,
            trace_id=trace_id or "-",
        )

    @staticmethod
    def _display_name(user_id: str) -> str:
        return user_id.replace("_", " ").replace("-", " ").title()
