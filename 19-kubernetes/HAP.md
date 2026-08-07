# HPA (Horizontal Pod Autoscaler)

### Problem 1: Pods are not scaling up
> First, I'd check the HPA status using **kubectl get hpa** and **kubectl describe hpa**. Then I'd verify whether the Metrics Server is working by checking **kubectl top pods** and **kubectl top nodes**. Next, I'd confirm that the Deployment has CPU and Memory requests configured and that the current utilization has crossed the target threshold. I'd also verify that the HPA is pointing to the correct Deployment and hasn't reached its maximum replica limit. Based on the findings, I'd fix the issue and validate that the replicas scale automatically.

**Possible Causes:**

* Metrics Server is not running or installed.
* CPU or Memory requests are not defined in the Deployment.
* Current resource utilization has not reached the configured threshold.
* HPA target utilization is configured incorrectly.
* HPA is pointing to the wrong Deployment.
* HPA has already reached the maximum replica limit.

**Investigation:**

```yaml
kubectl get hpa
kubectl describe hpa <hpa-name>
kubectl top pods
kubectl top nodes
kubectl describe deployment <deployment-name>
```

**Fixes:**

* Start or install the Metrics Server.
* Define CPU and Memory requests.
* Adjust the target utilization.
* Correct the HPA target Deployment.
* Increase the maximum replica limit if required.

### How to Fix
```yaml
# 1. Verify the Metrics Server**
kubectl top nodes
kubectl top pods

# If these commands fail, check the Metrics Server pod:
kubectl get pods -n kube-system
kubectl logs -n kube-system <metrics-server-pod>
------------------------------------------------------------
# 2. Verify CPU and Memory requests
kubectl describe deployment <deployment-name>

Ensure the Deployment defines resource requests:
resources:
  requests:
    cpu: 200m
    memory: 256Mi
------------------------------------------------------------
# 3. Verify HPA configuration**
kubectl describe hpa <hpa-name>
# Check: Current CPU utilization, Target utilization, Current replicas, Desired replicas, Events
------------------------------------------------------------
# 4. Generate load**
kubectl run load-test --rm -it --image=busybox -- sh

# Inside the pod:
while true; do
wget -q -O- http://my-service
done

# Monitor scaling:
kubectl get hpa -w
kubectl get pods -w
```
---

# Problem 2: Scale-up is delayed

> First, I'd verify whether the HPA has triggered a scale-up event using **kubectl describe hpa**. Then I'd check the current CPU or Memory utilization using **kubectl top pods** to confirm it has exceeded the configured threshold. If the HPA has already requested new replicas, I'd verify whether the new Pods are Pending due to insufficient cluster resources, image pull delays, or scheduling issues. Finally, I'd check whether the Cluster Autoscaler is provisioning a new node and validate that the new Pods become Ready and start receiving traffic.

**Possible Causes:**

* CPU or Memory utilization has not stayed above the threshold long enough.
* Metrics Server updates metrics with a slight delay.
* HPA sync interval is causing a delay.
* New Pods are Pending due to insufficient CPU or Memory.
* Container image takes a long time to download.
* Application startup time is high.
* Cluster Autoscaler is provisioning a new node.
* Node resources are exhausted.

**Investigation:**

```yaml
kubectl describe hpa <hpa-name>
kubectl top pods
kubectl get pods
kubectl describe pod <pod-name>
kubectl get nodes
kubectl top nodes
kubectl get events --sort-by=.metadata.creationTimestamp
```
**Fixes:**

* Wait until utilization consistently exceeds the threshold.
* Verify Metrics Server is working correctly.
* Increase available node resources.
* Optimize container image size.
* Reduce application startup time.
* Verify Cluster Autoscaler.
* Add worker nodes if necessary.

### How to Fix

```yaml
# 1. Verify HPA Events
kubectl describe hpa <hpa-name>
# Check: ScalingActive, ScalingLimited, Desired Replicas, Events
------------------------------------------------------------
# 2. Verify Resource Utilization. Ensure CPU or Memory usage is actually above the configured threshold.
kubectl top pods
kubectl top nodes
------------------------------------------------------------
# 3. Check whether new Pods are Pending
kubectl get pods
kubectl describe pod <pod-name>
# Look for: Insufficient CPU, Insufficient Memory, Node Affinity, Taints and Tolerations
------------------------------------------------------------
# 4. Check Cluster Capacity.  If nodes are fully utilized, verify whether Cluster Autoscaler is creating a new node.
kubectl get nodes
kubectl top nodes
------------------------------------------------------------
# 5. Verify Application Startup. Check whether the application initialization is taking too long.
kubectl logs <pod-name>
------------------------------------------------------------
# 6. Monitor Scaling
kubectl get hpa -w
kubectl get pods -w
```

