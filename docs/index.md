# Welcome to Odyssey Documentation

This documentation contains notes and guides covering various technologies including Docker and Kubernetes.

## Documentation Sections

* **Docker**
  * [Introduction](Docker/notes/1-docker-introduction.md)
  * [Basic Commands](Docker/notes/2-docker-basic-commands.md)
  * [Debugging Containers](Docker/notes/3-debugging-a-container.md)

* **Kubernetes**
  * [Introduction](Kubernetes/notes/1-kubernetes-introduction.md)
  * [Main Components](Kubernetes/notes/2-main-kube-components.md)
  * [Architecture](Kubernetes/notes/3-k8s-architecture.md)
  * [Local Setup](Kubernetes/notes/4-local-k8s-setup.md)
  * [Basic Commands](Kubernetes/notes/5-basic-kubectl-commands.md)
  * [Control Plane Components](Kubernetes/notes/6-control-plane-components.md)

## Getting Started

To work with this documentation locally:

* `mkdocs serve` - Start a local docs server with live-reloading
* `mkdocs build` - Build the static documentation site
* `mkdocs -h` - Show help options

## Documentation Structure

    docs/
    ├── index.md
    ├── Docker/
    │   └── notes/
    │       ├── 1-docker-introduction.md
    │       ├── 2-docker-basic-commands.md
    │       └── 3-debugging-a-container.md
    └── Kubernetes/
        ├── notes/
        │   ├── 1-kubernetes-introduction.md
        │   ├── 2-main-kube-components.md
        │   ├── 3-k8s-architecture.md
        │   ├── 4-local-k8s-setup.md
        │   ├── 5-basic-kubectl-commands.md
        │   └── 6-control-plane-components.md
        └── src/
            └── nginx-deployment.yaml

## Contributing

Feel free to contribute to this documentation by submitting pull requests or opening issues if you find any errors or have suggestions for improvements.
