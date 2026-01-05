---
notion_page_id: 2deff901-fc97-81b1-8ace-fdf206cdfeb9
title: local-k8s-setup
---

# Local Kubernetes Setup with Minikube

## Prerequisites

Install Hyperkit and Minikube using Homebrew:

```bash
brew install hyperkit
brew install minikube

```

## Starting Minikube

Start Minikube with the following command:

```bash
minikube start

```

Example output:

```bash
😄  minikube v1.34.0 on Darwin 15.0.1 (arm64)
✨  Automatically selected the docker driver. Other choices: ssh, podman (experimental), vfkit (experimental)
📌  Using Docker Desktop driver with root privileges
👍  Starting "minikube" primary control-plane node in "minikube" cluster
🚜  Pulling base image v0.0.45 ...
💾  Downloading Kubernetes v1.31.0 preload ...
    > preloaded-images-k8s-v18-v1...:  307.61 MiB / 307.61 MiB  100.00% 9.50 Mi
    > gcr.io/k8s-minikube/kicbase...:  441.45 MiB / 441.45 MiB  100.00% 12.26 M
🔥  Creating docker container (CPUs=2, Memory=4000MB) ...
🐳  Preparing Kubernetes v1.31.0 on Docker 27.2.0 ...
    ▪ Generating certificates and keys ...
    ▪ Booting up control plane ...
    ▪ Configuring RBAC rules ...
🔗  Configuring bridge CNI (Container Networking Interface) ...
🔎  Verifying Kubernetes components...
    ▪ Using image gcr.io/k8s-minikube/storage-provisioner:v5
🌟  Enabled addons: default-storageclass, storage-provisioner
🏄  Done! kubectl is now configured to use "minikube" cluster and "default" namespace by default

```

Check the status of Minikube:

```bash
minikube status

```

Example output:

```bash
minikube
type: Control Plane
host: Running
kubelet: Running
apiserver: Running
kubeconfig: Configured

```

## Using kubectl

Check the Kubernetes version:

```bash
kubectl version

```

Example output:

```bash
Client Version: v1.31.1
Kustomize Version: v5.4.2
Server Version: v1.31.0

```

Check for existing pods and services:

```bash
kubectl get pod
kubectl get services

```

Example output:

```bash
No resources found in default namespace.

NAME         TYPE        CLUSTER-IP   EXTERNAL-IP   PORT(S)   AGE
kubernetes   ClusterIP   10.96.0.1    <none>        443/TCP   5m12s

```

## Creating a Deployment

Create a deployment using the `nginx` image:

```bash
kubectl create deployment nginx-delp --image=nginx

```

Example output:

```bash
deployment.apps/nginx-delp created

```

Check the deployment status:

```bash
kubectl get deployment

```

Example output:

```bash
NAME         READY   UP-TO-DATE   AVAILABLE   AGE
nginx-depl   1/1     1            1           6s

```

Check the replicaset:

```bash
kubectl get replicaset

```

Example output:

```bash
NAME                    DESIRED   CURRENT   READY   AGE
nginx-depl-5796b5c499   1         1         1       9d

```

Check the pod status:

```bash
kubectl get pod

```

Example output:

```bash
NAME                          READY   STATUS         RESTARTS   AGE
nginx-delp-69499d958c-bj76r   0/1     ErrImagePull   0          15s

```

## Deleting a Deployment

Delete the deployment:

```bash
kubectl delete deployment nginx-delp

```

Example output:

```bash
deployment.apps "nginx-delp" deleted

```

Recreate the deployment with the correct image:

```bash
kubectl create deployment nginx-delp --image=nginx

```

Example output:

```bash
deployment.apps/nginx-delp created

```

Check the replicaset again:

```bash
kubectl get replicaset

```

Example output:

```bash
NAME                    DESIRED   CURRENT   READY   AGE
nginx-depl-5796b5c499   1         1         1       9d

```