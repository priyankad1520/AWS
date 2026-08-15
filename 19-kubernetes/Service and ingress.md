* **404** → Host / Path / Ingress Rule
* **502** → Service / Port / Backend Connection
* **503** → No Healthy Pods / No Endpoints
* **504** → Slow Backend / Timeout
* **SSL/TLS** → Certificate / TLS Secret / Redirect
### Final Ingress Troubleshooting Flow
Client → DNS → Ingress → IngressClass → Ingress Controller → Service → Endpoints → Pods → Application → Database / External APIs

# Service
### Problem 1: Service is Unreachable
> **"First, I'd verify the Service configuration using `kubectl describe svc`. Then I'd check whether the Service has active Endpoints and confirm that the backend Pods are running and Ready. Next, I'd compare the Service selector with the Pod labels and verify the Service ports. If required, I'd also check NetworkPolicies and DNS resolution. After fixing the issue, I'd validate that the Service is reachable and routing traffic successfully."**

| **Possible Causes**                        | **Fixes**                             |
| ------------------------------------------ | ------------------------------------- |
| Backend Pods are not running.              | Start failed Pods.                    |
| Pods are not Ready.                        | Fix Pod readiness.                    |
| Service selector doesn't match Pod labels. | Correct Service selector.             |
| Service type is incorrect.                 | Update Service type.                  |
| NetworkPolicy is blocking traffic.         | Modify NetworkPolicy.                 |
| DNS resolution issue.                      | Fix DNS resolution.                   |
| Firewall or security group restrictions.   | Update firewall/security group rules. |

### How to Fix and Investigation:

```yaml
# 1. Verify Service Configuration
kubectl describe svc <service-name>
# Verify: Type, Selector, Port, TargetPort.
------------------------------------------------------------
# 2. Verify Endpoints
kubectl get endpoints <service-name>
# Verify backend Pod IPs are listed.
------------------------------------------------------------
# 3. Verify Pod Labels
kubectl get pods --show-labels
# Compare Pod labels with Service selector.
------------------------------------------------------------
# 4. Verify Pod Health
kubectl describe pod <pod-name>
# Check: Running, Ready.
------------------------------------------------------------
# 5. Verify NetworkPolicy
kubectl get networkpolicy
kubectl describe networkpolicy <policy-name>
# Verify traffic is allowed.
------------------------------------------------------------
# 6. Validate
kubectl exec -it <pod-name> -- curl http://<service-name>:<port>
kubectl get endpoints <service-name>
# Verify Service is reachable.
```
---

### Problem 2: Service is Not Routing Traffic
> **"First, I'd verify whether the Service has active Endpoints using kubectl get endpoints because without Endpoints it cannot forward traffic. Then I'd confirm that the backend Pods are Ready and that the Service selector matches the Pod labels. Next, I'd verify the targetPort and ensure the application is listening on that port and I'd verify the Service ports and network connectivity. After correcting the configuration, I'd validate that requests are successfully routed to the backend Pods."**

| **Possible Causes**                                     | **Fixes**                                                |
| ------------------------------------------------------- | -------------------------------------------------------- |
| No active Endpoints.                                    |                                                          |
| Pods are Not Ready.                                     |   Fix Pod readiness.                                     |
| Selector mismatch.                                      |  Correct Service selector.                               |
| Incorrect `targetPort`.                                 |  Update `targetPort`.                                    |
| NetworkPolicy blocking traffic.                         |  Modify NetworkPolicy.                                   |
| Backend application not listening on the expected port. |  Configure the application to listen on the correct port.|                                                      
### How to Fix and Investigation:

```yaml
# 1. Verify Endpoints
kubectl get endpoints <service-name>
# Verify backend Pod IPs exist.
------------------------------------------------------------
# 2. Verify Pod Labels
kubectl get pods --show-labels
# Compare labels with Service selector.
------------------------------------------------------------
# 3. Verify Target Port
kubectl describe svc <service-name>
# Verify: Port, TargetPort.
------------------------------------------------------------
# 4. Verify Application Port
kubectl exec -it <pod-name> -- netstat -tuln
# Verify application is listening on the targetPort.
------------------------------------------------------------
# 5. Validate
kubectl exec -it <pod-name> -- curl http://<service-name>:<port>
# Verify traffic reaches the application.
```
---

