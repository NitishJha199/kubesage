from app.collector.client import KubernetesClient
from app.collector.persistent_volumes import (
    PersistentVolumeCollector,
)


def main():

    client = KubernetesClient()

    collector = PersistentVolumeCollector(client)

    volumes = collector.collect()

    for volume in volumes:
        print("=" * 80)
        print(volume)


if __name__ == "__main__":
    main()
