from __future__ import annotations

from dataclasses import dataclass

import pytest
from callibr_kernel import Command, CommandBus, Event, EventBus, HandlerNotFoundError


@dataclass(frozen=True, slots=True)
class StartDemoCommand(Command):
    scenario_id: str = "sav-001"


def test_command_bus_dispatches_registered_handler() -> None:
    bus = CommandBus()
    bus.register(StartDemoCommand, lambda command: f"started:{command.scenario_id}")

    result = bus.dispatch(StartDemoCommand(tenant_id="tenant_demo"))

    assert result == "started:sav-001"


def test_command_bus_raises_when_handler_is_missing() -> None:
    bus = CommandBus()

    with pytest.raises(HandlerNotFoundError) as exc:
        bus.dispatch(StartDemoCommand(tenant_id="tenant_demo"))

    assert exc.value.code == "HANDLER_NOT_FOUND"


def test_event_bus_publishes_to_specific_and_wildcard_handlers() -> None:
    bus = EventBus()
    received: list[str] = []

    bus.subscribe("simulation.started", lambda event: received.append(event.event_type))
    bus.subscribe("*", lambda event: received.append(f"wildcard:{event.event_type}"))

    count = bus.publish(Event(event_type="simulation.started", tenant_id="tenant_demo"))

    assert count == 2
    assert received == ["simulation.started", "wildcard:simulation.started"]
