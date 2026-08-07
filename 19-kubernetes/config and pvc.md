# Storage 

### Problem 1: PVC is in Pending State

> First, I'd verify that the PVC is in the **Pending** state using **kubectl get pvc**. Then I'd inspect the PVC using **kubectl describe pvc** to identify whether the issue is related to the StorageClass, available Persistent Volumes, capacity, or access mode. Next, I'd verify the PV status and CSI provisioner. Based on the findings, I'd resolve the storage provisioning issue and validate that the PVC transitions to the **Bound** state.
> **"First, I'd verify that the PVC is in the Pending state using `kubectl get pvc`. Then I'd inspect the PVC and verify the StorageClass, requested capacity, and access mode. Next, I'd check whether a matching Persistent Volume is available and confirm that the CSI driver is healthy. After resolving the provisioning issue, I'd validate that the PVC is successfully bound to a PV."**

**Possible Causes:**

* StorageClass does not exist.
* Dynamic provisioning is not working.
* No available Persistent Volume.
* Requested capacity is larger than the available PV.
* AccessMode mismatch.
* CSI driver is not running.
* Storage provisioner failure.

**Investigation:**

```yaml
kubectl get pvc
kubectl describe pvc <pvc-name>
kubectl get pv
kubectl describe pv <pv-name>
kubectl get storageclass
kubectl get pods -n kube-system
```

**Fixes:**

* Create or correct the StorageClass.
* Restore the CSI driver.
* Create a matching Persistent Volume.
* Correct the requested capacity.
* Correct the AccessMode.
* Restart the storage provisioner.

### How to Fix

```yaml
# 1. Verify PVC
kubectl describe pvc <pvc-name>
# Check: Status, StorageClass, Capacity, AccessModes, Events.
------------------------------------------------------------
# 2. Verify PV
kubectl get pv
kubectl describe pv <pv-name>
# Verify: Available, Bound, Capacity.
------------------------------------------------------------
# 3. Verify StorageClass
kubectl get storageclass
# Verify correct StorageClass exists.
------------------------------------------------------------
# 4. Verify CSI Driver
kubectl get pods -n kube-system
# Verify CSI Pods are Running.
------------------------------------------------------------
# 5. Validate
kubectl get pvc
# Verify PVC changes from Pending to Bound.
```
---

### Problem 2: Volume Mount Failed

> First, I'd inspect the Pod events using **kubectl describe pod** to identify the volume mount error. Then I'd verify the PVC, PV, and StorageClass configuration. Next, I'd confirm that the CSI driver is functioning correctly and that the volume is attached to the node. Based on the findings, I'd resolve the storage issue and validate that the Pod starts successfully.
> **"First, I'd inspect the Pod events to identify the exact volume mount error. Then I'd verify that the PVC is bound to a PV and confirm that the CSI driver is healthy. Next, I'd check whether the volume is successfully attached to the node and that the mount path is configured correctly. After fixing the issue, I'd validate that the Pod starts successfully."**

**Possible Causes:**

* PVC is Pending.
* PV is unavailable.
* CSI driver failure.
* Volume attachment failure.
* Storage permissions issue.
* Incorrect mount path.
* Node cannot attach the volume.

**Investigation:**

```yaml
kubectl describe pod <pod-name>
kubectl get pvc
kubectl describe pvc <pvc-name>
kubectl get pv
kubectl get pods -n kube-system
kubectl get events
```

**Fixes:**

* Resolve the Pending PVC.
* Restore the CSI driver.
* Fix volume attachment.
* Correct the mount path.
* Restore storage permissions.

### How to Fix

```yaml
# 1. Verify Pod Events
kubectl describe pod <pod-name>
# Check: FailedMount, FailedAttachVolume.
------------------------------------------------------------
# 2. Verify PVC
kubectl describe pvc <pvc-name>
# Verify Bound status.
------------------------------------------------------------
# 3. Verify PV
kubectl describe pv <pv-name>
# Verify volume availability.
------------------------------------------------------------
# 4. Verify CSI Driver
kubectl get pods -n kube-system
# Verify CSI Pods are Running.
------------------------------------------------------------
# 5. Validate
kubectl get pods
# Verify Pod reaches Running state.
```
---

### Problem 3: Volume is Mounted as Read-Only

