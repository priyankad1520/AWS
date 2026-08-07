# Node
### Problem 1: Node is NotReady

> First, I'd verify the node status using **kubectl get nodes** to confirm it's in the **NotReady** state. Then I'd inspect the node using **kubectl describe node** to identify any resource pressure or condition failures. Next, I'd verify the kubelet service, container runtime, node network connectivity, and system logs. Based on the findings, I'd restore the node to a healthy state and validate that it becomes **Ready** and starts scheduling Pods again.
> **"First, I'd verify that the node is in the NotReady state using `kubectl get nodes`. Then I'd inspect the node conditions using `kubectl describe node` and verify the kubelet service, container runtime, and node resource utilization. Next, I'd review the kubelet logs and check network connectivity with the control plane. After resolving the underlying issue, I'd validate that the node returns to the Ready state and resumes scheduling Pods."**

**Possible Causes:**

* Kubelet service is stopped.
* Container runtime is down.
* Network connectivity issue.
* Node resource exhaustion.
* Disk Pressure.
* Memory Pressure.
* Node lost communication with the control plane.
* Certificate expired.
* Node rebooted unexpectedly.

**Investigation:**

```yaml
kubectl get nodes
kubectl describe node <node-name>
systemctl status kubelet
systemctl status containerd
journalctl -u kubelet
df -h
free -h
```

**Fixes:**

* Restart kubelet.
* Restart container runtime.
* Restore network connectivity.
* Free node resources.
* Resolve Disk or Memory Pressure.
* Renew certificates if required.
* Rejoin the node if necessary.

### How to Fix

```yaml
# 1. Verify Node Status
kubectl describe node <node-name>
# Check: Ready, Conditions, Events.
------------------------------------------------------------
# 2. Verify Kubelet
systemctl status kubelet
journalctl -u kubelet
# Check kubelet errors.
------------------------------------------------------------
# 3. Verify Container Runtime
systemctl status containerd
# Verify runtime is active.
------------------------------------------------------------
# 4. Verify Resources
df -h
free -h
# Check Disk Usage, Memory Usage.
------------------------------------------------------------
# 5. Verify Network
ping <api-server>
# Verify node can reach the control plane.
------------------------------------------------------------
# 6. Validate
kubectl get nodes
# Verify node status changes to Ready.
```
---

### Problem 2: Node is in DiskPressure

> First, I'd verify the node conditions using **kubectl describe node** to confirm the DiskPressure status. Then I'd inspect the disk utilization on the worker node and identify whether container images, logs, or temporary files are consuming excessive storage. Based on the findings, I'd free disk space and validate that the node returns to a healthy state.
> **"First, I'd verify the DiskPressure condition using `kubectl describe node`. Then I'd inspect the node's disk usage and identify whether container images, logs, or temporary files are consuming excessive storage. After cleaning up unnecessary files or increasing disk capacity, I'd validate that the DiskPressure condition is cleared and the node returns to the Ready state."**

**Possible Causes:**

* Disk is full.
* Container images consuming storage.
* Large container logs.
* Ephemeral storage exhausted.
* Too many unused volumes.

**Investigation:**

```yaml
kubectl describe node <node-name>
df -h
du -sh /var/lib/containerd/*
journalctl --disk-usage
crictl images
```

**Fixes:**

* Delete unused container images.
* Remove unnecessary logs.
* Clean temporary files.
* Increase disk capacity.
* Configure log rotation.

### How to Fix

```yaml
# 1. Verify Node Condition
kubectl describe node <node-name>
# Check: DiskPressure.
------------------------------------------------------------
# 2. Verify Disk Usage
df -h
du -sh /var/lib/containerd/*
# Identify large directories.
------------------------------------------------------------
# 3. Verify Images
crictl images
# Remove unused images.
------------------------------------------------------------
# 4. Verify Logs
journalctl --disk-usage
# Clean unnecessary logs.
------------------------------------------------------------
# 5. Validate
kubectl get nodes
# Verify DiskPressure is cleared.
```
---

### Problem 3: Node is in MemoryPressure

> First, I'd verify the node conditions using **kubectl describe node** to confirm the MemoryPressure status. Then I'd inspect the node's memory utilization and identify Pods consuming excessive memory. Next, I'd verify the resource requests and limits. Based on the findings, I'd optimize memory usage or increase node capacity.
> **"First, I'd verify the MemoryPressure condition using `kubectl describe node`. Then I'd inspect the node's memory usage and identify Pods consuming excessive memory. Next, I'd review the resource requests and limits and optimize the workload or increase node capacity. Finally, I'd validate that the MemoryPressure condition is cleared."**

**Possible Causes:**

* Memory exhausted.
* Pods consuming excessive memory.
* Memory leak.
* Incorrect resource limits.
* Too many Pods on the node.

