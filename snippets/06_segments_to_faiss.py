from langchain_core.documents import Document
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings

def segments_to_docs(segments, client, window=60):
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

transcript_docs = segments_to_docs(segments, "ritmofit")
transcript_db = FAISS.from_documents(transcript_docs, OpenAIEmbeddings(model=EMBEDDINGS_MODEL))
print(len(transcript_docs), "chunks indexed")
