---
notion_page_id: 2dfff901-fc97-819f-bf6f-fa349e696b22
tags:
- kubernetes
- kubectl
- commands
- cli
- pods
- deployments
title: Basic kubectl Commands
---

# Basic kubectl Commands

```bash
kubectl create deployment nginx-depl --image=nginx
deployment.apps/nginx-depl created

kubectl get pod  
NAME                          READY   STATUS    RESTARTS     AGE
nginx-depl-5796b5c499-2rhcn   1/1     Running   1 (6d ago)   9d

# 
kubectl get replicaset
NAME                    DESIRED   CURRENT   READY   AGE
nginx-depl-5796b5c499   1         1         1       9d

kubectl delete deployment nginx-depl              
deployment.apps "nginx-depl" deleted

kubectl create deployment nginx-depl --image=nginx
deployment.apps/nginx-depl created

```

1. CRUD commands

```bash
kubectl create deployment [name]

kubectl edit deployment [name]

kubectl delete deployment [name]

```

1. Status of different K8s components

```bash
kubectl get nodes | pod | services | replicaset | deployment

```

1. Debugging pods

### Example

```bash
> kubectl create deployment nginx-depl --image=nginx
deployment.apps/nginx-depl created

> kubectl get pods
NAME                          READY   STATUS    RESTARTS   AGE
nginx-depl-85db6bcdc5-c28d8   1/1     Running   0          19s

> kubectl logs nginx-depl-85db6bcdc5-c28d8
/docker-entrypoint.sh: /docker-entrypoint.d/ is not empty, will attempt to perform configuration

> kubectl exec -it nginx-depl-85db6bcdc5-c28d8 -- /bin/bash
root@nginx-depl-85db6bcdc5-c28d8:/# who
root@nginx-depl-85db6bcdc5-c28d8:/# whoami
root

> kubectl get replicaset
NAME                    DESIRED   CURRENT   READY   AGE
nginx-depl-85db6bcdc5   1         1         1       5m51s
 
> kubectl get deployment
NAME         READY   UP-TO-DATE   AVAILABLE   AGE
nginx-depl   1/1     1            1           6m30s
 
> kubectl get pod
NAME                          READY   STATUS    RESTARTS        AGE
nginx-depl-85db6bcdc5-c28d8   1/1     Running   1 (4m22s ago)   6m45s
 
> kubectl delete deployment ngnix-depl
Error from server (NotFound): deployments.apps "ngnix-depl" not found
 
> kubectl delete deployment ngnix-depl
Error from server (NotFound): deployments.apps "ngnix-depl" not found
 
> kubectl get deployment              
NAME         READY   UP-TO-DATE   AVAILABLE   AGE
nginx-depl   1/1     1            1           25m
 
> kubectl delete deployment nginx-depl
deployment.apps "nginx-depl" deleted

```

### Layers of Abstraction

1. **Deployment** manages a

1. **ReplicaSet** manages a

1. **Pod** is an abstraction of

```markdown
4. Editing a deployment

```bash
kubectl edit deployment nginx-depl

```

If we edit, the existing pod is terminated and a new pod is created as soon as we save.

```plain text

### Pod Monitoring

1. Describe a pod

```bash
kubectl describe pod [pod name]

kubectl describe pod nginx-depl-6f7f5bff95-5ttr6

```

1. View logs of a pod

```bash
kubectl logs [pod name]

kubectl logs nginx-depl-6f7f5bff95-5ttr6

```

### Get Terminal of the Pod

```bash
kubectl exec -it nginx-depl-6f7f5bff95-5ttr6 -- /bin/bash

```

Odyssey > kubectl exec -it nginx-depl-6f7f5bff95-5ttr6 -- /bin/bashroot@nginx-depl-6f7f5bff95-5ttr6:/# lsbin   dev                  docker-entrypoint.sh  home  media  opt   root  sbin  sys  usrboot  docker-entrypoint.d  etc                   lib   mnt    proc  run   srv   tmp  varroot@nginx-depl-6f7f5bff95-5ttr6:/#

### Get Rid of the Pod

```bash
kubectl delete deployment <deployment-name>

```

```bash
Odyssey > kubectl delete deployment nginx-depl
deployment.apps "nginx-depl" deleted

Odyssey > kubectl get pods                    
No resources found in default namespace.

```

### Apply Configuration File

1. Apply a configuration file

```bash
kubectl apply -f ../manifests/nginx-deployment.yaml
deployment.apps/nginx-deployment created

```

1. Check the deployment status

```bash
kubectl get deployment
NAME               READY   UP-TO-DATE   AVAILABLE   AGE
nginx-deployment   1/1     1            1           27s

```

1. Edit the configuration file

```bash
vi ../manifests/nginx-deployment.yaml

```

1. Re-apply the configuration file

```bash
kubectl apply -f ../manifests/nginx-deployment.yaml
deployment.apps/nginx-deployment configured

```

1. Verify the updated deployment status

```bash
kubectl get deployment                
NAME               READY   UP-TO-DATE   AVAILABLE   AGE
nginx-deployment   2/2     2            2           56s

```

You can find the `nginx-deployment.yaml` file here.

```plain text

```