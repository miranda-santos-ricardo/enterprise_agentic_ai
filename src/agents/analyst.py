# src/agents/analyst.py
from dataclasses import dataclass
from typing import Any, Dict, List
from models.types import ExtractionResult, AnalysisResult
from agents.base import Agent


@dataclass
class AnalystAgent(Agent):
    def name(self) -> str:
        return "analyst"

    def run(self, extraction: ExtractionResult) -> AnalysisResult:
        # Placeholder: later use LLM with the structured data
        findings: Dict[str, Any] = {
            "is_long_document": extraction.structured_data.get("length_chars", 0) > 2000,
        }
        risks: List[str] = []
        comments = "Initial heuristic analysis only."

        return AnalysisResult(
            document_id=extraction.document_id,
            findings=findings,
            risks=risks,
            comments=comments,
        )
