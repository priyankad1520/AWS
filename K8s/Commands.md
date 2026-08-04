# `kubectl version`

```bash
kubectl version
# Shows Kubernetes Client & Server versions
```

**Purpose**

* Shows **Client Version** (Local `kubectl`).
* Shows **Server Version** (Kubernetes API Server).
* Verify client-server compatibility.
* Useful before Kubernetes upgrades.
* Helps troubleshoot version mismatch.

**Interview One-Liner**

`kubectl version` displays both the **kubectl client version** and the **Kubernetes API server version** to verify compatibility and troubleshoot version-related issues.

---

# `kubectl cluster-info`

```bash
kubectl cluster-info
# Shows Control Plane and Cluster service endpoints
```

**Purpose**

* Displays **Control Plane endpoint**.
* Shows **CoreDNS** and other cluster services.
* Verifies cluster connectivity.
* Confirms the cluster is running.
* Useful for troubleshooting cluster access.

**Interview One-Liner**

`kubectl cluster-info` displays the **Control Plane endpoint** and the URLs of core Kubernetes services, helping verify cluster connectivity and health.

---

# `kubectl get nodes -o wide`

```bash
kubectl get nodes -o wide
# Lists all nodes with detailed information
```

**Purpose**

* Lists all cluster nodes.
* Shows node status.
* Displays node roles.
* Shows Kubernetes version.
* Displays Internal & External IPs.
* Shows OS, Kernel, and Container Runtime.
## Output Fields

| Field                 | Description                               |
| --------------------- | ----------------------------------------- |
| **NAME**              | Node name                                 |
| **STATUS**            | Current state (Ready / NotReady)          |
| **ROLES**             | Control Plane / Worker                    |
| **AGE**               | How long the node has been in the cluster |
| **VERSION**           | Kubernetes version running on the node    |
| **INTERNAL-IP**       | Private IP used inside the cluster        |
| **EXTERNAL-IP**       | Public IP (if available)                  |
| **OS-IMAGE**          | Operating system installed on the node    |
| **KERNEL-VERSION**    | Linux kernel version                      |
| **CONTAINER-RUNTIME** | Docker / containerd / CRI-O               |

**Interview One-Liner**

`kubectl get nodes -o wide` lists all Kubernetes nodes along with their **status, roles, IP addresses, OS, kernel version, and container runtime**, making it useful for cluster health checks and node troubleshooting.
# `kubectl get pods`

```bash
kubectl get pods
# Lists all Pods in the current namespace
```

**Purpose**

* Lists all Pods.
* Quick health check after deployment.
* Shows Pod status and readiness.
* Detects restarting or failed Pods.
* First command during Pod troubleshooting.

## Output Fields

| Field        | Description                                                |
| ------------ | ---------------------------------------------------------- |
| **NAME**     | Pod name                                                   |
| **READY**    | Ready containers / Total containers (e.g., 1/1)            |
| **STATUS**   | Running, Pending, CrashLoopBackOff, Terminating, Completed |
| **RESTARTS** | Number of container restarts                               |
| **AGE**      | How long the Pod has been running                          |

**Interview One-Liner**

`kubectl get pods` provides a quick overview of all Pods, showing their **readiness, status, restart count, and age**.

---

# `kubectl get pods -o wide`

```bash
kubectl get pods -o wide
# Lists Pods with additional details
```

**Purpose**

* Shows Pod IP.
* Shows Node where Pod is running.
* Helps troubleshoot networking.
* Helps troubleshoot scheduling issues.
* Verifies Pod placement across nodes.

## Additional Output Fields

| Field               | Description                              |
| ------------------- | ---------------------------------------- |
| **IP**              | Pod IP address                           |
| **NODE**            | Node hosting the Pod                     |
| **NOMINATED NODE**  | Reserved node during scheduling (if any) |
| **READINESS GATES** | Additional readiness conditions          |

**Interview One-Liner**

`kubectl get pods -o wide` shows **Pod networking and node placement**, making it useful for scheduling and networking troubleshooting.

---

# `kubectl get pods -l`

```bash
kubectl get pods -l app=backend
# Lists Pods matching the label
```

**Purpose**

* Filters Pods using labels.
* Checks only a specific application.
* Useful for debugging one microservice.
* Helpful after deployment or scaling.

**Interview One-Liner**

`kubectl get pods -l` filters Pods based on **labels**, allowing you to view only the Pods belonging to a specific application.

---

# `kubectl get pod <pod-name>`

```bash
kubectl get pod nginx-7b6d4f8c9d-abc12
# Shows a specific Pod
```

**Purpose**

* Checks one Pod.
* Verifies readiness.
* Checks restart count.
* Useful for troubleshooting a single Pod.

**Interview One-Liner**

`kubectl get pod <pod-name>` displays the status of a **specific Pod** instead of listing all Pods.

---

# `kubectl describe pod`

```bash
kubectl describe pod nginx-7b6d4f8c9d-abc12
# Shows detailed Pod information
```

**Purpose**

