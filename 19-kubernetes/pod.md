# Pod

# Problem 1: Pod is in CrashLoopBackOff

> First, I'd check the Pod status using **kubectl get pods** to confirm it's in a CrashLoopBackOff state. Then I'd inspect the Pod events using **kubectl describe pod** and review the container logs using **kubectl logs** to identify why the application is crashing. Next, I'd verify the container image, startup command, ConfigMaps, Secrets, resource limits, and external dependencies such as the database or APIs. Based on the root cause, I'd fix the configuration or application issue, redeploy the Pod, and verify that it reaches the **Running** and **Ready** state without further restarts.

**Possible Causes:**

* Application crashes during startup.
* Incorrect container startup command or arguments.
* Missing or incorrect ConfigMap.
* Missing or incorrect Secret.
* Database or external service is unreachable.
* Application configuration error.
* Port conflict.
* Resource limits are too low (OOMKilled).
* Liveness probe failure.
* Required files or volumes are missing.


**Investigation:**

```yaml
kubectl get pods
kubectl describe pod <pod-name>
kubectl logs <pod-name>
kubectl logs <pod-name> --previous
kubectl get events --sort-by=.metadata.creationTimestamp
kubectl describe deployment <deployment-name>
```

**Fixes:**

* Fix the application error.
* Correct the startup command.
* Update ConfigMap or Secret.
* Restore database or external service connectivity.
* Increase CPU or Memory limits if required.
* Correct the liveness probe.
* Redeploy the application.

### How to Fix

```yaml
# 1. Verify Pod Events
kubectl describe pod <pod-name>
# Check: Failed, BackOff, OOMKilled, Unhealthy, FailedMount, FailedScheduling.
------------------------------------------------------------
# 2. Check Container Logs
kubectl logs <pod-name>
kubectl logs <pod-name> --previous
# Identify the exact application error before the container exited.
------------------------------------------------------------
# 3. Verify ConfigMap and Secret
kubectl get configmap
kubectl get secret
kubectl describe pod <pod-name>
# Verify: Environment Variables, Mounted Volumes, Secret References.
------------------------------------------------------------
# 4. Verify Resource Limits
kubectl describe pod <pod-name>
# Check: CPU Requests, CPU Limits, Memory Requests, Memory Limits, OOMKilled.
------------------------------------------------------------
# 5. Verify Liveness Probe
kubectl describe pod <pod-name>
# Check: Liveness Probe, Events, Restart Count.
------------------------------------------------------------
# 6. Verify External Dependencies
kubectl exec -it <pod-name> -- sh
# Check: Database Connectivity, DNS Resolution, API Connectivity.
------------------------------------------------------------
# 7. Restart and Validate
kubectl rollout restart deployment <deployment-name>
kubectl get pods -w
# Verify Pod reaches Running and Ready state without restarts.
```

---

# Problem 2: Pod is in Pending

> First, I'd check the Pod status using **kubectl get pods** to confirm it's in the **Pending** state. Then I'd inspect the Pod events using **kubectl describe pod** because Kubernetes usually reports the exact scheduling reason in the Events section. Next, I'd verify the node resources, node labels, taints and tolerations, PVC status, and scheduler events to determine why the Pod is not being scheduled. Based on the root cause, I'd fix the scheduling issue and verify that the Pod moves to the **Running** state successfully.
> **"First, I'd confirm that the Pod is in the Pending state using `kubectl get pods`. Then I'd run `kubectl describe pod` because the Events section usually shows the exact scheduling reason, such as insufficient CPU, memory, taints, node affinity, or PVC issues. Based on the error, I'd verify the worker node resources, node labels, taints and tolerations, PVC status, and scheduler health. After identifying the root cause, I'd fix the scheduling issue by adding resources, correcting the scheduling configuration, or resolving the storage problem. Finally, I'd monitor the Pod and verify that it successfully transitions to the Running state."**

**Possible Causes:**