---

# Problem 3: Scale-down is not happening

> First, I'd verify the HPA status using **kubectl describe hpa** and check the current CPU or Memory utilization using **kubectl top pods**. If utilization is still above the configured threshold, HPA will not scale down. Next, I'd verify the minimum replica count and review the HPA events to check whether the stabilization window is delaying the scale-down. Finally, I'd confirm that application traffic has reduced and validate that the replicas decrease automatically.

**Possible Causes:**

* CPU or Memory utilization is still above the configured threshold.
* HPA stabilization window is delaying scale-down.
* Minimum replica count has been reached.
* The application is still receiving traffic.
* Long-running requests are keeping resource utilization high.
* Metrics Server is reporting stale metrics.

**Investigation:**

```bash
kubectl get hpa
kubectl describe hpa <hpa-name>
kubectl top pods
kubectl top nodes
kubectl get deployment
kubectl get events
```

**Fixes:**

* Wait until utilization drops below the configured threshold.
* Verify the HPA stabilization window.
* Reduce the minimum replica count if appropriate.
* Confirm that application traffic has decreased.
* Verify Metrics Server accuracy.

### How to Fix

```yaml
# 1. Verify Current Utilization
kubectl top pods
kubectl top nodes
# If CPU or Memory usage is still high, HPA will not reduce replicas.
------------------------------------------------------------
# 2. Check HPA Configuration
kubectl describe hpa <hpa-name>
# Verify: Current CPU, Target CPU, Desired Replicas, Current Replicas
------------------------------------------------------------
# 3. Verify Minimum Replicas
kubectl describe hpa <hpa-name>
# Example: minReplicas: 2 --> HPA will never scale below this value.
------------------------------------------------------------
# 4. Review HPA Events
kubectl describe hpa <hpa-name>
# Check for: ScaleDownStabilized, SuccessfulRescale, FailedRescale
------------------------------------------------------------
# 5. Verify Application Traffic
kubectl top pods
# Ensure application load has actually reduced.
------------------------------------------------------------
# 6. Monitor Scale-down
kubectl get hpa -w
kubectl get pods -w
```
---
Perfect. These are the remaining HPA problems in the **same format** you've finalized. From now on, this is the format I'll use for all Kubernetes troubleshooting topics.

---

# Problem 4: HPA always shows one replica

> First, I'd verify the HPA configuration using **kubectl describe hpa** and check whether the current CPU or Memory utilization has exceeded the configured target. Then I'd verify that the Deployment has CPU and Memory requests defined because HPA calculates utilization based on resource requests. Next, I'd ensure the HPA is configured with **minReplicas** and **maxReplicas** correctly and is pointing to the correct Deployment. Based on the findings, I'd fix the configuration and validate that HPA increases the replica count when the threshold is exceeded.

---

**Possible Causes:**

* Current resource utilization has not crossed the configured threshold.
* CPU or Memory requests are not defined in the Deployment.
* `minReplicas` and `maxReplicas` are both set to **1**.
* HPA target utilization is configured too high.
* HPA is pointing to the wrong Deployment.
* Metrics Server is not working correctly.

---

**Investigation:**

```yaml
kubectl get hpa
kubectl describe hpa <hpa-name>
kubectl top pods
kubectl top nodes
kubectl describe deployment <deployment-name>
```

---

**Fixes:**

* Define CPU and Memory requests.
* Reduce the target utilization if required.
* Increase `maxReplicas`.
* Verify the correct target Deployment.
* Fix the Metrics Server if necessary.

---

### How to Fix

```yaml
# 1. Verify Current Utilization
kubectl top pods
kubectl top nodes
# Confirm CPU or Memory utilization has exceeded the configured threshold.
------------------------------------------------------------
# 2. Verify Deployment Resource Requests
kubectl describe deployment <deployment-name>
# Verify: CPU Requests, Memory Requests.
------------------------------------------------------------
# 3. Verify HPA Configuration
kubectl describe hpa <hpa-name>
# Verify: Current CPU, Target CPU, Min Replicas, Max Replicas, Desired Replicas.
------------------------------------------------------------
# 4. Verify Scale Target
kubectl describe hpa <hpa-name>
# Verify: ScaleTargetRef points to the correct Deployment.
------------------------------------------------------------
# 5. Monitor Scaling
kubectl get hpa -w
kubectl get pods -w
# Verify replicas increase automatically.
```

---

# Problem 5: CPU usage is high, but replicas are not increasing

