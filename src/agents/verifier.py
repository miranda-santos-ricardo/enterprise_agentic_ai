# src/agents/verifier.py
from dataclasses import dataclass
from typing import List
from models.types import AnalysisResult, VerificationResult
from agents.base import Agent

RISK_SEVERITY  = {
    "CRITICAL": 3,
    "HIGH": 2,
    "MEDIUM": 1,
    "LOW": 0,
}

@dataclass
class VerifierAgent(Agent):
    def name(self) -> str:
        return "verifier"

    def run(self, analysis: AnalysisResult) -> VerificationResult:

        issues: List[str] = []
        # 1. Risk-based issues from analysis.risks
        for risk in analysis.risks:
            # Expect risk strings like "CRITICAL_DATA_LEAK" or "MEDIUM_POLICY_GAP"
            # Extract the severity prefix if present
            parts = str(risk).split("_", 1)
            severity = parts[0] if parts else "LOW"

            if severity in ("CRITICAL", "HIGH"):
                issues.append(f"RISK_{risk}")
            else:
                #optional: treat medium/low risks less aggressively
                issues.append(f"RISK_{risk}")
        # 2. Completeness checks on findings
        if not analysis.findings:
            issues.append("EMPTY_FINDINGS")

        # 3. Comments quality heuristic
        comments_len = len(analysis.comments or "")
        if comments_len < 20:
            issues.append("COMMENTS_TOO_SHORT")

        # 4. Confidence heuristic
        # Start from a baseline and adjust down based on issues
        confidence = 0.9
        penalty_per_issue = 0.1

        confidence -= penalty_per_issue * len(issues)
        confidence = max (0.0, min(1.0, confidence))

        # basic validity rule: if there are critical issues, mark invalid
        is_valid = True
        if "EMPTY_FINDINGS" in issues:
            is_valid = False
        if confidence < 0.5:
            is_valid = False

        return VerificationResult(
            document_id=analysis.document_id,
            confidence=confidence,
            issues=issues,
            is_valid=is_valid,
        )
