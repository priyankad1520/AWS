## CrashLoopBackOff

### Problem

* Pod continuously crashes and restarts.
* Status shows **CrashLoopBackOff**.

- Step 1: Check Pod status.: **kubectl get pods**
- Step 2: Describe the Pod.: **kubectl describe pod <pod-name>** --> Check the **Events** section. --> Identify at which step the Pod failed.
- Step 3: View Pod logs. **kubectl logs <pod-name>** --> Find the exact application error. Example → Missing environment variable **DB_HOST**.
- Step 4: Fix the issue in the Pod or Deployment YAML. Add the missing environment variable or correct the configuration.
- Step 5: Apply the updated YAML. **kubectl apply -f <yaml-file>**

## ImagePullBackOff

### Problem
Kubernetes cannot pull the container image.
- Step 1: **kubectl get pods**
- Step 2: **kubectl describe pod <pod-name>**. Check the **Events** section.

### Most Common Cause

* Wrong image name.
* Wrong image tag.
* Image does not exist in the registry.
* Private registry authentication issue.

### Fix

* Correct the image name or tag.
* Push the image again through CI/CD.
* Configure **imagePullSecrets** for private registries.

## YAML Applied but No Pod Created
- Step 1: Check **kind**. Verify it is **Pod** or **Deployment**. Check for spelling mistakes.
- Step 2: Verify **apiVersion** and **spec**.
- Step 3: **kubectl get all**. Check whether resources were actually created.
- Step 4: **kubectl apply --dry-run=client -f <yaml-file>**. Validate the YAML before applying.

## YAML Parsing Error

### Problem
`kubectl apply` fails immediately.

### Check

* Indentation errors.
* Invalid YAML syntax.
* Wrong data types.
* Validate using a YAML linter.

### Root Cause
Kubernetes never received the request because the YAML file itself is invalid.

## Pod Stuck in Pending
- Step 1: **kubectl describe pod <pod-name>**. Check the **Events** section.
- Step 2: Check CPU and Memory availability. Update resource requests and limits if needed.
- Step 3: Check **Node Selector**. Check **Taints and Tolerations**. Check **Node Affinity**.
- **Root Cause:** Kubernetes cannot find a suitable worker node to schedule the Pod.

## OOMKilled

### Problem
Container exceeds its allocated memory. Exit Code **137**.

- Step 1: **kubectl describe pod <pod-name>**.Confirm **OOMKilled**.
- Step 2: **kubectl top pod <pod-name>**. Check current CPU and Memory usage.
- Step 3: Check Deployment YAML. Compare memory usage with configured memory limits.
- Step 4: Increase the memory limit. Example: **512Mi → 768Mi**
- Step 5: **kubectl apply -f deployment.yaml**
- Step 6:  Verify the Pod is no longer getting **OOMKilled**.
## Pod Restarts Frequently but No Logs Visible

### Problem

* Pod restarts continuously.

* No logs are visible.

* Status shows **CrashLoopBackOff**.

* **Step 1:** Check Pod status. **`kubectl get pods`**. Verify the restart count is increasing.

* **Step 2:** Describe the Pod. **`kubectl describe pod <pod-name>`**. Check the **Events** section.

* **Step 3:** Check logs from the previous failed container. **`kubectl logs --previous <pod-name>`**.

* **Step 4:** Identify the error. Example → **Database not reachable**.

* **Step 5:** Verify the database Service is running in the cluster.

* **Step 6:** If the database Service is healthy, coordinate with the **Database Team** to verify connectivity, authentication, or database availability.

* **Step 7:** After the issue is fixed, redeploy and verify the Pod is no longer restarting.

---

# Container Exits Immediately with Exit Code 1

### Problem

* Container exits immediately.

* Exit Code **1** indicates a general application error.

* **Step 1:** Check Pod status. **`kubectl get pods`**.

* **Step 2:** Describe the Pod. **`kubectl describe pod <pod-name>`**. Check the **Events** section.

* **Step 3:** View previous logs. **`kubectl logs --previous <pod-name>`**.

* **Step 4:** Identify the application error. Example → Missing configuration file, Invalid environment variable, Missing environment variable.

* **Step 5:** Update the **ConfigMap** or Deployment YAML with the correct configuration.

* **Step 6:** Redeploy. **`kubectl apply -f deployment.yaml`**.

