from __future__ import annotations

import pytest
from callibr_contracts import ExecuteCrmActionRequest
from callibr_crm import CrmActionBlockedError, CrmActionService


def test_crm_service_lists_eligible_actions() -> None:
    service = CrmActionService()

    actions = service.list_actions(
        {
            "eligible_actions": [
                "verification_identite",
                "creation_ticket_transporteur",
            ]
        }
    )

    assert [action.action_id for action in actions] == [
        "verification_identite",
        "creation_ticket_transporteur",
    ]


def test_crm_service_executes_identity_verification() -> None:
    service = CrmActionService()

    result = service.execute(
        {"identity_verified": False, "eligible_actions": ["verification_identite"]},
        ExecuteCrmActionRequest(action_id="verification_identite"),
    )

    assert result.context["identity_verified"] is True
    assert result.execution.status == "succeeded"


def test_crm_service_blocks_sensitive_action_before_identity_verification() -> None:
    service = CrmActionService()

    with pytest.raises(CrmActionBlockedError) as exc:
        service.execute(
            {
                "identity_verified": False,
                "eligible_actions": ["creation_ticket_transporteur"],
            },
            ExecuteCrmActionRequest(action_id="creation_ticket_transporteur"),
        )

    assert exc.value.code == "CRM_ACTION_BLOCKED"