**Investigation:**

```yaml
kubectl describe node <node-name>
free -h
kubectl top nodes
kubectl top pods
ps aux --sort=-%mem
```

**Fixes:**

* Increase node memory.
* Optimize application memory usage.
* Configure resource requests and limits.
* Move workloads to other nodes.
* Enable Cluster Autoscaler.

### How to Fix

```yaml
# 1. Verify Node Condition
kubectl describe node <node-name>
# Check: MemoryPressure.
------------------------------------------------------------
# 2. Verify Memory Usage
free -h
kubectl top nodes
kubectl top pods
# Identify high memory consumers.
------------------------------------------------------------
# 3. Verify Resource Configuration
kubectl describe pod <pod-name>
# Verify Requests, Limits.
------------------------------------------------------------
# 4. Redistribute Workloads
kubectl drain <node-name> --ignore-daemonsets
# Move workloads if required.
------------------------------------------------------------
# 5. Validate
kubectl get nodes
# Verify MemoryPressure is cleared.
```
---

### Problem 4: Node NetworkUnavailable

> First, I'd verify the node conditions using **kubectl describe node** and confirm the NetworkUnavailable status. Then I'd inspect the CNI plugin, node network configuration, and connectivity with the control plane. Based on the findings, I'd restore the node network and validate that the node becomes Ready.
> **"First, I'd verify the NetworkUnavailable condition using `kubectl describe node`. Then I'd inspect the CNI plugin, node network configuration, and routing. Next, I'd verify connectivity with the Kubernetes API server. After resolving the network issue, I'd validate that the node becomes Ready and resumes normal operation."**

**Possible Causes:**

* CNI plugin failure.
* Network interface issue.
* Routing problem.
* Firewall blocking traffic.
* Control plane connectivity issue.

**Investigation:**

```yaml
kubectl describe node <node-name>
kubectl get pods -n kube-system
ip addr
ip route
ping <api-server>
```

**Fixes:**

* Restart the CNI plugin.
* Fix routing configuration.
* Resolve firewall issues.
* Restore network connectivity.
* Restart node networking services.

### How to Fix

```yaml
# 1. Verify Node Condition
kubectl describe node <node-name>
# Check: NetworkUnavailable.
------------------------------------------------------------
# 2. Verify CNI
kubectl get pods -n kube-system
# Verify CNI Pods are Running.
------------------------------------------------------------
# 3. Verify Network
ip addr
ip route
# Check interface and routing.
------------------------------------------------------------
# 4. Verify Connectivity
ping <api-server>
# Verify node reaches control plane.
------------------------------------------------------------
# 5. Validate
kubectl get nodes
# Verify node becomes Ready.
```
---

### Problem 5: Node Unreachable

> First, I'd verify that the node is unreachable using **kubectl get nodes** and inspect the node conditions using **kubectl describe node**. Then I'd check whether the node itself is reachable through SSH and verify the kubelet service, container runtime, and network connectivity. Based on the findings, I'd restore connectivity and validate that the node reconnects to the cluster.
> **"First, I'd verify that the node is unreachable using `kubectl get nodes` and inspect its conditions. Then I'd check whether I can access the node through SSH and verify the kubelet service, container runtime, and network connectivity. After restoring the node or network connectivity, I'd validate that the node reconnects to the cluster and returns to the Ready state."**

**Possible Causes:**

* Node is powered off.
* Network failure.
* Kubelet stopped.
* Container runtime failure.
* Cloud instance failure.
* Firewall blocking communication.

**Investigation:**

```yaml
kubectl get nodes
kubectl describe node <node-name>
systemctl status kubelet
systemctl status containerd
ping <node-ip>
ssh <node-ip>
```

**Fixes:**

* Restart the node.
* Restart kubelet.
* Restart container runtime.
* Restore network connectivity.
* Recover the cloud instance.
* Update firewall rules.

### How to Fix

```yaml
# 1. Verify Node Status
kubectl describe node <node-name>
# Check: Node Conditions, Heartbeat.
------------------------------------------------------------
# 2. Verify Node Access
ping <node-ip>
ssh <node-ip>
# Verify node is reachable.
------------------------------------------------------------
# 3. Verify Kubelet
systemctl status kubelet
journalctl -u kubelet
# Check kubelet errors.
------------------------------------------------------------
# 4. Verify Runtime
systemctl status containerd
# Verify runtime is active.
------------------------------------------------------------
# 5. Validate
kubectl get nodes
# Verify node reconnects and becomes Ready.
```

**Node Troubleshooting Flow**
```text
Node
   ↓
Node Conditions
   ↓
Kubelet
   ↓
Container Runtime
   ↓
CPU / Memory / Disk
   ↓
Network / CNI
   ↓
Control Plane Connectivity
```
---
# Network