* **Step 7:** Verify the Pod is running. **`kubectl get pods`**.

---

# Deployment Created but No Pods Started

### Problem

* Deployment is created.

* No Pods are running.

* **Step 1:** Verify the Deployment. **`kubectl get deployment`**.

* **Step 2:** Check Pods. **`kubectl get pods`**.

* **Step 3:** Describe the Deployment. **`kubectl describe deployment <deployment-name>`**. Check the **Events** section.

* **Step 4:** If the event shows **ImagePullSecret not found** or **Failed to pull image**, verify the image pull secret.

### Most Common Cause

* Missing **imagePullSecret**.
* Private registry authentication not configured.

### Fix

* Create the Docker registry secret. **`kubectl create secret docker-registry <secret-name> ...`**
* Add **imagePullSecrets** to the Deployment YAML.
* Redeploy. **`kubectl apply -f deployment.yaml`**.
* Verify the Pods are created successfully.

---

# Init Containers Not Running

### Problem

* Pod is created.

* Init Containers are not executed.

* **Step 1:** Describe the Pod. **`kubectl describe pod <pod-name>`**.

* **Step 2:** Verify whether Init Containers are listed.

* **Step 3:** Check the Pod YAML under **spec**.

### Most Common Cause

* **initContainers** is placed inside **containers** instead of at the same level in the Pod specification.

### Fix

* Move **initContainers** to the correct location under **spec**.
* Redeploy. **`kubectl apply -f <pod.yaml>`**.
* Verify the Init Containers execute before the main container.
Absolutely. I understand what you want now.

You don't just want the **commands**. You also want the **purpose/comment** beside each command, like **"Check the Pod status"**, **"Check the namespace"**, **"Verify the Service Account"**, etc. That's actually much better for interview revision because you'll remember **why** you're running each command.

Here's your notes in that format.

---

# Init Container Stuck in CrashLoopBackOff

### Problem

* Init Container fails repeatedly.

* Main application container never starts.

* **Step 1: Check the Pod status.** **`kubectl get pods`**

  * Verify whether the Pod is in **Init:CrashLoopBackOff**.

* **Step 2: Describe the Pod.** **`kubectl describe pod <pod-name>`**

  * Check the **Events** section.
  * Verify why the Init Container failed.
  * Example → Exit Code **1**.

* **Step 3: Check Init Container logs.** **`kubectl logs <pod-name> -c <init-container-name>`**

  * Find the exact application error.
  * Example → Database connection failed.

* **Step 4: Verify the Database Service.** **`kubectl get svc`**

  * Confirm the database Service exists.
  * Verify DNS resolution.
  * Check whether the database is ready.

* **Step 5: Fix the issue and redeploy.**

  * Review the database migration script.
  * Verify database credentials.
  * Delete the failed Pod. **`kubectl delete pod <pod-name>`**
  * Apply the updated Deployment. **`kubectl apply -f deployment.yaml`**
  * Verify the Pod is running.

---

# Sidecar Container Cannot Read Logs

### Problem

* Main container writes logs.

* Sidecar container cannot access them.

* **Step 1: Check the Pod status.** **`kubectl get pods`**

  * Verify both containers are running.

* **Step 2: Describe the Pod.** **`kubectl describe pod <pod-name>`**

  * Check the **Events** section for container failures.

* **Step 3: Check the Sidecar logs.** **`kubectl logs <pod-name> -c <sidecar-container>`**

  * Verify whether the Sidecar is reading the log file.

* **Step 4: Verify the shared volume configuration.**

  * Ensure both containers mount the same volume.
  * Verify the mount path is identical.
  * Check file permissions.

### Most Common Cause

* Shared volume not mounted.
* Incorrect mount path.
* File permission issue.

### Fix

* Correct the **volumeMounts** configuration.
* Mount the same shared volume in both containers.
* Redeploy the Pod.
* Verify the Sidecar can now stream the logs.

---

# High Latency Between Pods

### Problem

* Communication between Pods is slow.

* **Step 1: Check Pod placement.** **`kubectl get pods -o wide`**

  * Verify which worker node each Pod is running on.

* **Step 2: Check Pod Affinity configuration.** **`kubectl describe pod <pod-name>`**

  * Verify whether **preferred** or **required** affinity is configured.

