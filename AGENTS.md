# AGENTS.md

Guidance for coding agents working in this repo.

## What this is

A teaching lab (Spanish-speaking course) that builds a technical sales proposal generator for NubeAndina Consulting, a fictional AWS consultancy. Pipeline: client call → Whisper transcript in FAISS → agent reads the OKF knowledge base by path → Jev typed checks as evals and inline guardrail → architecture diagram (`diagrams`) and slide (`gpt-image-2.5-flare`). Demo client: RitmoFit (fictional).

The same logic exists in three places:

| Location | Runs in | Notes |
| --- | --- | --- |
| `labii_propuestas_aws.ipynb` | Google Colab | Source of truth for the lab. Markdown cells explain each step. |
| `snippets/NN_*.py` | Pasted into Colab | One file per notebook **code** cell, in order (24 files ↔ 24 code cells). |
| `app/` | Locally, `python -m app` | Package version with no Colab dependencies. |

## Language conventions (important)

- **Code is in English**: identifiers, comments, docstrings, log/print messages, LLM prompts, Jev questions. `README.md` and this file are in English too.
- **Spanish stays Spanish**: notebook markdown cells, OKF content (`okf/`, the Plan B cell), the call transcript, golden-set inputs, and anything shown to the sales team or the client (chat UI text, guardrail warnings, diagram cluster labels, slide text, proposal section titles).
- The agent's system prompt is English but tells the model to always answer in Spanish.

## Keeping things in sync

- When you change a notebook code cell, write the same content to its snippet file, and vice versa. Map: code cells in order → `snippets/01_…` to `snippets/24_…`. Cell `03_chat_html.py` (the `html` string) is the chat UI; `app/templates/index.html` is the same page minus the Colab-only stylesheet link.
- When you rename an identifier, update the Spanish markdown cells that mention it.
- Logic changes usually belong in all three places (notebook, snippet, `app/`). Say so if you only change one.
- Write the notebook with `json.dumps(nb, indent=1, ensure_ascii=False)` plus a trailing newline, to keep diffs small. Keep cell ids.
- `okf/` and `okf.zip` must have the same 24 files; the notebook's Plan B cell recreates the same bundle.

## Code gotchas

- With reasoning models, `AIMessage.content` is a list of blocks (reasoning + text). Use `.text` for the answer. Tool results (`ToolMessage.content`) are plain strings.
- `ChatOpenAI` is created with `timeout=120, max_retries=1`, and `ask()` passes `recursion_limit: 40`. Don't remove them: without them, a stuck call hangs the Colab kernel.
- The Jev key is read from `os.environ["JEV_API_KEY"]` at call time.
- Flask servers bind in the main thread (`make_server(...)` then `serve_forever` in a thread) so port errors are visible. Re-running a server cell shuts down the previous `server`.
- Consulting prices must come only from `okf/company/rate-card.md`; AWS costs only from `okf/aws/basics/pricing-models.md` (illustrative). Totals for the slide are computed in code (`cost_totals`), never by the image model.
- Colab cells with `!` shell lines and `google.colab` imports only work in Colab; `app/` must not import `google.colab`.
- `app/` creates the agent, extractor and OpenAI client lazily, so modules import without API keys.

## Running and checking `app/`

```bash
pip install -r app/requirements.txt      # + Graphviz on the system; openai-whisper optional
cp app/.env.example app/.env             # OPENAI_API_KEY, JEV_API_KEY
python -m app                            # server on http://127.0.0.1:5002
python -m app.evals                      # golden set scored with Jev
```

There is no test suite. To check changes without spending API calls, use Flask's `app.test_client()` and replace `guardrails.ask`, `guardrails.jev`, `visuals.extract_architecture`, `visuals.draw` and `visuals._openai` with fakes; `transcripts.OpenAIEmbeddings` can be swapped for `langchain_core.embeddings.DeterministicFakeEmbedding`. Check the page's JavaScript with `node --check` on the extracted `<script>`.

Notebook cells can't be run locally (Colab-only). At least `ast.parse` every code cell that doesn't start with `!`.
