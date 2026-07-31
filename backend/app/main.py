from app.collector.client import KubernetesClient
from app.collector.pods import PodCollector
from app.collector.nodes import NodeCollector
from app.collector.events import EventCollector


def main():
    client = KubernetesClient()

    print("=" * 50)
    print("NODES")
    print("=" * 50)

    for node in NodeCollector(client).collect():
        print(node)

    print("\n" + "=" * 50)
    print("PODS")
    print("=" * 50)

    for pod in PodCollector(client).collect():
        print(pod)

    print("\n" + "=" * 50)
    print("EVENTS")
    print("=" * 50)

    events = EventCollector(client).collect()

    for event in events[:10]:
        print(event)


if __name__ == "__main__":
    main()
