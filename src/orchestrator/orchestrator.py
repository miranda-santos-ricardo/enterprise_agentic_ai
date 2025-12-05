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

        # Extraction
        extraction = self.extractor.run(document)
        state.extraction = extraction
        self.logger.log_state(state)

        # Analysis
        analysis = self.analyst.run(extraction)
        state.analysis = analysis
        self.logger.log_state(state)

        # Verification
        verification = self.verifier.run(analysis)
        state.verification = verification
        self.logger.log_state(state)

        # Policy evaluation
        control_decision = self.control_logic.evaluate(policy, verification)

        decision = DecisionOutcome(
            document_id=document.id,
            status=control_decision.status,
            final_summary=analysis.comments if control_decision.status == DecisionStatus.APPROVED else None,
            reasons=control_decision.reasons,
            policy_id=policy.id,
            verification=verification,
        )
        state.decision = decision

        self.logger.log_decision(decision)
        return decision
