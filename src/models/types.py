#src/models/types.py

from dataclasses import dataclass
from typing import Any, Dict, List, Optional
from enum import Enum

class DecisionStatus(str, Enum):
    APPROVED = "approved"
    REJECTED = "rejected"

@dataclass
class Document:
    id: str
    content: str
    metadata: Dict[str, Any]

@dataclass
class Policy:
    id: str
    name: str
    description: str
    min_confidence: float 
    allowed_risks: List[str]

@dataclass
class ExtractionResult:
    document_id: str
    structured_data: Dict[str, Any]
    raw_text: str

@dataclass
class AnalysisResult:
    document_id: str
    findings: Dict[str, Any]
    risks: List[str]
    comments: str

@dataclass
class VerificationResult:
    document_id: str
    confidence: float
    issues: List[str]
    is_valid: bool

@dataclass
class DecisionOutcome:
    document_id: str
    status: DecisionStatus
    final_summary: Optional[str]
    reasons: List[str]
    policy_id: str
    verification: VerificationResult
