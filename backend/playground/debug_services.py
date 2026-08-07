from app.collector.client import KubernetesClient
from app.collector.services import ServiceCollector


def main() -> None:
    client = KubernetesClient()

    services = ServiceCollector(client).collect()

    for service in services:
        print("=" * 80)
        print(service)


if __name__ == "__main__":
    main()
