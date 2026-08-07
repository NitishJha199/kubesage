from app.collector.client import KubernetesClient
from app.collector.persistent_volume_claims import (
    PersistentVolumeClaimCollector,
)


def main() -> None:

    client = KubernetesClient()

    pvcs = PersistentVolumeClaimCollector(client).collect()

    for pvc in pvcs:
        print("=" * 80)
        print(pvc)


if __name__ == "__main__":
    main()