* **Step 3: Check Node resource utilization.** **`kubectl top nodes`**

  * Verify CPU and Memory availability.
  * Check whether the preferred node has sufficient resources.

### Root Cause

* Preferred affinity allowed Kubernetes to place Pods on different nodes because the preferred node had insufficient resources.

### Fix

* Change **preferredDuringSchedulingIgnoredDuringExecution** to **requiredDuringSchedulingIgnoredDuringExecution** if the application requires co-location.
* Reapply the YAML.
* Verify both Pods are scheduled on the same worker node.

---

# Pod Not Receiving an IP Address

### Problem

* Pod has no IP address.

* Pod cannot communicate with other Pods.

* **Step 1: Check the Pod status.** **`kubectl get pods -o wide`**

  * Verify whether the Pod has an IP address.

* **Step 2: Describe the Pod.** **`kubectl describe pod <pod-name>`**

  * Check the **Events** section.
  * Verify whether network setup failed.

* **Step 3: Check the CNI Plugin Pods.** **`kubectl get pods -n kube-system`**

  * Verify Calico/Cilium/Flannel Pods are healthy.

* **Step 4: Check the failing CNI Pod logs.** **`kubectl logs <cni-pod-name> -n kube-system`**

  * Identify the networking issue.

### Most Common Cause

* CNI Plugin failure.
* Network configuration issue.

### Fix

* Restart the failing CNI Pod.
* Verify the CNI Plugin becomes healthy.
* Restart the application Pod.
* Verify the Pod receives an IP address.

---

# ReplicaSet Not Creating Pods

### Problem

* ReplicaSet exists.

* Desired replicas are configured.

* No Pods are created.

* **Step 1: Check ReplicaSet status.** **`kubectl get rs`**

  * Verify Desired, Current, and Ready replica count.

* **Step 2: Describe the ReplicaSet.** **`kubectl describe rs <replicaset-name>`**

  * Check the **Events** section.
  * Identify why Pods were not created.

* **Step 3: Verify the Pod template.**

  * Check the configured Service Account.
  * Verify image, labels, and selectors.

* **Step 4: Check whether the Service Account exists.** **`kubectl get sa`**

  * Confirm the required Service Account is available.

### Most Common Cause

* Missing Service Account.

### Fix

* Create the missing Service Account. **`kubectl create serviceaccount <service-account-name>`**
* Recreate or restart the ReplicaSet.
* Verify the Pods are created successfully.
# Deployment Scaled but Only Four Pods Running

### Problem

* Deployment scaled from **2 → 6** replicas.

* Only **4 Pods** are running.

* **Step 1: Check the Deployment status.** **`kubectl get deployment`**

  * Verify desired and available replica count.

* **Step 2: Check the ReplicaSet.** **`kubectl get rs`**

  * Verify whether ReplicaSet failed to create Pods.

* **Step 3: Check the Pods.** **`kubectl get pods`**

  * Identify Pending Pods.

* **Step 4: Describe the Pending Pod.** **`kubectl describe pod <pod-name>`**

  * Check the **Events** section.
  * Verify failed scheduling errors.

* **Step 5: Check Node resources.** **`kubectl top nodes`**

  * Verify CPU and Memory utilization.

### Root Cause

* Worker nodes had insufficient memory.
* Scheduler could not place the remaining Pods.

### Fix

* Reduce the memory request in the Deployment YAML.
* Or add more worker node capacity.
* Apply the updated Deployment. **`kubectl apply -f deployment.yaml`**
* Verify all **6 Pods** are running.

---

# Rolling Update Caused Downtime

### Problem

* Users experienced downtime during a Rolling Update.

* **Step 1: Check the rollout status.** **`kubectl rollout status deployment <deployment-name>`**

  * Verify whether the rollout completed successfully.

* **Step 2: Check the Deployment strategy.** **`kubectl describe deployment <deployment-name>`**

  * Verify **maxUnavailable** and **maxSurge** values.

* **Step 3: Check Readiness Probe configuration.**

  * Verify whether Pods become Ready only after the application is actually ready.

### Root Cause

* **maxUnavailable** was set too high.
* Readiness Probe was not configured properly.
* Kubernetes terminated old Pods before new Pods became Ready.

### Fix

* Set **maxUnavailable: 0**.
* Set **maxSurge: 1**.
* Configure **readinessProbe** with **initialDelaySeconds**.
* Apply the updated Deployment. **`kubectl apply -f deployment.yaml`**
* Verify zero-downtime rollout.

