---
notion_page_id: 2dfff901-fc97-81d6-8d37-ec01f78293ea
tags:
- kubernetes
- pod
- nginx
- yaml
- manifests
title: Nginx Pod Configuration
---

# Nginx Pod Configuration

This configuration creates a simple Kubernetes pod running Nginx.

## Configuration

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: nginx-pod
spec:
  containers:
    - name: nginx-container
      image: nginx:latest

```

## Usage

```bash
# Apply the pod
kubectl apply -f nginx-pod.yaml

# Check pod status
kubectl get pods

# View pod logs
kubectl logs nginx-pod

# Access the pod
kubectl exec -it nginx-pod -- /bin/bash

# Delete the pod
kubectl delete pod nginx-pod

```

## Expected Output

```bash
# kubectl get pods
NAME        READY   STATUS    RESTARTS   AGE
nginx-pod   1/1     Running   0          30s

# kubectl logs nginx-pod
/docker-entrypoint.sh: /docker-entrypoint.d/ is not empty, will attempt to perform configuration
/docker-entrypoint.sh: Looking for /docker-entrypoint.d/
/docker-entrypoint.sh: Launching /docker-entrypoint.d/10-listen-on-ipv6-by-default.sh
...

```

## Download

📥 Download YAML file

---

**Note**: This is a working reference file. You can copy the YAML content above or download the file for use with `kubectl apply -f`.