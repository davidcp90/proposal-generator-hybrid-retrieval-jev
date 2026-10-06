from diagrams import Diagram, Cluster, Edge
from diagrams.aws.analytics import EMR, ManagedStreamingForKafka, KinesisDataStreams
from diagrams.aws.compute import Lambda, EKS
from diagrams.aws.database import Dynamodb, Neptune
from diagrams.aws.integration import SNS
from diagrams.aws.management import Cloudwatch, AmazonManagedWorkflowsApacheAirflow
from diagrams.aws.ml import Sagemaker
from diagrams.aws.network import APIGateway
from diagrams.aws.storage import S3
from diagrams.onprem.client import User, Client
from IPython.display import Image, display

ICONS = {"user": User, "device": Client, "api_gateway": APIGateway, "lambda": Lambda,
         "sagemaker": Sagemaker, "dynamodb": Dynamodb, "neptune": Neptune, "msk": ManagedStreamingForKafka,
         "kinesis": KinesisDataStreams, "s3": S3, "emr": EMR, "mwaa": AmazonManagedWorkflowsApacheAirflow,
         "cloudwatch": Cloudwatch, "sns": SNS, "eks": EKS}
# Cluster titles are shown to the client, so they stay in Spanish
GROUPS = {"online": "En línea", "data": "Datos", "batch": "Batch diario", "observability": "Observabilidad"}

def draw(arch, filename="architecture"):
    with Diagram(arch.title, filename=filename, outformat="png", show=False, direction="LR",
                 graph_attr={"fontsize": "20", "pad": "0.4"}):
        nodes = {}
        for g, name in GROUPS.items():
            comps = [c for c in arch.components if c.group == g]
            if comps:
                with Cluster(name):
                    for c in comps:
                        nodes[c.id] = ICONS[c.service](c.label)
        for k in arch.connections:
            if k.source in nodes and k.target in nodes:
                nodes[k.source] >> Edge(label=k.label) >> nodes[k.target]
    return f"{filename}.png"

png = draw(arch)
display(Image(png))