---

# ClusterIP Service Not Reachable

### Problem

* Pods are running.

* ClusterIP Service is unreachable.

* **Step 1: Check the Service.** **`kubectl get svc`**

  * Verify the Service exists.

* **Step 2: Check the Endpoints.** **`kubectl get endpoints <service-name>`**

  * Verify whether the Service has backend Pods.

* **Step 3: Check the Service selector.** **`kubectl describe svc <service-name>`**

  * Verify the selector matches the Pod labels.

### Root Cause

* Service selector did not match the Pod labels.
* Service had no Endpoints.

### Fix

* Update the Service selector.
* Apply the updated Service YAML. **`kubectl apply -f service.yaml`**
* Verify connectivity.

---

# ClusterIP Resolves DNS but Connection Refused

### Problem

* DNS resolution works.

* Requests fail with **Connection Refused**.

* **Step 1: Check the Service.** **`kubectl get svc`**

  * Verify the Service exists.

* **Step 2: Check the Endpoints.** **`kubectl get endpoints <service-name>`**

  * Verify the Service has backend Pods.

* **Step 3: Check Service ports.** **`kubectl describe svc <service-name>`**

  * Compare **port** and **targetPort** with the container port.

### Root Cause

* **targetPort** did not match the application's listening port.
* Service forwarded traffic to the wrong port.

### Fix

* Update **targetPort** to the correct container port (Example: **8080**).
* Apply the updated Service YAML. **`kubectl apply -f service.yaml`**
* Verify requests succeed.

---

# NodePort Works on One Node but Fails on Another

### Problem

* NodePort Service works on one node.

* Fails on another node.

* **Step 1: Check the Service.** **`kubectl get svc`**

  * Verify the NodePort is configured correctly.

* **Step 2: Check the Endpoints.** **`kubectl get endpoints <service-name>`**

  * Verify backend Pods are healthy.

* **Step 3: Test NodePort from each node.** **kubectl get -l app=myapp -o wide**

  * Identify which node is failing. connection refused

* **Step 4: Check the firewall rules on the affected node.** **sudo ufw status**

  * Verify whether the NodePort is blocked. Action shows Deny

### Root Cause

* Firewall rule blocked the NodePort.
* Traffic could not reach **kube-proxy**.

### Fix

* Remove the firewall deny rule. using **sudo ufw allow 30080/tcp**
* Allow the NodePort.
* Verify the NodePort is reachable from all worker nodes. comforming the firewall is the root cause of this issue.
# Clients Outside the Cluster Cannot Access the NodePort

### Problem

* NodePort Service is created.

* External clients cannot access the application.

* Required NodePort is already open.

* **Step 1: Check the Service.** **`kubectl get svc external-nodeport -o wide`**

  * Verify the Service is created as **NodePort**.
  * Confirm the correct NodePort is exposed.

* **Step 2: Check the Endpoints.** **`kubectl get endpoints <service-name>`**

  * Verify backend Pod IPs are present.
  * Confirm Pods are healthy.

* **Step 3: Test the NodePort from inside the cluster.** **`curl -s http://<node-ip>:31080`**

  * Verify the Service is reachable internally.
  * If it works internally, Kubernetes networking is functioning correctly.

* **Step 4: Test the NodePort from outside the cluster.** **`curl -s http://<public-node-ip>:31080`**


  * Access the application using the node's public IP and NodePort.
  * Verify whether external traffic reaches the node.

* **Step 5: Check the external firewall or Security Group.** **`sudo iptables -L -n | grep 31080`**

  * Verify the NodePort is allowed in the firewall or cloud Security Group.
  * Check whether network ACLs or firewall rules are blocking the traffic.

### Root Cause

* External firewall, Security Group, or Network ACL blocked the NodePort.
* Traffic never reached the Kubernetes node.

### Fix

* Allow the required NodePort in the firewall, Security Group, or Network ACL.
* Coordinate with the Network/Firewall team if required.
* Verify external access using the node's public IP and NodePort.
* Confirm the application is accessible from outside the cluster.
Absolutely. From now on, I'll include the **actual troubleshooting command** wherever applicable, not just "check this". That's much more useful for interviews and real production.

---

# Service Has Multiple Endpoints but Traffic Reaches Only One Node