* Insufficient CPU resources on worker nodes. **Insufficient CPU/Memory**
* Insufficient Memory resources on worker nodes.
* No available worker nodes.
* Node Selector does not match any node labels. **Node Selector / Node Affinity mismatch**
* Taints are preventing Pod scheduling. **Taints & Tolerations**
* Missing Tolerations.
* Persistent Volume Claim (PVC) is in Pending state. **PVC Pending**
* Requested resources exceed available node capacity.
* Scheduler is not running or unhealthy.  **Scheduler issue**
* Node is in **NotReady** state. **Node NotReady**
* Node Affinity rules cannot be satisfied.
* ResourceQuota or LimitRange restrictions.

**Investigation:**

```yaml
kubectl get pods
kubectl describe pod <pod-name>
kubectl get nodes
kubectl describe node <node-name>
kubectl get pvc
kubectl describe pvc <pvc-name>
kubectl get events --sort-by=.metadata.creationTimestamp
kubectl top nodes
```

---

**Fixes:**

* Add CPU or Memory resources to worker nodes.
* Add new worker nodes or enable Cluster Autoscaler.
* Correct the Node Selector.
* Add the required Tolerations.
* Remove unnecessary Taints if appropriate.
* Fix the Pending PVC.
* Reduce the Pod's CPU or Memory requests.
* Bring the scheduler back to a healthy state.
* Recover the NotReady node.
* Correct Node Affinity rules.
* Increase ResourceQuota if appropriate.

---

## How to Fix

```yaml
# 1. Verify Scheduling Events
kubectl describe pod <pod-name>
# Check: FailedScheduling, Insufficient CPU, Insufficient Memory, NodeAffinity, Taints.
------------------------------------------------------------
# 2. Verify Worker Nodes
kubectl get nodes
kubectl describe node <node-name>
kubectl top nodes
# Verify: Node Ready, CPU Usage, Memory Usage, Allocatable Resources.
------------------------------------------------------------
# 3. Verify Node Selector & Affinity
kubectl describe pod <pod-name>
kubectl get nodes --show-labels
# Verify: Node Selector, Node Affinity, Available Labels.
------------------------------------------------------------
# 4. Verify Taints & Tolerations
kubectl describe node <node-name>
kubectl describe pod <pod-name>
# Verify: Taints, Tolerations.
------------------------------------------------------------
# 5. Verify Persistent Volume Claim
kubectl get pvc
kubectl describe pvc <pvc-name>
# Verify: PVC Bound Status, StorageClass, Capacity.
------------------------------------------------------------
# 6. Verify Resource Requests
kubectl describe pod <pod-name>
# Verify: CPU Requests, Memory Requests, Resource Limits.
------------------------------------------------------------
# 7. Verify Scheduler
kubectl get pods -n kube-system
# Verify: kube-scheduler Pod is Running.
------------------------------------------------------------
# 8. Verify ResourceQuota
kubectl get resourcequota
kubectl describe resourcequota
# Verify: CPU, Memory, Pod Limits.
------------------------------------------------------------
# 9. Validate Scheduling
kubectl get pods -w
# Verify Pod transitions from Pending → ContainerCreating → Running.
```
---

* **ErrImagePull** = Kubernetes failed to pull the image for the **first time**.
* **ImagePullBackOff** = Kubernetes has **already failed** and is now **retrying with exponential backoff**.

---

# Problem 3: Pod is in ImagePullBackOff

> First, I'd confirm the Pod status using **kubectl get pods** and verify that it's in the **ImagePullBackOff** state. Then I'd inspect the Pod events using **kubectl describe pod**, as the Events section usually provides the exact image pull error. Next, I'd verify the image name, image tag, container registry accessibility, image pull secrets, and node network connectivity. Based on the root cause, I'd correct the image or registry configuration and validate that the Pod successfully pulls the image and starts running.
> **"First, I'd confirm that the Pod is in the ImagePullBackOff state using `kubectl get pods`. Then I'd inspect the Events section with `kubectl describe pod` to identify the exact image pull error. Next, I'd verify the image name, tag, ImagePullSecret, ServiceAccount, and registry connectivity. If it's a private registry, I'd confirm the authentication credentials are correct. After fixing the issue, I'd restart the Deployment and verify that the Pod successfully pulls the image and reaches the Running state."**