> First, I'd verify the volume mount configuration in the Pod specification and inspect the PVC and PV. Then I'd determine whether the volume is intentionally configured as read-only or if the storage backend has switched the volume to read-only due to an error. Next, I'd review the storage provider and CSI logs. Based on the findings, I'd correct the configuration and validate that the application can write to the volume.
> **"First, I'd verify whether the volume is configured as read-only in the Pod specification. Then I'd inspect the PVC, PV, and CSI logs to determine whether the storage backend has forced the volume into read-only mode. After correcting the configuration or resolving the storage issue, I'd validate that the application can successfully write to the mounted volume."**

**Possible Causes:**

* Volume mounted with `readOnly: true`.
* Storage backend forced the volume to read-only.
* File system corruption.
* CSI driver issue.
* Incorrect storage permissions.

**Investigation:**

```yaml
kubectl describe pod <pod-name>
kubectl describe pvc <pvc-name>
kubectl describe pv <pv-name>
kubectl get pods -n kube-system
kubectl logs -n kube-system <csi-pod>
```

**Fixes:**

* Remove `readOnly: true` if not required.
* Repair the file system.
* Restore storage permissions.
* Restart the CSI driver.
* Recover the storage backend.

### How to Fix

```yaml
# 1. Verify Volume Mount
kubectl describe pod <pod-name>
# Verify: Mount Path, ReadOnly.
------------------------------------------------------------
# 2. Verify PVC & PV
kubectl describe pvc <pvc-name>
kubectl describe pv <pv-name>
# Verify storage status.
------------------------------------------------------------
# 3. Verify CSI Logs
kubectl logs -n kube-system <csi-pod>
# Check storage errors.
------------------------------------------------------------
# 4. Verify File System
# Check file system status on the storage backend if applicable.
------------------------------------------------------------
# 5. Validate
kubectl exec -it <pod-name> -- touch /mount-path/test.txt
# Verify write access succeeds.
```
---

### Problem 4: PV is Not Bound

> First, I'd verify the PV and PVC status using **kubectl get pv** and **kubectl get pvc**. Then I'd compare the StorageClass, capacity, and access mode between the PV and PVC. Next, I'd review the PV events and provisioning logs to identify the reason for the binding failure. Based on the findings, I'd correct the storage configuration and validate that the PV is successfully bound to the PVC.
> **"First, I'd verify the PV and PVC status and compare their StorageClass, capacity, and access modes. Then I'd inspect the events to identify the reason for the binding failure and confirm that the CSI provisioner is healthy. After correcting the configuration, I'd validate that the PV and PVC are successfully bound."**

**Possible Causes:**

* StorageClass mismatch.
* Capacity mismatch.
* AccessMode mismatch.
* PV already bound to another PVC.
* ClaimRef mismatch.
* CSI provisioning issue.

**Investigation:**

```yaml
kubectl get pv
kubectl describe pv <pv-name>
kubectl get pvc
kubectl describe pvc <pvc-name>
kubectl get storageclass
kubectl get events
```

**Fixes:**

* Match the StorageClass.
* Match the requested capacity.
* Match the AccessMode.
* Remove an incorrect ClaimRef if appropriate.
* Restore the CSI provisioner.

### How to Fix

```yaml
# 1. Verify PV
kubectl describe pv <pv-name>
# Check: Status, StorageClass, Capacity, AccessModes, ClaimRef.
------------------------------------------------------------
# 2. Verify PVC
kubectl describe pvc <pvc-name>
# Verify requested StorageClass, Capacity, AccessModes.
------------------------------------------------------------
# 3. Verify StorageClass
kubectl get storageclass
# Confirm StorageClass matches.
------------------------------------------------------------
# 4. Verify Events
kubectl get events --sort-by=.metadata.creationTimestamp
# Check for provisioning or binding failures.
------------------------------------------------------------
# 5. Validate
kubectl get pv
kubectl get pvc
# Verify PV and PVC are in Bound state.
```

**Storage Troubleshooting Flow** 

```text
Pod
   ↓
Volume Mount
   ↓
PVC
   ↓
PV
   ↓
StorageClass
   ↓
CSI Driver
   ↓
Storage Backend
```

* **PVC Pending** → **StorageClass → PV → CSI**
* **Volume Mount Failed** → **Pod Events → PVC → PV → CSI**
* **Read-Only Volume** → **Mount Options → CSI → Storage Backend**
* **PV Not Bound** → **StorageClass → Capacity → AccessMode → ClaimRef**