* Displays complete Pod configuration.
* Shows Node, Labels & Annotations.
* Displays Container Image & Ports.
* Shows Container State & Exit Code.
* Shows Restart History.
* Shows Events (Scheduling, Pull errors, BackOff).

## Important Sections

* Metadata
* Containers
* Conditions
* Volumes
* Events

**Interview One-Liner**

`kubectl describe pod` provides detailed information about a Pod, including **configuration, container states, events, and failure reasons**, making it the primary troubleshooting command.

---

# `kubectl logs`

```bash
kubectl logs nginx-7b6d4f8c9d-abc12
# Shows container logs
```

## Multiple Containers

```bash
kubectl logs nginx-7b6d4f8c9d-abc12 -c app-container
# Shows logs of a specific container
```

**Purpose**

* Checks application logs.
* Finds runtime errors.
* Troubleshoots CrashLoopBackOff.
* Identifies configuration issues.
* Checks connection failures.

**Interview One-Liner**

`kubectl logs` displays the **application logs** from a container, helping identify runtime errors and application failures.

---

# `kubectl exec -it`

```bash
kubectl exec -it nginx-7b6d4f8c9d-abc12 -- /bin/bash
# Opens an interactive shell inside the container
```

> If Bash is unavailable:

```bash
kubectl exec -it nginx-7b6d4f8c9d-abc12 -- /bin/sh
```

**Purpose**

* Access the running container.
* Check files.
* Verify configuration.
* Run Linux commands.
* Debug inside the container.

**Interview One-Liner**

`kubectl exec -it` opens an **interactive shell** inside a running container, allowing you to inspect files, configurations, and troubleshoot issues.

---

# `kubectl delete pod`

```bash
kubectl delete pod nginx-7b6d4f8c9d-abc12
# Deletes the specified Pod
```

**Purpose**

* Deletes a Pod.
* Forces Pod restart.
* Removes stuck Pods.
* Recovers failed Pods.
* If managed by a Deployment/ReplicaSet, Kubernetes automatically creates a new Pod.

**Interview One-Liner**

`kubectl delete pod` removes a Pod. If it's managed by a **Deployment or ReplicaSet**, Kubernetes automatically recreates it to maintain the desired replica count.
# `kubectl create deployment`

```bash id="v1kq8m"
kubectl create deployment myapp --image=nginx:latest
# Creates a Deployment with 1 replica (Default)
```

## Create with Multiple Replicas

```bash id="v0j4an"
kubectl create deployment myapp --image=nginx:latest --replicas=3
# Creates a Deployment with 3 replicas
```

**Purpose**

* Creates a new Deployment.
* Creates a ReplicaSet automatically.
* Creates Pods automatically.
* Default replicas = **1**.
* Quick way to deploy an application.

**Interview One-Liner**

`kubectl create deployment` creates a Deployment, which automatically creates a **ReplicaSet** and the required **Pods**.

---

# `kubectl get deployments`

```bash id="cax6es"
kubectl get deployments
# Lists all Deployments
```

**Purpose**

* Lists all Deployments.
* Checks rollout progress.
* Verifies replica count.
* Checks deployment health.

## Output Fields

| Field          | Description                       |
| -------------- | --------------------------------- |
| **NAME**       | Deployment name                   |
| **READY**      | Ready replicas / Desired replicas |
| **UP-TO-DATE** | Updated replicas                  |
| **AVAILABLE**  | Available replicas                |
| **AGE**        | Deployment age                    |

**Interview One-Liner**

`kubectl get deployments` displays all Deployments along with their **replica status, availability, and rollout progress**.

---

# `kubectl describe deployment`

```bash id="qmmyo8"
kubectl describe deployment myapp
# Shows detailed Deployment information
```

**Purpose**

* Displays Deployment configuration.
* Shows Replica information.
* Shows Update Strategy.
* Shows Pod Template.
* Shows Container Image.
* Shows Events.
* Troubleshoots rollout failures.

**Important Sections**

* Metadata
* Replicas
* Strategy
* Pod Template
* Conditions
* Events

**Interview One-Liner**

`kubectl describe deployment` provides detailed information about the Deployment, including **replicas, rollout strategy, Pod template, conditions, and events**.

---

# `kubectl scale deployment`

```bash id="8hm5y5"
kubectl scale deployment myapp --replicas=5
# Scales Deployment to 5 replicas
```

**Purpose**

* Scale Up Pods.
* Scale Down Pods.
* Creates or removes Pods automatically.
* Overrides the current replica count in the cluster.

> **Note:** If you later run `kubectl apply` with the original YAML, the replica count in the YAML will be applied again.

**Interview One-Liner**

`kubectl scale deployment` changes the number of running Pods by updating the Deployment's replica count.

---

# `kubectl rollout restart`

```bash id="jw1t6z"
kubectl rollout restart deployment myapp
# Restarts all Pods using Rolling Update
```

**Purpose**

* Restarts all Pods.
* No image or YAML changes required.
* Picks up updated ConfigMaps or Secrets.
* Minimal downtime.