**Possible Causes:**

* Incorrect image name.
* Incorrect image tag.
* Image does not exist in the registry.
* Private registry authentication failure.
* Missing or incorrect ImagePullSecret.
* Registry is unavailable.
* Worker node cannot access the registry.
* Docker Hub or registry rate limiting.
* Typographical error in the image name.

**Investigation:**

```yaml
kubectl get pods
kubectl describe pod <pod-name>
kubectl get secrets
kubectl describe secret <image-pull-secret>
kubectl get serviceaccount
kubectl describe serviceaccount <service-account>
kubectl get events --sort-by=.metadata.creationTimestamp
```

**Fixes:**

* Correct the image name.
* Correct the image tag.
* Push the missing image to the registry.
* Configure the correct ImagePullSecret.
* Restore registry connectivity.
* Attach the correct ServiceAccount.
* Resolve registry authentication issues.

## How to Fix

```yaml
# 1. Verify Pod Events
kubectl describe pod <pod-name>
# Check: ImagePullBackOff, Failed to pull image, Unauthorized, Not Found.
------------------------------------------------------------
# 2. Verify Image Name & Tag
kubectl describe deployment <deployment-name>
# Verify: Image Name, Image Tag.
------------------------------------------------------------
# 3. Verify ImagePullSecret
kubectl get secrets
kubectl describe secret <image-pull-secret>
# Verify: Secret Exists, Correct Registry Credentials.
------------------------------------------------------------
# 4. Verify ServiceAccount
kubectl get serviceaccount
kubectl describe serviceaccount <service-account>
# Verify: ImagePullSecrets are attached.
------------------------------------------------------------
# 5. Verify Registry Connectivity
kubectl run test --rm -it --image=busybox -- sh
wget https://<registry-url>
# Verify worker node can reach the registry.
------------------------------------------------------------
# 6. Restart Deployment
kubectl rollout restart deployment <deployment-name>
kubectl get pods -w
# Verify Pod successfully pulls the image and reaches Running state.
```
---

# Problem 4: Pod is in ErrImagePull

> First, I'd verify the Pod status using **kubectl get pods** and inspect the Events section using **kubectl describe pod**. Since **ErrImagePull** indicates the initial image pull has failed, I'd identify the exact reason, such as an incorrect image, invalid tag, authentication issue, or registry connectivity problem. After fixing the issue, I'd verify that Kubernetes retries the image pull successfully and the Pod transitions to the Running state.
> **"First, I'd verify the Pod status and inspect the Events section using `kubectl describe pod` because ErrImagePull usually provides the exact reason for the initial image pull failure. Then I'd verify the image name, tag, registry authentication, ImagePullSecret, and network connectivity to the registry. Once the issue is fixed, Kubernetes automatically retries the image pull. Finally, I'd monitor the Pod to ensure it progresses to the Running state."**

**Possible Causes:**

* Incorrect image name.
* Invalid image tag.
* Image is not available in the registry.
* Private registry authentication failure.
* Missing ImagePullSecret.
* Registry DNS or network issue.
* Registry temporarily unavailable.

**Investigation:**

```yaml
kubectl get pods
kubectl describe pod <pod-name>
kubectl get secrets
kubectl describe secret <image-pull-secret>
kubectl get events --sort-by=.metadata.creationTimestamp
```

**Fixes:**

* Correct the image name.
* Correct the image tag.
* Push the required image to the registry.
* Configure the correct ImagePullSecret.
* Restore registry connectivity.
* Verify registry credentials.

## How to Fix