### Problem 1: Pod Cannot Communicate with Another Pod

> First, I'd verify that both Pods are in the **Running** state and inspect their IP addresses. Then I'd test connectivity between the Pods using **ping**, **curl**, or **nc**. Next, I'd verify the Service, Endpoints, NetworkPolicy, CNI plugin, and DNS resolution. Based on the findings, I'd resolve the networking issue and validate that the Pods can communicate successfully.
> **"First, I'd verify that both Pods are Running and test Pod-to-Pod connectivity using `ping` or `curl`. Then I'd check the Service, Endpoints, and NetworkPolicy to ensure traffic is allowed. Next, I'd verify the CNI plugin and routing configuration. After resolving the issue, I'd validate that the Pods can communicate successfully."**

**Possible Causes:**

* Destination Pod is not Running.
* Service has no Endpoints.
* NetworkPolicy blocking traffic.
* CNI plugin issue.
* Incorrect Service selector.
* Firewall or routing issue.

**Investigation:**

```yaml
kubectl get pods -o wide
kubectl exec -it <pod-name> -- ping <pod-ip>
kubectl exec -it <pod-name> -- curl http://<pod-ip>:<port>
kubectl get svc
kubectl get endpoints
kubectl get networkpolicy
kubectl get pods -n kube-system
```

**Fixes:**

* Start the destination Pod.
* Fix Service selector.
* Restore Endpoints.
* Update NetworkPolicy.
* Restart the CNI plugin.
* Fix routing or firewall issues.

### How to Fix

```yaml
# 1. Verify Pod Status
kubectl get pods -o wide
# Verify both Pods are Running.
------------------------------------------------------------
# 2. Verify Connectivity
kubectl exec -it <pod-name> -- ping <destination-pod-ip>
kubectl exec -it <pod-name> -- curl http://<destination-pod-ip>:<port>
# Verify Pod-to-Pod communication.
------------------------------------------------------------
# 3. Verify Service
kubectl get svc
kubectl get endpoints
# Verify Endpoints exist.
------------------------------------------------------------
# 4. Verify NetworkPolicy
kubectl get networkpolicy
kubectl describe networkpolicy <policy-name>
# Check ingress and egress rules.
------------------------------------------------------------
# 5. Verify CNI
kubectl get pods -n kube-system
# Verify CNI Pods are Running.
------------------------------------------------------------
# 6. Validate
kubectl exec -it <pod-name> -- curl http://<destination-pod-ip>:<port>
# Verify communication is successful.
```
---

### Problem 2: DNS Resolution Failed

> First, I'd verify whether DNS resolution is failing by using **nslookup** or **dig** from inside the Pod. Then I'd inspect the CoreDNS Pods and confirm that the DNS Service is running correctly. Next, I'd verify the Pod's DNS configuration and network connectivity. Based on the findings, I'd restore DNS functionality and validate that service names resolve successfully.
> **"First, I'd verify DNS resolution from inside the Pod using `nslookup`. Then I'd check whether the CoreDNS Pods and the DNS Service are healthy. Next, I'd review the CoreDNS logs and ensure that NetworkPolicies are not blocking DNS traffic. After restoring DNS functionality, I'd validate that Service names resolve successfully."**

**Possible Causes:**

* CoreDNS Pods are down.
* CoreDNS configuration issue.
* DNS Service unavailable.
* NetworkPolicy blocking DNS traffic.
* CNI networking issue.
* Incorrect DNS configuration in the Pod.

**Investigation:**

```yaml
kubectl exec -it <pod-name> -- nslookup kubernetes.default
kubectl get pods -n kube-system
kubectl get svc -n kube-system
kubectl logs -n kube-system <coredns-pod>
kubectl describe pod <pod-name>
```

**Fixes:**

* Restart CoreDNS.
* Fix CoreDNS configuration.
* Restore DNS Service.
* Allow DNS traffic in NetworkPolicy.
* Resolve CNI issues.

### How to Fix

```yaml
# 1. Verify DNS Resolution
kubectl exec -it <pod-name> -- nslookup kubernetes.default
# Verify DNS lookup succeeds.
------------------------------------------------------------
# 2. Verify CoreDNS
kubectl get pods -n kube-system
kubectl logs -n kube-system <coredns-pod>
# Verify CoreDNS is Running.
------------------------------------------------------------
# 3. Verify DNS Service
kubectl get svc -n kube-system
# Verify kube-dns Service exists.
------------------------------------------------------------
# 4. Verify NetworkPolicy
kubectl get networkpolicy
# Ensure DNS traffic on port 53 is allowed.
------------------------------------------------------------
# 5. Validate
kubectl exec -it <pod-name> -- nslookup <service-name>
# Verify Service name resolves.
```
---

