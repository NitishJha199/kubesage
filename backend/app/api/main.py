from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.collector.client import KubernetesClient
from app.diagnosis.service import DiagnosisService

app = FastAPI(title="KubeSage API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def root():
    return {
        "message": "Welcome to the KubeSage API"
    }


@app.get("/diagnose")
def diagnose():
    client = KubernetesClient()
    service = DiagnosisService(client)

    return service.diagnose()