```yaml
# 1. Verify Pod Events
kubectl describe pod <pod-name>
# Check: ErrImagePull, Manifest Unknown, Unauthorized, Repository Not Found.
------------------------------------------------------------
# 2. Verify Deployment Image
kubectl describe deployment <deployment-name>
# Verify: Image Name, Image Tag.
------------------------------------------------------------
# 3. Verify ImagePullSecret
kubectl get secrets
kubectl describe secret <image-pull-secret>
# Verify: Registry Credentials.
------------------------------------------------------------
# 4. Verify Registry Access
kubectl run test --rm -it --image=busybox -- sh
wget https://<registry-url>
# Verify registry is reachable.
------------------------------------------------------------
# 5. Verify Events
kubectl get events --sort-by=.metadata.creationTimestamp
# Identify the exact image pull error.
------------------------------------------------------------
# 6. Validate
kubectl rollout restart deployment <deployment-name>
kubectl get pods -w
# Verify Pod moves from ErrImagePull → ContainerCreating → Running.
```
---

# Problem 5: Pod is in OOMKilled

> First, I'd verify that the container was terminated due to an **OOMKilled** event using **kubectl describe pod**. Then I'd review the container's resource requests and limits and check whether the application is consuming more memory than allocated. Next, I'd analyze the application logs to determine whether the high memory usage is expected or caused by a memory leak. Based on the findings, I'd increase the memory limit, optimize the application, or fix the memory leak. Finally, I'd verify that the Pod runs without further OOMKilled events.
> **"First, I'd verify the OOMKilled event using `kubectl describe pod`. Then I'd review the previous container logs and compare the application's memory usage with the configured memory requests and limits. If the application is legitimately using more memory, I'd increase the limits. If it's caused by a memory leak, I'd work with the development team to fix the application. Finally, I'd redeploy the application and confirm that the Pod remains stable without further OOMKilled events."**

**Possible Causes:**

* Memory limit is too low.
* Application has a memory leak.
* Unexpected traffic caused high memory consumption.
* Memory requests are configured incorrectly.
* Large files or data are loaded into memory.
* Infinite loop causing excessive memory usage.

**Investigation:**

```yaml
kubectl get pods
kubectl describe pod <pod-name>
kubectl logs <pod-name> --previous
kubectl top pod <pod-name>
kubectl describe deployment <deployment-name>
```

**Fixes:**

* Increase memory limits.
* Increase memory requests.
* Fix application memory leak.
* Optimize memory usage.
* Enable Horizontal Pod Autoscaler if appropriate.

### How to Fix

```yaml
# 1. Verify OOMKilled Event
kubectl describe pod <pod-name>
# Check: Last State, Exit Code, Reason: OOMKilled.
------------------------------------------------------------
# 2. Check Previous Logs
kubectl logs <pod-name> --previous
# Identify what the application was doing before termination.
------------------------------------------------------------
# 3. Verify Resource Configuration
kubectl describe deployment <deployment-name>
# Verify: Memory Requests, Memory Limits.
------------------------------------------------------------
# 4. Check Current Memory Usage
kubectl top pod <pod-name>
# Compare actual usage with configured limits.
------------------------------------------------------------
# 5. Update Resources
kubectl edit deployment <deployment-name>
# Increase Memory Requests and Limits if required.
------------------------------------------------------------
# 6. Validate
kubectl rollout restart deployment <deployment-name>
kubectl get pods -w
# Verify Pod remains Running without OOMKilled.
```
---

# Problem 6: Pod is in ContainerCreating

> First, I'd confirm that the Pod is stuck in the **ContainerCreating** state using **kubectl get pods**. Then I'd inspect the Pod events using **kubectl describe pod** to determine whether the delay is caused by image pulling, volume mounting, Secret or ConfigMap mounting, or CNI network initialization. Based on the findings, I'd resolve the underlying issue and verify that the Pod successfully transitions to the Running state.
> **"First, I'd verify that the Pod is in the ContainerCreating state and inspect the Events section using `kubectl describe pod`. Then I'd check whether the issue is related to image downloading, volume attachment, ConfigMap or Secret mounting, or network initialization. Based on the findings, I'd resolve the underlying issue and monitor the Pod until it successfully transitions to the Running state."**

**Possible Causes:**