**Interview One-Liner**

`kubectl rollout restart` performs a **rolling restart** of all Pods in a Deployment without changing the application image or configuration.

---

# `kubectl rollout status`

```bash id="rk7oxh"
kubectl rollout status deployment myapp
# Shows rollout progress
```

**Purpose**

* Monitors rollout.
* Checks update progress.
* Verifies successful deployment.
* Detects rollout failures.

**Interview One-Liner**

`kubectl rollout status` monitors the progress of a Deployment rollout and confirms whether it completed successfully.

---

# `--dry-run=client -o yaml`

```bash id="8sy04x"
kubectl create deployment myapp --image=nginx:latest --dry-run=client -o yaml
# Generates Deployment YAML without creating the resource
```

**Purpose**

* Generates Deployment YAML.
* Does not create the Deployment.
* Preview the manifest.
* Useful for learning and editing.

---

# Save YAML to a File

```bash id="l4g60k"
kubectl create deployment myapp --image=nginx:latest --dry-run=client -o yaml > myapp.yaml
# Saves the generated Deployment YAML into myapp.yaml
```

**Purpose**

* Generates Deployment YAML.
* Saves it to a file.
* Useful for Git version control.
* Edit before deployment.
* Declarative Kubernetes approach.

---

# Apply the YAML

```bash id="lcql2d"
kubectl apply -f myapp.yaml
# Creates the Deployment from the YAML file
```

**Purpose**

* Creates or updates Kubernetes resources from YAML.
* Recommended approach for production deployments.

**Interview One-Liner**

Using `--dry-run=client -o yaml` lets you **generate a Deployment manifest without creating it**, making it easy to review, modify, save to a file, and later deploy using `kubectl apply`.
# `kubectl get services`

```bash id="7q2z8m"
kubectl get services
# Lists all Services in the current namespace
```

**Purpose**

* Lists all Services.
* Verifies Service availability.
* Checks Service type.
* Checks ClusterIP / External IP.
* Verifies exposed ports.

## Output Fields

| Field           | Description                         |
| --------------- | ----------------------------------- |
| **NAME**        | Service name                        |
| **TYPE**        | ClusterIP / NodePort / LoadBalancer |
| **CLUSTER-IP**  | Internal Service IP                 |
| **EXTERNAL-IP** | Public IP (if available)            |
| **PORT(S)**     | Service port mapping                |
| **AGE**         | Service age                         |

**Interview One-Liner**

`kubectl get services` lists all Services and shows their **type, ClusterIP, External IP, ports, and age**, helping verify service availability.

---

# `kubectl describe service`

```bash id="m4k1pv"
kubectl describe service my-app-service
# Shows detailed Service information
```

**Purpose**

* Displays Service configuration.
* Shows Service type.
* Shows Selector.
* Shows Ports & TargetPorts.
* Shows Endpoints.
* Shows Events.
* Troubleshoots Service routing issues.

## Important Sections

* Metadata
* Type
* Selector
* ClusterIP
* Ports
* Endpoints
* Events

**Interview One-Liner**

`kubectl describe service` provides detailed information about a Service, including its **selectors, ports, endpoints, and events**, making it the primary command for Service troubleshooting.

---

# `kubectl expose pod`

```bash id="e8g5tm"
kubectl expose pod nginx-pod --port=80
# Creates a ClusterIP Service for the Pod
```

**Purpose**

* Exposes a single Pod.
* Creates a Service automatically.
* Default Service type = **ClusterIP**.
* Useful for quick testing.
* No YAML required.

**Interview One-Liner**

`kubectl expose pod` creates a **Service** for a Pod, allowing other Pods inside the cluster to access it.

---

# `kubectl delete service`

```bash id="2wd4sn"
kubectl delete service my-app-service
# Deletes the Service
```

**Purpose**

* Removes the Service.
* Stops exposing the Pods.
* Does **not** delete the Pods.
* Used for cleanup or replacing Services.

**Interview One-Liner**

`kubectl delete service` removes a Service from the cluster but **does not delete the underlying Pods**.

---

# `kubectl port-forward`

```bash id="gcp7ta"
kubectl port-forward pod/nginx-pod 8080:80
# Forwards local port 8080 to Pod port 80
```

**Purpose**

* Access a Pod from your local machine.
* No Service required.
* Useful for debugging.
* Useful for local testing.
* Temporary connection.

## Flow

Local Browser → `localhost:8080` → Port Forward → Pod:80

**Interview One-Liner**

`kubectl port-forward` creates a **temporary tunnel** from your local machine to a Pod, allowing direct access for testing and debugging without exposing the application through a Service.

---

# Quick Revision

| Command                    | Purpose                                |
| -------------------------- | -------------------------------------- |
| `kubectl get services`     | List all Services                      |
| `kubectl describe service` | Detailed Service information           |
| `kubectl expose pod`       | Create a Service for a Pod             |
| `kubectl delete service`   | Delete a Service                       |
| `kubectl port-forward`     | Access a Pod locally without a Service |
