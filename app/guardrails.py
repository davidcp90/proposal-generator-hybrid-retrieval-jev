"""Stage 3 · Jev: typed "System 1" checks on every answer, used as an inline guardrail."""
import logging
import os

import requests
from langchain_core.messages import ToolMessage

from . import config
from .agent import ask

log = logging.getLogger("nubeandina")

CTX_CHARS = 4000          # cap each tool result sent to Jev

# Constraints are generic (any client); the eval set in evals.py swaps in RitmoFit's
QUESTIONS = {
  "type": {"type": "choice",
    "instructions": "What type of answer did the agent give?",
    "criteria": {
      "proposal": "proposal with architecture, services and prices",
      "direct_answer": "answers a specific question",
      "out_of_catalog": "states that the service is not offered and gives no price",
      "hallucination": "offers a service or price that is not in the context"}},
  "prices_ok": {"type": "noul",
    "instructions": "Does every consulting price in the answer appear exactly the same in the rate-card.md context? If there are no prices, answer yes."},
  "constraints_ok": {"type": "noul",
    "instructions": "Does the answer respect the client's constraints stated in the call transcript (team skills, budget, timeline, technology)? If there are no constraints in the context, answer yes."},
  "coverage": {"type": "score",
    "instructions": "How complete is the answer relative to what the user asked?",
    "criteria": ["does not answer", "answers part of it", "answers the main point, missing details", "complete and with sources"]},
}


def jev(state, questions, model="jev-latest"):
    api_key = os.environ.get("JEV_API_KEY")
    if not api_key:
        raise RuntimeError("Missing JEV_API_KEY")
    r = requests.post(config.JEV_URL, headers={"Authorization": f"Bearer {api_key}"},
                      json={"model": model, "state": state, "questions": questions}, timeout=15)
    r.raise_for_status()
    return r.json()


def evaluate(question, r, questions=QUESTIONS):
    """Runs the Jev questions on an agent result; returns {type, prices_ok, constraints_ok, coverage}."""
    ctx = [str(m.content)[:CTX_CHARS] for m in r["messages"] if isinstance(m, ToolMessage)]
    a = jev({"question": question, "tool_context": ctx, "agent_answer": r["messages"][-1].text}, questions)
    ans = a["answers"]
    return {"type": ans["type"]["choice"],
            "prices_ok": round(ans["prices_ok"]["noul"], 2),
            "constraints_ok": round(ans["constraints_ok"]["noul"], 2),
            "coverage": ans["coverage"]["score"],
            "jev_usd": a.get("usage", {}).get("cost_usd")}


def ask_with_guardrail(msg, session):
    """Agent + Jev. Returns (answer, checks); checks is None if Jev is unavailable."""
    r = ask(msg, session)
    for m in r["messages"]:
        for tc in getattr(m, "tool_calls", None) or []:
            log.info("   🔧 %s(%s)", tc["name"], ", ".join(f"{k}={v!r}" for k, v in tc["args"].items()))
    answer = r["messages"][-1].text
    try:
        checks = evaluate(msg, r)
    except Exception as e:
        log.warning("   🛡️ Jev unavailable, answer not checked: %s", e)
        return answer, None
    checks["blocked"] = checks["type"] == "hallucination" or checks["prices_ok"] < config.PRICES_MIN
    # Messages shown to the sales team, so they stay in Spanish
    if checks["blocked"]:
        log.info("   🚫 blocked: %r", answer[:300])
        answer = "⚠️ La propuesta no pasó la revisión de precios: revísala contra el rate card antes de enviarla."
    elif checks["type"] == "proposal" and checks["constraints_ok"] < config.CONSTRAINTS_MIN:
        answer = ("> ⚠️ **Revisar antes de enviar:** la propuesta podría no respetar las restricciones del cliente.\n\n"
                  + answer)
    return answer, checks
