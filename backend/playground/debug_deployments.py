from app.collector.client import KubernetesClient
from app.collector.deployments import DeploymentCollector


def main() -> None:

    client = KubernetesClient()

    collector = DeploymentCollector(client)

    deployments = collector.collect()

    for deployment in deployments:
        print("=" * 80)
        print(deployment)


if __name__ == "__main__":
    main()
