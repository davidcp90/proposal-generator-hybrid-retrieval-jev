"""Flask server: chat + Jev guardrails + call upload + diagram and slide."""
import logging
import time
from pathlib import Path

from flask import Flask, jsonify, render_template, request, send_from_directory
from werkzeug.utils import secure_filename

from . import config
from .guardrails import ask_with_guardrail
from .okf import validate_okf
from .transcripts import add_call, load_segments
from .visuals import cost_totals, make_visuals

log = logging.getLogger("nubeandina")
app = Flask(__name__)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/ask_bot", methods=["POST"])
def ask_bot():
    data = request.form or request.json
    log.info("💬 [%s] %s", data.get("session_id", "default"), data["msg"])
    t0 = time.time()
    try:
        answer, checks = ask_with_guardrail(data["msg"], data.get("session_id", "default"))   # agent + Jev
    except Exception as e:
        log.exception("   ❌ agent failed")
        return jsonify({"error": str(e)}), 500
    log.info("   🤖 %.1f s · 🛡️ %s", time.time() - t0, checks)
    is_proposal = bool(checks) and checks["type"] == "proposal" and not checks["blocked"]
    return jsonify({"msg": answer, "checks": checks, "visuals": is_proposal})


@app.route("/visuals", methods=["POST"])
def visuals():
    t0 = time.time()
    try:
        arch, png, slide = make_visuals(request.json["proposal"])
    except Exception as e:
        log.exception("   ❌ visuals failed")
        return jsonify({"error": str(e)}), 500
    log.info("   🖼️ %s + %s (%.1f s)", Path(png).name, Path(slide).name, time.time() - t0)
    return jsonify({"diagram": f"/img/{Path(png).name}", "slide": f"/img/{Path(slide).name}",
                    "totals": cost_totals(arch)})


@app.route("/img/<name>")
def img(name):
    return send_from_directory(config.IMG_DIR.resolve(), name)


@app.route("/upload_audio", methods=["POST"])
def upload_audio():
    f = request.files["audio"]
    client = request.form.get("client", "").strip() or "unknown"
    config.UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
    path = config.UPLOAD_DIR / secure_filename(f.filename)
    f.save(path)
    log.info("📥 %s · client=%s", path.name, client)
    t0 = time.time()
    try:
        segs = load_segments(path)          # audio → Whisper, .json → backup transcript
    except Exception as e:
        log.exception("   ❌ transcription failed")
        return jsonify({"error": str(e)}), 500
    if not segs:
        return jsonify({"error": "empty transcript"}), 400
    docs = add_call(segs, client)
    log.info("   📝 %d segments → %d chunks (%.1f s)", len(segs), len(docs), time.time() - t0)
    return jsonify({"client": client, "chunks": len(docs), "minutes": round(segs[-1]["end"] / 60, 1)})


def main():
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(message)s", datefmt="%H:%M:%S")
    logging.getLogger("werkzeug").setLevel(logging.WARNING)       # hide per-request noise
    logging.getLogger("httpx").setLevel(logging.WARNING)
    config.require_keys()
    invalid = validate_okf()
    log.info("📚 OKF %s · %s", config.OKF_DIR, "✅ valid" if not invalid else f"❌ missing 'type': {invalid}")
    if config.PRELOAD_TRANSCRIPT:
        path = Path(config.PRELOAD_TRANSCRIPT)
        path = path if path.is_absolute() else config.ROOT / path
        docs = add_call(load_segments(path), config.PRELOAD_CLIENT)
        log.info("📝 preloaded %s · client=%s · %d chunks", path.name, config.PRELOAD_CLIENT, len(docs))
    log.info("✅ Open the chat: http://%s:%d", config.HOST, config.PORT)
    app.run(host=config.HOST, port=config.PORT, threaded=True)


if __name__ == "__main__":
    main()
