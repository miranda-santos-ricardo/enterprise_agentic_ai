from dataclasses import dataclass, field
from typing import Any, Dict
from models.types import (
    Document,
    ExtractionResult,
    AnalysisResult,
    VerificationResult,
    DecisionOutcome
)

@dataclass
class OrchestratorState:
    request_id: str
    document: Document
    extraction: ExtractionResult | None = None
    analysis: AnalysisResult | None = None
    verification: VerificationResult | None = None
    decision: DecisionOutcome | None = None
    context: Dict[str,Any] = field(default_factory=dict)
