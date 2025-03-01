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

## Component Planes in Kubernetes

Kubernetes components can be categorized into two main planes:

1. **Control Plane** (Master Components):
   - Contains the master processes (API Server, Scheduler, Controller Manager, etcd)
   - Acts as the brain of the cluster
   - Users and administrators interact with this plane through kubectl or API
   - Makes global decisions about the cluster
   - Handles orchestration and management

2. **Compute Plane** (Worker Components):
   - Contains the worker node components (Container Runtime, Kubelet, Kube Proxy)
   - Runs the actual workloads
   - Never interacted with directly by users
   - Receives instructions from Control Plane
   - Executes the actual container operations

This architecture ensures a clear separation of concerns, where users only need to interact with the Control Plane, which then manages and coordinates with the Compute Plane components.
