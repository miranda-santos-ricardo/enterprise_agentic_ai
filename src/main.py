# src/main.py
from models.types import Document, Policy
from governance.logger import JsonLineFileLogger
from control.policy import ControlLogic
from orchestrator.orchestrator import Orchestrator


def main() -> None:
    doc = Document(
        id="doc-001",
        content="Sample policy or contract text goes here...",
        metadata={"title": "Sample Policy"},
    )

    policy = Policy(
        id="policy-default",
        name="Default Enterprise Policy",
        description="Baseline constraints for AI document analysis.",
        min_confidence=0.75,
        allowed_risks=["LENGTH_WARNING"],
    )

    logger = JsonLineFileLogger("audit_log.jsonl")
    orchestrator = Orchestrator(logger=logger, control_logic=ControlLogic())

    decision = orchestrator.run(doc, policy)

    print("Decision:", decision.status.value)
    print("Reasons:", decision.reasons)


if __name__ == "__main__":
    main()
