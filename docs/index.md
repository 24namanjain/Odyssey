# Welcome to Odyssey Documentation

This documentation contains notes and guides covering various technologies including Docker and Kubernetes.

## Documentation Sections

* **Personal**
  * [Important Links](_personal/links.md)
  * [TODOs](_personal/todo.md)

* **Docker**
  * Guides
    * [Introduction](Docker/guides/1-docker-introduction.md)
    * [Debugging Containers](Docker/guides/3-debugging-a-container.md)
  * Commands
    * [Basic Commands](Docker/commands/2-docker-basic-commands.md)

* **Kubernetes**
  * Guides
    * [Introduction](Kubernetes/guides/1-kubernetes-introduction.md)
    * [Main Components](Kubernetes/guides/2-main-kube-components.md)
    * [Architecture](Kubernetes/guides/3-k8s-architecture.md)
    * [Local Setup](Kubernetes/guides/4-local-k8s-setup.md)
    * [Control Plane Components](Kubernetes/guides/6-control-plane-components.md)
    * [Multi-node Cluster with Kind](Kubernetes/guides/8-mutli-node-cluster-with-kind.md)
    * [Running Containers in Kubernetes](Kubernetes/guides/9-running-your-containers-in-kube.md)
  * Commands
    * [Basic kubectl Commands](Kubernetes/commands/5-basic-kubectl-commands.md)
    * [Minikube Commands](Kubernetes/commands/7-minikube-cluster-cmds.md)

* **System Design**
  * Guides
    * [Overview](SystemDesign/guides/README.md)
  * References
    * [Overview](SystemDesign/references/README.md)

## Getting Started

To work with this documentation locally:

* `mkdocs serve` - Start a local docs server with live-reloading
* `mkdocs build` - Build the static documentation site
* `mkdocs -h` - Show help options

## Documentation Structure

    docs/
    ├── index.md
    ├── _personal/
    │   ├── links.md
    │   └── todo.md
    ├── Docker/
    │   ├── guides/
    │   │   ├── 1-docker-introduction.md
    │   │   └── 3-debugging-a-container.md
    │   └── commands/
    │       └── 2-docker-basic-commands.md
    └── Kubernetes/
        ├── guides/
        │   ├── 1-kubernetes-introduction.md
        │   ├── 2-main-kube-components.md
        │   ├── 3-k8s-architecture.md
        │   ├── 4-local-k8s-setup.md
        │   ├── 6-control-plane-components.md
        │   ├── 8-mutli-node-cluster-with-kind.md
        │   └── 9-running-your-containers-in-kube.md
        ├── commands/
        │   ├── 5-basic-kubectl-commands.md
        │   └── 7-minikube-cluster-cmds.md
        └── manifests/
            ├── kind-multi-node-cluster.yaml
            ├── nginx-deployment.yaml
            └── nginx-pod.yaml
        
    ├── SystemDesign/
    │   ├── guides/
    │   │   └── README.md
    │   └── references/
    │       └── README.md

## Contributing

Feel free to contribute to this documentation by submitting pull requests or opening issues if you find any errors or have suggestions for improvements.
