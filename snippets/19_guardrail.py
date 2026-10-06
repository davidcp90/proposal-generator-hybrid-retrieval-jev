# Extra: inline guardrail. Jev checks every answer before it reaches the sales team.
from langchain_core.messages import ToolMessage

PRICES_MIN = 0.5          # below this, the answer is blocked
CONSTRAINTS_MIN = 0.5     # below this, a proposal is shown with a warning

def evaluate(question, r):
    """Runs the Jev QUESTIONS on an agent result; returns {type, prices_ok, constraints_ok, coverage}."""
    ctx = [str(m.content)[:4000] for m in r["messages"] if isinstance(m, ToolMessage)]
    a = jev({"question": question, "tool_context": ctx, "agent_answer": r["messages"][-1].text}, QUESTIONS)
    ans = a["answers"]
    return {"type": ans["type"]["choice"],
            "prices_ok": round(ans["prices_ok"]["noul"], 2),
            "constraints_ok": round(ans["constraints_ok"]["noul"], 2),
            "coverage": ans["coverage"]["score"]}

def ask_bot_with_guardrail(msg, session):
    """Agent + Jev. Returns (answer, checks); checks is None if Jev is unavailable."""
    r = ask(msg, session)
    answer = r["messages"][-1].text
    try:
        checks = evaluate(msg, r)
    except Exception as e:
        print(f"   🛡️ Jev unavailable, answer not checked: {e}")
        return answer, None
    checks["blocked"] = checks["type"] == "hallucination" or checks["prices_ok"] < PRICES_MIN
    # Messages shown to the sales team, so they stay in Spanish
    if checks["blocked"]:
        answer = "⚠️ La propuesta no pasó la revisión de precios: revísala contra el rate card antes de enviarla."
    elif checks["type"] == "proposal" and checks["constraints_ok"] < CONSTRAINTS_MIN:
        answer = ("> ⚠️ **Revisar antes de enviar:** la propuesta podría no respetar las restricciones del cliente.\n\n"
                  + answer)
    return answer, checks
