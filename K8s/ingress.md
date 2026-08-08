**Ingress:** Ingress is a Kubernetes resource used to manage **external HTTP/HTTPS traffic** and route it to services inside the cluster. Instead of exposing every service separately using NodePort or LoadBalancer, Ingress provides a **centralized routing layer**.

Ingress can route traffic based on **path, hostname, and TLS/HTTPS**.

Important point: **Ingress is only a set of routing rules.** It needs an **Ingress Controller**, such as NGINX Ingress Controller, to actually process the traffic.

```text id="f8r3kc"
User Request → Ingress Controller → Ingress Rules → Kubernetes Service → Pod
Internet → NGINX Ingress Controller → Ingress Rule: / → my-app-service:80 → Application Pod
```

### Basic Ingress YAML

```yaml id="k3m9px"
apiVersion: networking.k8s.io/v1           # Defines the Kubernetes API version for Ingress.
kind: Ingress                              # Creates an Ingress resource.
metadata:                                  # Name of the Ingress object.
  name: my-app-ingress
  annotations:
    nginx.ingress.kubernetes.io/rewrite-target: /        # NGINX rewrites the incoming URL path before forwarding it to the backend.
spec:
  rules:        # Defines the routing rules. No `host` is specified → The rule can apply to **any host** matching the path
  - http:
      paths:
      - path: /                         # Matches requests starting with `/`.
        pathType: Prefix            # pathType: Prefix` → Matches the path and its subpaths, such as:  / → Match or  /home → Match
        backend:                    # `backend.service.name` → The Kubernetes Service receiving the traffic.
          service:
            name: my-app-service
            port:                   # `backend.service.port` → The Service port receiving the request.
              number: 80
```

**Quick revision:**

```text id="p9s4kd"
Ingress → Routing Rules. It manages external HTTP/HTTPS traffic and routes requests to Kubernetes Services. The Ingress resource contains the rules, while the Ingress Controller actually processes those rules.
Ingress Controller → Implements the Rules. NGINX, AWS Load Balancer Controller, etc. It watches Ingress resources and actually handles incoming traffic.
Path → Routes traffic based on the URL path.
Host → Routes traffic based on the hostname/domain.

**Ingress Controller:** An Ingress resource only contains **routing rules**. It doesn't route traffic by itself. The **Ingress Controller** watches those rules and actually handles incoming traffic. NGINX is a popular Ingress Controller and supports features like **TLS, path-based routing, rate limiting, and traffic routing**.

```text id="z6k3pq"
User → Load Balancer → NGINX Ingress Controller → Ingress Rules → Service → Pod
```

### Install NGINX Ingress Controller

```bash
kubectl apply -f https://raw.githubusercontent.com/kubernetes/ingress-nginx/main/deploy/static/provider/cloud/deploy.yaml  # Installs the NGINX Ingress Controller and required Kubernetes resources.
```

This manifest creates resources such as **Namespace, ServiceAccount, Roles, Deployment, and Service**.

```text id="h8w2nm"
Install Manifest → NGINX Ingress Controller → Watches Ingress Resources → Routes Traffic
```

**Important:** Without an Ingress Controller, the Ingress resource exists, but **traffic won't actually be routed**.

---

### Path-Based Routing

Path-based routing sends traffic to different Services based on the **URL path**. It is useful when multiple applications need to be exposed under the **same domain**.

```text id="r3m7vk"
example.com/app1 → app1-service → app1 Pods
example.com/app2 → app2-service → app2 Pods
```

### Path-Based Routing YAML

```yaml id="p8x4nz"
spec:
  rules:                                      # Defines the Ingress routing rules.
  - http:
      paths:
      - path: /app1                           # Requests starting with /app1.
        pathType: Prefix                      # Matches /app1 and subpaths like /app1/home.
        backend:
          service:
            name: app1-service                # Sends matching traffic to app1-service.
            port:
              number: 80                      # Service port receiving the traffic.
      - path: /app2                           # Requests starting with /app2.
        pathType: Prefix                      # Matches /app2 and subpaths like /app2/home.
        backend:
          service:
            name: app2-service                # Sends matching traffic to app2-service.
            port:
              number: 80                      # Service port receiving the traffic.
```

