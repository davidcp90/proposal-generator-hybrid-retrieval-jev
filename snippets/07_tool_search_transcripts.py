from langchain_core.tools import tool

@tool
def search_transcripts(query: str) -> str:
    """Searches client calls (in Spanish): needs, budget, timelines, team and constraints."""
    hits = transcript_db.similarity_search(query, k=4)
    return "\n\n".join(
        f"[{d.metadata['client']} {d.metadata['start']}s-{d.metadata['end']}s] {d.page_content}"
        for d in hits)

# ✅ Checkpoint (the call is in Spanish, so Spanish queries match best)
print(search_transcripts.invoke("presupuesto"))