### Problem

* Service has multiple endpoints.

* Traffic always reaches Pods on only one node.

* **Step 1: Check the Service.** **`kubectl get svc <service-name>`**

  * Verify the Service exists.

* **Step 2: Check the Service Endpoints.** **`kubectl get endpoints <service-name>`**

  * Verify all backend Pod IPs are registered.

* **Step 3: Check Pod distribution across nodes.** **`kubectl get pods -o wide`**

  * Verify Pods are running on multiple worker nodes.

* **Step 4: Check the kube-proxy Pods.** **`kubectl get pods -n kube-system -l k8s-app=kube-proxy -o wide`**

  * Verify kube-proxy is running on every worker node.
  * Identify if kube-proxy is missing or not running on any node.

* **Step 5: Check kube-proxy logs on the affected node.**
  **`kubectl logs -n kube-system <kube-proxy-pod-name>`**

  * Verify whether kube-proxy failed to configure **iptables** or **IPVS** rules.

* **Step 6: Restart the kube-proxy Pod.**
  **`kubectl delete pod <kube-proxy-pod-name> -n kube-system`**

  * Kubernetes recreates the kube-proxy Pod automatically because it runs as a **DaemonSet**.

* **Step 7: Verify traffic balancing.**

  * **`kubectl get pods -n kube-system -l k8s-app=kube-proxy -o wide`** → Confirm kube-proxy is running on all nodes.
  * **`kubectl get endpoints <service-name>`** → Confirm endpoints are healthy.
  * **`curl http://<NodeIP>:<NodePort>`** *(run multiple times from a client or another Pod)* → Verify requests are distributed across Pods on different nodes.

### Root Cause

* **kube-proxy** was not running on one worker node.
* It could not program the **iptables/IPVS** rules.
* Traffic was routed only to Pods on the healthy node.

### Fix

* Restart the kube-proxy Pod.
* Verify kube-proxy is healthy on every worker node.
* Confirm traffic is balanced across all Pods.

# Service Name Fails but Endpoints Exist

### Problem

* Service exists.

* Endpoints exist.

* Traffic works using **Pod IP**.

* Traffic fails only when using the **Service Name**.

* **Step 1: Check the Service.** **`kubectl get svc <service-name>`**

  * Verify the Service exists.

* **Step 2: Check the Endpoints.** **`kubectl get endpoints <service-name>`**

  * Verify backend Pod IPs are present.

* **Step 3: Verify direct Pod connectivity.**
  **`kubectl exec -it <pod-name> -- curl http://<pod-ip>:<port>`**

  * Confirm the application is reachable using the Pod IP.

* **Step 4: Check Service DNS resolution.**
  **`kubectl exec -it <pod-name> -- nslookup <service-name>`**

  * Verify whether the Service name resolves to a ClusterIP.

* **Step 5: Check CoreDNS Pods.**
  **`kubectl get pods -n kube-system -l k8s-app=kube-dns`**

  * Verify CoreDNS Pods are running.

* **Step 6: Check CoreDNS logs.**
  **`kubectl logs -n kube-system <coredns-pod-name>`**

  * Verify whether CoreDNS is in **CrashLoopBackOff** or reporting DNS errors.

### Root Cause

* CoreDNS failed.
* Service name resolution was unavailable.

### Fix

* Restart the CoreDNS Pod.
  **`kubectl delete pod <coredns-pod-name> -n kube-system`**
* Verify DNS resolution.
  **`kubectl exec -it <pod-name> -- nslookup <service-name>`**
* Verify Service connectivity.
  **`kubectl exec -it <pod-name> -- curl http://<service-name>:<port>`**

---

# Headless Service Returns No DNS Records

### Problem

* Headless Service exists.

* Pods are running.

* DNS returns no records.

* **Step 1: Check the Headless Service.**
  **`kubectl get svc <service-name>`**

  * Verify **ClusterIP = None**.

* **Step 2: Check DNS resolution.**
  **`kubectl exec -it <pod-name> -- nslookup <service-name>`**

  * Verify whether Pod IPs are returned.

* **Step 3: Check the Endpoints.**
  **`kubectl get endpoints <service-name>`**

  * Verify whether backend Pod IPs exist.

* **Step 4: Verify the Service selector.**
  **`kubectl describe svc <service-name>`**

  * Compare the Service selector with the Pod labels.