```text id="k5c9yt"
Request /app1 → Ingress Controller → /app1 Rule → app1-service → app1 Pod
Request /app2 → Ingress Controller → /app2 Rule → app2-service → app2 Pod
```

**Quick revision:**

```text id="u2v6qa"
Ingress → Rules
Ingress Controller → Implements Rules
NGINX → Popular Ingress Controller
Path-Based Routing → Routes using URL Path
Prefix → Matches Path + Subpaths
```
**Host-Based Routing:** Host-based routing sends traffic to different Services based on the **domain name**. The Ingress first checks the **Host header**, then checks the path, and finally forwards the request to the matching backend Service.

```text id="f7k2nm"
app1domain.com → Ingress Controller → Host Match → app1-service → app1 Pod
app2domain.com → Ingress Controller → Host Match → app2-service → app2 Pod
```

### Host-Based Routing YAML

```yaml id="m4q8vz"
spec:
  rules:                                      # Defines host-based routing rules.
  - host: app1domain.com                      # Requests for this domain.
    http:
      paths:
      - path: /                               # Matches the root path and subpaths.
        pathType: Prefix
        backend:
          service:
            name: app1-service                # Sends traffic to app1-service.
            port:
              number: 80
  - host: app2domain.com                      # Requests for this domain.
    http:
      paths:
      - path: /                               # Matches the root path and subpaths.
        pathType: Prefix
        backend:
          service:
            name: app2-service                # Sends traffic to app2-service.
            port:
              number: 80
```

```text id="j9v3rx"
Request → Host Header → Host Match → Path Match → Service → Pod
```

---

**TLS Termination:** TLS termination means the **Ingress Controller handles HTTPS encryption/decryption**. The client connects using HTTPS, and after TLS is terminated at the Ingress, the backend can receive HTTP traffic.

```text id="q6w8pk"
Client HTTPS → Ingress Controller → TLS Termination → HTTP → Service → Pod
```

### Create TLS Secret

```bash id="c2n7lm"
kubectl create secret tls my-app-tls --cert=tls.crt --key=tls.key  # Creates a TLS Secret containing the certificate and private key.
```

### TLS YAML

```yaml id="v5x3qa"
spec:
  tls:                                        # Defines HTTPS/TLS configuration.
  - hosts:
    - app1domain.com                           # TLS applies to app1domain.com.
    - app2domain.com                           # TLS applies to app2domain.com.
    secretName: my-app-tls                    # Secret containing tls.crt and tls.key.
```

```text id="b8r4yc"
HTTPS Request → Ingress → TLS Secret → Decrypt → Route → Service → Pod
```

---

**HTTP to HTTPS Redirect:** If users access the application using HTTP, NGINX can automatically redirect them to HTTPS using this annotation.

### YAML

```yaml id="n3k7wd"
metadata:
  annotations:
    nginx.ingress.kubernetes.io/force-ssl-redirect: "true"  # Redirects HTTP requests to HTTPS.
```

```text id="p2x6hv"
HTTP Request → NGINX Ingress → 301 Redirect → HTTPS → TLS Termination → Service → Pod
```

**Quick revision:**

```text id="c7m4zs"
Host-Based Routing → Routes using Domain
TLS Termination → Ingress handles HTTPS
TLS Secret → Stores Certificate + Private Key
Force SSL Redirect → HTTP → HTTPS
```
**Wildcard Domain:** A wildcard domain allows a **single TLS certificate** to secure multiple subdomains under the same domain. The correct wildcard format is `*.domain.com`.

```text id="v8k3qp"
*.domain.com → app.domain.com + api.domain.com + web.domain.com
```

### Wildcard TLS YAML

```yaml id="m6x2rd"
spec:
  tls:                                      # Defines TLS configuration.
  - hosts:
    - "*.domain.com"                        # Wildcard certificate covers subdomains under domain.com.
    secretName: my-app-tls                  # TLS Secret containing the certificate and private key.
```

