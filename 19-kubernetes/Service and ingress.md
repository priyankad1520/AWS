# Service
### Problem 1: Service is Unreachable

> First, I'd verify the Service configuration using **kubectl get svc** and **kubectl describe svc**. Then I'd check whether the Service has active Endpoints and verify that the backend Pods are running and Ready. Next, I'd validate the Service selector, ports, and network connectivity between the Service and Pods. Based on the findings, I'd fix the configuration and verify that the application becomes accessible.
> **"First, I'd verify the Service configuration using `kubectl describe svc`. Then I'd check whether the Service has active Endpoints and confirm that the backend Pods are running and Ready. Next, I'd compare the Service selector with the Pod labels and verify the Service ports. If required, I'd also check NetworkPolicies and DNS resolution. After fixing the issue, I'd validate that the Service is reachable and routing traffic successfully."**

**Possible Causes:**

* Backend Pods are not running.
* Pods are not Ready.
* Service selector doesn't match Pod labels.
* Service type is incorrect.
* NetworkPolicy is blocking traffic.
* DNS resolution issue.
* Firewall or security group restrictions.

**Investigation:**

```yaml
kubectl get svc
kubectl describe svc <service-name>
kubectl get endpoints <service-name>
kubectl get pods --show-labels
kubectl describe pod <pod-name>
kubectl get networkpolicy
```

**Fixes:**

* Start failed Pods.
* Fix Pod readiness.
* Correct Service selector.
* Update Service type.
* Modify NetworkPolicy.
* Fix DNS resolution.
* Update firewall/security group rules.

### How to Fix

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

> First, I'd verify whether the Service has active Endpoints using **kubectl get endpoints**. Then I'd check that the backend Pods are Ready and confirm that the Service selector matches the Pod labels. Next, I'd verify the Service ports and network connectivity. Based on the findings, I'd correct the configuration and validate that traffic reaches the backend Pods.
> **"First, I'd verify whether the Service has active Endpoints because without Endpoints it cannot forward traffic. Then I'd confirm that the backend Pods are Ready and that the Service selector matches the Pod labels. Next, I'd verify the targetPort and ensure the application is listening on that port. After correcting the configuration, I'd validate that requests are successfully routed to the backend Pods."**

**Possible Causes:**

* No active Endpoints.
* Pods are Not Ready.
* Selector mismatch.
* Incorrect targetPort.
* NetworkPolicy blocking traffic.
* Backend application not listening on the expected port.

**Investigation:**

```yaml
kubectl get svc
kubectl describe svc <service-name>
kubectl get endpoints <service-name>
kubectl get pods --show-labels
kubectl describe pod <pod-name>
kubectl exec -it <pod-name> -- netstat -tuln
```

**Fixes:**

* Fix Pod readiness.
* Correct Service selector.
* Update targetPort.
* Modify NetworkPolicy.
* Configure the application to listen on the correct port.

### How to Fix

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
> **"First, I'd verify the Service configuration and compare the configured port and targetPort with the application's listening port. Then I'd check the Deployment's containerPort and confirm that the application is listening correctly inside the container. After correcting the Service configuration, I'd validate that traffic successfully reaches the application."**

**Possible Causes:**

* Incorrect targetPort.
* Incorrect Service port.
* Application listening on a different port.
* Wrong containerPort configuration.
* Deployment updated but Service not updated.

**Investigation:**

```yaml
kubectl describe svc <service-name>
kubectl describe deployment <deployment-name>
kubectl describe pod <pod-name>
kubectl exec -it <pod-name> -- netstat -tuln
```

**Fixes:**

* Correct the targetPort.
* Correct the Service port.
* Update containerPort.
* Configure the application to listen on the expected port.

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
> **"First, I'd check whether the Service has active Endpoints using `kubectl get endpoints`. If no Endpoints exist, I'd compare the Service selector with the Pod labels and confirm that the backend Pods are Running and Ready. I'd also verify that the Pods are in the correct namespace. After correcting the selector or resolving the Pod issue, I'd validate that Endpoints are created and the Service starts routing traffic."**

**Possible Causes:**

* Service selector doesn't match Pod labels.
* Pods are Not Ready.
* Pods are in a different namespace.
* Backend Pods are not running.
* Deployment has zero replicas.

**Investigation:**

```yaml
kubectl get endpoints <service-name>
kubectl describe svc <service-name>
kubectl get pods --show-labels
kubectl get deployment
kubectl describe pod <pod-name>
```

**Fixes:**

* Correct the Service selector.
* Fix Pod readiness.
* Deploy backend Pods.
* Scale the Deployment.
* Ensure the Service and Pods are in the same namespace.

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
> **"First, I'd inspect the Ingress configuration using `kubectl describe ingress` and verify the host, path, and backend Service. Then I'd confirm that the DNS resolves to the correct Ingress IP and that the backend Service has active Endpoints. Finally, I'd validate that the application is accessible through the configured URL after correcting any routing issues."**

