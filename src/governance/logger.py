from abc import ABC, abstractmethod
from typing import Any, Dict
from memory.state import OrchestratorState
from models.types import DecisionOutcome

class GovernanceLogger(ABC):
    @abstractmethod
    def log_state(self, state: OrchestratorState) -> None:
        """Logs the current state of the governance orchestrator."""
        ...

    @abstractmethod
    def log_decision(self, decision: DecisionOutcome) -> None:
        """Logs a specific event with its details."""
        ...

class JsonLineFileLogger(GovernanceLogger):
    
    def __init__(self, file_path: str = "audit_log.jsonl") -> None:
        self.filepath = file_path

    def log_state(self, state: OrchestratorState) -> None:
        record: Dict[str, Any] = {
            "request_id": state.request_id,
            "document_id": state.document.id,
            "has_extraction": state.extraction is not None,
            "has_analysis": state.analysis is not None,
            "has_verification": state.verification is not None,
            "context": state.context,
        }
        with open(self.filepath, "a", encoding="utf-8") as f:
            f.write(f"{record}\n")

    def log_decision(self, decision: DecisionOutcome) -> None:
        record: Dict[str, Any] = {
            "document_id": decision.document_id,
            "policy_id": decision.policy_id,
            "status": decision.status.value,
            "reasons": decision.reasons,
            "verification_confidence": decision.verification.confidence,
        }
        with open(self.filepath, "a", encoding="utf-8") as f:
            f.write(f"{record}\n")