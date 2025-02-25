# Kubernetes Node Architecture

Each node has multiple pods.

## Essential Components Required for a Kubernetes Node:

1. **Container Runtime**: The software that is responsible for running containers.
2. **Kubelet**: Interacts with both the container and the node to ensure that containers are running in a pod.
3. **Kube Proxy**: Forwards the request to the appropriate pod or service.

## Master Processes

Four processes run on every master node:

1. **API Server**: Acts as the cluster gateway, receiving requests for cluster changes such as deployments. It validates and authenticates the requests.
2. **Scheduler**: Determines on which node a pod should be placed.
3. **Controller Manager**: Detects changes in the cluster state, such as when pods die, and requests the scheduler to take action.
4. **etcd**: A key-value store that acts as the cluster's brain. Cluster changes are stored here. The scheduler checks it for available resources, and the controller manager uses it for cluster data. It does not store application data.