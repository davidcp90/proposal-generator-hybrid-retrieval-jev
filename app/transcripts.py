"""Stage 1 · Whisper: client calls become timestamped chunks in a FAISS index."""
import json
import threading
from pathlib import Path

from langchain_community.vectorstores import FAISS
from langchain_core.documents import Document
from langchain_core.tools import tool
from langchain_openai import OpenAIEmbeddings

from . import config

_whisper_model = None
_db = None
_db_lock = threading.Lock()


def transcribe(path):
    """Returns [{start, end, text}] using local Whisper (optional dependency)."""
    global _whisper_model
    try:
        import torch
        import whisper
    except ImportError as e:
        raise RuntimeError("Local Whisper is not installed: pip install openai-whisper, "
                           "or upload the .json transcript instead") from e
    device = "cuda" if torch.cuda.is_available() else "cpu"
    if _whisper_model is None:
        _whisper_model = whisper.load_model(config.WHISPER_MODEL, device=device)
    r = _whisper_model.transcribe(str(path), language="es", fp16=(device == "cuda"))   # the calls are in Spanish
    return [{"start": s["start"], "end": s["end"], "text": s["text"].strip()} for s in r["segments"]]


def load_segments(path):
    """Audio goes through Whisper; a .json file is a backup transcript, loaded as is."""
    path = Path(path)
    if path.suffix == ".json":
        return json.loads(path.read_text(encoding="utf-8"))
    return transcribe(path)


def segments_to_docs(segments, client, window=60):
    """Groups segments into ~60 s windows, keeping client and times in the metadata."""
    docs, buf, start = [], [], None

    def close(end):
        docs.append(Document(" ".join(buf), metadata={
            "source": "transcript", "client": client, "start": round(start), "end": round(end)}))

    for s in segments:
        start = s["start"] if start is None else start
        buf.append(s["text"])
        if s["end"] - start >= window:
            close(s["end"]); buf, start = [], None
    if buf:
        close(segments[-1]["end"])
    return docs


def add_call(segments, client):
    """Indexes a call; creates the index on the first one. Returns the new chunks."""
    global _db
    docs = segments_to_docs(segments, client)
    with _db_lock:
        if _db is None:
            _db = FAISS.from_documents(docs, OpenAIEmbeddings(model=config.EMBEDDINGS_MODEL))
        else:
            _db.add_documents(docs)
    return docs


@tool
def search_transcripts(query: str) -> str:
    """Searches client calls (in Spanish): needs, budget, timelines, team and constraints."""
    if _db is None:
        return "No client call has been indexed yet. Ask the user to upload the call first."
    hits = _db.similarity_search(query, k=4)
    return "\n\n".join(
        f"[{d.metadata['client']} {d.metadata['start']}s-{d.metadata['end']}s] {d.page_content}"
        for d in hits)
