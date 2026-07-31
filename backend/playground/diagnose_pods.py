from app.collector.client import KubernetesClient
from app.collector.events import EventCollector
from app.collector.nodes import NodeCollector
from app.collector.pods import PodCollector
from app.diagnosis.pod import PodDiagnoser


def main() -> None:
    """
    Playground script for testing collectors and the diagnosis engine.
    """

    client = KubernetesClient()

    node_collector = NodeCollector(client)
    pod_collector = PodCollector(client)
    event_collector = EventCollector(client)

    nodes = node_collector.collect()
    pods = pod_collector.collect()
    events = event_collector.collect()

    diagnoser = PodDiagnoser(pods, events)
    results = diagnoser.diagnose()

    print("=" * 60)
    print("NODES")
    print("=" * 60)

    for node in nodes:
        print(node)

    print("\n" + "=" * 60)
    print("POD DIAGNOSIS")
    print("=" * 60)

    if not results:
        print("No issues detected.")
    else:
        for result in results:
            print(result)


if __name__ == "__main__":
    main()