---
# ConfigMaps and Secrets
### Problem 1: Application Cannot Start Due to ConfigMap or Secret Issue

> First, I'd verify the Pod status using **kubectl get pods** and inspect the Pod events using **kubectl describe pod**. Then I'd review the container logs to identify whether the application failed because of missing configuration or secrets. Next, I'd verify the ConfigMap, Secret, environment variables, and mounted volumes. Based on the findings, I'd correct the configuration and validate that the application starts successfully.
> **"First, I'd inspect the Pod events and application logs to determine whether the startup failure is related to a ConfigMap or Secret. Then I'd verify that the required ConfigMap and Secret exist and that the correct keys are referenced in the Deployment. After correcting the configuration, I'd restart the Deployment and validate that the application starts successfully."**

**Possible Causes:**

* ConfigMap does not exist.
* Secret does not exist.
* Incorrect ConfigMap key.
* Incorrect Secret key.
* Incorrect environment variable reference.
* ConfigMap or Secret not mounted.
* Application expecting a missing configuration.

**Investigation:**

```yaml
kubectl get pods
kubectl describe pod <pod-name>
kubectl logs <pod-name>
kubectl get configmap
kubectl get secret
kubectl describe deployment <deployment-name>
```

**Fixes:**

* Create the missing ConfigMap.
* Create the missing Secret.
* Correct ConfigMap or Secret keys.
* Correct environment variable references.
* Mount ConfigMap or Secret correctly.
* Restart the Deployment.

### How to Fix

```yaml
# 1. Verify Pod Events
kubectl describe pod <pod-name>
# Check: FailedMount, CreateContainerConfigError, CreateContainerError.
------------------------------------------------------------
# 2. Verify Application Logs
kubectl logs <pod-name>
# Identify missing configuration or Secret errors.
------------------------------------------------------------
# 3. Verify ConfigMap
kubectl get configmap
kubectl describe configmap <configmap-name>
# Verify ConfigMap exists and required keys are present.
------------------------------------------------------------
# 4. Verify Secret
kubectl get secret
kubectl describe secret <secret-name>
# Verify Secret exists and required keys are present.
------------------------------------------------------------
# 5. Validate
kubectl rollout restart deployment <deployment-name>
kubectl get pods -w
# Verify Pod reaches Running state.
```
---

### Problem 2: Missing Environment Variable

> First, I'd inspect the Pod specification using **kubectl describe pod** to verify whether the required environment variables are present. Then I'd review the Deployment configuration to confirm that the environment variables correctly reference the ConfigMap or Secret. Based on the findings, I'd update the configuration and validate that the application receives the required environment variables.
> **"First, I'd inspect the Pod environment variables and compare them with the Deployment configuration. Then I'd verify that the ConfigMap or Secret contains the required keys and that the Deployment references them correctly. After fixing the configuration, I'd restart the Deployment and validate that the application receives the required environment variables."**

**Possible Causes:**

* Incorrect ConfigMap key.
* Incorrect Secret key.
* Wrong environment variable name.
* ConfigMap or Secret deleted.
* Incorrect `env` or `envFrom` configuration.

**Investigation:**

```yaml
kubectl describe pod <pod-name>
kubectl describe deployment <deployment-name>
kubectl get configmap
kubectl get secret
kubectl exec -it <pod-name> -- env
```

**Fixes:**

* Correct the ConfigMap key.
* Correct the Secret key.
* Correct the environment variable mapping.
* Recreate the missing ConfigMap or Secret.
* Restart the Deployment.

### How to Fix

```yaml
# 1. Verify Environment Variables
kubectl exec -it <pod-name> -- env
# Verify required variables exist.
------------------------------------------------------------
# 2. Verify Deployment
kubectl describe deployment <deployment-name>
# Verify env, envFrom, ConfigMapKeyRef, SecretKeyRef.
------------------------------------------------------------
# 3. Verify ConfigMap
kubectl describe configmap <configmap-name>
# Verify required keys.
------------------------------------------------------------
# 4. Verify Secret
kubectl describe secret <secret-name>
# Verify required keys.
------------------------------------------------------------
# 5. Validate
kubectl rollout restart deployment <deployment-name>
kubectl exec -it <pod-name> -- env
# Verify environment variables are available.
```
---

### Problem 3: Secret is Not Mounted

