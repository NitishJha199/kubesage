from fastapi import APIRouter

from app.collector.client import KubernetesClient
from app.diagnosis.service import DiagnosisService

router = APIRouter()


@router.get("/")
def root():
    return {
        "message": "Welcome to KubeSage API"
    }


@router.get("/health")
def health():
    return {
        "status": "ok"
    }


@router.get("/diagnose")
def diagnose():

    client = KubernetesClient()

    service = DiagnosisService(client)

    results = service.diagnose()

    return results
