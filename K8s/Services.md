# Why Services Exist

**Definition**

* Pods are **temporary** (can restart, die, or move to another node).
* Pod IPs are **dynamic** (change after restart).
* Service provides a **stable virtual IP (ClusterIP)**. / reliable networking inside the cluster.
* Service uses **Labels & Selectors** to find Pods.
* Traffic is automatically routed to **healthy Pods**.
* Frontend communicates with the **Service**, not directly with Pods.

## Service YAML Quick Revision

```yaml
apiVersion: v1                 # Core API version for Service
kind: Service                  # Creates a Service object

metadata:
  name: my-app-service         # Service name (used for DNS)

spec:
  selector:
    app: my-app                # Selects Pods with this label

  ports:
  - protocol: TCP              # Communication protocol (Default: TCP)
    port: 80                   # Service port (Clients connect here)
    targetPort: 8080           # Pod application port

  type: ClusterIP              # Default Service type (Internal only)
```
## Flow

Client → Service (Stable ClusterIP) → Healthy Pods

If a Pod restarts → Pod IP changes → Service automatically routes traffic to the new Pod.

## Interview One-Liner

**Service** provides a **stable IP and DNS name** for accessing Pods. Even if Pods are recreated and their IPs change, the Service continues routing traffic to the healthy Pods using **labels and selectors**.

# ClusterIP Service
* Default Service type in Kubernetes.
* Accessible **only inside the cluster**.
* Gets a **stable ClusterIP** and DNS name.
* Used for **Pod-to-Pod** communication.
* Cannot be accessed from outside the cluster.
* Common Use Cases: Frontend → Backend, Backend → Database, Microservice → Microservice

## ClusterIP YAML Quick Revision

```yaml id="vqg5od"
apiVersion: v1                  # Core API version
kind: Service                   # Creates a Service

metadata:
  name: my-app-service          # Service name

spec:
  selector:
    app: my-app                 # Selects target Pods

  ports:
  - protocol: TCP               # Communication protocol
    port: 80                    # Service port
    targetPort: 8080            # Pod port

  type: ClusterIP               # Internal access only (Default)

# NodePort
    nodePort: 30007             # External port (30000–32767). under targetPort

  type: NodePort                # Exposes Service outside the cluster. Instead of ClusterIP

# LoadBalancer
 type: LoadBalancer            # Creates a Cloud Load Balancer. Instead of ClusterIP
```

## Access

* Inside Cluster → ✅ `my-app-service:80`
* Outside Cluster → ❌ Not Accessible

## Flow

Pod → ClusterIP Service → Target Pods

## Interview One-Liner

**ClusterIP** is the **default Service type** that provides a **stable internal IP and DNS** for communication **within the Kubernetes cluster**.

---

# NodePort Service
* Exposes the application **outside the cluster**.
* Opens a port on **every Kubernetes Node**.
* External users access the application using:
  **NodeIP:NodePort**
* NodePort range = **30000–32767**.
## Access
* Inside Cluster → ✅ `my-app-service:80`
* Outside Cluster → ✅ `NodeIP:30007`

## Flow

External User → NodeIP:30007 → NodePort Service → Target Pods

## Interview One-Liner

**NodePort** exposes an application **outside the cluster** by opening a port (**30000–32767**) on every node, allowing access using **NodeIP:NodePort**.
# LoadBalancer Service

**Definition**

* Exposes the application **outside the cluster** using a **Cloud Load Balancer**.
* Supported by cloud providers like **AWS, Azure, GCP**.
* Provides a **Public IP** or **DNS name**.
* Best choice for **production external access**.
* No need to know Node IPs or NodePorts.
* Kubernetes creates a **ClusterIP**.
* Kubernetes creates a **NodePort**.
* Cloud Provider creates a **Load Balancer**.
* Load Balancer forwards traffic → NodePort → Pods.

## Access

* Inside Cluster → ✅ Service DNS / ClusterIP
* Outside Cluster → ✅ Public IP or DNS

## Flow

External User → Cloud Load Balancer → NodePort → ClusterIP → Pods

## On-Premise Kubernetes

**Option 1: NodePort + External Load Balancer**

* Expose application using **NodePort**.
* Use **Nginx, Traefik, F5** or any external Load Balancer.
* Forward traffic to the NodePort.

**Option 2: MetalLB**

