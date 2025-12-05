# src/agents/extractor.py
from dataclasses import dataclass
from typing import Any, Dict
from models.types import Document, ExtractionResult
from agents.base import Agent


@dataclass
class ExtractorAgent(Agent):
    def name(self) -> str:
        return "extractor"

    def run(self, document: Document) -> ExtractionResult:
        # Placeholder: later you replace with actual LLM / parsing logic
        structured: Dict[str, Any] = {
            "title": document.metadata.get("title", "Unknown"),
            "length_chars": len(document.content),
        }
        return ExtractionResult(
            document_id=document.id,
            structured_data=structured,
            raw_text=document.content,
        )