**Possible Causes:**

* Incorrect host configured in Ingress.
* Incorrect path configured.
* Wrong backend Service name.
* Ingress Controller is not processing the rule.
* DNS points to the wrong Ingress IP.
* Application URL doesn't match the configured path.

**Investigation:**

```yaml
kubectl get ingress
kubectl describe ingress <ingress-name>
kubectl get svc
kubectl get endpoints
kubectl get pods
kubectl get ingressclass
```

**Fixes:**

* Correct the host.
* Correct the path.
* Update the backend Service.
* Fix DNS configuration.
* Configure the correct IngressClass.
* Reload or restart the Ingress Controller if required.

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

> First, I'd verify that the Ingress is forwarding traffic to the correct backend Service. Then I'd check whether the Service has active Endpoints and confirm that the backend Pods are Running and Ready. Next, I'd verify that the application is listening on the correct port and review the Ingress Controller logs. Based on the findings, I'd fix the backend connectivity issue and validate that the application responds successfully.
> **"First, I'd verify that the Ingress is forwarding requests to the correct backend Service. Then I'd check whether the Service has active Endpoints and confirm that the backend Pods are healthy and Ready. Next, I'd verify the application's listening port and review the Ingress Controller logs for backend connection errors. After resolving the issue, I'd validate that requests return a successful response."**

**Possible Causes:**

* Backend Pods are not running.
* Service has no Endpoints.
* Wrong targetPort.
* Application is not listening on the configured port.
* Readiness probe failure.
* Ingress Controller cannot connect to the backend.

**Investigation:**

```yaml
kubectl describe ingress <ingress-name>
kubectl get svc
kubectl get endpoints
kubectl get pods
kubectl describe pod <pod-name>
kubectl logs -n ingress-nginx <ingress-controller-pod>
```

**Fixes:**

* Start backend Pods.
* Fix Service Endpoints.
* Correct targetPort.
* Fix readiness probe.
* Configure the application to listen on the correct port.
* Resolve Ingress Controller connectivity issues.


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

> First, I'd inspect the Ingress configuration and verify the backend Service. Then I'd check whether the Service has active Endpoints because a 503 error commonly occurs when there are no healthy backend Pods. Next, I'd verify the Pod status, readiness probes, and application health. Based on the findings, I'd restore healthy backend Pods and validate that the Ingress successfully routes traffic.
> **"First, I'd verify the Ingress configuration and backend Service. Then I'd check whether the Service has active Endpoints because a 503 error usually indicates that there are no healthy backend Pods available. Next, I'd verify the Deployment, Pod status, readiness probes, and Service selector. After restoring healthy backend Pods, I'd validate that the Ingress successfully routes traffic to the application."**

**Possible Causes:**

* Service has no Endpoints.
* All backend Pods are Not Ready.
* Deployment has zero running replicas.
* Readiness probe is failing.
* Incorrect Service selector.
* Backend application is unavailable.

**Investigation:**

```yaml
kubectl describe ingress <ingress-name>
kubectl get svc
kubectl get endpoints
kubectl get deployment
kubectl get pods
kubectl describe pod <pod-name>
```

**Fixes:**

* Restore backend Pods.
* Fix readiness probe.
* Correct Service selector.
* Scale the Deployment.
* Restore application availability.

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

> First, I'd verify whether the application domain resolves to the Ingress LoadBalancer by using **nslookup** or **dig**. Then I'd compare the DNS record with the external IP or hostname assigned to the Ingress. Next, I'd verify the Ingress host configuration, DNS provider settings, and LoadBalancer status. Based on the findings, I'd correct the DNS configuration and validate that the application is accessible through the domain name.
> **"First, I'd verify whether the domain resolves correctly using `nslookup` or `dig`. Then I'd compare the resolved IP with the Ingress LoadBalancer address and verify the Ingress host configuration. If the DNS record is incorrect, I'd update it or fix the ExternalDNS configuration. Finally, I'd validate that the domain resolves correctly and the application is accessible."**

**Possible Causes:**

* DNS record is missing.
* DNS record points to the wrong IP or LoadBalancer.
* DNS propagation is still in progress.
* Incorrect host configured in Ingress.
* ExternalDNS is not updating records.
* LoadBalancer external IP is unavailable.

**Investigation:**

```yaml
kubectl get ingress
kubectl describe ingress <ingress-name>
kubectl get svc -n ingress-nginx
nslookup <domain-name>
dig <domain-name>
```

**Fixes:**