* Install **MetalLB**.
* Assigns external IPs from a configured IP pool.
* Makes **LoadBalancer Services** work like a cloud environment.

## Interview One-Liner

**LoadBalancer Service** exposes an application externally by provisioning a **cloud load balancer** with a **public IP/DNS**, which forwards traffic to the Kubernetes Service and then to the Pods.

---

* **ClusterIP** → Internal communication only.
* **NodePort** → External access using **NodeIP:Port**.
* **LoadBalancer** → External access using **Cloud Load Balancer**.
* **On-Premise** → Use **NodePort + External LB** or **MetalLB**.

# Headless Service
* A Service **without a ClusterIP**.
* Does **not perform load balancing**.
* Returns **individual Pod IPs** through DNS.
* Clients connect **directly to Pods**.
* Used when applications need **Pod-level communication**.

## Headless Service YAML Quick Revision

```yaml
spec:
  clusterIP: None               # No ClusterIP (Headless Service)
```
Common Use Cases: **StatefulSet, Kafka, MongoDB, Cassandra, ZooKeeper, Applications that require direct Pod access**

## Flow

Client → DNS Query → Pod IPs Returned → Client connects directly to the required Pod.

## Interview One-Liner

**Headless Service** is a Service with **`clusterIP: None`**. It **does not provide load balancing**; instead, it returns the **individual Pod IPs**, making it ideal for **StatefulSets** and distributed databases like **Kafka, MongoDB, and Cassandra**.

---
# Service Selectors

**Definition**

* Service does **not use Pod names or Pod IPs**.
* Service uses **Labels & Selectors** to find Pods.
* Selector matches Pods with the same label.
* Kubernetes automatically creates **Endpoints** for matching Pods.

## Service Selector YAML Quick Revision

```yaml id="0rm0oc"
apiVersion: v1                  # Core API version
kind: Service                   # Creates a Service

metadata:
  name: my-app-service          # Service name

spec:
  selector:
    app: my-app                 # Selects Pods with label app=my-app

  ports:
  - port: 80                    # Service port
    targetPort: 8080            # Pod application port
```

## Matching Pod

```yaml id="o1gg08"
apiVersion: v1                  # Core API version
kind: Pod                       # Creates a Pod

metadata:
  labels:
    app: my-app                 # Must match Service selector

spec:
  containers:
  - name: my-app
    image: my-java-app:1.0
```

## Flow

Service Selector (`app=my-app`) → Finds Matching Pods → Kubernetes Creates Endpoints → Traffic Routed to Healthy Pods

## Without Selector

**Definition**

* Service does **not automatically discover Pods**.
* You must create an **Endpoints** object manually.
* Commonly used to connect to **external applications** or **external databases**.

## Service Without Selector

```yaml id="4ljlwm"
apiVersion: v1
kind: Service

metadata:
  name: external-service

spec:
  ports:
  - port: 80
    targetPort: 80
```

## Endpoints

```yaml id="n0ndlg"
apiVersion: v1
kind: Endpoints

metadata:
  name: external-service

subsets:
- addresses:
  - ip: 192.168.1.100          # External Server IP

  ports:
  - port: 80
```

## Flow

Service (No Selector) → Endpoints Object → External Server / External Application

## Interview One-Liner

**Service Selectors** use **labels** to automatically discover Pods and route traffic. If a Service has **no selector**, Kubernetes does **not** create Endpoints automatically, so you must define an **Endpoints** object manually.
---
# Endpoints
* Endpoints contain the **actual Pod IPs and Ports** behind a Service.
* Created automatically when the Service has a **selector**.
* Created manually when the Service has **no selector**.
* Service sends traffic to the **Endpoints**, not directly to Pods.

## Auto-Created Endpoints
### Flow
Deployment → Creates Pods → Service Selector Matches Pods → Kubernetes Creates Endpoints → Traffic Routed to Pods

## Common Use Cases (Manual Endpoints)
### Flow

Service (No Selector) → Manual Endpoints → External Database / External API / External Server

* External Database
* External API
* Legacy Application
* Non-Kubernetes Server

## Interview One-Liner

**Endpoints** are the actual **Pod IPs and Ports** behind a Service. If a Service has a **selector**, Kubernetes creates Endpoints automatically. If it has **no selector**, you must create the **Endpoints** object manually to route traffic to external resources.
---