* Large container image is still downloading.
* Image pull is slow.
* Persistent Volume is not attached.
* ConfigMap or Secret mounting failed.
* CNI plugin issue.
* CSI driver issue.
* Node is under heavy load.

**Investigation:**

```yaml
kubectl get pods
kubectl describe pod <pod-name>
kubectl get pvc
kubectl describe pvc <pvc-name>
kubectl get events --sort-by=.metadata.creationTimestamp
kubectl get nodes
```

**Fixes:**

* Wait for image download to complete.
* Fix image pull issues.
* Resolve PVC or volume attachment problems.
* Fix ConfigMap or Secret mounting.
* Restart the CNI or CSI components.
* Reduce node resource utilization.

### How to Fix

```yaml
# 1. Verify Pod Events
kubectl describe pod <pod-name>
# Check: Pulling Image, FailedMount, FailedAttachVolume, FailedCreatePodSandBox.
------------------------------------------------------------
# 2. Verify Image Download
kubectl describe pod <pod-name>
# Check image pull progress.
------------------------------------------------------------
# 3. Verify PVC
kubectl get pvc
kubectl describe pvc <pvc-name>
# Verify PVC is Bound.
------------------------------------------------------------
# 4. Verify ConfigMap & Secret
kubectl get configmap
kubectl get secret
# Verify required resources exist.
------------------------------------------------------------
# 5. Verify Node
kubectl get nodes
kubectl describe node <node-name>
# Check Node Ready, Disk Pressure, Memory Pressure.
------------------------------------------------------------
# 6. Validate
kubectl get pods -w
# Verify Pod moves to Running.
```
---

# Problem 7: Pod status is Completed

Many people think this is an error. **It is actually NOT an error.**

A Pod enters **Completed** when its container finishes successfully and exits with **Exit Code 0**.

This commonly happens with: Kubernetes Jobs, CronJobs, Database backup Pods, Migration Pods, One-time scripts, Batch processing

If a normal web application Pod shows **Completed**, then **that is a problem** because the application exited instead of continuing to run.

> First, I'd verify whether the Pod belongs to a Job or CronJob. If it does, the Completed status is expected because the task finished successfully. If it's a Deployment Pod, I'd investigate why the application exited by reviewing the container logs and startup command. Based on the findings, I'd correct the application behavior or configuration and verify that the Pod remains in the Running state.
> **"First, I'd determine whether the Pod belongs to a Job, CronJob, or Deployment. If it's a Job or CronJob, a Completed status is expected because the task finished successfully. If it's a Deployment Pod, I'd review the container logs and startup command to understand why the application exited. After fixing the issue, I'd verify that the application remains in the Running state."**

**Possible Causes:**

* Job completed successfully. ✅
* CronJob completed successfully. ✅
* Application exited normally.
* Startup script finished execution.
* Incorrect container command.
* Application designed to run once instead of continuously.

**Investigation:**

```yaml
kubectl get pods
kubectl describe pod <pod-name>
kubectl logs <pod-name>
kubectl get jobs
kubectl get cronjobs
kubectl describe deployment <deployment-name>
```

**Fixes:**

* No action required if it's a Job or CronJob.
* Modify the application to keep running if it's a Deployment.
* Correct the startup command.
* Fix the container entrypoint.

### How to Fix

```yaml
# 1. Verify Pod Owner
kubectl describe pod <pod-name>
# Check: Controlled By (Job, CronJob, Deployment).
------------------------------------------------------------
# 2. Check Container Logs
kubectl logs <pod-name>
# Verify application completed successfully or exited unexpectedly.
------------------------------------------------------------
# 3. Verify Startup Command
kubectl describe deployment <deployment-name>
# Verify: Command, Args, Entrypoint.
------------------------------------------------------------
# 4. Verify Job Status
kubectl get jobs
kubectl get cronjobs
# Confirm whether Completed is expected.
------------------------------------------------------------
# 5. Validate
kubectl get pods -w
# Verify Deployment Pods remain Running or Jobs complete successfully.
```

