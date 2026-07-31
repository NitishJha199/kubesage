from app.collector.client import KubernetesClient
from app.collector.nodes import NodeCollector

client = KubernetesClient()

collector = NodeCollector(client)

nodes = collector.collect()

print("=" * 50)

for node in nodes:
    print(node)

print("=" * 50)