* **Step 5: Verify Pod labels.**
  **`kubectl get pods --show-labels`**

  * Confirm the labels exactly match the Service selector.

### Root Cause

* Service selector did not match the Pod labels.
* No Endpoints were created.
* DNS had no Pod IPs to publish.

### Fix

* Correct the Service selector in the YAML.
* Apply the updated Service.
  **`kubectl apply -f service.yaml`**
* Verify Endpoints.
  **`kubectl get endpoints <service-name>`**
* Verify DNS.
  **`kubectl exec -it <pod-name> -- nslookup <service-name>`**

---

# Pods Stuck in ContainerCreating

### Problem

* Deployment shows the desired replicas.

* Some Pods remain in **ContainerCreating**.

* **Step 1: Check Deployment and Pod status.**
  **`kubectl get deployment`**
  **`kubectl get pods`**

  * Verify which Pods are stuck.

* **Step 2: Describe the affected Pod.**
  **`kubectl describe pod <pod-name>`**

  * Check the **Events** section.
  * Look for volume mount, image pull, or scheduling errors.

* **Step 3: Inspect the volume configuration.**
  **`kubectl get pod <pod-name> -o yaml`**

  * Verify **hostPath**, **PVC**, or **volumeMounts** configuration.

* **Step 4: Verify the directory on the worker node (for hostPath volumes).**

  ```bash
  #create
  sudo mkdir -p /data/app
  sudo chmod 755 /data/app
  #Confirm the directory exists with the correct permissions.
  ls -ld /data/app
  ```
### Root Cause

* Required **hostPath** directory was missing or incorrectly configured.
* Volume mount failed.
* Pod remained in **ContainerCreating**.

### Fix

* Create the required directory on the worker node with correct permissions, or update the Pod YAML with the correct path.
* Apply the updated Deployment.
  **`kubectl apply -f deployment.yaml`**
* Verify the Pods.
  **`kubectl get pods`**
* Confirm all Pods reach the **Running** and **Ready** state.

# Ingress Returns 404 Even Though Service and Pods Are Running

### Problem

* Ingress is created.

* Service and Pods are healthy.

* Every request returns **404 Not Found**.

* **Step 1: Test the Ingress endpoint.**
  **`curl http://<ingress-ip>/users`**

  * Verify the request reaches the Ingress.
  * Confirm Ingress returns **404**.

* **Step 2: Check the Ingress configuration.**
  **`kubectl describe ingress <ingress-name>`**

  * Verify the configured host and path rules.

* **Step 3: Verify the request path.**

  * Compare the client request path with the Ingress path.
  * Example:

    * Client → **`/users`**
    * Ingress → **`/api`**

### Root Cause

* Client request path does not match the Ingress path.
* Ingress has no matching rule, so it returns **404**.

### Fix

* Update the Ingress path to match the client request.
* Apply the updated Ingress.
  **`kubectl apply -f ingress.yaml`**
* Verify.
  **`curl http://<ingress-ip>/users`**
* Confirm traffic reaches the backend service.

---

# TLS Secret Configured but HTTP Still Works

### Problem

* TLS Secret is configured.

* Users can still access the application over HTTP.

* **Step 1: Verify HTTP access.**
  **`curl -I http://example.com`**

  * Confirm HTTP requests are successful.

* **Step 2: Check the Ingress configuration.**
  **`kubectl describe ingress <ingress-name>`**

  * Verify the TLS Secret is configured.

* **Step 3: Check the Ingress annotations.**

  * Verify whether HTTP to HTTPS redirection is configured.

### Root Cause

* TLS only enables HTTPS.
* HTTP to HTTPS redirection is not configured.

### Fix

* Add the SSL redirect annotation.
* Apply the updated Ingress.
  **`kubectl apply -f ingress.yaml`**
* Verify.
  **`curl -I http://example.com`**
* Confirm HTTP requests are redirected to HTTPS.

---

# Ingress Rewrite Rule Not Working

### Problem

* Backend receives **`/api/users`** instead of **`/v1/users`**.

* **Step 1: Check the backend logs.**
  **`kubectl logs <pod-name>`**

  * Verify the path received by the application.

* **Step 2: Verify the client request.**

  * Confirm the client sends **`/api/users`**.