### Problem 3: Wrong Port Configuration

> First, I'd inspect the Service configuration using **kubectl describe svc** and verify the configured **port** and **targetPort**. Then I'd check whether the application inside the Pod is listening on the expected port. Next, I'd compare the Deployment containerPort with the Service targetPort. Based on the findings, I'd update the Service configuration and validate that traffic reaches the application.

| **Possible Causes**                         | **Fixes**                                                 |
| ------------------------------------------- | --------------------------------------------------------- |
| Incorrect `targetPort`.                     | Correct the `targetPort`.                                 |
| Incorrect Service `port`.                   | Correct the Service `port`.                               |
| Application listening on a different port.  | Configure the application to listen on the expected port. |
| Wrong `containerPort` configuration.        | Update `containerPort`.                                   |
| Deployment updated but Service not updated. | Update the Service configuration.                         |

### How to Fix

```yaml
# 1. Verify Service Ports
kubectl describe svc <service-name>
# Verify: Port, TargetPort.
------------------------------------------------------------
# 2. Verify Deployment
kubectl describe deployment <deployment-name>
# Verify: ContainerPort.
------------------------------------------------------------
# 3. Verify Listening Port
kubectl exec -it <pod-name> -- netstat -tuln
# Confirm application is listening on the targetPort.
------------------------------------------------------------
# 4. Update Service
kubectl edit svc <service-name>
# Correct the Port or TargetPort.
------------------------------------------------------------
# 5. Validate
kubectl exec -it <pod-name> -- curl http://<service-name>:<port>
# Verify successful response.
```
---

### Problem 4: Service Has No Endpoints

> First, I'd verify whether the Service has any backend Endpoints using **kubectl get endpoints**. If no Endpoints are present, I'd compare the Service selector with the Pod labels and confirm that the Pods are in the Running and Ready state. Next, I'd verify that the Pods belong to the correct namespace. After fixing the selector or Pod issue, I'd validate that Endpoints are created and the Service starts routing traffic.

| **Possible Causes**                        | **Fixes**                                              |
| ------------------------------------------ | ------------------------------------------------------ |
| Service selector doesn't match Pod labels. | Correct the Service selector.                          |
| Pods are Not Ready.                        | Fix Pod readiness.                                     |
| Pods are in a different namespace.         | Ensure the Service and Pods are in the same namespace. |
| Backend Pods are not running.              | Deploy backend Pods.                                   |
| Deployment has zero replicas.              | Scale the Deployment.                                  |

### How to Fix

```yaml
# 1. Verify Endpoints
kubectl get endpoints <service-name>
# Verify endpoint IPs exist.
------------------------------------------------------------
# 2. Verify Service Selector
kubectl describe svc <service-name>
# Verify: Selector.
------------------------------------------------------------
# 3. Verify Pod Labels
kubectl get pods --show-labels
# Compare Pod labels with Service selector.
------------------------------------------------------------
# 4. Verify Pod Status
kubectl get pods
kubectl describe pod <pod-name>
# Verify Pods are Running and Ready.
------------------------------------------------------------
# 5. Validate
kubectl get endpoints <service-name>
kubectl exec -it <pod-name> -- curl http://<service-name>:<port>
# Verify Endpoints are created and traffic is routed.
```
**Service Troubleshooting Flow** : Service --> Selector --> Endpoints --> Pods (Running & Ready) -->Application Port --> NetworkPolicy / DNS

---
# Ingress
### Problem 1: Ingress Returns 404 Not Found

> First, I'd verify the Ingress configuration using **kubectl describe ingress** to ensure the host and path rules are correct. Then I'd confirm that the request hostname matches the configured host and that the backend Service exists. Next, I'd verify the Service, Endpoints, and backend Pods. Based on the findings, I'd correct the Ingress rule or backend configuration and validate that the application is accessible.

| **Possible Causes**                                | **Fixes**                                             |
| -------------------------------------------------- | ----------------------------------------------------- |
| Incorrect host configured in Ingress.              | Correct the host.                                     |
| Incorrect path configured.                         | Correct the path.                                     |
| Wrong backend Service name.                        | Update the backend Service.                           |
| Ingress Controller is not processing the rule.     | Configure the correct `IngressClass`.                 |
| DNS points to the wrong Ingress IP.                | Fix DNS configuration.                                |
| Application URL doesn't match the configured path. | Reload or restart the Ingress Controller if required. |

