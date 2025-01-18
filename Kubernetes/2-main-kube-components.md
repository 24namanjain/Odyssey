# Main Kubernetes Components

## Node
- A **Node** is a server in the Kubernetes cluster.
- It can be a physical or virtual machine.
- Each node runs pods and is managed by the Kubernetes master.
- Nodes contain the necessary services to run pods and are responsible for maintaining the running pods.

## Pod
- A **Pod** is the smallest and simplest Kubernetes object.
- It represents a single instance of a running process in the cluster and can contain one or more containers.
- Each pod gets its own IP address, and when a pod is re-created, it gets a new IP address.
- Pods are ephemeral and can be replaced by new pods if they fail or are terminated.

## Service
- A **Service** provides a permanent IP address and DNS name for a set of pods.
- It acts as an abstraction layer that defines a logical set of pods and a policy by which to access them.
- The lifecycle of a service is not connected with the lifecycle of the pods it targets, ensuring a stable network endpoint for accessing the pods.

## Ingress
- An **Ingress** is an API object that manages external access to services within a cluster, typically HTTP.
- Ingress can provide load balancing, SSL termination, and name-based virtual hosting.
- It allows you to define rules for routing traffic to different services based on the URL path or host.

## ConfigMap
- A **ConfigMap** is used to store external configuration of the application.
- It allows you to decouple configuration artifacts from image content to keep containerized applications portable.

## Secret
- A **Secret** is used to store secret data, such as passwords, OAuth tokens, and SSH keys.
- The data is base64 encoded and can be mounted as files or exposed as environment variables in a pod.

## Volume
- A **Volume** attaches a physical storage which can be either on a local machine or outside of the Kubernetes cluster.
- Volumes allow data to persist across pod restarts and can be shared between containers in the same pod.
- Different types of volumes are available, such as `emptyDir`, `hostPath`, `persistentVolumeClaim`, and more, each with its own use case and characteristics.
- Volumes are defined in the pod specification and are mounted into the containers at specified paths.

## Deployment
- A **Deployment** is used to manage stateless applications.
- It provides declarative updates to applications and ensures that the desired number of pod replicas are running.
- Deployments allow you to roll out updates, roll back to previous versions, and scale the number of replicas easily.

## StatefulSet
- A **StatefulSet** is used to manage stateful applications or databases.
- It ensures that each pod has a unique, stable network identity and persistent storage.
- StatefulSets maintain the order and uniqueness of pods, which is crucial for applications that require stable, persistent storage and ordered deployment and scaling.
- They are typically used for applications like databases, where the state needs to be preserved across pod restarts and rescheduling.