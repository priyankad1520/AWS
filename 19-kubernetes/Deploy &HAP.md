# Deployment
### A deployment was successful, all pods are Running and Ready, but after deployment users report that the new version is returning errors. What would you check first, and how would you decide whether to rollback?
"First, I’ll confirm that the deployment itself is healthy by checking the pods, readiness status, rollout status, and deployment events. Since users are seeing errors after the new version, I’ll check the application logs and monitoring dashboards to understand what changed.

Then I’ll compare the new version with the previous known-good deployment revision and check whether the errors started exactly after the rollout. I’ll also verify the application configuration, environment variables, Secrets, API dependencies, and database connectivity, because sometimes the deployment is technically successful but the application behavior is incorrect.

If the issue is clearly introduced by the new release and is impacting production users, my priority is to restore service quickly. Based on our rollback procedure, I’ll roll back to the last known-good revision using something like kubectl rollout undo deployment/<name> or through our deployment tool. After rollback, I’ll verify that the pods are healthy, error rates return to normal, and users can access the application.

Once service is stable, I’ll perform the root cause analysis with the development team and identify what needs to be fixed before redeploying."

Deployment → Health → Logs/Metrics → Compare with previous revision → Identify impact → Rollback if required → Validate → RCA
```bash
kubectl rollout status deployment/<deployment-name>
kubectl rollout history deployment/<deployment-name>
kubectl rollout undo deployment/<deployment-name>
```
### Problem 1: Deployment Replica Mismatch

> First, I'd compare the desired and available replicas using **kubectl get deployment**. Then I'd inspect the Deployment using **kubectl describe deployment** to identify why the desired replicas are not matching the available replicas. Next, I'd verify the ReplicaSet, Pod status, scheduling events, image pull status, and readiness probes. Based on the root cause, I'd fix the issue and validate that all desired replicas become available successfully.
> **"First, I'd compare the desired and available replicas using `kubectl get deployment`. Then I'd inspect the Deployment and ReplicaSet to identify why replicas are unavailable. Next, I'd verify the Pod status, readiness probe, image pull status, and scheduling events. After fixing the underlying issue, I'd monitor the rollout and confirm that all desired replicas become available."**

**Possible Causes:**

* Pods are in Pending state.
* Pods are crashing (CrashLoopBackOff).
* Readiness probe is failing.
* ImagePullBackOff or ErrImagePull.
* Insufficient node resources.
* Deployment update is still in progress.
* ReplicaSet issue.
* ResourceQuota restrictions.

**Investigation:**

```yaml
kubectl get deployment
kubectl describe deployment <deployment-name>
kubectl get replicaset
kubectl describe replicaset <replicaset-name>
kubectl get pods
kubectl get events --sort-by=.metadata.creationTimestamp
```
**Fixes:**

* Resolve Pending Pods.
* Fix CrashLoopBackOff.
* Resolve ImagePullBackOff.
* Fix readiness probe.
* Add worker node resources.
* Correct ReplicaSet issues.
* Increase ResourceQuota if required.

### How to Fix

```yaml
# 1. Verify Deployment Status
kubectl describe deployment <deployment-name>
# Check: Desired Replicas, Updated Replicas, Available Replicas, Conditions.
------------------------------------------------------------
# 2. Verify ReplicaSet
kubectl get rs
kubectl describe rs <replicaset-name>
# Verify: Desired, Current, Ready Pods.
------------------------------------------------------------
# 3. Verify Pod Status
kubectl get pods
kubectl describe pod <pod-name>
# Check: Pending, CrashLoopBackOff, ImagePullBackOff, Running.
------------------------------------------------------------
# 4. Verify Events
kubectl get events --sort-by=.metadata.creationTimestamp
# Check: FailedScheduling, FailedCreate, FailedMount.
------------------------------------------------------------
# 5. Validate
kubectl rollout status deployment <deployment-name>
kubectl get deployment
# Verify Available Replicas = Desired Replicas.
```
---

### Problem 2: Deployment Rollout Stuck

> First, I'd check the rollout status using **kubectl rollout status**. Then I'd inspect the Deployment events and ReplicaSet to identify why the rollout is not progressing. Next, I'd verify the new Pods, readiness probes, image version, and resource availability. Based on the findings, I'd resolve the issue or rollback to the previous stable version if required.
> **"First, I'd verify the rollout status using `kubectl rollout status`. Then I'd inspect the Deployment events and ReplicaSet to determine why the rollout is blocked. Next, I'd check the new Pods for readiness probe failures, application crashes, image issues, or scheduling problems. If necessary, I'd rollback to the previous stable version, fix the root cause, and validate that the rollout completes successfully."**

**Possible Causes:**

* Readiness probe failure.
* CrashLoopBackOff.
* ImagePullBackOff.
* Incorrect image version.
* ProgressDeadlineExceeded.
* Insufficient node resources.
* RollingUpdate strategy configuration.
* Pod scheduling issues.