### How to Fix

```yaml
# 1. Verify Ingress Rules
kubectl describe ingress <ingress-name>
# Verify: Host, Path, Backend Service, IngressClass.
------------------------------------------------------------
# 2. Verify Backend Service
kubectl get svc
kubectl describe svc <service-name>
# Verify Service exists.
------------------------------------------------------------
# 3. Verify Endpoints
kubectl get endpoints <service-name>
# Verify backend Pod IPs are available.
------------------------------------------------------------
# 4. Verify DNS
nslookup <application-domain>
# Verify domain resolves to the Ingress IP.
------------------------------------------------------------
# 5. Validate
curl http://<host>/<path>
# Verify application returns HTTP 200.
```
---

### Problem 2: Ingress Returns 502 Bad Gateway

> First, I'd verify that the Ingress is forwarding traffic to the correct backend Service. Then I'd check whether the Service has active Endpoints and confirm that the backend Pods are healthy Running and Ready. Next, I'd verify that the application is listening on the correct port and review the Ingress Controller logs. Based on the findings, I'd fix the backend connectivity issue and validate that the application responds successfully.

| **Possible Causes**                                  | **Fixes**                                                |
| ---------------------------------------------------- | -------------------------------------------------------- |
| Backend Pods are not running.                        | Start backend Pods.                                      |
| Service has no Endpoints.                            | Fix Service Endpoints.                                   |
| Wrong `targetPort`.                                  | Correct `targetPort`.                                    |
| Application is not listening on the configured port. | Configure the application to listen on the correct port. |
| Readiness probe failure.                             | Fix the readiness probe.                                 |
| Ingress Controller cannot connect to the backend.    | Resolve Ingress Controller connectivity issues.          |

### How to Fix

```yaml
# 1. Verify Backend Service
kubectl describe ingress <ingress-name>
# Verify Backend Service.
------------------------------------------------------------
# 2. Verify Endpoints
kubectl get endpoints <service-name>
# Verify backend Pod IPs exist.
------------------------------------------------------------
# 3. Verify Pod Health
kubectl get pods
kubectl describe pod <pod-name>
# Verify Running, Ready.
------------------------------------------------------------
# 4. Verify Application Port
kubectl exec -it <pod-name> -- netstat -tuln
# Verify application is listening on the targetPort.
------------------------------------------------------------
# 5. Verify Ingress Controller Logs
kubectl logs -n ingress-nginx <ingress-controller-pod>
# Check backend connection errors.
------------------------------------------------------------
# 6. Validate
curl http://<host>
# Verify application returns HTTP 200.
```
---

### Problem 3: Ingress Returns 503 Service Unavailable

> "First, I’ll identify where the 503 is coming from and trace the request path: Ingress or Load Balancer → Ingress Controller → Service → Endpoints → Pod.
> I’ll first check whether the backend pods are Running and Ready using kubectl get pods. Then I’ll verify the Kubernetes Service and make sure the selector is matching the correct pods. I’ll check kubectl get endpoints to confirm the service actually has healthy backend endpoints.
> Next, I’ll verify the Ingress backend configuration, including the service name and port, and compare the Service port and targetPort with the application port. I’ll also check the Ingress Controller logs and events to see whether it is reporting connection refused, no healthy upstreams, or another backend issue.
> If required, I’ll test connectivity directly from inside the cluster to the Service. Once I identify whether it is a **readiness issue, service selector issue, endpoint issue, port mismatch, or ingress-controller problem**, I’ll fix it and then validate the request end-to-end.
> Finally, I’ll verify that the application is returning a successful response through the Ingress and monitor the production traffic to make sure the 503s are resolved."

| **Possible Causes**                   | **Fixes**                         |
| ------------------------------------- | --------------------------------- |
| Service has no Endpoints.             | Restore backend Pods.             |
| All backend Pods are Not Ready.       | Fix readiness probe.              |
| Deployment has zero running replicas. | Scale the Deployment.             |
| Readiness probe is failing.           | Fix readiness probe.              |
| Incorrect Service selector.           | Correct Service selector.         |
| Backend application is unavailable.   | Restore application availability. |

