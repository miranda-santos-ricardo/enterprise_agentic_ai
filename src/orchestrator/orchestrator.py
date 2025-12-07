# src/orchestrator/orchestrator.py
import uuid

from models.types import Document, Policy, DecisionOutcome, DecisionStatus
from memory.state import OrchestratorState
from governance.logger import GovernanceLogger
from control.policy import ControlLogic
from agents.extractor import ExtractorAgent
from agents.analyst import AnalystAgent
from agents.verifier import VerifierAgent


class Orchestrator:
    def __init__(
        self,
        logger: GovernanceLogger,
        control_logic: ControlLogic | None = None,
    ) -> None:
        self.logger = logger
        self.control_logic = control_logic or ControlLogic()
        self.extractor = ExtractorAgent()
        self.analyst = AnalystAgent()
        self.verifier = VerifierAgent()

    def run(self, document: Document, policy: Policy) -> DecisionOutcome:
        request_id = str(uuid.uuid4())
        state = OrchestratorState(request_id=request_id, document=document)

        # Global context
        state.context["policy_id"] = policy.id
        state.context["document_title"] = document.metadata.get("title")
        state.context["file_type"] = document.metadata.get("file_type")

        # --- Extraction ---
        state.context["stage"] = "extraction"
        state.context["last_agent"] = "extractor"

        extraction = self.extractor.run(document)
        state.extraction = extraction
        state.context["extraction_length_chars"] = extraction.structured_data.get(
            "length_chars", len(document.content)
        )

        self.logger.log_state(state)

        # --- Analysis ---
        state.context["stage"] = "analysis"
        state.context["last_agent"] = "analyst"

        analysis = self.analyst.run(extraction)
        state.analysis = analysis
        state.context["analysis_risk_count"] = len(analysis.risks)

        self.logger.log_state(state)

        # --- Verification ---
        state.context["stage"] = "verification"
        state.context["last_agent"] = "verifier"

        verification = self.verifier.run(analysis)
        state.verification = verification
        state.context["verification_confidence"] = verification.confidence
        state.context["verification_issue_count"] = len(verification.issues)

        self.logger.log_state(state)

        # --- Policy evaluation ---
        control_decision = self.control_logic.evaluate(policy, verification)

        decision = DecisionOutcome(
            document_id=document.id,
            status=control_decision.status,
            final_summary=(
                analysis.comments
                if control_decision.status == DecisionStatus.APPROVED
                else None
            ),
            reasons=control_decision.reasons,
            policy_id=policy.id,
            verification=verification,
        )
        state.decision = decision

        self.logger.log_decision(decision)
        return decision