```text id="q4n7zs"
Request → Host Header → Wildcard TLS Certificate → Ingress Rule → Service → Pod
```

**Important:** `*.domain.com` covers `app.domain.com` and `api.domain.com`, but not the root `domain.com` itself.

---

**Default Backend:** The default backend handles requests that **don't match any configured host or path rule**. It can return a **404 page, maintenance page, or custom message**.

### Default Backend YAML

```yaml id="r5w2kc"
spec:
  defaultBackend:                           # Backend used when no host/path rule matches.
    service:
      name: default-backend                 # Service that handles unmatched requests.
      port:
        number: 80                          # Service port.
```

```text id="p3x8vn"
Request → Ingress Rules → Match Found → Matching Service
                      → No Match → Default Backend → 404/Maintenance Page
```

---

**Rewrite Rule:** A rewrite rule **modifies the URL path before sending the request to the backend**.

For example:

```text id="k7m4qt"
Client: /app1/page2 → Ingress Rewrite → /page2 → app1-service → Pod
```

This is useful when the backend application expects requests from the **root path `/`**, while externally we want to expose it under `/app1`.

### Rewrite YAML

```yaml id="c9v2hx"
metadata:
  annotations:
    nginx.ingress.kubernetes.io/use-regex: "true"             # Enables regular-expression paths.
    nginx.ingress.kubernetes.io/rewrite-target: /$2           # Sends the captured path after /app1 or /app2 to the backend.
spec:
  rules:
  - http:
      paths:
      - path: /app1(/|$)(.*)                                  # Captures everything after /app1.
        pathType: ImplementationSpecific                       # Allows NGINX-specific regex path behavior.
        backend:
          service:
            name: app1-service
            port:
              number: 80
```

```text id="n6q3wy"
Incoming /app1/page2 → Regex Match → Capture /page2 → Rewrite /$2 → Backend receives /page2
```

**Quick revision:**

```text id="x4m8kp"
Wildcard Domain → One TLS Certificate → Multiple Subdomains
Default Backend → Handles Unmatched Requests
Rewrite Rule → Changes URL Before Backend
*.domain.com → app.domain.com / api.domain.com
/app1/page2 → Rewrite → /page2
```
Exactly. For interviews, knowing **what it does** is not enough. You should also know **why we need it** and **when we use it**. Here’s the simple reasoning:

### 1. TLS Termination — Why do we need it?

TLS termination means the **Ingress handles HTTPS encryption/decryption** instead of every backend application handling TLS.

**Why?**

* Centralizes certificate management.
* Backend applications don't need to manage certificates individually.
* Reduces TLS configuration on every application.
* Makes certificate renewal easier.
* Ingress can handle HTTPS for multiple services.

```text
Client HTTPS → Ingress → TLS Termination → HTTP → Service → Pod
```

**Example:** If you have 20 microservices, instead of configuring certificates on all 20 applications, you can handle TLS at the Ingress.

---

### 2. HTTP → HTTPS Redirect — Why do we need it?

TLS alone allows HTTPS, but users can still access the application using HTTP.

**Why?**

* Forces users to use **encrypted HTTPS communication**.
* Prevents sensitive data from being sent over plain HTTP.
* Provides a consistent secure entry point.

```text
HTTP Request → Ingress → Redirect → HTTPS → Application
```

**Example:**

```text
http://app.example.com → https://app.example.com
```

So, **TLS enables HTTPS**, while **redirect forces users to HTTPS**.

---

### 3. Wildcard Domain — Why do we need it?

Wildcard certificates are useful when you have **many subdomains**.

Without wildcard:

```text
app.example.com → Certificate 1
api.example.com → Certificate 2
admin.example.com → Certificate 3
```

With wildcard:

```text
*.example.com → One Certificate → app/api/admin.example.com
```

**Why?**

* Reduces the number of certificates to manage.
* Simplifies TLS configuration.
* Useful for environments with many dynamically created subdomains.