### How to Fix

```yaml
# 1. Verify Backend Service
kubectl describe ingress <ingress-name>
# Verify Backend Service.
------------------------------------------------------------
# 2. Verify Endpoints
kubectl get endpoints <service-name>
# Verify endpoint IPs exist.
------------------------------------------------------------
# 3. Verify Deployment
kubectl get deployment
# Verify desired replicas are available.
------------------------------------------------------------
# 4. Verify Pod Health
kubectl get pods
kubectl describe pod <pod-name>
# Check: Running, Ready, Readiness Probe.
------------------------------------------------------------
# 5. Verify Service Selector
kubectl describe svc <service-name>
# Verify selector matches Pod labels.
------------------------------------------------------------
# 6. Validate
kubectl get endpoints <service-name>
curl http://<host>
# Verify application returns HTTP 200.
```

**Ingress Troubleshooting Flow:** Client Request --> DNS --> Ingress --> Ingress Controller --> Service --> Endpoints --> Pods --> Application

* **404** → Think **Ingress Rule** (Host, Path, Backend).
* **502** → Think **Backend Connection** (Service, Port, Application).
* **503** → Think **No Healthy Backend** (Endpoints, Pods, Readiness).
---

### Problem 4: DNS Resolution Issue
> **"First, I'd verify whether the domain resolves correctly using `nslookup` or `dig`. Then I'd compare the resolved IP with the Ingress LoadBalancer address and verify the Ingress host configuration. If the DNS record is incorrect, I'd update it or fix the ExternalDNS configuration. Finally, I'd validate that the domain resolves correctly and the application is accessible."**

| **Possible Causes**                                | **Fixes**                                         |
| -------------------------------------------------- | ------------------------------------------------- |
| DNS record is missing.                             | Create or update the DNS record.                  |
| DNS record points to the wrong IP or LoadBalancer. | Point the DNS record to the correct LoadBalancer. |
| DNS propagation is still in progress.              | Wait for DNS propagation if recently updated.     |
| Incorrect host configured in Ingress.              | Correct the Ingress host.                         |
| ExternalDNS is not updating records.               | Fix ExternalDNS configuration.                    |
| LoadBalancer external IP is unavailable.           | Verify and restore the LoadBalancer external IP.  |

### How to Fix

```yaml
# 1. Verify Ingress Address
kubectl get ingress
kubectl describe ingress <ingress-name>
# Verify: Host, Address.
------------------------------------------------------------
# 2. Verify DNS
nslookup <domain-name>
dig <domain-name>
# Verify domain resolves to the Ingress IP or hostname.
------------------------------------------------------------
# 3. Verify LoadBalancer
kubectl get svc -n ingress-nginx
# Verify External IP is assigned.
------------------------------------------------------------
# 4. Verify Host Configuration
kubectl describe ingress <ingress-name>
# Verify Host matches the DNS record.
------------------------------------------------------------
# 5. Validate
curl http://<domain-name>
# Verify application returns HTTP 200.
```
---

### Problem 5: Ingress Controller is Not Running
> **"First, I'd verify whether the Ingress Controller Pods are running by checking the ingress namespace. Then I'd review the controller logs, events and Deployment status to identify startup or configuration issues. Next, I'd verify the LoadBalancer Service and external IP. After resolving the issue, I'd restart the controller if required and validate that it starts routing traffic successfully."**

| **Possible Causes**                 | **Fixes**                            |
| ----------------------------------- | ------------------------------------ |
| Ingress Controller Pod is crashed.  | Restart the Ingress Controller.      |
| `CrashLoopBackOff`.                 | Resolve Pod startup issues.          |
| `ImagePullBackOff`.                 | Resolve `ImagePullBackOff`.          |
| Controller Deployment failed.       | Fix controller configuration.        |
| LoadBalancer Service issue.         | Restore LoadBalancer Service.        |
| Insufficient node resources.        | Increase node resources if required. |
| Incorrect controller configuration. | Fix controller configuration.        |


### How to Fix

