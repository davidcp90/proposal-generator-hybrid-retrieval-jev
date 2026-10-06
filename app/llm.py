from langchain_openai import ChatOpenAI

from . import config


def create_llm():
    # A stuck request fails after 2 min instead of hanging (OpenAI's default is 10 min, retried twice)
    limits = dict(timeout=120, max_retries=1)
    if config.MODEL.startswith("gpt-4"):       # non-reasoning fallback, e.g. "gpt-4.1-mini"
        return ChatOpenAI(model=config.MODEL, temperature=0.2, **limits)
    return ChatOpenAI(model=config.MODEL, reasoning_effort=config.EFFORT, **limits)   # reasoning models: no temperature
