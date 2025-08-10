---
title: Basic kubectl Commands
tags: [kubernetes, kubectl, commands, cli, pods, deployments]
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

2. Status of different K8s components

```bash
kubectl get nodes | pod | services | replicaset | deployment
```

3. Debugging pods
    1. Logs to console

    ```bash
    kubectl logs [pod name]
    ```

    2. Get interactive terminal

    ```bash
    kubectl exec -it [pod name] -- /bin/bash
    
    kubectl exec -it nginx-depl-85db6bcdc5-c28d8 -- /bin/bash
    ```

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
    - ReplicaSet

2. **ReplicaSet** manages a
    - Pod

3. **Pod** is an abstraction of
    - Container

```markdown
4. Editing a deployment

```bash
kubectl edit deployment nginx-depl
```

If we edit, the existing pod is terminated and a new pod is created as soon as we save.
```

### Pod Monitoring

1. Describe a pod

```bash
kubectl describe pod [pod name]

kubectl describe pod nginx-depl-6f7f5bff95-5ttr6
```

2. View logs of a pod

```bash
kubectl logs [pod name]

kubectl logs nginx-depl-6f7f5bff95-5ttr6
```

### Get Terminal of the Pod

```bash
kubectl exec -it nginx-depl-6f7f5bff95-5ttr6 -- /bin/bash
```

Odyssey > kubectl exec -it nginx-depl-6f7f5bff95-5ttr6 -- /bin/bash
root@nginx-depl-6f7f5bff95-5ttr6:/# ls
bin   dev                  docker-entrypoint.sh  home  media  opt   root  sbin  sys  usr
boot  docker-entrypoint.d  etc                   lib   mnt    proc  run   srv   tmp  var
root@nginx-depl-6f7f5bff95-5ttr6:/#

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

2. Check the deployment status

```bash
kubectl get deployment
NAME               READY   UP-TO-DATE   AVAILABLE   AGE
nginx-deployment   1/1     1            1           27s
```

3. Edit the configuration file

```bash
vi ../manifests/nginx-deployment.yaml
```

4. Re-apply the configuration file

```bash
kubectl apply -f ../manifests/nginx-deployment.yaml
deployment.apps/nginx-deployment configured
```

5. Verify the updated deployment status

```bash
kubectl get deployment                
NAME               READY   UP-TO-DATE   AVAILABLE   AGE
nginx-deployment   2/2     2            2           56s
```
You can find the `nginx-deployment.yaml` file [here](../manifests/nginx-deployment.yaml).

```
