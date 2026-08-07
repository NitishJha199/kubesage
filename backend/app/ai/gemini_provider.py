import json
import os

from dotenv import load_dotenv
from google import genai

from app.ai.prompts import SYSTEM_PROMPT
from app.ai.schemas import AIExplanation
from app.ai.batch import BatchAIResponse
from app.diagnosis.result import DiagnosisResult

load_dotenv()


class GeminiProvider:
    """
    Google Gemini provider.
    Generates explanations for ALL diagnoses in one request.
    """

    def __init__(self) -> None:

        api_key = os.getenv("GEMINI_API_KEY")

        if not api_key:
            raise RuntimeError(
                "GEMINI_API_KEY not found in environment."
            )

        self.client = genai.Client(api_key=api_key)

    def explain_batch(
        self,
        diagnoses: list[DiagnosisResult],
    ) -> list[AIExplanation]:

        diagnosis_text = ""

        for index, diagnosis in enumerate(diagnoses, start=1):

            diagnosis_text += f"""
Diagnosis #{index}

Diagnosis:
{diagnosis.diagnosis}

Resource:
{diagnosis.resource_type}

Evidence:
{chr(10).join("- " + e for e in diagnosis.evidence)}

Recommendation:
{diagnosis.recommendation}

"""

        prompt = f"""
{SYSTEM_PROMPT}

You will receive multiple Kubernetes diagnoses.

Return ONE explanation for EACH diagnosis.

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

{diagnosis_text}

Do not use markdown.
Do not use code fences.
"""

        response = self.client.models.generate_content(
            model="gemini-2.0-flash",
            contents=prompt,
        )

        text = response.text.strip()

        if text.startswith("```"):
            text = text.replace("```json", "")
            text = text.replace("```", "")
            text = text.strip()

        data = json.loads(text)

        parsed = BatchAIResponse(**data)

        return parsed.explanations
