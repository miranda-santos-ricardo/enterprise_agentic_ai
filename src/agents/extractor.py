# src/agents/extractor.py
import json
import os
from dataclasses import dataclass, field
from typing import Any, Dict

from openai import OpenAI
from dotenv import load_dotenv

from models.types import Document, ExtractionResult
from agents.base import Agent

load_dotenv()


EXTRACTION_PROMPT = """
You are the Extraction Agent. Your job is to extract structured information from the document.

Return ONLY valid JSON with the schema:
{
  "title": "...",
  "summary": "...",
  "entities": {
    "people": [],
    "organizations": [],
    "dates": [],
    "risks": []
  },
  "keywords": []
}

If the document does not contain some information, leave the fields as empty strings or empty lists.

Document:
{{document}}
"""


@dataclass
class ExtractorAgent(Agent):
    client: OpenAI = field(
        default_factory=lambda: OpenAI(api_key=os.environ.get("OPENAI_API_KEY", ""))
    )
    model: str = field(
        default_factory=lambda: os.environ.get("MODEL_ID", "gpt-4.1-mini")
    )

    def name(self) -> str:
        return "extractor"

    def run(self, document: Document) -> ExtractionResult:
        # Basic fallback in case of any failure
        fallback_structured: Dict[str, Any] = {
            "title": document.metadata.get("title", "Unknown"),
            "summary": "",
            "entities": {
                "people": [],
                "organizations": [],
                "dates": [],
                "risks": [],
            },
            "keywords": [],
            "length_chars": len(document.content),
        }

        if not self.client.api_key:
            # No API key -> return fallback, don't crash the pipeline
            return ExtractionResult(
                document_id=document.id,
                structured_data=fallback_structured,
                raw_text=document.content,
            )

        try:
            prompt = EXTRACTION_PROMPT.replace("{{document}}", document.content)

            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": "You extract structured information from enterprise documents.",
                    },
                    {"role": "user", "content": prompt},
                ],
                response_format={"type": "json_object"},
            )

            content = response.choices[0].message.content
            structured = json.loads(content)

            # Optionally enrich with length for downstream agents
            structured.setdefault("length_chars", len(document.content))

        except Exception as e:
            # In an enterprise-grade system this would go to a logger, not print
            # For now we just fall back gracefully
            structured = fallback_structured

        return ExtractionResult(
            document_id=document.id,
            structured_data=structured,
            raw_text=document.content,
        )
