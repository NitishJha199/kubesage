from kubernetes import client, config


class KubernetesClient:
    """
    Wrapper around the Kubernetes Python client.

    All Kubernetes SDK calls should go through this class.
    """

    def __init__(self):
        config.load_kube_config()

        self.core = client.CoreV1Api()
        self.apps = client.AppsV1Api()

    def list_pods(self):
        """Return all pods across all namespaces."""
        return self.core.list_pod_for_all_namespaces()

    def list_nodes(self):
        """Return all nodes."""
        return self.core.list_node()

    def list_events(self):
        """Return all events across all namespaces."""
        return self.core.list_event_for_all_namespaces()
