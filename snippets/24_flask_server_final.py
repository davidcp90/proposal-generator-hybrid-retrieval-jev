import json, threading, time, uuid
from pathlib import Path
from flask import Flask, request, jsonify, render_template_string, send_from_directory
from werkzeug.serving import make_server
from werkzeug.utils import secure_filename
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings

PORT = 5002
IMG_DIR = Path("/content/chat_images")
IMG_DIR.mkdir(exist_ok=True)

# Re-running this cell: stop the previous server and free the port
if "server" in globals():
    server.shutdown()
    server.server_close()
    print("♻️ Previous server stopped.")

app = Flask(__name__)

@app.route("/")
def home():
    return render_template_string(html)

@app.route("/ask_bot", methods=["POST"])
def ask_bot():
    data = request.form or request.json
    print(f"💬 {data['msg']}", flush=True)
    t0 = time.time()
    answer, checks = ask_bot_with_guardrail(data["msg"], data.get("session_id", "default"))   # agent + Jev
    print(f"   🤖 {time.time() - t0:.1f} s · 🛡️ {checks}", flush=True)
    is_proposal = checks["type"] == "proposal" and not checks["blocked"] if checks else False
    return jsonify({"msg": answer, "checks": checks, "visuals": is_proposal})

@app.route("/visuals", methods=["POST"])
def visuals():
    name = uuid.uuid4().hex[:8]
    try:
        t0 = time.time()
        arch = extract_architecture(request.json["proposal"])
        png = draw(arch, filename=str(IMG_DIR / f"arch_{name}"))
        print(f"   📐 {png} ({time.time() - t0:.1f} s)", flush=True)
        slide = make_slide(arch, png, filename=str(IMG_DIR / f"slide_{name}.png"))
        print(f"   🖼️ {slide} ({time.time() - t0:.1f} s)", flush=True)
    except Exception as e:
        print(f"   ❌ visuals failed: {type(e).__name__}: {e}", flush=True)
        return jsonify({"error": str(e)}), 500
    return jsonify({"diagram": f"/img/{Path(png).name}", "slide": f"/img/{Path(slide).name}",
                    "totals": cost_totals(arch)})

@app.route("/img/<name>")
def img(name):
    return send_from_directory(IMG_DIR, name)

@app.route("/upload_audio", methods=["POST"])
def upload_audio():
    global transcript_db
    f = request.files["audio"]
    client = request.form.get("client", "").strip() or "unknown"
    path = f"/content/{secure_filename(f.filename)}"
    f.save(path)
    print(f"📥 {path} · client={client}", flush=True)
    segs = json.load(open(path)) if path.endswith(".json") else transcribe(path)   # .json = backup transcript
    if not segs:
        return jsonify({"error": "empty transcript"}), 400
    new_docs = segments_to_docs(segs, client)
    if "transcript_db" in globals():
        transcript_db.add_documents(new_docs)
    else:                                 # no call indexed yet: create the index here
        transcript_db = FAISS.from_documents(new_docs, OpenAIEmbeddings(model=EMBEDDINGS_MODEL))
    print(f"   📝 {len(new_docs)} chunks indexed", flush=True)
    return jsonify({"client": client, "chunks": len(new_docs), "minutes": round(segs[-1]["end"] / 60, 1)})

# Bind here (not inside the thread) so a busy port raises an error in this cell
server = make_server("0.0.0.0", PORT, app, threaded=True)
server_thread = threading.Thread(target=server.serve_forever, daemon=True)
server_thread.start()
print(f"✅ Server running on port {PORT}")

from google.colab.output import eval_js
print("Open the chat:", eval_js(f"google.colab.kernel.proxyPort({PORT})"))