**Investigation:**

```yaml
kubectl rollout status deployment <deployment-name>
kubectl describe deployment <deployment-name>
kubectl rollout history deployment <deployment-name>
kubectl get rs
kubectl get pods
kubectl get events
```

**Fixes:**

* Fix readiness probe.
* Fix application startup issue.
* Correct image version.
* Resolve scheduling issues.
* Increase node resources.
* Rollback Deployment if required.

### How to Fix

```yaml
# 1. Verify Rollout Status
kubectl rollout status deployment <deployment-name>
# Check rollout progress.
------------------------------------------------------------
# 2. Verify Deployment Events
kubectl describe deployment <deployment-name>
# Check: ProgressDeadlineExceeded, ReplicaFailure, MinimumReplicasUnavailable.
------------------------------------------------------------
# 3. Verify ReplicaSet
kubectl get rs
kubectl describe rs <replicaset-name>
# Verify new ReplicaSet creation.
------------------------------------------------------------
# 4. Verify Pod Status
kubectl get pods
kubectl describe pod <pod-name>
# Check: Readiness, CrashLoopBackOff, ImagePullBackOff.
------------------------------------------------------------
# 5. Rollback if Required
kubectl rollout undo deployment <deployment-name>
# Restore previous stable version.
------------------------------------------------------------
# 6. Validate
kubectl rollout status deployment <deployment-name>
kubectl get deployment
# Verify rollout completed successfully.
```
---

### Problem 3: Pods are not updating after Deployment

> First, I'd verify whether a new rollout has been triggered by checking the rollout history and Deployment generation. Then I'd inspect the Deployment specification to confirm that the image or Pod template has actually changed. Next, I'd verify the rollout strategy, ReplicaSet, and Pod status. Based on the findings, I'd trigger a new rollout if necessary and validate that the new Pods replace the old ones successfully.
> **"First, I'd verify whether the Deployment has detected a new change by checking the rollout history and Deployment specification. Then I'd confirm that the image or Pod template has actually been updated and that the rollout is progressing. If no rollout has been triggered, I'd perform a rollout restart or update the image tag. Finally, I'd verify that a new ReplicaSet is created and the new Pods replace the old ones successfully."**
**Possible Causes:**

* Image tag has not changed (for example, using `latest` without forcing a rollout).
* Deployment YAML has no Pod template changes.
* Rollout paused.
* Incorrect rollout strategy.
* ImagePullPolicy configuration.
* ArgoCD or GitOps synchronization issue.
* Manual changes overwritten.

**Investigation:**

```yaml
kubectl get deployment
kubectl describe deployment <deployment-name>
kubectl rollout history deployment <deployment-name>
kubectl get rs
kubectl get pods
kubectl get events
```

**Fixes:**

* Update the image tag.
* Trigger a rollout restart.
* Resume a paused rollout.
* Correct the rollout strategy.
* Sync ArgoCD or GitOps configuration.
* Set the appropriate ImagePullPolicy.

### How to Fix

```yaml
# 1. Verify Deployment Changes
kubectl describe deployment <deployment-name>
# Verify: Image, Generation, Pod Template.
------------------------------------------------------------
# 2. Verify Rollout History
kubectl rollout history deployment <deployment-name>
# Check whether a new revision was created.
------------------------------------------------------------
# 3. Verify Rollout Status
kubectl rollout status deployment <deployment-name>
# Confirm rollout progress.
------------------------------------------------------------
# 4. Trigger Rollout
kubectl rollout restart deployment <deployment-name>
# Force Deployment to create new Pods.
------------------------------------------------------------
# 5. Verify ReplicaSets
kubectl get rs
# Confirm new ReplicaSet is created.
------------------------------------------------------------
# 6. Validate
kubectl get pods -w
kubectl rollout status deployment <deployment-name>
# Verify old Pods terminate and new Pods become Running.
```

For Deployment troubleshooting, always remember this flow: Deployment --> ReplicaSet --> Pods -->Container

Almost every Deployment issue eventually traces back to one of these:

* **Pod issue** (CrashLoopBackOff, Pending, ImagePullBackOff)
* **ReplicaSet issue**
* **Rolling update configuration**
* **Readiness probe failure**
* **Resource constraints**

---

# Problem 4: Old Version is Still Running After Deployment

> First, I'd verify the Deployment status and rollout history using **kubectl rollout status** and **kubectl rollout history**. Then I'd check whether a new ReplicaSet has been created and whether the new Pods are running the expected image version. Next, I'd verify the image tag, rollout strategy, and Pod status. If the old Pods are still serving traffic, I'd identify whether the rollout is paused, stuck, or the image wasn't updated correctly. After fixing the issue, I'd validate that all Pods are running the latest application version.
> **"First, I'd verify the rollout status and rollout history to confirm whether a new deployment was triggered. Then I'd check the ReplicaSets and running Pods to ensure they're using the expected image version. Next, I'd verify the image tag, rollout strategy, and readiness probe because these commonly prevent new Pods from replacing old ones. After correcting the issue, I'd validate that the old ReplicaSet is scaled down and all Pods are running the latest application version."**


