# Creating a Pod with Imperative Syntax

## Creating an Nginx Pod

Run an Nginx pod using the `nginx:latest` image:

```bash
kubectl run nginx-pod --image nginx:latest
```

Output:

```
pod/nginx-pod created
```

## Checking Pod Status

Check the pod status:

```bash
kubectl get pods
```

Example output (while the container is creating):

```
NAME        READY   STATUS              RESTARTS   AGE
nginx-pod   0/1     ContainerCreating   0          6s
```

After a few seconds, the pod should be running:

```
NAME        READY   STATUS    RESTARTS   AGE
nginx-pod   1/1     Running   0          14s
```

## Watching Pod Status

You can watch the pod status in real-time:

```bash
kubectl get po -w
```

Output:

```
NAME        READY   STATUS    RESTARTS   AGE
nginx-pod   1/1     Running   0          33s
```

Stop watching with `Ctrl+C`.

## Deleting the Pod

To delete the pod:

```bash
kubectl delete pod nginx-pod
```

Output:

```
pod "nginx-pod" deleted
```

## Verifying Deletion

Check if the pod has been successfully deleted:

```bash
kubectl get pods
```

Output:

```
No resources found in default namespace.
```

# Creating a Pod with Declarative Syntax

## Pod Configuration File: `nginx-pod.yaml`

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

## Applying the Configuration

Run the pod using the YAML configuration:

```bash
kubectl apply -f ../manifests/nginx-pod.yaml
```

## Related file
[ngninx-pod.yaml](../manifests/nginx-pod.yaml)