# CoreDNS
* CoreDNS is the **DNS Server** of Kubernetes.
* Runs as a **Deployment** in the **kube-system** namespace.
* Resolves **Service names** and **Pod names** into IP addresses.
* Enables **Service Discovery** inside the cluster.

## CoreDNS Flow

Pod → DNS Query → CoreDNS → Kubernetes API → Returns IP Address

* **Normal Service** → Returns **ClusterIP**
* **Headless Service** → Returns **Pod IP(s)**
```text
# Service DNS Name
<Service-Name>.<Namespace>.svc.cluster.local

# Example
my-service.default.svc.cluster.local

# `svc` → Service. `cluster.local` → Cluster DNS domain
```
> **Same Namespace:** Just use `my-service`.

# Pod DNS
* Pods can also have DNS names. Mainly used with **StatefulSets** and **Headless Services**.

```text
# Pod DNS Pattern
<Pod-Name>.<Service-Name>.<Namespace>.svc.cluster.local
```
```text
# Example
mongodb-0.mongodb.default.svc.cluster.local
```
# CoreDNS ConfigMap
* Controls CoreDNS behavior. Stored as a **ConfigMap**.

## Common Uses

* Forward DNS queries to external DNS.
* Configure Split DNS.
* Add Custom Internal DNS Zones.
* Customize DNS resolution.

## Interview One-Liner

**CoreDNS** is the **DNS server** in Kubernetes that runs in the **kube-system** namespace. It resolves **Service names to ClusterIPs** and **Headless Service names to individual Pod IPs**, enabling seamless service discovery inside the cluster.
# Service Discovery

**Definition**

* Service Discovery = Find and connect to applications using **Service names**, not Pod IPs.
* Powered by **Services + CoreDNS**.
* Pod IPs change, Service names remain stable.

## Service Discovery Flow

Frontend Pod → Service DNS → CoreDNS → ClusterIP → Endpoints → Backend Pod

Even if Pods restart or change IPs → Service & Endpoints automatically route traffic.

---

# Service Discovery Methods

## 1. Environment Variables
* Kubernetes automatically injects Service environment variables into Pods.
* Available **only if the Service existed before the Pod started**.
```text id="z1m2sa"
# Example
DB_SERVICE_HOST
DB_SERVICE_PORT
```
## 2. DNS (Recommended)
* Uses **CoreDNS** to resolve Service names.
* Dynamic and works for all Services.
* Most commonly used in production.

```text id="0z2vga"
# Same Namespace
db-service

# Different Namespace
db-service.default.svc.cluster.local
```

### 1. Frontend → Backend (Inside Cluster)
**Service:** ClusterIP
* Internal communication.
* No external exposure.

### 2. Minikube / Local Testing
**Service:** NodePort
* Access application from browser.
* Simple external testing.

### 3. Public API on AWS / Azure / GCP
**Service:** LoadBalancer
* Public IP/DNS.
* Production-ready.

### 4. On-Premise Kubernetes
**Service:** NodePort + External Load Balancer **or** MetalLB
* No cloud Load Balancer available.

### 5. Stateful Database (Kafka, MongoDB, Cassandra)
**Service:** Headless Service
* Direct Pod-level access.
* Each Pod has a unique identity.

### 6. External Database
**Service:** Service (No Selector) + Manual Endpoints
* Stable Service DNS.
* Routes traffic to an external database.

### 7. Multiple Application Versions (v1 & v2)
**Service:** ClusterIP + Different Selectors
* Route traffic to different application versions.

### 8. Internal Microservices
**Service:** ClusterIP
* Secure internal communication.
* Stable networking.

### 9. Connect to a Specific Stateful Pod
**Service:** Headless Service
* DNS returns individual Pod IPs.
* No load balancing.

### 10. Internal + External Database Access
**Service:** ClusterIP + Ingress / LoadBalancer
* ClusterIP for internal clients.
* Ingress/LoadBalancer for external users.

## Interview One-Liner

* **Service Discovery** → Services + CoreDNS allow applications to communicate using **stable Service names** instead of changing Pod IPs.
* **ClusterIP** → Internal communication.
* **NodePort** → External access via `NodeIP:NodePort`.
* **LoadBalancer** → Production external access using a cloud load balancer.
* **Headless Service** → Direct Pod-level communication.
* **Endpoints** → Connect Kubernetes Services to external systems.