* Create or update the DNS record.
* Point the DNS record to the correct LoadBalancer.
* Correct the Ingress host.
* Fix ExternalDNS configuration.
* Wait for DNS propagation if recently updated.

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

> First, I'd verify whether the Ingress Controller Pods are running in the ingress namespace. Then I'd inspect the controller logs and events to identify startup failures or configuration issues. Next, I'd verify the controller Service and LoadBalancer status. Based on the findings, I'd restore the Ingress Controller and validate that it starts routing traffic successfully.
> **"First, I'd verify whether the Ingress Controller Pods are running by checking the ingress namespace. Then I'd review the controller logs and Deployment status to identify startup or configuration issues. Next, I'd verify the LoadBalancer Service and external IP. After resolving the issue, I'd restart the controller if required and validate that it starts routing traffic successfully."**

**Possible Causes:**

* Ingress Controller Pod is crashed.
* CrashLoopBackOff.
* ImagePullBackOff.
* Controller Deployment failed.
* LoadBalancer Service issue.
* Insufficient node resources.
* Incorrect controller configuration.

**Investigation:**

```yaml
kubectl get pods -n ingress-nginx
kubectl describe pod <controller-pod>
kubectl logs <controller-pod> -n ingress-nginx
kubectl get deployment -n ingress-nginx
kubectl get svc -n ingress-nginx
```
**Fixes:**

* Restart the Ingress Controller.
* Fix controller configuration.
* Resolve Pod startup issues.
* Resolve ImagePullBackOff.
* Restore LoadBalancer Service.
* Increase node resources if required.

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

**Possible Causes:**

* Incorrect `ingressClassName`.
* IngressClass does not exist.
* Ingress Controller is watching a different class.
* Default IngressClass is configured incorrectly.
* Typographical error in the IngressClass name.

**Investigation:**

```yaml
kubectl get ingress
kubectl describe ingress <ingress-name>
kubectl get ingressclass
kubectl describe ingressclass <class-name>
kubectl logs <controller-pod> -n ingress-nginx
```

**Fixes:**

* Update the correct `ingressClassName`.
* Create the missing IngressClass.
* Configure the controller to watch the correct class.
* Correct spelling mistakes.
* Restart the controller if required.

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

> First, I'd verify whether the client can resolve the application hostname using **nslookup** or **dig**. Then I'd compare the resolved IP or hostname with the Ingress LoadBalancer address. Next, I'd verify the DNS record, Ingress host configuration, and LoadBalancer status. Based on the findings, I'd correct the DNS or Ingress configuration and validate that the hostname resolves successfully.
> **"First, I'd verify whether the hostname resolves correctly using `nslookup` or `dig`. Then I'd compare the resolved IP with the Ingress LoadBalancer address and verify the configured host in the Ingress resource. If required, I'd update the DNS record or correct the Ingress configuration. Finally, I'd validate that the hostname resolves successfully and the application is accessible."**

**Possible Causes:**

* DNS record is missing.
* DNS record points to the wrong LoadBalancer.
* Incorrect hostname configured in Ingress.
* LoadBalancer External IP is not assigned.
* ExternalDNS is not updating records.
* DNS propagation is still in progress.

**Investigation:**

```yaml
kubectl get ingress
kubectl describe ingress <ingress-name>
kubectl get svc -n ingress-nginx
nslookup <host-name>
dig <host-name>
```

**Fixes:**

* Create or update the DNS record.
* Correct the Ingress host.
* Point DNS to the correct LoadBalancer.
* Fix ExternalDNS configuration.
* Wait for DNS propagation.

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

**Possible Causes:**

* Incorrect path configured.
* Incorrect `pathType`.
* Wrong backend Service.
* Service has no Endpoints.
* Backend Pods are Not Ready.
* Application is serving a different context path.

**Investigation:**

```yaml
kubectl get ingress
kubectl describe ingress <ingress-name>
kubectl get svc
kubectl get endpoints
kubectl get pods
kubectl describe svc <service-name>
```

**Fixes:**

* Correct the path.
* Correct the `pathType`.
* Update the backend Service.
* Restore Service Endpoints.
* Update the application's context path.

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

> First, I'd verify the configured host rule using **kubectl describe ingress** and confirm that the client is sending the correct Host header. Then I'd verify that the DNS record resolves to the Ingress LoadBalancer and that the backend Service exists. Next, I'd check the Endpoints and backend Pods. Based on the findings, I'd correct the host rule or DNS configuration and validate that requests are routed to the correct application.
> **"First, I'd verify the configured host rule in the Ingress resource and ensure the client is sending the correct Host header. Then I'd confirm that the DNS record resolves to the Ingress LoadBalancer and verify that the backend Service has active Endpoints. After correcting the host rule or DNS configuration, I'd validate that requests are routed to the correct backend application."**