> First, I'd inspect the Pod events using **kubectl describe pod** to identify the Secret mount failure. Then I'd verify that the Secret exists and that the Deployment references the correct Secret name. Next, I'd review the volume and volumeMount configuration. Based on the findings, I'd correct the Secret configuration and validate that it is mounted successfully.
> **"First, I'd inspect the Pod events to identify the Secret mount failure. Then I'd verify that the Secret exists and that the Deployment references the correct Secret name and mount path. After correcting the configuration, I'd validate that the Secret is mounted successfully and the application starts normally."**

**Possible Causes:**

* Secret does not exist.
* Incorrect Secret name.
* Incorrect Secret key.
* Wrong mount path.
* Incorrect volume configuration.
* RBAC permission issue.

**Investigation:**

```yaml
kubectl describe pod <pod-name>
kubectl get secret
kubectl describe secret <secret-name>
kubectl describe deployment <deployment-name>
```

**Fixes:**

* Create the missing Secret.
* Correct the Secret name.
* Correct the Secret key.
* Fix volume and volumeMount configuration.
* Correct RBAC permissions.

### How to Fix

```yaml
# 1. Verify Pod Events
kubectl describe pod <pod-name>
# Check: FailedMount, Secret not found.
------------------------------------------------------------
# 2. Verify Secret
kubectl get secret
kubectl describe secret <secret-name>
# Verify Secret exists.
------------------------------------------------------------
# 3. Verify Deployment
kubectl describe deployment <deployment-name>
# Verify Secret Name, Volume, VolumeMount.
------------------------------------------------------------
# 4. Verify Mount Path
kubectl exec -it <pod-name> -- ls <mount-path>
# Verify Secret files exist.
------------------------------------------------------------
# 5. Validate
kubectl get pods
# Verify Secret is mounted successfully.
```
---

### Problem 4: ConfigMap is Not Mounted

> First, I'd inspect the Pod events using **kubectl describe pod** to identify the ConfigMap mount failure. Then I'd verify that the ConfigMap exists and that the Deployment references the correct ConfigMap name. Next, I'd review the volume and volumeMount configuration. Based on the findings, I'd correct the configuration and validate that the ConfigMap is mounted successfully.
> **"First, I'd inspect the Pod events to identify the ConfigMap mount failure. Then I'd verify that the ConfigMap exists and that the Deployment references the correct ConfigMap name and mount path. After correcting the configuration, I'd restart the Deployment and validate that the ConfigMap is mounted successfully."**

**Possible Causes:**

* ConfigMap does not exist.
* Incorrect ConfigMap name.
* Incorrect ConfigMap key.
* Wrong mount path.
* Incorrect volume configuration.
* Deployment references an outdated ConfigMap.

**Investigation:**

```yaml
kubectl describe pod <pod-name>
kubectl get configmap
kubectl describe configmap <configmap-name>
kubectl describe deployment <deployment-name>
```

**Fixes:**

* Create the missing ConfigMap.
* Correct the ConfigMap name.
* Correct the ConfigMap key.
* Fix volume and volumeMount configuration.
* Restart the Deployment.

### How to Fix

```yaml
# 1. Verify Pod Events
kubectl describe pod <pod-name>
# Check: FailedMount, ConfigMap not found.
------------------------------------------------------------
# 2. Verify ConfigMap
kubectl get configmap
kubectl describe configmap <configmap-name>
# Verify ConfigMap exists and contains required keys.
------------------------------------------------------------
# 3. Verify Deployment
kubectl describe deployment <deployment-name>
# Verify ConfigMap Name, Volume, VolumeMount.
------------------------------------------------------------
# 4. Verify Mount Path
kubectl exec -it <pod-name> -- ls <mount-path>
# Verify ConfigMap files exist.
------------------------------------------------------------
# 5. Validate
kubectl get pods
# Verify ConfigMap is mounted successfully.
```
---

**ConfigMap & Secret Troubleshooting Flow** 

```text
Pod
   ↓
Pod Events
   ↓
Application Logs
   ↓
ConfigMap / Secret
   ↓
Environment Variables
   ↓
Volume & VolumeMount
   ↓
Deployment
```

* **App not starting** → **Logs → ConfigMap → Secret**
* **Missing environment variable** → **Deployment → env/envFrom → ConfigMap/Secret**
* **Secret not mounted** → **Secret → Volume → VolumeMount**
* **ConfigMap not mounted** → **ConfigMap → Volume → VolumeMount**
