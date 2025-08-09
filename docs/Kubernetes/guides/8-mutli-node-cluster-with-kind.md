# Multi-Node Kubernetes Cluster with Kind

Kind (Kubernetes IN Docker) allows you to create multi-node Kubernetes clusters for local development and testing. This guide demonstrates how to set up a cluster with multiple worker nodes.

## Creating a Multi-Node Cluster Configuration

Create a configuration file that defines the cluster structure. We'll create a cluster with 1 control plane node and 3 worker nodes.


```yaml
kind: Cluster
apiVersion: kind.x-k8s.io/v1alpha4
nodes:
- role: control-plane
- role: worker
- role: worker
- role: worker
```

This configuration specifies:
- One control-plane node for cluster management
- Three worker nodes for running workloads

## Creating and Managing the Cluster

1. Create a basic single-node cluster:
```bash
kind create cluster --name test-kind
```
This command:
- Creates a cluster named "test-kind"
- Sets up a single control plane node
- Installs CNI (Container Network Interface)
- Configures StorageClass

2. Verify the cluster information:
```bash
kubectl cluster-info --context kind-test-kind
```

3. Create a multi-node cluster using a configuration file:
```bash
kind create cluster --config ../manifests/kind-multi-node-cluster.yaml
```
This creates a cluster with:
- 1 control plane node
- 3 worker nodes

4. Verify the nodes in your cluster:
```bash
kubectl get nodes
```

Example output:

```
NAME                 STATUS   ROLES           AGE    VERSION
kind-control-plane   Ready    control-plane   2m7s   v1.32.2
kind-worker          Ready    <none>          114s   v1.32.2
kind-worker2         Ready    <none>          113s   v1.32.2
kind-worker3         Ready    <none>          113s   v1.32.2
```

The output shows:
- One control plane node (`kind-control-plane`)
- Three worker nodes (`kind-worker`, `kind-worker2`, `kind-worker3`)
- All nodes are in `Ready` status
- The Kubernetes version running on the nodes (v1.32.2)


# Kubernetes Cluster Setup with Kind

## Current Context and Nodes

Check the current context:

```bash
kubectl config current-context
```

Output:

```
kind-kind
```

Check the current nodes:

```bash
kubectl get nodes
```

Output:

```
NAME                 STATUS   ROLES           AGE   VERSION
kind-control-plane   Ready    control-plane   23h   v1.32.2
kind-worker          Ready    <none>          23h   v1.32.2
kind-worker2         Ready    <none>          23h   v1.32.2
kind-worker3         Ready    <none>          23h   v1.32.2
```

## Creating a New Kind Cluster

Create a new Kind cluster with a specific config and Kubernetes version:

```bash
kind create cluster \
--name my-kind-cluster \
--config ../manifests/kind-multi-node-cluster.yaml \
--image kindest/node:v1.29.0
```

Output:

```
Creating cluster "my-kind-cluster" ...
 ✓ Ensuring node image (kindest/node:v1.29.0) 🖼 
 ✓ Preparing nodes 📦 📦 📦 📦  
 ✓ Writing configuration 📜 
 ✓ Starting control-plane 🕹️ 
 ✓ Installing CNI 🔌 
 ✓ Installing StorageClass 💾 
 ✓ Joining worker nodes 🚜 
Set kubectl context to "kind-my-kind-cluster"
You can now use your cluster with:

kubectl cluster-info --context kind-my-kind-cluster
```

## Verify the New Cluster

Check the nodes in the new cluster:

```bash
kubectl get nodes
```

Output:

```
NAME                            STATUS   ROLES           AGE   VERSION
my-kind-cluster-control-plane   Ready    control-plane   33s   v1.29.0
my-kind-cluster-worker          Ready    <none>          11s   v1.29.0
my-kind-cluster-worker2         Ready    <none>          11s   v1.29.0
my-kind-cluster-worker3         Ready    <none>          13s   v1.29.0
```

## Cluster Info

Get cluster details:

```bash
kubectl cluster-info
```

Output:

```
Kubernetes control plane is running at https://127.0.0.1:49349
CoreDNS is running at https://127.0.0.1:49349/api/v1/namespaces/kube-system/services/kube-dns:dns/proxy

To further debug and diagnose cluster problems, use 'kubectl cluster-info dump'.
```

## Next Steps

For more information and guides, check out the [Kind Quick Start Docs](https://kind.sigs.k8s.io/docs/user/quick-start/).


## Related file
[Simple kind cluster config](../manifests/kind-multi-node-cluster.yaml)