**Possible Causes:**

* Incorrect host configured in Ingress.
* DNS record points to the wrong IP.
* Client is using the wrong hostname.
* Backend Service is incorrect.
* Service has no Endpoints.
* Default backend is handling the request.

**Investigation:**

```yaml
kubectl get ingress
kubectl describe ingress <ingress-name>
nslookup <host-name>
kubectl get svc
kubectl get endpoints
kubectl get pods
```

**Fixes:**

* Correct the host rule.
* Update the DNS record.
* Use the correct hostname.
* Correct the backend Service.
* Restore Endpoints.

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

> First, I'd verify whether the application is continuously redirecting between HTTP and HTTPS by testing the URL and reviewing the Ingress configuration. Then I'd inspect the TLS configuration and NGINX annotations to determine whether both the Ingress and the application are forcing HTTPS redirects. Next, I'd review the application configuration and LoadBalancer settings. Based on the findings, I'd remove the duplicate redirect configuration and validate that the application loads successfully without entering a redirect loop.
> **"First, I'd verify whether the application is repeatedly redirecting between HTTP and HTTPS. Then I'd inspect the Ingress TLS configuration and NGINX annotations to determine whether both the Ingress and the application are forcing HTTPS redirects. Next, I'd verify that the application correctly handles the `X-Forwarded-Proto` header. After correcting the redirect configuration, I'd validate that the application is accessible without entering a redirect loop."**

**Possible Causes:**

* Both Ingress and application are forcing HTTPS.
* Incorrect SSL redirect annotation.
* Incorrect backend redirect configuration.
* LoadBalancer terminates SSL, but the application is unaware.
* Missing `X-Forwarded-Proto` header.
* Incorrect reverse proxy configuration.

**Investigation:**

```yaml
kubectl get ingress
kubectl describe ingress <ingress-name>
kubectl logs -n ingress-nginx <ingress-controller-pod>
kubectl describe svc <service-name>
kubectl describe deployment <deployment-name>
curl -I http://<host-name>
curl -Ik https://<host-name>
```
**Fixes:**

* Configure HTTPS redirection in only one place.
* Correct the SSL redirect annotation.
* Configure the application to trust `X-Forwarded-Proto`.
* Update reverse proxy configuration.
* Correct TLS configuration.

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

> First, I'd verify that the Ingress is forwarding requests to the correct backend Service. Then I'd confirm that the backend Pods are Running and that the application responds within the configured timeout. Next, I'd inspect the Ingress Controller logs, backend application logs, and network connectivity to identify whether the request is timing out because of a slow application or incorrect timeout configuration. Based on the findings, I'd optimize the application or increase the timeout values and validate that requests complete successfully.
> **"First, I'd verify that the backend Pods are healthy and responding correctly. Then I'd review the application logs and Ingress Controller logs to determine whether the timeout is caused by a slow backend, database query, or external API call. Next, I'd verify the Ingress timeout configuration and backend resource utilization. After optimizing the application or increasing the timeout values, I'd validate that requests complete successfully without returning a 504 Gateway Timeout error."**

**Possible Causes:**

* Backend application is taking too long to respond.
* Database queries are slow.
* Application is waiting on an external API.
* NGINX Ingress timeout is too low.
* Backend Pods are overloaded.
* Network latency between Ingress and backend.
* CPU or Memory resource exhaustion.

**Investigation:**

```yaml
kubectl describe ingress <ingress-name>
kubectl logs -n ingress-nginx <ingress-controller-pod>
kubectl get svc
kubectl get endpoints
kubectl get pods
kubectl logs <pod-name>
kubectl top pods
```

**Fixes:**

* Increase Ingress timeout values.
* Optimize application performance.
* Optimize slow database queries.
* Increase backend Pod replicas.
* Increase CPU or Memory resources.
* Resolve network latency.

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

**Final Ingress Troubleshooting Flow** (Interview Cheat Sheet)
> Client --> DNS
   ↓
Ingress
   ↓
IngressClass
   ↓
Ingress Controller
   ↓
Service
   ↓
Endpoints
   ↓
Pods
   ↓
Application
   ↓
Database / External APIs
```
 
* **404** → Host / Path / Ingress Rule
* **502** → Service / Port / Backend Connection
* **503** → No Healthy Pods / No Endpoints
* **504** → Slow Backend / Timeout
* **SSL/TLS** → Certificate / TLS Secret / Redirect
* **DNS / Host** → DNS Record / LoadBalancer / Host Rule
* **IngressClass** → Controller Selection
* **Ingress Controller** → Controller Pod / Logs
* **Path Routing** → Path / `pathType`
* **Host Routing** → Host Header / DNS
* **Redirect Loop** → Duplicate HTTP→HTTPS Redirect