* **OOMKilled** → Almost always a **memory-related issue**.
* **ContainerCreating** → Usually an **infrastructure dependency issue** (image, PVC, Secret, CNI, CSI).
* **Completed** → **Not an error** for Jobs/CronJobs, but **unexpected** for Deployments.

---

# Problem 8: Pod is Running but Not Ready

> First, I'd verify that the Pod is in the **Running** state but **Not Ready** using **kubectl get pods**. Then I'd inspect the Pod using **kubectl describe pod** to check the readiness probe status and events. Next, I'd review the application logs, verify the readiness endpoint, ConfigMaps, Secrets, and external dependencies such as databases or APIs. Based on the root cause, I'd fix the readiness issue and verify that the Pod becomes **Ready** and starts receiving traffic.
> **"First, I'd verify that the Pod is Running but Not Ready using `kubectl get pods`. Then I'd inspect the readiness probe and events using `kubectl describe pod`. Next, I'd review the application logs and verify that the readiness endpoint is responding successfully. I'd also check external dependencies such as the database, APIs, ConfigMaps, and Secrets. After fixing the issue, I'd validate that the Pod becomes Ready and starts receiving traffic."**


**Possible Causes:**

* Readiness probe is failing.
* Application is still initializing.
* Incorrect readiness probe configuration.
* Database or external service is unavailable.
* ConfigMap or Secret configuration is incorrect.
* Application port is incorrect.
* DNS resolution failure.

**Investigation:**

```yaml
kubectl get pods
kubectl describe pod <pod-name>
kubectl logs <pod-name>
kubectl get events --sort-by=.metadata.creationTimestamp
kubectl exec -it <pod-name> -- sh
kubectl describe deployment <deployment-name>
```

**Fixes:**

* Correct the readiness probe.
* Increase `initialDelaySeconds` if the application starts slowly.
* Restore database or external service connectivity.
* Update ConfigMap or Secret.
* Correct the application port.
* Fix DNS issues.

### How to Fix

```yaml
# 1. Verify Readiness Probe
kubectl describe pod <pod-name>
# Check: Readiness Probe, Events, HTTP Status, Timeout, Failure Count.
------------------------------------------------------------
# 2. Check Application Logs
kubectl logs <pod-name>
# Identify startup errors or dependency failures.
------------------------------------------------------------
# 3. Verify Readiness Endpoint
kubectl exec -it <pod-name> -- sh
curl http://localhost:<port>/<health-endpoint>
# Verify readiness endpoint returns HTTP 200.
------------------------------------------------------------
# 4. Verify External Dependencies
kubectl exec -it <pod-name> -- sh
# Verify: Database Connectivity, API Connectivity, DNS Resolution.
------------------------------------------------------------
# 5. Verify Deployment Configuration
kubectl describe deployment <deployment-name>
# Verify: Container Port, Readiness Probe, ConfigMap, Secret.
------------------------------------------------------------
# 6. Validate
kubectl get pods -w
# Verify READY changes from 0/1 to 1/1.
```

---

# Problem 9: Pod is Restarting Frequently

> First, I'd check the Pod restart count using **kubectl get pods** and inspect the Pod events using **kubectl describe pod**. Then I'd review the current and previous container logs to identify why the container is restarting. Next, I'd verify resource usage, health probes, application configuration, and external dependencies. Based on the root cause, I'd fix the issue and confirm that the restart count stops increasing.
> **"First, I'd check the restart count and Pod events using `kubectl get pods` and `kubectl describe pod`. Then I'd review both the current and previous container logs to identify the exact reason for the restart. Next, I'd verify resource usage, liveness probe configuration, application settings, and external dependencies. After resolving the root cause, I'd monitor the Pod and confirm that the restart count remains stable."**

**Possible Causes:**

* Application crash.
* OOMKilled.
* Liveness probe failure.
* Application configuration error.
* Database or API connectivity issue.
* Resource limits are too low.
* Container startup failure.

**Investigation:**

