from pydantic import BaseModel

from app.ai.schemas import AIExplanation
from app.diagnosis.result import DiagnosisResult


class DiagnosisWithAI(DiagnosisResult):
    ai: AIExplanation
