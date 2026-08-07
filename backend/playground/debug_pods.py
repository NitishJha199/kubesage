from app.collector.client import KubernetesClient
from app.collector.pods import PodCollector


def main() -> None:
    client = KubernetesClient()

    collector = PodCollector(client)

    pods = collector.collect()

    for pod in pods:
        print("=" * 80)
        print(f"Pod: {pod.namespace}/{pod.name}")

        for container in pod.containers:
            print(f"Container      : {container.name}")
            print(f"State          : {container.state}")
            print(f"Reason         : {container.reason}")
            print(f"Last State     : {container.last_state}")
            print(f"Last Reason    : {container.last_reason}")
            print(f"Exit Code      : {container.exit_code}")
            print(f"Signal         : {container.signal}")
            print(f"Restart Count  : {container.restart_count}")
            print(f"Ready          : {container.ready}")
            print(f"Started At     : {container.started_at}")
            print(f"Finished At    : {container.finished_at}")


if __name__ == "__main__":
    main()