```yaml
# 1. Verify Controller Pod
kubectl get pods -n ingress-nginx
# Verify Pod is Running.
------------------------------------------------------------
# 2. Verify Controller Logs
kubectl logs <controller-pod> -n ingress-nginx
# Check startup or configuration errors.
------------------------------------------------------------
# 3. Verify Deployment
kubectl describe deployment ingress-nginx-controller -n ingress-nginx
# Verify desired and available replicas.
------------------------------------------------------------
# 4. Verify Service
kubectl get svc -n ingress-nginx
# Verify LoadBalancer External IP.
------------------------------------------------------------
# 5. Restart Controller
kubectl rollout restart deployment ingress-nginx-controller -n ingress-nginx
------------------------------------------------------------
# 6. Validate
kubectl get pods -n ingress-nginx
kubectl get ingress
# Verify traffic is routed successfully.
```
---

### Problem 6: Wrong IngressClass

> First, I'd inspect the Ingress resource using **kubectl describe ingress** and verify the configured **IngressClass**. Then I'd compare it with the installed Ingress Controller to ensure they match. Next, I'd verify that the Ingress Controller is watching the correct IngressClass. Based on the findings, I'd update the Ingress configuration and validate that the controller starts processing the resource.
> **"First, I'd verify the configured `ingressClassName` using `kubectl describe ingress`. Then I'd compare it with the available IngressClasses and confirm that the Ingress Controller is watching the same class. If there's a mismatch, I'd update the Ingress configuration or controller settings. Finally, I'd validate that the Ingress is processed correctly and starts routing traffic."**

| **Possible Causes**                               | **Fixes**                                            |
| ------------------------------------------------- | ---------------------------------------------------- |
| Incorrect `ingressClassName`.                     | Update the correct `ingressClassName`.               |
| IngressClass does not exist.                      | Create the missing IngressClass.                     |
| Ingress Controller is watching a different class. | Configure the controller to watch the correct class. |
| Default IngressClass is configured incorrectly.   | Correct the default IngressClass configuration.      |
| Typographical error in the IngressClass name.     | Correct spelling mistakes.                           |
| —                                                 | Restart the controller if required.                  |

### How to Fix

```yaml
# 1. Verify IngressClass
kubectl describe ingress <ingress-name>
# Verify: ingressClassName.
------------------------------------------------------------
# 2. Verify Available Classes
kubectl get ingressclass
# Verify required IngressClass exists.
------------------------------------------------------------
# 3. Verify Controller
kubectl logs <controller-pod> -n ingress-nginx
# Check whether the controller is watching the correct class.
------------------------------------------------------------
# 4. Update Ingress
kubectl edit ingress <ingress-name>
# Update ingressClassName if required.
------------------------------------------------------------
# 5. Validate
kubectl get ingress
kubectl describe ingress <ingress-name>
# Verify Ingress is processed by the controller.
```
Whenever the interviewer asks **any Ingress issue**, think in this order:

DNS --> Ingress --> IngressClass --> Ingress Controller --> Service --> Endpoints --> Pods

---

### Problem 7: Host is Not Resolving

> First, I'd verify whether the client can resolve the application hostname using **nslookup** or **dig**. Then I'd compare the resolved IP or hostname with the Ingress LoadBalancer address. Next, I'd verify the DNS record, Ingress host configuration, and LoadBalancer status. If required, I'd update the DNS record or correct the Ingress configuration. Based on the findings, I'd correct the DNS or Ingress configuration and validate that the hostname resolves successfully.

| **Possible Causes**                          | **Fixes**                                        |
| -------------------------------------------- | ------------------------------------------------ |
| DNS record is missing.                       | Create or update the DNS record.                 |
| DNS record points to the wrong LoadBalancer. | Point DNS to the correct LoadBalancer.           |
| Incorrect hostname configured in Ingress.    | Correct the Ingress host.                        |
| LoadBalancer External IP is not assigned.    | Verify and restore the LoadBalancer External IP. |
| ExternalDNS is not updating records.         | Fix ExternalDNS configuration.                   |
| DNS propagation is still in progress.        | Wait for DNS propagation.                        |

### How to Fix

