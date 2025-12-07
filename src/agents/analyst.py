# src/agents/analyst.py
import json
import os
from dataclasses import dataclass, field
from typing import Any, Dict, List

from dotenv import load_dotenv
from openai import OpenAI

from models.types import ExtractionResult, AnalysisResult
from agents.base import Agent

load_dotenv()

ANALYSIS_PROMPT = """
You are the Analyst Agent. Using the structured extraction, perform a risk and meaning analysis.

Return ONLY valid JSON with schema:
{
  "findings": { ... },
  "risks": [],
  "comments": "..."
}

Be factual. No hallucinations. Never invent entities.
Structured data:
{{structured}}
"""


@dataclass
class AnalystAgent(Agent):
    client: OpenAI = field(
        default_factory=lambda: OpenAI(api_key=os.environ.get("OPENAI_API_KEY", ""))
    )
    model: str = field(
        default_factory=lambda: os.environ.get("MODEL_ID", "gpt-4.1-mini")
    )

    def name(self) -> str:
        return "analyst"

    def run(self, extraction: ExtractionResult) -> AnalysisResult:
        # Safe fallback if LLM is not available or fails
        fallback_findings: Dict[str, Any] = {
            "notes": "Fallback analysis only. No LLM output available.",
            "length_chars": extraction.structured_data.get("length_chars", 0),
        }
        fallback_risks: List[str] = []
        fallback_comments: str = "Analysis performed without LLM. Heuristic only."

        # No API key: don't break the pipeline
        if not self.client.api_key:
            return AnalysisResult(
                document_id=extraction.document_id,
                findings=fallback_findings,
                risks=fallback_risks,
                comments=fallback_comments,
            )

        try:
            structured_str = json.dumps(extraction.structured_data, ensure_ascii=False)
            prompt = ANALYSIS_PROMPT.replace("{{structured}}", structured_str)

            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": "You analyze structured information from enterprise documents.",
                    },
                    {"role": "user", "content": prompt},
                ],
                response_format={"type": "json_object"},
            )

            content = response.choices[0].message.content
            parsed = json.loads(content)

            findings = parsed.get("findings", {})
            risks = parsed.get("risks", [])
            comments = parsed.get("comments", "")

            # Defensive normalization
            if not isinstance(findings, dict):
                findings = {"_raw": findings}
            if not isinstance(risks, list):
                risks = [str(risks)]
            if not isinstance(comments, str):
                comments = str(comments)

        except Exception:
            # In enterprise setting, you would log the exception; here we fail gracefully
            findings = fallback_findings
            risks = fallback_risks
            comments = fallback_comments

        return AnalysisResult(
            document_id=extraction.document_id,
            findings=findings,
            risks=risks,
            comments=comments,
        )
