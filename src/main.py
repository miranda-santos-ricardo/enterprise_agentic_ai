# src/main.py
import sys
from models.types import Document, Policy
from governance.logger import JsonLineFileLogger
from control.policy import ControlLogic
from orchestrator.orchestrator import Orchestrator
from utils.document_loader import load_document
from pypdf import PdfReader


from pypdf import PdfReader

def load_pdf_as_text(path: str) -> str:
    reader = PdfReader(path)
    return "\n\n".join(page.extract_text() or "" for page in reader.pages)

def main() -> None:
    if len(sys.argv) < 2:
        print("Usage: python src/main.py <path-to-document>")
        raise SystemExit(1)

    path = sys.argv[1]
    doc = load_document(path)
    
    policy = Policy(
    id="policy-default",
    name="Default Enterprise Policy",
    description="Baseline constraints for AI document analysis in a regulated environment.",
    min_confidence=0.75,
    allowed_risks=[
        "RISK_LOW_FORMATTING_ISSUE",
        "RISK_MEDIUM_LENGTH_WARNING",
    ],
)


    logger = JsonLineFileLogger("audit_log.jsonl")
    orchestrator = Orchestrator(logger=logger, control_logic=ControlLogic())

    decision = orchestrator.run(doc, policy)

    print("Decision:", decision.status.value)
    print("Reasons:", decision.reasons)


if __name__ == "__main__":
    main()