```yaml
kubectl get pods
kubectl describe pod <pod-name>
kubectl logs <pod-name>
kubectl logs <pod-name> --previous
kubectl top pod <pod-name>
kubectl get events --sort-by=.metadata.creationTimestamp
```

**Fixes:**

* Fix application errors.
* Increase CPU or Memory limits.
* Correct the liveness probe.
* Restore external dependency connectivity.
* Update application configuration.
* Optimize resource usage.

### How to Fix

```yaml
# 1. Verify Restart Reason
kubectl describe pod <pod-name>
# Check: Restart Count, Last State, Exit Code, Reason.
------------------------------------------------------------
# 2. Review Container Logs
kubectl logs <pod-name>
kubectl logs <pod-name> --previous
# Identify the reason for the restart.
------------------------------------------------------------
# 3. Verify Resource Usage
kubectl top pod <pod-name>
kubectl describe deployment <deployment-name>
# Verify: CPU Requests, CPU Limits, Memory Requests, Memory Limits.
------------------------------------------------------------
# 4. Verify Liveness Probe
kubectl describe pod <pod-name>
# Check: Liveness Probe, Failure Count, Events.
------------------------------------------------------------
# 5. Verify External Dependencies
kubectl exec -it <pod-name> -- sh
# Verify: Database, API, DNS Connectivity.
------------------------------------------------------------
# 6. Validate
kubectl get pods -w
# Verify restart count no longer increases.
```

---

# Problem 10: Pod is Evicted

> First, I'd verify that the Pod has been **Evicted** using **kubectl get pods** and inspect the eviction reason using **kubectl describe pod**. Then I'd determine whether the node is under Memory Pressure, Disk Pressure, or Ephemeral Storage Pressure. Next, I'd review the node's resource utilization and the Pod's resource requests and limits. Based on the findings, I'd free up node resources, adjust the resource configuration, or move workloads to other nodes. Finally, I'd verify that the Pod is recreated successfully and remains in the Running state.
> **"First, I'd confirm that the Pod was evicted by checking `kubectl describe pod` and identify whether the reason is Memory Pressure, Disk Pressure, or Ephemeral Storage exhaustion. Then I'd inspect the node's resource utilization and verify the Pod's CPU and Memory requests. Based on the findings, I'd free node resources, add capacity if needed, or optimize the workload configuration. Finally, I'd verify that the Pod is recreated successfully and remains in the Running state."**

**Possible Causes:**

* Memory Pressure on the node.
* Disk Pressure on the node.
* Ephemeral Storage exhaustion.
* Node resource exhaustion.
* CPU or Memory requests are too low.
* Too many Pods running on the same node.

**Investigation:**

```yaml
kubectl get pods
kubectl describe pod <pod-name>
kubectl get nodes
kubectl describe node <node-name>
kubectl top nodes
kubectl get events --sort-by=.metadata.creationTimestamp
```

**Fixes:**

* Free disk space on the node.
* Increase node memory or storage.
* Add worker nodes.
* Configure proper CPU and Memory requests.
* Clean unused container images and logs.
* Redistribute workloads.

### How to Fix

```yaml
# 1. Verify Eviction Reason
kubectl describe pod <pod-name>
# Check: Evicted, MemoryPressure, DiskPressure, EphemeralStorage.
------------------------------------------------------------
# 2. Verify Node Status
kubectl describe node <node-name>
# Check: Conditions, Allocatable Resources, Pressure States.
------------------------------------------------------------
# 3. Verify Resource Usage
kubectl top nodes
kubectl top pods
# Compare resource usage with node capacity.
------------------------------------------------------------
# 4. Verify Pod Resource Configuration
kubectl describe deployment <deployment-name>
# Verify: CPU Requests, Memory Requests, Limits.
------------------------------------------------------------
# 5. Free Node Resources
kubectl drain <node-name> --ignore-daemonsets
# Remove unnecessary files, logs, or images if required.
------------------------------------------------------------
# 6. Validate
kubectl get pods -w
kubectl get nodes
# Verify Pod is recreated and remains Running.
```

