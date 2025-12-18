# Kind for K8s - Quickstart

A Hello World example for using Kind to start a local multi-node K8s cluster where each node is represented as a docker container.

## Requirements

- [Docker Desktop](https://docs.docker.com/desktop/)
- [`kubectl`](https://kubernetes.io/docs/reference/kubectl/)
- [Kind](https://kind.sigs.k8s.io/)

## Configure Cluster Template

Check `kind-config.yaml`. In this example, four nodes are created as a K8s cluster - one control plane and 3 worker nodes. In Kind, they are created as docker containers to mimic a multi-node cluster deployment on a single machine.

## Create a Cluster via Kind

Run the following command:

```bash
kind create cluster --name dncc --config kind-config.yaml
```

The cluster will be created with the following output:

```text
kind create cluster --name dncc --config kind-config.yaml
Creating cluster "dncc" ...
 ✓ Ensuring node image (kindest/node:v1.31.2) 🖼
 ✓ Preparing nodes 📦 📦 📦 📦
 ✓ Writing configuration 📜
 ✓ Starting control-plane 🕹️
 ✓ Installing CNI 🔌
 ✓ Installing StorageClass 💾
 ✓ Joining worker nodes 🚜
Set kubectl context to "kind-dncc"
You can now use your cluster with:

kubectl cluster-info --context kind-dncc

Have a nice day! 👋
```

Verify the cluster on Docker Desktop, or via:

```bash
kind get clusters
```

The output will be the name of this cluster:

```text
dncc
```

## Switch to the Cluster Context for `kubectl`

When creating the K8s cluster, Kind automatically adds the cluster context to `kubectl` config. Find this context via `kubectl config get-contexts`:

```text
CURRENT   NAME        CLUSTER     AUTHINFO    NAMESPACE
*         kind-dncc   kind-dncc   kind-dncc
```

The asterisk (`*`) indicates the current context `kubectl` is working on. By default, Kind automatically switches `kubectl` to use the context of the latest created cluster. If not, manually switch to that context via:

```bash
kubectl config use-context kind-dncc
```

The output will be:

```text
Switched to context "kind-dncc".
```

## Play with the Cluster using `kubectl`

### Imperatively Create `nginx` Service

Create a new deployment that maintains a replica set with 1 single pod - each pod possesses 1 single nginx server inside 1 single pod:

```bash
kubectl create deployment nginx --image=nginx:1.27
```

Then, expose the deployment via a specific port (i.e., `80`) as a service:

```bash
kubectl expose deployment nginx --port=80
```

Record the `Cluster-IP` of the exposed service:

```bash
kubectl get svc
```

For example, the output is as follow:

```text
NAME         TYPE        CLUSTER-IP     EXTERNAL-IP   PORT(S)   AGE
kubernetes   ClusterIP   10.96.0.1      <none>        443/TCP   5m50s
nginx        ClusterIP   10.96.83.116   <none>        80/TCP    9s
```

This means the `Cluster-IP` of the `nginx` service is `10.96.83.116`. Now the nginx service can be accessed from `10.96.83.116:80` or `10.96.83.116` (since `80` is the default port via HTTP/HTTPS), but only within the cluster. The IP address here is not for external clients.

### Create the Same `nginx` Service via Declarative Configuration

According to the [official documentation](https://kubernetes.io/docs/concepts/overview/working-with-objects/object-management/#declarative-object-configuration) of declarative configuration:

> The user does not define the operations to be taken on the files. Create, update, and delete operations are automatically detected per-object by kubectl.

Check `nginx-service.yaml`. The same deployment and service created by imperative commands can be set up via:

```bash
kubectl apply -f nginx-service.yaml
```

> **If the image pulling inside the container is not successful, try pulling the image from localhost, then [loading it into the Kind cluster](https://kind.sigs.k8s.io/docs/user/quick-start/#loading-an-image-into-your-cluster). You might find extra image loading issues where a solution might work in [this PR](https://github.com/kubernetes-sigs/kind/issues/3795#issuecomment-2488735728).**

### Test Connection to the `nginx` Service within the Cluster

Kind considers each K8s cluster node as a docker container. A `Cluster-IP` service enables internal access within the cluster. Therefore, we need to test connection to the `nginx` service from one of the cluster nodes. We will test from the control plane node for this demo.

First, verify the container name for the Kind K8s control plane node via:

```bash
docker container ls
```

The output is similar to the one below:

```text
CONTAINER ID   IMAGE                  COMMAND                  CREATED         STATUS         PORTS                       NAMES
a4f12f48eec9   kindest/node:v1.31.2   "/usr/local/bin/entr…"   7 minutes ago   Up 7 minutes                               dncc-worker2
74019a32a24b   kindest/node:v1.31.2   "/usr/local/bin/entr…"   7 minutes ago   Up 7 minutes                               dncc-worker3
709af45665c7   kindest/node:v1.31.2   "/usr/local/bin/entr…"   7 minutes ago   Up 7 minutes   127.0.0.1:39855->6443/tcp   dncc-control-plane
c33980d999ff   kindest/node:v1.31.2   "/usr/local/bin/entr…"   7 minutes ago   Up 7 minutes                               dncc-worker
```

From the output, we know that the control plane node is configured by Kind inside the container named `dncc-control-plane`.

Now we can start a `curl` command inside this container to the service via:

```bash
docker exec -it dncc-control-plane curl 10.96.83.116
```

The output will be:

```text
<!DOCTYPE html>
<html>
<head>
<title>Welcome to nginx!</title>
...
</html>
```

This means the connection test has become successful.

Now you can play with the cluster to get familiar with other `kubectl` commands. Check [this official documentation](https://kubernetes.io/docs/reference/kubectl/) for more info.

## Clean Up the Cluster After Exploration

**REMEMBER** to delete the cluster after playing with it. Do this via:

```bash
kind delete cluster --name dncc
```

The following outputs mark the process successful:

```text
Deleting cluster "dncc" ...
Deleted nodes: ["dncc-control-plane" "dncc-worker3" "dncc-worker2" "dncc-worker"]
```
