from __future__ import annotations

from typing import Any

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

from faceta.db import postgres_connect
from faceta.query.errors import ConsultaRejeitada

app = FastAPI(
    title="Faceta API",
    description="API HTTP da Fase 7 — pergunta em linguagem natural (sem autenticação nesta fase).",
    version="0.7.0",
)


class AskRequest(BaseModel):
    pergunta: str = Field(..., min_length=1, description="Pergunta em linguagem natural")
    sem_narracao: bool = Field(
        False,
        description="Se true, só entendimento+consulta (1 LLM); sem narração",
    )


class AskResponse(BaseModel):
    pergunta: str
    params: dict[str, Any]
    resultado: dict[str, Any]
    narracao: str
    llm_calls: int
    insights: list[Any] = []
    trace_id: str | None = None
    trace_path: str | None = None


@app.get("/health")
def health() -> dict[str, Any]:
    """Checagem leve (não substitui faceta.ops health)."""
    try:
        with postgres_connect() as pg:
            with pg.cursor() as cur:
                cur.execute("SELECT 1")
        return {"ok": True, "postgres": True}
    except Exception as e:
        raise HTTPException(status_code=503, detail=f"postgres indisponível: {e}") from e


@app.post("/ask", response_model=AskResponse)
def ask(body: AskRequest) -> dict[str, Any]:
    """Pipeline ask (≤2 LLM). Sem autenticação nesta fase."""
    from faceta.ask.pipeline import perguntar

    try:
        with postgres_connect() as pg:
            resp = perguntar(pg, body.pergunta, narrar=not body.sem_narracao)
    except ConsultaRejeitada as e:
        raise HTTPException(status_code=400, detail=str(e)) from e
    except SystemExit as e:
        raise HTTPException(status_code=503, detail=str(e)) from e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"{type(e).__name__}: {e}") from e

    data = resp.to_dict()
    if data.get("llm_calls", 0) > 2:
        raise HTTPException(
            status_code=500,
            detail=f"llm_calls={data['llm_calls']} excede o máximo de 2",
        )
    return data