### Problem 3: NetworkPolicy Blocking Traffic

> First, I'd verify whether a NetworkPolicy exists in the namespace. Then I'd inspect the ingress and egress rules to determine whether traffic between the source and destination Pods is allowed. Next, I'd test connectivity from the source Pod. Based on the findings, I'd update the NetworkPolicy rules and validate that traffic flows successfully.
> **"First, I'd verify whether a NetworkPolicy is applied to the namespace. Then I'd inspect the ingress and egress rules along with the Pod and namespace selectors. Next, I'd test connectivity between the Pods to confirm whether traffic is being blocked. After updating the policy to allow the required traffic, I'd validate that communication succeeds."**

**Possible Causes:**

* Ingress rule blocks traffic.
* Egress rule blocks traffic.
* Incorrect Pod selector.
* Incorrect namespace selector.
* Required ports are not allowed.

**Investigation:**

```yaml
kubectl get networkpolicy
kubectl describe networkpolicy <policy-name>
kubectl get pods --show-labels
kubectl exec -it <pod-name> -- curl http://<destination-pod-ip>:<port>
```
**Fixes:**

* Update ingress rules.
* Update egress rules.
* Correct Pod selector.
* Correct namespace selector.
* Allow required ports.

### How to Fix

```yaml
# 1. Verify NetworkPolicy
kubectl get networkpolicy
kubectl describe networkpolicy <policy-name>
# Verify ingress and egress rules.
------------------------------------------------------------
# 2. Verify Pod Labels
kubectl get pods --show-labels
# Compare labels with the policy selector.
------------------------------------------------------------
# 3. Verify Namespace Labels
kubectl get namespace --show-labels
# Verify namespace selector.
------------------------------------------------------------
# 4. Test Connectivity
kubectl exec -it <pod-name> -- curl http://<destination-pod-ip>:<port>
# Verify whether traffic is blocked.
------------------------------------------------------------
# 5. Validate
kubectl exec -it <pod-name> -- curl http://<destination-pod-ip>:<port>
# Verify communication succeeds after updating the policy.
```
---

### Problem 4: CNI Plugin Issue

> First, I'd verify whether the CNI plugin Pods are running in the **kube-system** namespace. Then I'd inspect the CNI logs and check the node network configuration. Next, I'd verify Pod IP allocation and Pod-to-Pod connectivity. Based on the findings, I'd restore the CNI plugin and validate that networking is functioning correctly across the cluster.
> **"First, I'd verify that the CNI plugin Pods are running in the `kube-system` namespace. Then I'd inspect the CNI logs and node network configuration to identify networking or IP allocation issues. Next, I'd verify Pod IP addresses and test Pod-to-Pod connectivity. After restoring the CNI plugin, I'd validate that networking works correctly across the cluster."**

**Possible Causes:**

* CNI plugin Pod crashed.
* CNI configuration is corrupted.
* IP address allocation failure.
* Node network configuration issue.
* CNI daemon not running.
* Version mismatch after cluster upgrade.

**Investigation:**

```yaml
kubectl get pods -n kube-system
kubectl logs -n kube-system <cni-pod>
kubectl describe node <node-name>
kubectl get pods -o wide
ip addr
ip route
```
**Fixes:**

* Restart the CNI plugin.
* Restore CNI configuration.
* Resolve IP allocation issues.
* Fix node network configuration.
* Upgrade or reinstall the CNI plugin if required.

### How to Fix

```yaml
# 1. Verify CNI Pods
kubectl get pods -n kube-system
# Verify CNI Pods are Running.
------------------------------------------------------------
# 2. Verify CNI Logs
kubectl logs -n kube-system <cni-pod>
# Check for networking or IP allocation errors.
------------------------------------------------------------
# 3. Verify Node Network
ip addr
ip route
# Verify network interfaces and routing.
------------------------------------------------------------
# 4. Verify Pod IP Allocation
kubectl get pods -o wide
# Verify Pods have valid IP addresses.
------------------------------------------------------------
# 5. Validate
kubectl exec -it <pod-name> -- ping <destination-pod-ip>
# Verify Pod-to-Pod communication works.
```
**Kubernetes Network Troubleshooting Flow** 

```text
Pod
   ↓
Service
   ↓
Endpoints
   ↓
DNS (CoreDNS)
   ↓
NetworkPolicy
   ↓
CNI Plugin
   ↓
Node Network
```

* **Pod ↔ Pod issue** → Check **Service → Endpoints → NetworkPolicy → CNI**
* **DNS issue** → Think **CoreDNS**
* **NetworkPolicy issue** → Think **Ingress/Egress Rules + Selectors**
* **CNI issue** → Think **CNI Pods + Node Networking + Pod IP Allocation**