* **Step 3: Check the Ingress configuration.**
  **`kubectl describe ingress <ingress-name>`**

  * Verify the rewrite annotation.
  * Verify the path contains capture groups.

### Root Cause

* Rewrite annotation exists.
* Path does not use capture groups.
* Rewrite rule is never applied.

### Fix

* Update the Ingress path with the correct capture group.
* Configure the rewrite target.
* Apply the updated Ingress.
  **`kubectl apply -f ingress.yaml`**
* Verify the backend logs.
* Confirm the backend receives **`/v1/users`**.

---

# Ingress Returns 404 Because of Wrong Path

### Problem

* User accesses **`example.com/app`**.

* Service and Pods are healthy.

* Every request returns **404 Not Found**.

* **Step 1: Verify the request.**
  **`curl http://example.com/app`**

  * Confirm Ingress returns **404**.

* **Step 2: Check the Ingress configuration.**
  **`kubectl describe ingress <ingress-name>`**

  * Verify the configured path and **pathType**.

* **Step 3: Compare the client request with the Ingress rule.**

  * Client → **`/app`**
  * Ingress → **`/application`**
  * **pathType = Exact**

### Root Cause

* Ingress path does not match the client request.
* **pathType: Exact** requires an exact path match.

### Fix

* Update the path to **`/app`**.
* Change **pathType** to **Prefix**.
* Apply the updated Ingress.
  **`kubectl apply -f ingress.yaml`**
* Verify.
  **`curl http://example.com/app`**
* Confirm requests are successfully routed to the backend service.
# Ingress Routes Admin Traffic to the Main Application

### Problem

* User accesses **`admin.example.com`**.

* Request reaches the **Main Application** instead of the **Admin Application**.

* **Step 1: Test the Ingress.**
  **`curl http://admin.example.com`**

  * Verify the request reaches the wrong application.

* **Step 2: Check the Ingress rules.**
  **`kubectl describe ingress <ingress-name>`**

  * Verify all host and path rules.
  * Check the order of the rules.

* **Step 3: Compare the host rules.**

  * Verify **`example.com`** and **`admin.example.com`** rules.
  * Check whether both use a catch-all path.

### Root Cause

* The **example.com** rule is matched before **admin.example.com**.
* The catch-all path routes traffic to the Main Application.

### Fix

* Reorder the Ingress rules so the **admin.example.com** rule is matched correctly.
* Apply the updated Ingress.
  **`kubectl apply -f ingress.yaml`**
* Verify.
  **`curl http://admin.example.com`**
* Confirm traffic reaches the Admin Application.

---

# Application Crashes Because ConfigMap Value Is Missing

### Problem

* ConfigMap is created successfully.

* Application crashes during startup.

* Required configuration value is missing.

* **Step 1: Check the Pod status.**
  **`kubectl get pods`**

  * Verify the Pod is crashing.

* **Step 2: Check the application logs.**
  **`kubectl logs <pod-name>`**

  * Identify the missing configuration value.

* **Step 3: Verify the ConfigMap.**
  **`kubectl get configmap <configmap-name> -o yaml`**

  * Confirm the ConfigMap exists.
  * Verify all required keys are present.

* **Step 4: Check the Deployment configuration.**
  **`kubectl describe deployment <deployment-name>`**

  * Verify whether the ConfigMap is referenced using **env**, **envFrom**, or a volume mount.

### Root Cause

* The Deployment does not reference the ConfigMap.
* Kubernetes never injects the configuration into the container.

### Fix

* Add the ConfigMap reference (**envFrom** or **env**) in the Deployment YAML.
* Apply the updated Deployment.
  **`kubectl apply -f deployment.yaml`**
* Verify the Pod starts successfully.

---

# ConfigMap Referenced but Environment Variables Are Missing

### Problem

* Pod starts successfully.

* Environment variables are empty or missing.

* No application errors.

* **Step 1: Verify the environment variables inside the Pod.**
  **`kubectl exec -it <pod-name> -- env`**

  * Confirm the expected environment variables are missing.

* **Step 2: Check the ConfigMap.**
  **`kubectl get configmap <configmap-name> -o yaml`**

  * Verify the ConfigMap exists.
  * Confirm the required keys are present.

* **Step 3: Check the Deployment configuration.**
  **`kubectl describe deployment <deployment-name>`**

  * Verify the Deployment references the ConfigMap using **envFrom**.

