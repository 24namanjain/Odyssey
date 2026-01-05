---
notion_page_id: 2dfff901-fc97-811a-90ba-c95a2a5b5681
tags:
- kubernetes
- kind
- cluster-config
- yaml
- manifests
title: Kind Multi-node Cluster Configuration
---

# Kind Multi-node Cluster Configuration

This configuration creates a Kubernetes cluster with 1 control plane node and 3 worker nodes using Kind (Kubernetes IN Docker).

## Configuration

```yaml
kind: Cluster
apiVersion: kind.x-k8s.io/v1alpha4
nodes:
- role: control-plane
- role: worker
- role: worker
- role: worker

```

## Usage

```bash
# Create cluster using this configuration
kind create cluster --name my-cluster --config kind-multi-node-cluster.yaml

# Verify the cluster
kubectl get nodes

```

## Expected Output

```plain text
NAME                 STATUS   ROLES           AGE   VERSION
kind-control-plane   Ready    control-plane   2m    v1.32.2
kind-worker          Ready    <none>          1m    v1.32.2
kind-worker2         Ready    <none>          1m    v1.32.2
kind-worker3         Ready    <none>          1m    v1.32.2

```

## Download

📥 Download YAML file

---

**Note**: This is a working reference file. You can copy the YAML content above or download the file for use with `kind create cluster --config`.