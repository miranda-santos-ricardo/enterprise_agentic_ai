# src/control/policy.py
from dataclasses import dataclass
from typing import List

from models.types import Policy, VerificationResult, DecisionOutcome, DecisionStatus


@dataclass
class ControlDecision:
    status: DecisionStatus
    reasons: List[str]


class ControlLogic:
    """Evaluates verification results against policy constraints."""

    def evaluate(self, policy: Policy, verification: VerificationResult) -> ControlDecision:
        reasons: List[str] = []

        if not verification.is_valid:
            reasons.append("Verification marked output as invalid.")

        if verification.confidence < policy.min_confidence:
            reasons.append(
                f"Confidence {verification.confidence:.2f} is below policy minimum {policy.min_confidence:.2f}."
            )

        disallowed_issues = [
            issue for issue in verification.issues if issue not in policy.allowed_risks
        ]
        if disallowed_issues:
            reasons.append(f"Disallowed issues present: {', '.join(disallowed_issues)}.")

        if reasons:
            return ControlDecision(status=DecisionStatus.REJECTED, reasons=reasons)

        return ControlDecision(status=DecisionStatus.APPROVED, reasons=["All policy checks passed."])
