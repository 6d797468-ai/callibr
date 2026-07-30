from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
from typing import Any

from callibr_contracts import CrmActionDefinition, CrmActionExecution, ExecuteCrmActionRequest
from callibr_kernel import CallibrError, new_id, utc_now


class CrmActionNotFoundError(CallibrError):
    def __init__(self, action_id: str) -> None:
        super().__init__(
            "CRM_ACTION_NOT_FOUND",
            f"CRM action {action_id} was not found.",
            details={"action_id": action_id},
        )


class CrmActionBlockedError(CallibrError):
    def __init__(self, action_id: str, reason: str) -> None:
        super().__init__(
            "CRM_ACTION_BLOCKED",
            f"CRM action {action_id} is blocked: {reason}.",
            details={"action_id": action_id, "reason": reason},
        )


@dataclass(frozen=True, slots=True)
class CrmActionResult:
    context: dict[str, Any]
    execution: CrmActionExecution


CrmActionHandler = Callable[[dict[str, Any], dict[str, Any]], CrmActionResult]


class CrmActionService:
    def __init__(self) -> None:
        self._actions = {
            "verification_identite": CrmActionDefinition(
                action_id="verification_identite",
                label="Verifier identite",
                category="identity",
                description="Confirme l'identite client avant toute action sensible.",
                required_fields=[],
                produces=["identity_verified"],
            ),
            "consultation_suivi_colis": CrmActionDefinition(
                action_id="consultation_suivi_colis",
                label="Consulter suivi colis",
                category="order",
                description="Recupere l'etat transporteur et l'estimation de livraison.",
                required_fields=[],
                produces=["delivery_status", "delivery_eta"],
            ),
            "creation_ticket_transporteur": CrmActionDefinition(
                action_id="creation_ticket_transporteur",
                label="Creer ticket transporteur",
                category="ticket",
                description="Ouvre un ticket SAV pour relance transporteur.",
                required_fields=[],
                produces=["ticket_id", "ticket_status"],
            ),
            "notification_client": CrmActionDefinition(
                action_id="notification_client",
                label="Notifier client",
                category="notification",
                description="Programme une notification client avec le recapitulatif.",
                required_fields=[],
                produces=["customer_notification"],
            ),
            "consultation_facture": CrmActionDefinition(
                action_id="consultation_facture",
                label="Consulter facture",
                category="billing",
                description="Verifie le statut de facturation dans le CRM.",
                required_fields=[],
                produces=["invoice_status", "billing_analysis"],
            ),
            "creation_ticket_facturation": CrmActionDefinition(
                action_id="creation_ticket_facturation",
                label="Creer ticket facturation",
                category="ticket",
                description="Ouvre un ticket back-office facturation.",
                required_fields=[],
                produces=["ticket_id", "ticket_status"],
            ),
            "demande_remboursement": CrmActionDefinition(
                action_id="demande_remboursement",
                label="Demander remboursement",
                category="billing",
                description="Declenche une demande de remboursement.",
                required_fields=[],
                produces=["refund_status"],
            ),
        }
        self._handlers: dict[str, CrmActionHandler] = {
            "verification_identite": self._verify_identity,
            "consultation_suivi_colis": self._check_delivery,
            "creation_ticket_transporteur": self._create_carrier_ticket,
            "notification_client": self._notify_customer,
            "consultation_facture": self._check_invoice,
            "creation_ticket_facturation": self._create_billing_ticket,
            "demande_remboursement": self._request_refund,
        }

    def list_actions(self, crm_context: dict[str, Any]) -> list[CrmActionDefinition]:
        eligible_action_ids = set(crm_context.get("eligible_actions", []))
        return [
            action
            for action_id, action in self._actions.items()
            if not eligible_action_ids or action_id in eligible_action_ids
        ]

    def execute(
        self,
        crm_context: dict[str, Any],
        request: ExecuteCrmActionRequest,
    ) -> CrmActionResult:
        action = self._actions.get(request.action_id)
        handler = self._handlers.get(request.action_id)
        if action is None or handler is None:
            raise CrmActionNotFoundError(request.action_id)

        eligible_action_ids = set(crm_context.get("eligible_actions", []))
        if eligible_action_ids and request.action_id not in eligible_action_ids:
            raise CrmActionBlockedError(request.action_id, "action non eligible pour ce scenario")

        return handler(dict(crm_context), request.payload)

    def _execution(
        self,
        action_id: str,
        *,
        message: str,
        output: dict[str, Any],
        status: str = "succeeded",
    ) -> CrmActionExecution:
        action = self._actions[action_id]
        return CrmActionExecution(
            execution_id=new_id("crmexec"),
            action_id=action.action_id,
            label=action.label,
            status=status,
            executed_at=utc_now(),
            message=message,
            output=output,
        )

    def _verify_identity(
        self,
        context: dict[str, Any],
        _: dict[str, Any],
    ) -> CrmActionResult:
        context["identity_verified"] = True
        execution = self._execution(
            "verification_identite",
            message="Identite client verifiee.",
            output={"identity_verified": True},
        )
        return CrmActionResult(context=context, execution=execution)

    def _check_delivery(
        self,
        context: dict[str, Any],
        _: dict[str, Any],
    ) -> CrmActionResult:
        context["delivery_status"] = "retard confirme par le transporteur"
        context["delivery_eta"] = "24-48h"
        execution = self._execution(
            "consultation_suivi_colis",
            message="Suivi transporteur consulte : livraison estimee sous 24-48h.",
            output={
                "delivery_status": context["delivery_status"],
                "delivery_eta": context["delivery_eta"],
            },
        )
        return CrmActionResult(context=context, execution=execution)

    def _create_carrier_ticket(
        self,
        context: dict[str, Any],
        _: dict[str, Any],
    ) -> CrmActionResult:
        self._require_identity(context, "creation_ticket_transporteur")
        ticket_id = new_id("ticket")
        context["ticket_id"] = ticket_id
        context["ticket_status"] = "transporteur_contacte"
        execution = self._execution(
            "creation_ticket_transporteur",
            message="Ticket transporteur cree et affecte au SAV.",
            output={"ticket_id": ticket_id, "ticket_status": context["ticket_status"]},
        )
        return CrmActionResult(context=context, execution=execution)

    def _notify_customer(
        self,
        context: dict[str, Any],
        _: dict[str, Any],
    ) -> CrmActionResult:
        if context.get("ticket_status") in (None, "non_cree"):
            raise CrmActionBlockedError("notification_client", "aucun ticket ou suivi n'a ete cree")
        context["customer_notification"] = "notification_programmee"
        execution = self._execution(
            "notification_client",
            message="Notification client programmee avec le recapitulatif.",
            output={"customer_notification": context["customer_notification"]},
        )
        return CrmActionResult(context=context, execution=execution)

    def _check_invoice(
        self,
        context: dict[str, Any],
        _: dict[str, Any],
    ) -> CrmActionResult:
        context["billing_analysis"] = "double prelevement probable"
        execution = self._execution(
            "consultation_facture",
            message="Facture consultee : double prelevement probable detecte.",
            output={
                "invoice_status": context.get("invoice_status"),
                "billing_analysis": context["billing_analysis"],
            },
        )
        return CrmActionResult(context=context, execution=execution)

    def _create_billing_ticket(
        self,
        context: dict[str, Any],
        _: dict[str, Any],
    ) -> CrmActionResult:
        self._require_identity(context, "creation_ticket_facturation")
        ticket_id = new_id("ticket")
        context["ticket_id"] = ticket_id
        context["ticket_status"] = "facturation_en_cours"
        execution = self._execution(
            "creation_ticket_facturation",
            message="Ticket facturation cree pour analyse back-office.",
            output={"ticket_id": ticket_id, "ticket_status": context["ticket_status"]},
        )
        return CrmActionResult(context=context, execution=execution)

    def _request_refund(
        self,
        context: dict[str, Any],
        _: dict[str, Any],
    ) -> CrmActionResult:
        self._require_identity(context, "demande_remboursement")
        if context.get("ticket_status") in (None, "non_cree"):
            raise CrmActionBlockedError(
                "demande_remboursement",
                "aucun ticket facturation n'a ete cree",
            )
        context["refund_status"] = "demande_transmise"
        execution = self._execution(
            "demande_remboursement",
            message="Demande de remboursement transmise.",
            output={"refund_status": context["refund_status"]},
        )
        return CrmActionResult(context=context, execution=execution)

    @staticmethod
    def _require_identity(context: dict[str, Any], action_id: str) -> None:
        if not context.get("identity_verified", False):
            raise CrmActionBlockedError(action_id, "identite client non verifiee")
