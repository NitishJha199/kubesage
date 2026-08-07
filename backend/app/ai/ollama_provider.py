import json

import requests

from app.ai.batch import BatchAIResponse
from app.ai.prompts import SYSTEM_PROMPT
from app.diagnosis.result import DiagnosisResult


class OllamaProvider:
    """
    Generates AI explanations for multiple diagnoses
    in a single Ollama request.
    """

    def __init__(self) -> None:
        self.url = "http://localhost:11434/api/generate"
        self.model = "llama3.2:1b"

    def explain_batch(
        self,
        diagnoses: list[DiagnosisResult],
    ) -> BatchAIResponse:

        prompt = self._build_prompt(diagnoses)

        response = requests.post(
            self.url,
            json={
                "model": self.model,
                "prompt": prompt,
                "stream": False,
            },
            timeout=180,
        )

        response.raise_for_status()

        text = response.json()["response"].strip()

        if text.startswith("```"):
            text = (
                text.replace("```json", "")
                .replace("```", "")
                .strip()
            )

        data = json.loads(text)

        return BatchAIResponse(**data)

    def _build_prompt(
        self,
        diagnoses: list[DiagnosisResult],
    ) -> str:

        items = []

        for i, d in enumerate(diagnoses, start=1):

            evidence = "\n".join(
                f"- {e}" for e in d.evidence
            )

            items.append(
                f"""
Diagnosis #{i}

Resource:
{d.resource_type}/{d.resource_name}

Namespace:
{d.namespace}

Diagnosis:
{d.diagnosis}

Recommendation:
{d.recommendation}

Evidence:
{evidence}
"""
            )

        return f"""
{SYSTEM_PROMPT}

You will receive multiple Kubernetes diagnoses.

Generate one explanation for EACH diagnosis.

Return ONLY valid JSON.

Schema:

{{
  "explanations": [
    {{
      "summary": "...",
      "root_cause": "...",
      "impact": "...",
      "verification_steps": [
        "...",
        "..."
      ],
      "kubectl_commands": [
        "...",
        "..."
      ],
      "prevention": "..."
    }}
  ]
}}

Do not use markdown.
Do not use code fences.

{''.join(items)}
"""
