import pandas as pd, time
from langchain_core.messages import ToolMessage

CTX_CHARS = 4000        # cap each tool result sent to Jev: the full OKF reads make the request heavy

rows = []
for i, c in enumerate(golden):
    print(f"[{i + 1}/{len(golden)}] {c['input'][:70]}", flush=True)
    row = {"case": i}
    try:
        t0 = time.time()
        r = ask(c["input"], session=f"eval-{time.time_ns()}")       # new session: no memory between cases
        row["agent_s"] = round(time.time() - t0, 1)
        state = {"question": c["input"],
                 "tool_context": [str(m.content)[:CTX_CHARS] for m in r["messages"] if isinstance(m, ToolMessage)],
                 "agent_answer": r["messages"][-1].text}
        t0 = time.time()
        a = jev(state, QUESTIONS)
        ans = a["answers"]
        row.update({"type": ans["type"]["choice"], "type_ok": ans["type"]["choice"] == c["type"],
                    "prices_ok": round(ans["prices_ok"]["noul"], 2),
                    "constraints_ok": round(ans["constraints_ok"]["noul"], 2),
                    "coverage": ans["coverage"]["score"],
                    "jev_ms": int((time.time() - t0) * 1000), "jev_usd": a["usage"]["cost_usd"]})
        print(f"    ✅ agent {row['agent_s']} s · jev {row['jev_ms']} ms", flush=True)
    except Exception as e:                              # one failing case doesn't stop the run
        row["error"] = f"{type(e).__name__}: {e}"[:200]
        print(f"    ⚠️ {row['error']}", flush=True)
    rows.append(row)

df = pd.DataFrame(rows)
df
