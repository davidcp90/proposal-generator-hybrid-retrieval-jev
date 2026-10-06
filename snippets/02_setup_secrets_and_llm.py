import os
from google.colab import userdata

def secret(name, required=False):
    try:
        return userdata.get(name)
    except Exception:
        if required:
            raise RuntimeError(f"Missing Colab secret {name}")
        print(f"⚠️ No {name}")
        return None

os.environ["OPENAI_API_KEY"] = secret("OPENAI_API_KEY", required=True)
os.environ["JEV_API_KEY"] = secret("JEV_API_KEY", required=True)

# Chat model: cheap, with tool calling. Change it here if your account doesn't have it.
MODEL = "gpt-6-luna"               # cheapest in the GPT-6 line (USD 0.10 / 0.50 per 1M tokens)
EFFORT = "medium"                  # reasoning: "low" is cheaper and faster, "medium" gives better proposals
EMBEDDINGS_MODEL = "text-embedding-3-small"
IMAGE_MODEL = "gpt-image-2.5-flare"     # bonus: fast and cheap

from langchain_openai import ChatOpenAI

def create_llm():
    # A stuck request fails after 2 min instead of hanging (OpenAI's default is 10 min, retried twice)
    limits = dict(timeout=120, max_retries=1)
    if MODEL.startswith("gpt-4"):      # non-reasoning fallback, e.g. "gpt-4.1-mini"
        return ChatOpenAI(model=MODEL, temperature=0.2, **limits)
    return ChatOpenAI(model=MODEL, reasoning_effort=EFFORT, **limits)    # reasoning models: no temperature

print(create_llm().invoke("Reply only: ready").text)
