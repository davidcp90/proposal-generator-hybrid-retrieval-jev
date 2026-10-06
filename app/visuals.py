"""Bonus: proposal → typed architecture → diagram with AWS icons → slide from the image model."""
import base64
import uuid
from typing import Literal

from openai import OpenAI
from pydantic import BaseModel, Field

from . import config
from .llm import create_llm

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


# Cluster titles are shown to the client, so they stay in Spanish
GROUPS = {"online": "En línea", "data": "Datos", "batch": "Batch diario", "observability": "Observabilidad"}

_extractor = None
_openai = None


def extract_architecture(proposal):
    global _extractor
    if _extractor is None:
        _extractor = create_llm().with_structured_output(Architecture)
    return _extractor.invoke(
        "Extract the AWS architecture and the costs from this proposal. Use only services and figures present in the text. "
        "Keep the title, labels and cost items in Spanish.\n\n"
        + proposal)


def draw(arch, filename):
    """Draws the diagram with the official AWS icons (needs Graphviz). Returns the PNG path."""
    from diagrams import Cluster, Diagram, Edge
    from diagrams.aws.analytics import EMR, KinesisDataStreams, ManagedStreamingForKafka
    from diagrams.aws.compute import EKS, Lambda
    from diagrams.aws.database import Dynamodb, Neptune
    from diagrams.aws.integration import SNS
    from diagrams.aws.management import AmazonManagedWorkflowsApacheAirflow, Cloudwatch
    from diagrams.aws.ml import Sagemaker
    from diagrams.aws.network import APIGateway
    from diagrams.aws.storage import S3
    from diagrams.onprem.client import Client, User

    icons = {"user": User, "device": Client, "api_gateway": APIGateway, "lambda": Lambda,
             "sagemaker": Sagemaker, "dynamodb": Dynamodb, "neptune": Neptune, "msk": ManagedStreamingForKafka,
             "kinesis": KinesisDataStreams, "s3": S3, "emr": EMR, "mwaa": AmazonManagedWorkflowsApacheAirflow,
             "cloudwatch": Cloudwatch, "sns": SNS, "eks": EKS}
    with Diagram(arch.title, filename=str(filename), outformat="png", show=False, direction="LR",
                 graph_attr={"fontsize": "20", "pad": "0.4"}):
        nodes = {}
        for g, name in GROUPS.items():
            comps = [c for c in arch.components if c.group == g]
            if comps:
                with Cluster(name):
                    for c in comps:
                        nodes[c.id] = icons[c.service](c.label)
        for k in arch.connections:
            if k.source in nodes and k.target in nodes:
                nodes[k.source] >> Edge(label=k.label) >> nodes[k.target]
    return f"{filename}.png"


def cost_totals(arch):
    """Totals per kind, computed in code (never by the image model)."""
    return {kind: sum(c.usd for c in arch.costs if c.kind == kind) for kind in ("consulting", "aws_monthly")}


def make_slide(arch, png, filename):
    """Turns the diagram into a 16:9 proposal slide with the pricing table. Returns the PNG path."""
    global _openai
    if _openai is None:
        _openai = OpenAI()
    totals = cost_totals(arch)
    lines = "\n".join(f"- {c.item}: USD {c.usd:,.0f}" + (" / mes" if c.kind == "aws_monthly" else "")
                      for c in arch.costs)
    prompt = f"""Turn this AWS architecture diagram into a sales proposal slide, 16:9 format,
clean and professional style, white background. All text on the slide must be in Spanish.
Keep the same AWS icons, services and arrows from the diagram. Do not add or remove services.
On the right, add a pricing table with exactly these lines:
{lines}
Total consultoría (una vez): USD {totals['consulting']:,.0f}
Total AWS estimado ilustrativo: USD {totals['aws_monthly']:,.0f} / mes
Title: {arch.title}. Provider: NubeAndina Consulting."""
    with open(png, "rb") as diagram:
        res = _openai.images.edit(             # edits from the diagram: keeps icons and arrows
            model=config.IMAGE_MODEL,
            image=diagram,
            prompt=prompt,
            size="1536x1024",                  # landscape, slide-like
            quality=config.SLIDE_QUALITY,
        )
    with open(filename, "wb") as f:
        f.write(base64.b64decode(res.data[0].b64_json))
    return str(filename)


def make_visuals(proposal):
    """Full pipeline for one proposal. Returns (arch, diagram_path, slide_path)."""
    config.IMG_DIR.mkdir(parents=True, exist_ok=True)
    name = uuid.uuid4().hex[:8]
    arch = extract_architecture(proposal)
    png = draw(arch, config.IMG_DIR / f"arch_{name}")
    slide = make_slide(arch, png, config.IMG_DIR / f"slide_{name}.png")
    return arch, png, slide
