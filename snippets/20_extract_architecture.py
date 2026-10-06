from typing import Literal
from pydantic import BaseModel, Field

Service = Literal["user", "device", "api_gateway", "lambda", "sagemaker", "dynamodb", "neptune",
                  "msk", "kinesis", "s3", "emr", "mwaa", "cloudwatch", "sns", "eks"]

class Component(BaseModel):
    id: str = Field(description="short identifier, no spaces")
    service: Service
    label: str = Field(description="short name shown under the icon, in Spanish")
    group: Literal["online", "data", "batch", "observability"]

class Connection(BaseModel):
    source: str
    target: str
    label: str = ""

class CostItem(BaseModel):
    item: str = Field(description="cost line as written in the proposal, in Spanish")
    usd: float = Field(description="for ranges use the high value")
    kind: Literal["consulting", "aws_monthly"]

class Architecture(BaseModel):
    title: str = Field(description="diagram title, in Spanish")
    components: list[Component]
    connections: list[Connection]
    costs: list[CostItem]

extractor = create_llm().with_structured_output(Architecture)

def extract_architecture(proposal):
    return extractor.invoke(
        "Extract the AWS architecture and the costs from this proposal. Use only services and figures present in the text. "
        "Keep the title, labels and cost items in Spanish.\n\n"
        + proposal)

if "proposal" not in globals():       # normally created by the agent cell (12)
    print("No proposal yet: asking the agent for one…")
    proposal = ask("Genera la propuesta para RitmoFit: plataforma de recomendaciones en tiempo real.")["messages"][-1].text

arch = extract_architecture(proposal)
arch.model_dump()
