import json, threading
from flask import Flask, request, jsonify, render_template_string
from werkzeug.serving import make_server
from werkzeug.utils import secure_filename
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings

PORT = 5002

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
    r = ask(data["msg"], data.get("session_id", "default"))
    return jsonify({"msg": r["messages"][-1].text})

@app.route("/upload_audio", methods=["POST"])
def upload_audio():
    global transcript_db
    f = request.files["audio"]
    client = request.form.get("client", "").strip() or "unknown"
    path = f"/content/{secure_filename(f.filename)}"
    f.save(path)
    segs = json.load(open(path)) if path.endswith(".json") else transcribe(path)   # .json = backup transcript
    if not segs:
        return jsonify({"error": "empty transcript"}), 400
    new_docs = segments_to_docs(segs, client)
    if "transcript_db" in globals():
        transcript_db.add_documents(new_docs)
    else:                                 # no call indexed yet: create the index here
        transcript_db = FAISS.from_documents(new_docs, OpenAIEmbeddings(model=EMBEDDINGS_MODEL))
    return jsonify({"client": client, "chunks": len(new_docs), "minutes": round(segs[-1]["end"] / 60, 1)})

# Bind here (not inside the thread) so a busy port raises an error in this cell
server = make_server("0.0.0.0", PORT, app, threaded=True)
server_thread = threading.Thread(target=server.serve_forever, daemon=True)
server_thread.start()
print(f"✅ Server running on port {PORT}")

from google.colab.output import eval_js
print("Open the chat:", eval_js(f"google.colab.kernel.proxyPort({PORT})"))
# Fallback if the proxy doesn't open: !npx localtunnel --port 5002  (as in raglab.ipynb)