```text
Wildcard Certificate → Multiple Subdomains → Same TLS Configuration
```

---

### 4. Default Backend — Why do we need it?

Not every request will match your Ingress rules.

For example:

```text
app.example.com → app-service
api.example.com → api-service
unknown.example.com → No Matching Rule
```

Without a proper fallback, the unmatched request may result in an error.

A default backend gives you a **controlled response**, such as a 404 page or maintenance page.

```text
Request → Ingress Rules → Match → Service
                    ↓
                  No Match
                    ↓
              Default Backend
                    ↓
                 404 Page
```

**Why?** It gives predictable handling for **unknown hosts or unmatched requests**.

---

### 5. Rewrite Rule — Why do we need it?

This is useful when the **external URL structure and backend application's expected URL structure are different**.

Suppose your backend application only understands:

```text
/page1
/page2
```

But you want users to access it as:

```text
/app1/page1
/app1/page2
```

Without rewriting, the backend receives:

```text
/app1/page1
```

and the application may not know what `/app1` means.

With rewriting:

```text
User → /app1/page1 → Ingress Rewrite → /page1 → Backend
```

**Why?**

* Allows multiple applications to share one domain.
* Keeps backend applications simple.
* Removes unnecessary prefixes before sending requests.
* Useful when applications are designed to run from `/`.

### Quick Interview Revision

```text
TLS Termination → Centralize HTTPS and certificate management
HTTP → HTTPS → Force secure communication
Wildcard Domain → One certificate for many subdomains
Default Backend → Handle unmatched requests
Rewrite Rule → Change external URL before sending to backend
```

The easiest way to remember **why**:

```text
TLS → Secure
Redirect → Force Secure
Wildcard → Simplify Certificates
Default Backend → Handle Unknown Requests
Rewrite → Adapt URL for Backend
```
**Rate Limiting:** Rate limiting controls **how many requests a client can send within a specific time period**. It protects the backend from excessive traffic, accidental overload, or abusive clients.

**Why do we need it?** To prevent one client from consuming too many resources and affecting other users.

```text id="r8m2kv"
Client → Ingress → Rate Limit Check → Within Limit → Backend
                              ↓
                         Limit Exceeded
                              ↓
                           Reject
```

### Rate Limiting YAML

```yaml id="n5x7qp"
metadata:
  annotations:
    nginx.ingress.kubernetes.io/limit-connections: "5"       # Allows maximum 5 concurrent connections per client.
    nginx.ingress.kubernetes.io/limit-rps: "60"              # Limits the request rate per client to 60 requests per second.
```

**Important:** `limit-rps: 60` means **60 requests per second**, not per minute.

```text id="c3v9hx"
Client → 60 RPS Allowed → Requests Pass
       → More Than Limit → Excess Requests Restricted
```

---

**CORS (Cross-Origin Resource Sharing):** CORS controls **which external domains are allowed to access your application from a browser**.

For example, if the frontend is hosted on `frontend-domain.com` and the API is on `api-domain.com`, the browser treats them as different origins. CORS tells the browser which origins are allowed.

**Why do we need it?** To allow legitimate frontend applications to call the API while preventing unwanted cross-origin browser requests.

```text id="k6p4ws"
Frontend → Browser → CORS Check → Allowed Origin → API
                              ↓
                         Not Allowed
                              ↓
                           Blocked
```

### CORS YAML

```yaml id="v2q8mn"
metadata:
  annotations:
    nginx.ingress.kubernetes.io/enable-cors: "true"                         # Enables CORS.
    nginx.ingress.kubernetes.io/cors-allow-origin: "https://frontend-domain.com"  # Allows this frontend origin.
    nginx.ingress.kubernetes.io/cors-allow-methods: "GET, POST, PUT, DELETE, OPTIONS" # Allows these HTTP methods.
    nginx.ingress.kubernetes.io/cors-allow-headers: "Content-Type, Authorization"       # Allows these request headers.
    nginx.ingress.kubernetes.io/cors-max-age: "172800"                     # Browser caches preflight result for 172800 seconds.
```

