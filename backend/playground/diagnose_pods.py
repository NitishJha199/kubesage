from app.collector.client import KubernetesClient
from app.collector.nodes import NodeCollector
from app.diagnosis.service import DiagnosisService


def main() -> None:
    """
    Playground script for testing the diagnosis service.
    """

    client = KubernetesClient()

    # Optional: still print nodes for visibility during development.
    nodes = NodeCollector(client).collect()

    # All diagnosis orchestration is delegated to the service.
    service = DiagnosisService(client)
    results = service.diagnose()

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
