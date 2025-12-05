# src/agents/verifier.py
from dataclasses import dataclass
from typing import List
from models.types import AnalysisResult, VerificationResult
from agents.base import Agent


@dataclass
class VerifierAgent(Agent):
    def name(self) -> str:
        return "verifier"

    def run(self, analysis: AnalysisResult) -> VerificationResult:
        # Placeholder: later make this LLM-assisted or rules-driven
        issues: List[str] = []
        confidence = 0.8  # arbitrary baseline

        if analysis.findings.get("is_long_document"):
            issues.append("LENGTH_WARNING")

        is_valid = True  # for now

        return VerificationResult(
            document_id=analysis.document_id,
            confidence=confidence,
            issues=issues,
            is_valid=is_valid,
        )
