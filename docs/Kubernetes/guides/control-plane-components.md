---
title: Control Plane Components
tags: [kubernetes, control-plane, api-server, etcd, scheduler, controller-manager, architecture]
---

# Control Plane Components

## API Server (kube-apiserver)

The API Server is the primary control plane component that exposes the Kubernetes API. It acts as the front-end for the Kubernetes control plane and is designed to scale horizontally.

Key characteristics:
- Entry point for all REST commands used to control the cluster
- Can be accessed through:
  - kubectl CLI tool
  - Direct API calls
  - Kubernetes Dashboard (Web UI)
- Validates and processes API requests
- Serves as the gateway to the cluster
- Responsible for:
  - Authentication
  - Authorization
  - Request validation
  - API object manipulation (CRUD operations)

## etcd

etcd is a distributed key-value store that serves as the cluster's primary datastore:

Key aspects:
- Stores all cluster configuration data and state
- Acts as the single source of truth for the cluster
- All cluster changes are persisted here
- Can only be accessed through the API server
- Deployment options:
  - Co-located with kube-apiserver (simpler setup)
  - As a separate external cluster (more complex but better for production)

The API server is the only component that directly communicates with etcd, ensuring:
- Consistent data access patterns
- Data integrity and security
- Proper authentication and authorization

## Scheduler (kube-scheduler)

The Scheduler is responsible for assigning newly created pods to worker nodes in the cluster.

Key responsibilities:
- Monitors for unscheduled pods
- Selects optimal nodes for pod placement
- Updates pod configuration with node assignment

Scheduling process:
1. New pods are created without node assignments (unscheduled state)
2. Pod information is stored in etcd without a nodeName property
3. Scheduler continuously monitors API server for unscheduled pods
4. When found, scheduler selects an appropriate worker node
5. Updates the pod's nodeName property to mark it as scheduled

Deployment considerations:
- Should be deployed on highly available nodes
- Often co-located with other control plane components like kube-apiserver
- Critical for efficient cluster resource utilization

## Controller Manager (kube-controller-manager)

The Controller Manager is a core component that manages the cluster's state and ensures the desired state is maintained:

Key responsibilities:
- Manages the lifecycle of various Kubernetes resources
- Ensures the desired state is maintained
- Handles resource allocation and management
- Manages node and pod health
- Implements various controllers (e.g., Node Controller, Job Controller, Endpoint Controller)

Deployment considerations:
- Should be deployed on highly available nodes
- Often co-located with other control plane components like kube-apiserver
- Handles resource allocation and management
- Manages node and pod health
- Implements various controllers (e.g., Node Controller, Job Controller, Endpoint Controller)

## Cloud Controller Manager (cloud-controller-manager)

The Cloud Controller Manager is a specialized component that manages cloud-specific resources:

Key responsibilities:
- Manages cloud-specific resources (e.g., load balancers, storage, and network)
- Interfaces with cloud provider APIs
- Handles resource allocation and management
- Manages node and pod health
- Implements various controllers (e.g., Node Controller, Job Controller, Endpoint Controller)

Deployment considerations:
- Should be deployed on highly available nodes
- Often co-located with other control plane components like kube-apiserver
- Handles resource allocation and management
- Manages node and pod health

## Summary

The Kubernetes control plane consists of five main components:

1. **API Server**: The gateway to the cluster, handling all API requests and authentication
2. **etcd**: The distributed database storing all cluster state and configuration
3. **Scheduler**: Assigns pods to nodes based on resource requirements and constraints
4. **Controller Manager**: Maintains desired state and manages various controllers
5. **Cloud Controller Manager**: Handles cloud-provider specific resources and integration

These components work together to:
- Maintain cluster state
- Handle scheduling and resource allocation
- Manage cloud provider integration
- Ensure high availability and scalability
- Provide a unified API interface for cluster management

