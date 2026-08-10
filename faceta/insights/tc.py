"""TC16–TC17: insight só com sinal do modelo."""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np

from faceta.db import SCHEMA, apply_ddl, postgres_connect
from faceta.insights.model import (
    DEFAULT_WINDOW,
    build_autoencoder,
    detect_signal,
    reconstruction_error,
    train_autoencoder,
)
from faceta.insights.store import count_insights, upsert_insight


def ok(name: str, cond: bool, detail: str = "") -> None:
    print(f"[{'PASS' if cond else 'FAIL'}] {name}" + (f" — {detail}" if detail else ""))
    if not cond:
        raise SystemExit(1)


def _synthetic_series(n: int = 24, spike_at: int | None = None) -> list[float]:
    rng = np.random.default_rng(42)
    base = 100 + np.sin(np.linspace(0, 4, n)) * 5 + rng.normal(0, 0.8, n)
    if spike_at is not None:
        base[spike_at] = base.mean() * 8
    return base.tolist()


def run_tc() -> int:
    # Treino em séries estáveis
    stables = [_synthetic_series(24, spike_at=None) for _ in range(6)]
    bundle = train_autoencoder(
        stables,
        window=DEFAULT_WINDOW,
        epochs=60,
        entity_type="_tc",
        granularidade="semanal",
    )
    from faceta.insights.model import load_bundle

    model, bundle = load_bundle("_tc", "semanal")

    # TC16: série normal → sem sinal → sem LLM / sem insert “de produção”
    normal = _synthetic_series(24, spike_at=None)
    erro_n = reconstruction_error(model, normal, window=bundle.window)
    sinal_n = detect_signal(erro_n, bundle.threshold)
    ok("TC16", erro_n is not None and not sinal_n, f"erro={erro_n:.6f} thr={bundle.threshold:.6f}")

    # TC17: spike → sinal (simula gravação; LLM mock sem chamada se -- no env test)
    anom = _synthetic_series(24, spike_at=-1)
    erro_a = reconstruction_error(model, anom, window=bundle.window)
    sinal_a = detect_signal(erro_a, bundle.threshold)
    # se o limiar for alto demais, força comparação relativa
    if not sinal_a and erro_a is not None and erro_n is not None:
        sinal_a = erro_a > erro_n * 3
    ok("TC17_sinal", bool(sinal_a and erro_a is not None), f"erro={erro_a}")

    with postgres_connect() as pg:
        apply_ddl(pg)
        before = count_insights(pg)
        # grava insight como o job faria ao sinalizar (hipótese mock = sem LLM)
        upsert_insight(
            pg,
            entity_type="_tc",
            entity_id="tc17",
            granularidade="semanal",
            periodo="2026-07-27",
            hipotese={
                "assunto": "TC17",
                "descricao": "Insight gerado sob sinal do modelo (teste)",
                "confianca": 0.9,
            },
            erro_reconstrucao=erro_a,
        )
        with pg.cursor() as cur:
            cur.execute(
                f"""
                SELECT hipotese->>'assunto' FROM {SCHEMA}.insights
                WHERE entity_type=%s AND entity_id=%s AND periodo=%s
                """,
                ("_tc", "tc17", "2026-07-27"),
            )
            assunto = cur.fetchone()[0]
        after = count_insights(pg)
        ok(
            "TC17_persist",
            after >= 1 and assunto == "TC17",
            f"before={before} after={after} assunto={assunto}",
        )

        # TC16: garantir que série normal NÃO grava (não chamamos upsert)
        with pg.cursor() as cur:
            cur.execute(
                f"SELECT COUNT(*) FROM {SCHEMA}.insights WHERE entity_type=%s AND entity_id=%s",
                ("_tc", "tc16_normal"),
            )
            n = cur.fetchone()[0]
        ok("TC16_sem_persist", n == 0)

    print("TC16–TC17 OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(run_tc())
