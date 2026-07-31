from kubernetes import client, config

config.load_kube_config()

v1 = client.CoreV1Api()

nodes = v1.list_node()

print("=" * 50)
print("Connected to Kubernetes")
print("=" * 50)

for node in nodes.items:
    print(node.metadata.name)
