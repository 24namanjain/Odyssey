---
notion_page_id: 2deff901-fc97-819e-9bc2-e2e649818395
title: kubernetes-introduction
---

# Kubernetes Introduction

Kubernetes is an open-source platform designed to automate deploying, scaling, and operating application containers. It groups containers that make up an application into logical units for easy management and discovery.

## Key Concepts

1. **Cluster**: A set of nodes (physical or virtual machines) that run containerized applications managed by Kubernetes.

1. **Node**: A single machine in a Kubernetes cluster, which can be either a physical or virtual machine.

1. **Pod**: The smallest and simplest Kubernetes object. A pod represents a single instance of a running process in a cluster and can contain one or more containers.

1. **Service**: An abstraction that defines a logical set of pods and a policy by which to access them.

1. **Deployment**: A controller that provides declarative updates to applications. It manages the deployment of pods and ensures the desired number of replicas are running.

## Benefits of Kubernetes

1. **Scalability**: Automatically scale applications up or down based on demand.

1. **Portability**: Run applications consistently across different environments.

1. **High Availability**: Ensure applications are always running and available.

1. **Resource Efficiency**: Optimize the use of resources by managing containerized applications efficiently.

1. **Self-Healing**: Automatically replace or reschedule containers that fail, are terminated, or are unresponsive.

## How Kubernetes Works

1. **Kubernetes Master**: The control plane that manages the cluster. It consists of components like the API server, scheduler, and controller manager.

1. **Kubelet**: An agent that runs on each node in the cluster and ensures containers are running in a pod.

1. **kubectl**: A command-line tool for interacting with the Kubernetes API server and managing Kubernetes resources.

By using Kubernetes, developers can deploy and manage applications at scale, ensuring high availability and efficient use of resources.