**Possible Causes:**

* Image tag was not updated.
* Same image tag (for example, `latest`) is reused.
* Deployment rollout is stuck.
* Rollout is paused.
* Readiness probe failure preventing new Pods from becoming Ready.
* ImagePullPolicy configuration issue.
* ArgoCD or GitOps synchronization issue.
* Old ReplicaSet is still serving traffic.

**Investigation:**

```yaml
kubectl get deployment
kubectl rollout status deployment <deployment-name>
kubectl rollout history deployment <deployment-name>
kubectl get rs
kubectl get pods -o wide
kubectl describe deployment <deployment-name>
```

**Fixes:**

* Update the image tag.
* Use unique image versions.
* Resume paused rollout.
* Fix readiness probe.
* Correct ImagePullPolicy.
* Sync ArgoCD or GitOps.
* Restart Deployment if required.

### How to Fix

```yaml
# 1. Verify Current Image
kubectl describe deployment <deployment-name>
# Verify: Image Name, Image Tag.
------------------------------------------------------------
# 2. Verify Rollout
kubectl rollout status deployment <deployment-name>
kubectl rollout history deployment <deployment-name>
# Check: Latest Revision, Rollout Progress.
------------------------------------------------------------
# 3. Verify ReplicaSets
kubectl get rs
# Verify: New ReplicaSet created, Old ReplicaSet scaled down.
------------------------------------------------------------
# 4. Verify Running Pods
kubectl get pods -o wide
kubectl describe pod <pod-name>
# Verify: Running Image Version.
------------------------------------------------------------
# 5. Restart Deployment if Required
kubectl rollout restart deployment <deployment-name>
------------------------------------------------------------
# 6. Validate
kubectl rollout status deployment <deployment-name>
kubectl get pods
# Verify all Pods are running the latest version.
```
---

# Problem 5: Rollback Failed

> First, I'd verify the rollback status using **kubectl rollout history** and inspect the Deployment events using **kubectl describe deployment**. Then I'd confirm whether the previous ReplicaSet still exists and whether the rollback revision is available. Next, I'd check for image issues, Pod failures, and resource constraints preventing the rollback. Based on the findings, I'd fix the underlying issue and validate that the Deployment successfully returns to the previous stable version.
> **"First, I'd verify the rollout history to ensure the previous revision is available for rollback. Then I'd inspect the Deployment events and ReplicaSets to identify why the rollback failed. Next, I'd verify the Pod status, image availability, and readiness probes to determine whether the previous version can start successfully. After resolving the issue, I'd perform the rollback again and validate that the Deployment is running the previous stable version without errors."**

**Possible Causes:**

* Previous ReplicaSet is unavailable.
* Rollback revision does not exist.
* Previous image has been deleted from the registry.
* Rollback Pods are failing with CrashLoopBackOff.
* ImagePullBackOff during rollback.
* Insufficient cluster resources.
* Readiness probe failure.
* Deployment configuration error.

**Investigation:**

```yaml
kubectl rollout history deployment <deployment-name>
kubectl describe deployment <deployment-name>
kubectl get rs
kubectl get pods
kubectl describe pod <pod-name>
kubectl get events --sort-by=.metadata.creationTimestamp
```

**Fixes:**

* Verify rollback revision.
* Restore the previous image.
* Fix Pod startup issues.
* Resolve ImagePullBackOff.
* Add cluster resources.
* Correct readiness probe.
* Redeploy the previous stable version manually if required.

### How to Fix

```yaml
# 1. Verify Rollback History
kubectl rollout history deployment <deployment-name>
# Verify: Available Revisions.
------------------------------------------------------------
# 2. Verify Deployment Events
kubectl describe deployment <deployment-name>
# Check: Rollback Events, Replica Failures.
------------------------------------------------------------
# 3. Verify ReplicaSets
kubectl get rs
# Confirm previous ReplicaSet exists.
------------------------------------------------------------
# 4. Verify Pod Status
kubectl get pods
kubectl describe pod <pod-name>
# Check: CrashLoopBackOff, ImagePullBackOff, Readiness Probe.
------------------------------------------------------------
# 5. Perform Rollback
kubectl rollout undo deployment <deployment-name>
# Or rollback to a specific revision:
kubectl rollout undo deployment <deployment-name> --to-revision=<revision>
------------------------------------------------------------
# 6. Validate
kubectl rollout status deployment <deployment-name>
kubectl get pods
# Verify previous stable version is running successfully.
```

**Deployment Interview Flow**: Deployment --> Rollout Status --> ReplicaSet --> Pods --> Container Logs --> Application

This flow works for almost every Deployment problem:

* Replica mismatch
* Rollout stuck
* Pods not updating
* Old version still running
* Rollback failed

---
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
