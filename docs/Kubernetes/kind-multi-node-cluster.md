---
notion_page_id: 2deff901-fc97-81ea-9ec5-c2bac120530c
title: kind-multi-node-cluster
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