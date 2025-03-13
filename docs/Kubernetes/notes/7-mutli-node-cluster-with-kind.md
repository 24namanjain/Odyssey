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
kind create cluster --config src/3-kind-multi-node-cluster/kind_cluster
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

Note: Unlike regular pods, you cannot directly execute commands on nodes using `kubectl exec`. To interact with nodes, you'll need to use different approaches which we'll cover in later sections.



## Related file
[Simple kind cluster config](../src/3-kind-multi-node-cluster/kind_cluster)