```text id="b7w3cq"
Browser → Preflight Request → Ingress CORS Check → Allowed → Actual API Request
                                             ↓
                                          Denied → Browser Blocks Request
```

**Quick revision:**

```text id="j9k4sx"
Rate Limiting → Controls Request Rate → Protects Backend
CORS → Controls Allowed Origins → Protects Browser-Based API Access
```

**Easy way to remember:**

```text id="z4n8hp"
Rate Limiting → "How many requests?"
CORS → "Which origin can access?"
```
If **Ingress is created but traffic is not flowing**, I would check these common issues one by one.

### 1. Ingress Controller Not Running

If the NGINX Ingress Controller isn't running, the Ingress rules won't actually process traffic.

```bash
kubectl get pods -n ingress-nginx                  # Check whether NGINX Ingress Controller pods are running.
kubectl get svc -n ingress-nginx                  # Check the Ingress Controller Service and its external IP.
```

```text id="p3m7kx"
Request → Ingress Controller Not Running → ❌ Traffic Not Routed
```

---

### 2. DNS / Host Resolution Issue

If host-based routing is configured, the domain must resolve to the **Ingress Controller's external IP**.

```bash
kubectl get ingress                              # Check the Ingress address and configured hosts.
nslookup mydomain.com                            # Verify that the domain resolves correctly.
```

```text id="q8v4zn"
User → mydomain.com → DNS → Ingress External IP → Ingress Controller
```

If DNS points somewhere else, the request won't reach the Ingress.

---

### 3. TLS / Certificate Issue

TLS problems can occur when the **Secret is missing, incorrect, or the certificate doesn't match the requested host**.

```bash
kubectl get secret my-app-tls                    # Check whether the TLS Secret exists.
kubectl describe secret my-app-tls               # Verify the TLS Secret details.
```

Check that the certificate covers the required hostname or wildcard domain.

```text id="w5k2rx"
HTTPS Request → TLS Secret → Certificate Match → Success
                              ↓
                         Certificate Error
```

---

### 4. Rewrite Rule Not Working

If the backend expects `/page1`, but the user accesses `/app1/page1`, the rewrite configuration must correctly remove `/app1`.

```yaml id="c7n4mq"
annotations:
  nginx.ingress.kubernetes.io/use-regex: "true"        # Enables regex path matching.
  nginx.ingress.kubernetes.io/rewrite-target: /$2      # Sends the captured path to the backend.
```

Check that the **Ingress path and rewrite rule match correctly**.

```text id="h3x7vp"
Client /app1/page1 → Ingress Rewrite → /page1 → Backend
```

---

### 5. CORS / Rate-Limiting Configuration

Incorrect annotations or values can cause legitimate requests to be blocked.

For CORS, verify the allowed origin, methods, and headers.

```yaml id="m9q2kf"
nginx.ingress.kubernetes.io/enable-cors: "true"                 # Enables CORS.
nginx.ingress.kubernetes.io/cors-allow-origin: "https://frontend-domain.com"  # Allows the frontend origin.
```

For rate limiting, verify the configured limits.

```yaml id="v6r8px"
nginx.ingress.kubernetes.io/limit-connections: "5"              # Maximum concurrent connections.
nginx.ingress.kubernetes.io/limit-rps: "60"                     # Maximum requests per second.
```

```text id="k4w7zs"
Request → Ingress Annotations → Valid → Backend
                              → Invalid/Exceeded → ❌ Request Blocked
```

### Quick Troubleshooting Flow

```text id="x8m3qn"
Ingress Created → Controller Running? → DNS Correct? → TLS Correct? → Rewrite Correct? → CORS/Rate Limit Correct? → Service/Pod
```

**Key idea:** First verify the **Ingress Controller**, then **DNS**, **TLS**, **routing/rewrite**, and finally **annotations such as CORS and rate limiting**.

Backend → Kubernetes Service. The Ingress normally sends traffic to a Kubernetes Service, and the Service forwards it to the appropriate Pods
```
