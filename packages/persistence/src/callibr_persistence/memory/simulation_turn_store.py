from callibr_contracts.simulation import SimulationMessage
from callibr_contracts.ports import SimulationTurnStore

class MemorySimulationTurnStore(SimulationTurnStore):
    def __init__(self) -> None:
        self._turns: dict[str, list[SimulationMessage]] = {}

    def save_turns(self, session_id: str, turns: list[SimulationMessage]) -> None:
        self._turns[session_id] = turns

    def get_turns(self, session_id: str) -> list[SimulationMessage]:
        return self._turns.get(session_id, [])
