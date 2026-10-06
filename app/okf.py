"""Stage 2 · OKF: the curated knowledge base (services, rates, AWS basics), read by path."""
import frontmatter
from langchain_core.tools import tool

from . import config


def validate_okf():
    """Returns the OKF files without the required `type` (log.md is exempt)."""
    return [str(p) for p in config.OKF_DIR.rglob("*.md")
            if p.name != "log.md" and not frontmatter.load(p).get("type")]


@tool
def read_okf(path: str = "index.md") -> str:
    """Reads the NubeAndina OKF knowledge base (in Spanish): services, rates, AWS fundamentals and reference costs.
    Start at 'index.md' and follow the links. Examples: 'company/rate-card.md', 'aws/basics/pricing-models.md'."""
    root = config.OKF_DIR.resolve()
    p = (root / path).resolve()
    if not p.is_relative_to(root):
        return "Path outside OKF."
    if p.is_dir():
        p = p / "index.md"
    if not p.exists():
        return f"{path} does not exist. Read the folder's index.md."
    post = frontmatter.load(p)
    return f"[okf:{p.relative_to(root)}] {post.metadata}\n\n{post.content}"
