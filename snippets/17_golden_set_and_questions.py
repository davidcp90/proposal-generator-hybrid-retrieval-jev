# Golden set: inputs stay in Spanish, as the sales team would write them
golden = [
  {"input": "Genera la propuesta para RitmoFit: plataforma de recomendaciones en tiempo real.",
   "type": "proposal"},
  {"input": "¿Cuánto cuesta un Well-Architected Review?", "type": "direct_answer"},
  {"input": "¿Cuál es el presupuesto de RitmoFit para la fase 1?", "type": "direct_answer"},
  {"input": "¿Pueden operar la plataforma cada mes después del MVP?", "type": "direct_answer"},
  {"input": "Cotiza una migración a Azure para RitmoFit", "type": "out_of_catalog"},
]

QUESTIONS = {
  "type": {"type": "choice",
    "instructions": "What type of answer did the agent give?",
    "criteria": {
      "proposal": "proposal with architecture, services and prices",
      "direct_answer": "answers a specific question",
      "out_of_catalog": "states that the service is not offered and gives no price",
      "hallucination": "offers a service or price that is not in the context"}},
  "prices_ok": {"type": "noul",
    "instructions": "Does every consulting price in the answer appear exactly the same in the rate-card.md context? If there are no prices, answer yes."},
  "constraints_ok": {"type": "noul",
    "instructions": "Does the answer respect the client's constraints in the transcript: managed services without Kubernetes, a budget of USD 25,000 and an MVP in 10 weeks?"},
  "coverage": {"type": "score",
    "instructions": "How complete is the answer relative to what the user asked?",
    "criteria": ["does not answer", "answers part of it", "answers the main point, missing details", "complete and with sources"]},
}