```yaml
# 1. Verify Ingress Host
kubectl describe ingress <ingress-name>
# Verify: Host, Address.
------------------------------------------------------------
# 2. Verify DNS
nslookup <host-name>
dig <host-name>
# Verify hostname resolves to the Ingress IP.
------------------------------------------------------------
# 3. Verify LoadBalancer
kubectl get svc -n ingress-nginx
# Verify External IP is assigned.
------------------------------------------------------------
# 4. Verify DNS Record
# Compare DNS record with the LoadBalancer IP/Hostname.
------------------------------------------------------------
# 5. Validate
curl http://<host-name>
# Verify application is accessible.
```
---

# Problem 8: Path-Based Routing is Not Working

> First, I'd inspect the Ingress configuration using **kubectl describe ingress** and verify the configured path rules. Then I'd confirm that the request URL matches the configured path and that the backend Service exists. Next, I'd verify the Service, Endpoints, and backend Pods. Based on the findings, I'd correct the path configuration and validate that requests are routed to the correct backend Service.
> **"First, I'd verify the configured path and pathType in the Ingress resource. Then I'd confirm that the backend Service exists and has active Endpoints. Next, I'd verify that the backend Pods are Running and Ready and that the application supports the configured path. After correcting the configuration, I'd validate that requests are routed to the correct backend Service."**

| **Possible Causes**                              | **Fixes**                              |
| ------------------------------------------------ | -------------------------------------- |
| Incorrect path configured.                       | Correct the path.                      |
| Incorrect `pathType`.                            | Correct the `pathType`.                |
| Wrong backend Service.                           | Update the backend Service.            |
| Service has no Endpoints.                        | Restore Service Endpoints.             |
| Backend Pods are Not Ready.                      | Fix Pod readiness.                     |
| Application is serving a different context path. | Update the application's context path. |

### How to Fix

```yaml
# 1. Verify Ingress Path
kubectl describe ingress <ingress-name>
# Verify: Path, PathType, Backend Service.
------------------------------------------------------------
# 2. Verify Backend Service
kubectl describe svc <service-name>
# Verify Service Name, Port.
------------------------------------------------------------
# 3. Verify Endpoints
kubectl get endpoints <service-name>
# Verify backend Pod IPs exist.
------------------------------------------------------------
# 4. Verify Pod Health
kubectl get pods
kubectl describe pod <pod-name>
# Verify Pods are Running and Ready.
------------------------------------------------------------
# 5. Validate
curl http://<host-name>/<path>
# Verify request reaches the correct backend service.
```
---

### Problem 9: Host-Based Routing is Not Working
> **"First, I'd verify the configured host rule using kubectl describe ingress in the Ingress resource and ensure the client is sending the correct Host header. Then I'd confirm that the DNS record resolves to the Ingress LoadBalancer and verify that the backend Service has active Endpoints. After correcting the host rule or DNS configuration, I'd validate that requests are routed to the correct backend application."**

| **Possible Causes**                      | **Fixes**                                 |
| ---------------------------------------- | ----------------------------------------- |
| Incorrect host configured in Ingress.    | Correct the host rule.                    |
| DNS record points to the wrong IP.       | Update the DNS record.                    |
| Client is using the wrong hostname.      | Use the correct hostname.                 |
| Backend Service is incorrect.            | Correct the backend Service.              |
| Service has no Endpoints.                | Restore Endpoints.                        |
| Default backend is handling the request. | Verify and correct the Ingress host rule. |

### How to Fix

```yaml
# 1. Verify Host Rule
kubectl describe ingress <ingress-name>
# Verify: Host, Backend Service.
------------------------------------------------------------
# 2. Verify DNS
nslookup <host-name>
# Verify hostname resolves to the Ingress IP.
------------------------------------------------------------
# 3. Verify Backend Service
kubectl describe svc <service-name>
# Verify Service Name, Port.
------------------------------------------------------------
# 4. Verify Endpoints
kubectl get endpoints <service-name>
# Verify backend Pod IPs exist.
------------------------------------------------------------
# 5. Validate
curl -H "Host: <host-name>" http://<ingress-ip>
# Verify request is routed to the correct application.
```
**Ingress Troubleshooting Flow:**

DNS → Ingress → IngressClass → Ingress Controller → Service → Endpoints → Pods → Application

---

### Problem 10: Redirect Loop (HTTP ↔ HTTPS)

