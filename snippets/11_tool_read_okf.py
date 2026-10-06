@tool
def read_okf(path: str = "index.md") -> str:
    """Reads the NubeAndina OKF knowledge base (in Spanish): services, rates, AWS fundamentals and reference costs.
    Start at 'index.md' and follow the links. Examples: 'company/rate-card.md', 'aws/basics/pricing-models.md'."""
    p = (OKF / path).resolve()
    if not p.is_relative_to(OKF.resolve()):
        return "Path outside OKF."
    if p.is_dir():
        p = p / "index.md"
    if not p.exists():
        return f"{path} does not exist. Read the folder's index.md."
    post = frontmatter.load(p)
    return f"[okf:{p.relative_to(OKF.resolve())}] {post.metadata}\n\n{post.content}"

# ✅ Checkpoint
print(read_okf.invoke({"path": "company/rate-card.md"}))
