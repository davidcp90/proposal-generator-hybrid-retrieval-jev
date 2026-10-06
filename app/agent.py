"""The proposal agent: transcripts + OKF tools, memory per session."""
from langchain.agents import create_agent
from langgraph.checkpoint.memory import InMemorySaver

from .llm import create_llm
from .okf import read_okf
from .transcripts import search_transcripts

SYSTEM = """You are the technical sales proposal generator for NubeAndina Consulting.
The sales team uses you to prepare AWS services proposals based on calls with clients.
Always answer in Spanish: the clients, the call and the knowledge base are in Spanish.
Process:
1. search_transcripts: the client's needs, budget, timelines, team and constraints.
2. read_okf starting at index.md: services in company/services/, prices in company/rate-card.md,
   pattern in aws/patterns/, fundamentals in aws/basics/, AWS costs in aws/basics/pricing-models.md.
Rules:
- Consulting prices ONLY from company/rate-card.md. If a service is not there, say so and do not quote it.
- AWS costs ONLY from aws/basics/pricing-models.md, labeled as "estimado ilustrativo".
- Respect the client's constraints (team, budget, timeline). If a fact is missing, list it under Supuestos.
Proposal format (section titles in Spanish): 1) Necesidad del cliente (cite [client Xs-Ys])
2) Arquitectura propuesta 3) Servicios AWS y costo mensual estimado
4) Servicios de consultoría (table with price) 5) Total y supuestos
6) Fuentes (okf: paths and call fragments).
For specific questions, answer briefly, with the source."""

_agent = None


def get_agent():
    global _agent
    if _agent is None:
        _agent = create_agent(
            model=create_llm(),
            tools=[search_transcripts, read_okf],
            system_prompt=SYSTEM,
            checkpointer=InMemorySaver(),
        )
    return _agent


def ask(msg, session="demo"):
    return get_agent().invoke({"messages": [{"role": "user", "content": msg}]},
                              config={"configurable": {"thread_id": session},
                                      "recursion_limit": 40})    # caps tool-call loops (~20 tool calls)