> First, I'd verify whether HPA is receiving the latest metrics using **kubectl top pods** and **kubectl describe hpa**. Then I'd confirm that CPU requests are configured because HPA calculates utilization based on requested CPU. Next, I'd verify whether the current utilization has exceeded the target value and ensure that the HPA has not reached the maximum replica limit. Finally, I'd validate that the Metrics Server is functioning correctly and monitor whether new replicas are created.

---

**Possible Causes:**

* CPU requests are not defined.
* Metrics Server is unavailable.
* HPA target utilization is configured too high.
* HPA has reached the maximum replica limit.
* HPA is targeting the wrong Deployment.
* Metrics are stale or unavailable.

---

**Investigation:**

```yaml
kubectl get hpa
kubectl describe hpa <hpa-name>
kubectl top pods
kubectl top nodes
kubectl describe deployment <deployment-name>
kubectl get events
```

---

**Fixes:**

* Configure CPU requests.
* Repair the Metrics Server.
* Reduce the target utilization.
* Increase the maximum replica limit.
* Correct the HPA target Deployment.

---

### How to Fix

```yaml
# 1. Verify Metrics
kubectl top pods
kubectl top nodes
# Confirm metrics are available.
------------------------------------------------------------
# 2. Verify CPU Requests
kubectl describe deployment <deployment-name>
# Verify: CPU Requests, Memory Requests.
------------------------------------------------------------
# 3. Check HPA Configuration
kubectl describe hpa <hpa-name>
# Verify: Current CPU, Target CPU, Desired Replicas, Max Replicas.
------------------------------------------------------------
# 4. Verify Metrics Server
kubectl get pods -n kube-system
kubectl logs -n kube-system <metrics-server-pod>
# Confirm Metrics Server is healthy.
------------------------------------------------------------
# 5. Monitor Scaling
kubectl get hpa -w
kubectl get pods -w
# Verify replicas increase after CPU exceeds the threshold.
```

---

# Problem 6: HPA status shows **Unknown**

> First, I'd verify the HPA status using **kubectl describe hpa** and review the events section for any metric-related errors. Then I'd check whether the Metrics Server is running and confirm that metrics are available using **kubectl top pods** and **kubectl top nodes**. Next, I'd verify the Metrics Server logs and ensure it can communicate with the kubelets. After resolving the issue, I'd validate that HPA starts receiving metrics and changes its status from **Unknown** to **AbleToScale**.

---

**Possible Causes:**

* Metrics Server is not running.
* Metrics API is unavailable.
* Metrics Server cannot communicate with kubelets.
* RBAC permissions are incorrect.
* Network connectivity issues between Metrics Server and worker nodes.
* Metrics Server certificate or TLS issues.

---

**Investigation:**

```yaml
kubectl get hpa
kubectl describe hpa <hpa-name>
kubectl top pods
kubectl top nodes
kubectl get pods -n kube-system
kubectl logs -n kube-system <metrics-server-pod>
```

---

**Fixes:**

* Start or reinstall the Metrics Server.
* Resolve Metrics API issues.
* Fix RBAC permissions.
* Resolve network connectivity problems.
* Correct certificate or TLS configuration.

---

### How to Fix

```yaml
# 1. Verify Metrics Availability
kubectl top pods
kubectl top nodes
# If these commands fail, Metrics Server is unavailable.
------------------------------------------------------------
# 2. Verify Metrics Server
kubectl get pods -n kube-system
kubectl logs -n kube-system <metrics-server-pod>
# Check for startup or communication errors.
------------------------------------------------------------
# 3. Verify HPA Events
kubectl describe hpa <hpa-name>
# Check: FailedGetResourceMetric, FailedComputeMetricsReplicas, ScalingActive.
------------------------------------------------------------
# 4. Verify Metrics API
kubectl get apiservices
# Confirm metrics.k8s.io API is available.
------------------------------------------------------------
# 5. Monitor HPA
kubectl get hpa -w
# Verify STATUS changes from Unknown to AbleToScale and metrics are displayed.
```
---

**Root Cause (Most Common):**

* A one-line summary of the issue most commonly seen in production.

For example:

* **Pods not scaling up** → *Usually caused by missing CPU requests or a non-functional Metrics Server.*
* **Scale-up delayed** → *Usually caused by insufficient cluster resources or Cluster Autoscaler delay.*
* **Scale-down not happening** → *Usually caused by high resource utilization or HPA stabilization window.*
* **HPA always one replica** → *Usually caused by CPU not crossing the threshold or `maxReplicas` set to 1.*
* **CPU high but no scaling** → *Usually caused by missing CPU requests or Metrics Server issues.*
* **HPA status Unknown** → *Usually caused by Metrics Server or Metrics API failure.*

This gives you a quick takeaway to remember for each scenario and is very useful during interviews.
