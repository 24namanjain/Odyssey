---
notion_page_id: 2deff901-fc97-8110-8980-d78de05e41a5
title: k8s-architecture
---

# Kubernetes Node Architecture

Each node has multiple pods.

## Essential Components Required for a Kubernetes Node:

1. **Container Runtime**: The software that is responsible for running containers.

1. **Kubelet**: Interacts with both the container and the node to ensure that containers are running in a pod.

1. **Kube Proxy**: Forwards the request to the appropriate pod or service.

## Master Processes

Four processes run on every master node:

1. **API Server**: Acts as the cluster gateway, receiving requests for cluster changes such as deployments. It validates and authenticates the requests.

1. **Scheduler**: Determines on which node a pod should be placed.

1. **Controller Manager**: Detects changes in the cluster state, such as when pods die, and requests the scheduler to take action.

1. **etcd**: A key-value store that acts as the cluster's brain. Cluster changes are stored here. The scheduler checks it for available resources, and the controller manager uses it for cluster data. It does not store application data.

## Component Planes in Kubernetes

Kubernetes components can be categorized into two main planes:

1. **Control Plane** (Master Components):

1. **Compute Plane** (Worker Components):

This architecture ensures a clear separation of concerns, where users only need to interact with the Control Plane, which then manages and coordinates with the Compute Plane components.