---
title: Nginx Deployment Configuration
tags: [kubernetes, deployment, nginx, yaml, manifests]
---

# Nginx Deployment Configuration

This configuration creates a Kubernetes deployment running Nginx with 2 replicas.

## Configuration

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
    name: nginx-deployment
    labels:
        app: nginx
spec:
    replicas: 2
    selector:
        matchLabels:
            app: nginx
    template:
        metadata:
            labels:
                app: nginx
        spec:
            containers:
            - name: nginx
              image: nginx:1.16
              ports:
              - containerPort: 80
```

## Usage

```bash
# Apply the deployment
kubectl apply -f nginx-deployment.yaml

# Check deployment status
kubectl get deployments

# Check pods
kubectl get pods

# Scale the deployment
kubectl scale deployment nginx-deployment --replicas=3
```

## Expected Output

```bash
# kubectl get deployments
NAME               READY   UP-TO-DATE   AVAILABLE   AGE
nginx-deployment   2/2     2            2           30s

# kubectl get pods
NAME                                READY   STATUS    RESTARTS   AGE
nginx-deployment-66b6c48dd5-abc12   1/1     Running   0          30s
nginx-deployment-66b6c48dd5-def34   1/1     Running   0          30s
```

## Download

[:octicons-download-16: Download YAML file](nginx-deployment.yaml){ .md-button .md-button--primary }

---

**Note**: This is a working reference file. You can copy the YAML content above or download the file for use with `kubectl apply -f`.
