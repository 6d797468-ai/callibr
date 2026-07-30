from __future__ import annotations

import pytest
from callibr_contracts import LoginRequest
from callibr_identity import AuthenticationFailedError, DemoIdentityProvider, decode_token
from callibr_kernel import TenantContext


def test_demo_identity_provider_authenticates_current_context() -> None:
    provider = DemoIdentityProvider(tenant_id="tenant_demo", environment="local")

    user = provider.authenticate(
        TenantContext(
            tenant_id="tenant_acme",
            user_id="amina_agent",
            trace_id="trace_001",
        )
    )

    assert user.tenant_id == "tenant_acme"
    assert user.user_id == "amina_agent"
    assert user.display_name == "Amina Agent"
    assert "agent" in user.roles
    assert user.trace_id == "trace_001"


def test_demo_identity_provider_login_issues_signed_token() -> None:
    provider = DemoIdentityProvider(
        tenant_id="tenant_demo",
        demo_user_email="learner@demo.callibr.local",
        demo_user_password="callibr-demo",
        auth_secret="test-secret",
    )

    token = provider.login(
        LoginRequest(
            tenant_id="tenant_demo",
            email="learner@demo.callibr.local",
            password="callibr-demo",
        ),
        trace_id="trace_login",
    )

    claims = decode_token(token.access_token, secret="test-secret")
    assert token.user.user_id == "learner_demo"
    assert token.user.trace_id == "trace_login"
    assert claims["tenant_id"] == "tenant_demo"
    assert claims["user_id"] == "learner_demo"


def test_demo_identity_provider_rejects_bad_password() -> None:
    provider = DemoIdentityProvider(
        tenant_id="tenant_demo",
        demo_user_email="learner@demo.callibr.local",
        demo_user_password="callibr-demo",
        auth_secret="test-secret",
    )

    with pytest.raises(AuthenticationFailedError):
        provider.login(
            LoginRequest(
                tenant_id="tenant_demo",
                email="learner@demo.callibr.local",
                password="wrong",
            ),
            trace_id="trace_login",
        )