> **"First, I'd verify whether the application is repeatedly redirecting between HTTP and HTTPS. Then I'd inspect the Ingress TLS configuration and NGINX annotations to determine whether both the Ingress and the application are forcing HTTPS redirects. Next, I'd verify that the application correctly handles the `X-Forwarded-Proto` header. After correcting the redirect configuration, I'd validate that the application is accessible without entering a redirect loop."**

| **Possible Causes**                                          | **Fixes**                                                  |
| ------------------------------------------------------------ | ---------------------------------------------------------- |
| Both Ingress and application are forcing HTTPS.              | Configure HTTPS redirection in only one place.             |
| Incorrect SSL redirect annotation.                           | Correct the SSL redirect annotation.                       |
| Incorrect backend redirect configuration.                    | Correct the backend redirect configuration.                |
| LoadBalancer terminates SSL, but the application is unaware. | Configure the application to trust `X-Forwarded-Proto`.    |
| Missing `X-Forwarded-Proto` header.                          | Ensure the `X-Forwarded-Proto` header is correctly passed. |
| Incorrect reverse proxy configuration.                       | Update reverse proxy configuration.                        |
| —                                                            | Correct TLS configuration.                                 |
### How to Fix

```yaml
# 1. Verify Ingress TLS Configuration
kubectl describe ingress <ingress-name>
# Verify: TLS, Host, SSL Redirect Annotation.
------------------------------------------------------------
# 2. Verify NGINX Annotations
kubectl describe ingress <ingress-name>
# Check: nginx.ingress.kubernetes.io/ssl-redirect, force-ssl-redirect.
------------------------------------------------------------
# 3. Verify Application Configuration
kubectl describe deployment <deployment-name>
# Verify application HTTPS redirect settings.
------------------------------------------------------------
# 4. Verify Response Headers
curl -I http://<host-name>
curl -Ik https://<host-name>
# Check Location header for repeated redirects.
------------------------------------------------------------
# 5. Validate
curl -L http://<host-name>
# Verify application loads without redirect loop.
```
---

### Problem 11: 504 Gateway Timeout

> **"First, I'd verify that the backend Pods are healthy and responding correctly. Then I'd review the application logs and Ingress Controller logs to determine whether the timeout is caused by a slow backend, database query, or external API call. Next, I'd verify the Ingress timeout configuration and backend resource utilization. After optimizing the application or increasing the timeout values, I'd validate that requests complete successfully without returning a 504 Gateway Timeout error."**
| **Possible Causes**                                | **Fixes**                                        |
| -------------------------------------------------- | ------------------------------------------------ |
| Backend application is taking too long to respond. | Increase Ingress timeout values.                 |
| Database queries are slow.                         | Optimize slow database queries.                  |
| Application is waiting on an external API.         | Optimize or resolve the external API dependency. |
| NGINX Ingress timeout is too low.                  | Increase Ingress timeout values.                 |
| Backend Pods are overloaded.                       | Increase backend Pod replicas.                   |
| Network latency between Ingress and backend.       | Resolve network latency.                         |
| CPU or Memory resource exhaustion.                 | Increase CPU or Memory resources.                |

### How to Fix

```yaml
# 1. Verify Backend Pods
kubectl get pods
kubectl describe pod <pod-name>
# Verify Pods are Running and Ready.
------------------------------------------------------------
# 2. Verify Application Logs
kubectl logs <pod-name>
# Check for slow requests, database delays, external API delays.
------------------------------------------------------------
# 3. Verify Ingress Controller Logs
kubectl logs -n ingress-nginx <ingress-controller-pod>
# Check timeout-related errors.
------------------------------------------------------------
# 4. Verify Resource Usage
kubectl top pods
# Verify CPU and Memory utilization.
------------------------------------------------------------
# 5. Verify Ingress Timeout Configuration
kubectl describe ingress <ingress-name>
# Check: proxy-read-timeout, proxy-send-timeout, proxy-connect-timeout.
------------------------------------------------------------
# 6. Validate
curl http://<host-name>
# Verify request completes successfully without timing out.
```
---


 
* **DNS / Host** → DNS Record / LoadBalancer / Host Rule
* **IngressClass** → Controller Selection
* **Ingress Controller** → Controller Pod / Logs
* **Path Routing** → Path / `pathType`
* **Host Routing** → Host Header / DNS
* **Redirect Loop** → Duplicate HTTP→HTTPS Redirect