* **Step 4: Check the namespace of the Deployment.**
  **`kubectl get deployment <deployment-name> -o jsonpath='{.metadata.namespace}'`**

  * Verify which namespace the Deployment is running in.

* **Step 5: Check the namespace of the ConfigMap.**
  **`kubectl get configmap <configmap-name> --all-namespaces`**

  * Verify the ConfigMap exists in the same namespace as the Deployment.

### Root Cause

* The Deployment and ConfigMap are in different namespaces.
* ConfigMaps are **namespace-scoped** and cannot be shared across namespaces.

### Fix

* Create the ConfigMap in the correct namespace or move the Deployment to the same namespace.
* Restart the Pods.
  **`kubectl rollout restart deployment <deployment-name>`**
* Verify the environment variables.
  **`kubectl exec -it <pod-name> -- env`**
* Confirm the application receives the expected configuration.
# ConfigMap Mounted as Volume but File Not Found

### Problem

* Pod is running.

* Application cannot find the configuration file.

* **Step 1: Check the Pod status.** **`kubectl get pods`**

  * Verify the Pod is running.

* **Step 2: Check the ConfigMap.** **`kubectl get configmap <configmap-name> -o yaml`**

  * Verify the ConfigMap exists.
  * Confirm the required file (for example, **configmap.yaml**) is present.

* **Step 3: Verify the mounted files inside the container.**
  **`kubectl exec -it <pod-name> -- ls -l <mount-path>`**

  * Check whether the expected file exists.
  * Verify whether Kubernetes created a directory instead of a file.

* **Step 4: Check the volumeMount configuration.**
  **`kubectl describe pod <pod-name>`**

  * Verify the **mountPath** and **subPath** configuration.

### Root Cause

* **subPath** was not configured.
* Kubernetes mounted the ConfigMap as a directory instead of mounting the individual file.
* The application looked for the file at the wrong path.

### Fix

* Add **subPath** to mount only the required file.
* Apply the updated Deployment.
  **`kubectl apply -f deployment.yaml`**
* Verify the mounted file.
  **`kubectl exec -it <pod-name> -- ls -l <mount-path>`**
* Confirm the application starts successfully.

---

# Secret Injected but Database Authentication Fails

### Problem

* Pod starts successfully.

* Database authentication fails.

* Environment variables contain incorrect values.

* **Step 1: Check the application logs.**
  **`kubectl logs <pod-name>`**

  * Verify the authentication error.

* **Step 2: Check the environment variables inside the container.**
  **`kubectl exec -it <pod-name> -- env`**

  * Verify the username and password values.

* **Step 3: Check the Kubernetes Secret.**
  **`kubectl get secret <secret-name> -o yaml`**

  * Verify the stored values.

* **Step 4: Decode the Secret.**

  ```bash
  kubectl get secret <secret-name> -o jsonpath='{.data.password}' | base64 -d
  ```

  * Verify the stored password matches the current database password.

### Root Cause

* The database password changed externally.
* Kubernetes Secret still contained the old password.
* The application received outdated credentials.

### Fix

* Update the Kubernetes Secret with the correct password.
* Restart the Deployment.
  **`kubectl rollout restart deployment <deployment-name>`**
* Verify the application authenticates successfully.

---

# ConfigMap Updated but Some Pods Still Use Old Values

### Problem

* ConfigMap updated.

* Some Pods use the new configuration.

* Other Pods still use the old configuration.

* **Step 1: Check the Pod age.**
  **`kubectl get pods`**

  * Verify whether some Pods are older than others.

* **Step 2: Verify the ConfigMap.**
  **`kubectl get configmap <configmap-name> -o yaml`**

  * Confirm the ConfigMap contains the updated value.

* **Step 3: Compare the environment variables inside the Pods.**
  **`kubectl exec -it <pod-name> -- env`**

  * Verify the feature flag value in both old and new Pods.

### Root Cause

* The ConfigMap is consumed as **environment variables**.
* Environment variables are loaded only when the container starts.
* Existing Pods do not automatically reload updated ConfigMap values.

### Fix

* Restart the Deployment.
  **`kubectl rollout restart deployment <deployment-name>`**
* Verify new Pods are created.
  **`kubectl get pods`**
* Verify the updated environment variable.
  **`kubectl exec -it <pod-name> -- env`**
* Confirm all Pods use the updated ConfigMap value.

