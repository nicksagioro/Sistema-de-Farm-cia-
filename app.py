"""
app.py - Ponto de entrada da API FastAPI.

Execucao:
    uvicorn app:app --reload
"""

from datetime import datetime

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from database import init_db
from routers import clientes, fornecedores, medicamentos, vendas

app = FastAPI(
    title="Farmacia API",
    description="API REST para sistema de gerenciamento de farmacia",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(medicamentos.router)
app.include_router(clientes.router)
app.include_router(fornecedores.router)
app.include_router(vendas.router)


@app.on_event("startup")
def startup():
    init_db()


@app.get("/health")
def health_check():
    return {"status": "OK", "timestamp": datetime.utcnow().isoformat()}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
