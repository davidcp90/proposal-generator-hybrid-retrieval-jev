"""Runs the golden set against the agent and scores it with Jev: python -m app.evals"""
import logging
import time

import pandas as pd

from . import config
from .agent import ask
from .guardrails import QUESTIONS, evaluate
from .transcripts import add_call, load_segments

# Golden set: inputs stay in Spanish, as the sales team would write them
GOLDEN = [
  {"input": "Genera la propuesta para RitmoFit: plataforma de recomendaciones en tiempo real.",
   "type": "proposal"},
  {"input": "¿Cuánto cuesta un Well-Architected Review?", "type": "direct_answer"},
  {"input": "¿Cuál es el presupuesto de RitmoFit para la fase 1?", "type": "direct_answer"},
  {"input": "¿Pueden operar la plataforma cada mes después del MVP?", "type": "direct_answer"},
  {"input": "Cotiza una migración a Azure para RitmoFit", "type": "out_of_catalog"},
]

# Same questions as the guardrail, with RitmoFit's constraints spelled out
EVAL_QUESTIONS = {**QUESTIONS, "constraints_ok": {"type": "noul",
    "instructions": "Does the answer respect the client's constraints in the transcript: managed services without Kubernetes, a budget of USD 25,000 and an MVP in 10 weeks?"}}


def run():
    rows = []
    for i, c in enumerate(GOLDEN):
        print(f"[{i + 1}/{len(GOLDEN)}] {c['input'][:70]}", flush=True)
        row = {"case": i}
        try:
            t0 = time.time()
            r = ask(c["input"], session=f"eval-{time.time_ns()}")       # new session: no memory between cases
            row["agent_s"] = round(time.time() - t0, 1)
            checks = evaluate(c["input"], r, EVAL_QUESTIONS)
            row.update(checks, type_ok=checks["type"] == c["type"])
            print(f"    ✅ agent {row['agent_s']} s · type={checks['type']}", flush=True)
        except Exception as e:                              # one failing case doesn't stop the run
            row["error"] = f"{type(e).__name__}: {e}"[:200]
            print(f"    ⚠️ {row['error']}", flush=True)
        rows.append(row)
    return pd.DataFrame(rows)


if __name__ == "__main__":
    logging.basicConfig(level=logging.WARNING)
    config.require_keys()
    add_call(load_segments(config.ROOT / (config.PRELOAD_TRANSCRIPT or "transcripcion_respaldo.json")),
             config.PRELOAD_CLIENT)
    df = run()
    print()
    print(df.to_string(index=False))
    # Approval rule from the notebook: type_ok, prices_ok >= 0.8, coverage >= 2 (constraints_ok applies to case 0)
