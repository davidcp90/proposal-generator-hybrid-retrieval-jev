# LABII · Technical sales proposal generator for NubeAndina

A lab that builds, on top of a RAG with Flask + chat + a ReAct agent, an internal tool for the sales team of **NubeAndina Consulting** (a fictional AWS consultancy). After a discovery call, the tool transcribes the call, checks the catalog and delivers a proposal with architecture and pricing, reviewed by guardrails and accompanied by a diagram and a slide.

Example case: **RitmoFit**, a fictional connected-fitness company, inspired by [Peloton's real-time recommendations architecture on AWS](https://www.youtube.com/watch?v=ym_Gz_zH7w8).

| Stage | What it does | Technology |
| --- | --- | --- |
| 1 · Whisper | The call (MP3) is transcribed and indexed in ~60 s timestamped chunks | Local Whisper + FAISS |
| 2 · OKF | Services, rates and AWS fundamentals are read **by path**, not by similarity | Open Knowledge Format |
| 3 · Jev | Typed evaluations (choice, score, yes/no) and an inline guardrail on every answer | Jev (System 1) |
| Bonus | Diagram with the official AWS icons and a slide with pricing | `diagrams` + `gpt-image-2.5-flare` |

The code is in English; the call, the OKF knowledge base, the proposals, the diagram and the slide are in Spanish, because the sales team and the clients are Spanish-speaking.

## Structure

```
labii_propuestas_aws.ipynb   Lab notebook (Colab)
snippets/                    Each notebook code cell, numbered in execution order
app/                         App version (local, no Colab)
okf/  ·  okf.zip             NubeAndina's OKF knowledge base (24 files)
transcripcion_respaldo.json  Backup transcript of the RitmoFit call
llamadanubeandina.mp3        Call audio
guion_llamada_ritmofit.md    Call script and client constraints
raglab.ipynb · whispr.ipynb  Base notebooks from previous sessions
```

## Option 1 · Notebook in Colab

1. Open `labii_propuestas_aws.ipynb` in Colab with a **T4 GPU** (for Whisper).
2. In **Secrets (🔑)**, add `OPENAI_API_KEY` and `JEV_API_KEY` and enable "Notebook access".
3. Run the cells in order. Have `llamadanubeandina.mp3` (or `transcripcion_respaldo.json`) and `okf.zip` at hand.
4. The last cell starts the final server: chat + guardrails + diagram and slide.

If you'd rather paste cell by cell, use `snippets/` (`01_install.py` … `24_flask_server_final.py`).

## Option 2 · Local app

Requirements: Python 3.10+ and [Graphviz](https://graphviz.org/download/) (`brew install graphviz` or `apt install graphviz`) for the diagrams.

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r app/requirements.txt
pip install openai-whisper          # optional: only to upload audio; without it, upload the .json
cp app/.env.example app/.env        # and fill in OPENAI_API_KEY and JEV_API_KEY
python -m app                       # opens http://127.0.0.1:5002
```

With `PRELOAD_TRANSCRIPT=transcripcion_respaldo.json` (the default in `.env.example`), the RitmoFit call is already indexed at startup: ask directly for *"Genera la propuesta para RitmoFit: plataforma de recomendaciones en tiempo real."*

What happens on each message (everything is logged to the terminal):

1. **Agent**: searches the call (`search_transcripts`) and the OKF (`read_okf`).
2. **Jev guardrail**: if the answer is a hallucination or `prices_ok` < `PRICES_MIN`, it is blocked; if a proposal has a low `constraints_ok`, it is shown with a warning. The chat shows the Jev result under each answer.
3. **Visuals** (approved proposals only): architecture extracted by the LLM → diagram with AWS icons → 16:9 slide.

The **📤 Subir consulta** (upload consultation) button loads a new call (audio or `.json`) without restarting.

### Evaluations

```bash
python -m app.evals
```

Runs the golden set (5 cases) against the agent and scores it with Jev. Suggested pass rule: `type_ok`, `prices_ok` ≥ 0.8, `coverage` ≥ 2; `constraints_ok` applies to case 0.

### Configuration

All variables are in `app/.env.example`: models (`MODEL`, `EFFORT`, `IMAGE_MODEL`, `SLIDE_QUALITY`, `WHISPER_MODEL`), guardrail thresholds (`PRICES_MIN`, `CONSTRAINTS_MIN`), paths (`OKF_DIR`, `DATA_DIR`) and server (`HOST`, `PORT`). Uploads and generated images are stored in `app/data/` (ignored by git).

## Notes

- NubeAndina, RitmoFit and their data are fictional. The AWS costs in the OKF are **illustrative**; always validate with the AWS Pricing Calculator.
