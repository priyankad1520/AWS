# Horizontal Pod Autoscaler (HPA)

Imagine your application suddenly gets massive traffic. CPU usage spikes, and requests keep increasing, but the application is still running without crashing. Instead of manually increasing the number of pods, Kubernetes automatically creates more pods to handle the additional load. This is called **Horizontal Pod Autoscaling (HPA)**.

Today, we are learning how Kubernetes automatically scales applications in production using **Horizontal Pod Autoscaler (HPA)**.

---

## What is HPA?

* **HPA** stands for **Horizontal Pod Autoscaler**.
* The important keyword is **Horizontal**.

**Horizontal scaling** means Kubernetes increases the **number of pods** instead of making a single pod larger. When traffic increases, Kubernetes creates additional pod replicas. When traffic decreases, Kubernetes removes the extra pods automatically.

---

## Real-World Example

Imagine your application is normally running with **2 pods**.

Suddenly, there is a huge traffic spike because of an event like **Black Friday**, **Diwali Sale**, or a major product launch.

As more users access the application:

* CPU utilization increases.
* Incoming requests keep increasing.
* Response time becomes slower.
* Users may start experiencing latency.

Instead of manually increasing the replica count, **HPA automatically scales the application** by creating more pod replicas.

When the traffic reduces, HPA automatically removes the unnecessary pods and brings the application back to its normal size. This automatic scale-up and scale-down process is called **autoscaling**.

---

## How HPA Works

Suppose the HPA configuration is:

* Minimum Pods: **2**
* Maximum Pods: **10**
* Target CPU Utilization: **70%**

HPA continuously monitors the **average CPU utilization** across all running pods.

* If the average CPU usage goes above **70%**, Kubernetes increases the number of pod replicas.
* The replicas may increase gradually from **2 → 4 → 6 → ... → 10**, depending on the workload.
* When CPU usage comes back below the target value, Kubernetes gradually reduces the replicas from **10 → 6 → 4 → 2**.

This ensures the application has enough pods to handle the traffic while avoiding unnecessary resource usage.

---

## Important Point

* HPA **does not create more containers inside an existing pod**.
* HPA **creates additional pod replicas**.
* That is why it is called **Horizontal Pod Autoscaler**.

---

## Interview Points

* HPA automatically scales applications based on resource utilization or metrics.
* It performs **horizontal scaling** by increasing or decreasing the number of pod replicas.
* It helps maintain application performance during traffic spikes.
* It reduces infrastructure cost by scaling down pods when traffic decreases.
* Common metrics used by HPA include **CPU utilization**, **memory utilization**, and **custom/external metrics** (using Metrics Server or Prometheus Adapter).
# CPU-Based Horizontal Pod Autoscaling

CPU-based autoscaling is the **most common type of autoscaling** in Kubernetes.

**Why?**

Because when the workload increases, CPU usage usually increases as well.

* More user requests
* More processing
* More CPU utilization

This makes CPU a good metric for automatically scaling applications.

---

## Real-World Example

Imagine your API server normally handles **100 requests per second**.

Suddenly, during a sale or peak event, it starts receiving **2,000 requests per second**.

As the workload increases:

* CPU usage increases from **30% to 90%**.
* HPA continuously monitors the CPU utilization.
* Once the target CPU threshold is crossed, HPA automatically creates more pod replicas.
* The additional pods distribute the incoming traffic, reducing the load on each pod.

---

## How CPU-Based HPA Works

Suppose the HPA target CPU utilization is **50%**.

* If the average CPU utilization **goes above 50%**, HPA **scales up** by creating more pods.
* If the average CPU utilization **drops below 50%**, HPA **scales down** by removing unnecessary pods.

The goal is to keep the average CPU utilization close to the configured target value.

> **Note:** In your explanation, the scale-up and scale-down statements were reversed. The correct behavior is:
>
> * CPU **above** target → **Scale Up**
> * CPU **below** target → **Scale Down**

---

## How HPA Calculates CPU Utilization

HPA calculates CPU utilization based on the **CPU Request**, **not the CPU Limit**.

**Example:**

* CPU Request = **500m**
* Actual CPU Usage = **300m**

CPU Utilization = (300m ÷ 500m) × 100 = **60%**

HPA uses this percentage to decide whether it should increase or decrease the number of pod replicas.

---

## Important Point

CPU **Requests must be configured** in the Deployment.

If CPU Requests are **not defined**:

* Kubernetes cannot calculate the CPU utilization percentage.
* HPA will not be able to make scaling decisions correctly.
* As a result, **CPU-based autoscaling will not work properly**.

---

# Deployment YAML (CPU Requests Required)

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: my-app
spec:
  replicas: 2
  selector:
    matchLabels:
      app: my-app
  template:
    metadata:
      labels:
        app: my-app
    spec:
      containers:
      - name: my-app
        image: nginx:latest
        ports:
        - containerPort: 80

        resources:
          requests:
            cpu: "500m"
            memory: "256Mi"
          limits:
            cpu: "1"
            memory: "512Mi"
```

---

# Horizontal Pod Autoscaler YAML

```yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: my-app-hpa
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: my-app

  minReplicas: 2
  maxReplicas: 10

  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 50
```

---

## Interview Points

* CPU-based autoscaling is the most commonly used HPA strategy.
* HPA monitors the **average CPU utilization** across all pods.
* CPU utilization is calculated based on the **CPU Request**, not the CPU Limit.
* If CPU utilization goes **above** the target, HPA **scales up**.
* If CPU utilization goes **below** the target, HPA **scales down**.
* Without CPU Requests, HPA cannot calculate utilization correctly, so CPU-based autoscaling will not function properly.
# Memory-Based Horizontal Pod Autoscaling

Memory-based autoscaling allows Kubernetes to scale applications based on **memory utilization** instead of CPU utilization.

Many beginners think:

> **CPU scales on CPU, so memory should scale on memory.**

It sounds correct, but **memory-based autoscaling can be risky** in many production applications.

---

## Why Memory-Based Autoscaling Can Be Dangerous

Unlike CPU, **memory usage usually does not decrease immediately** after the workload reduces.

This is common in applications such as:

* Java applications
* Node.js applications
* Applications using in-memory caching
* Applications with long-running processes

These applications often retain memory even after the traffic has dropped.

---

## Real-World Example

Imagine a traffic spike occurs.

* Memory utilization increases.
* HPA detects high memory usage.
* Kubernetes creates additional pods.

Later, the traffic drops.

However, the application's memory usage **remains high** because the memory is not released immediately.

HPA still sees high memory utilization and assumes the application is under heavy load.

As a result:

* Pods are not scaled down.
* Extra resources continue running.
* Infrastructure cost increases unnecessarily.

This is why **CPU-based autoscaling is preferred in most production environments.**

---

## How Memory-Based HPA Works

Suppose the target memory utilization is **75%**.

* If the average memory utilization **goes above 75%**, HPA **scales up** by creating more pods.
* If the memory utilization **drops below the target**, HPA **scales down** by removing unnecessary pods.

However, since memory often does not decrease quickly, scale-down may not happen as expected.

---

## Important Point

Use **memory-based autoscaling** only when you clearly understand your application's memory behavior.

For most stateless applications, **CPU-based autoscaling is the recommended approach.**

---

# Memory-Based HPA YAML

```yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: memory-hpa
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: my-app

  minReplicas: 2
  maxReplicas: 10

  metrics:
  - type: Resource
    resource:
      name: memory
      target:
        type: Utilization
        averageUtilization: 75
```

---

# Custom Metrics Autoscaling

CPU and memory are not always sufficient for autoscaling.

Sometimes applications need to scale based on **business-specific metrics**, such as:

* Queue length
* Requests per second (RPS)
* Kafka consumer lag
* Active users
* RabbitMQ queue size
* Payment transactions
* API request backlog

These are called **Custom Metrics**.

---

## Real-World Example

Imagine a payment processing service.

* CPU utilization is low.
* Memory utilization is low.
* But the message queue suddenly contains **50,000 pending messages**.

Although CPU and memory look healthy, the application is overloaded because it cannot process the queue fast enough.

In this situation, CPU-based HPA will not scale the application.

Instead, HPA can monitor the **queue length** and create more pods to process the pending messages.

---

## How Custom Metrics HPA Works

Suppose a custom metric named **queue_messages** is configured.

* If the average queue messages per pod exceed **100**, HPA creates additional pods.
* As more pods process the messages, the queue size decreases.
* Once the queue returns to a normal level, HPA scales the pods back down.

This type of autoscaling is very common in **event-driven architectures** and **message queue-based applications**.

---

## Important Point

Custom metrics require additional monitoring components.

A typical setup includes:

* Metrics Server (for basic resource metrics)
* Prometheus
* Prometheus Adapter
* External Metrics API (if using external metrics)

Without a proper metrics pipeline, **custom metric-based HPA will not work.**

---

# Custom Metrics HPA YAML

```yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: queue-hpa
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: payment-service

  minReplicas: 2
  maxReplicas: 20

  metrics:
  - type: Pods
    pods:
      metric:
        name: queue_messages
      target:
        type: AverageValue
        averageValue: "100"
```

---

# Stabilization Window and HPA Tuning

Autoscaling looks simple, but in production it can become unstable if it reacts to every small traffic fluctuation.

This repeated scaling activity is known as **Thrashing** or **Flapping**.

---

## Real-World Example

Imagine the following sequence:

* CPU utilization increases for **10 seconds**.
* HPA immediately scales up the application.
* CPU utilization drops shortly afterward.
* HPA scales the application back down.
* A few seconds later, traffic increases again.
* HPA scales up once more.

This continuous cycle of scaling up and down is called **thrashing (or flapping).**

As a result:

* Pods are constantly created and deleted.
* Cluster resources are wasted.
* Application stability is reduced.

---

## Stabilization Window

To prevent frequent scale-down operations, Kubernetes provides a **Stabilization Window**.

The stabilization window tells HPA to **wait for a specified period before scaling down**, ensuring the traffic decrease is sustained rather than temporary.

---

## Example

A common production configuration is:

* **Scale up immediately** when demand increases.
* **Wait 5 minutes before scaling down**.

This avoids unnecessary scaling caused by short-lived traffic fluctuations.

---

## Why It Is Important

In production environments:

* Traffic naturally fluctuates.
* Short traffic spikes are common.
* Immediate scale-down may remove pods that are needed again within seconds.

A stabilization window provides smoother and more stable autoscaling behavior.

---

# HPA Behavior YAML (Stabilization Window)

```yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: production-hpa
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: my-app

  minReplicas: 2
  maxReplicas: 10

  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 70

  behavior:
    scaleUp:
      stabilizationWindowSeconds: 0

    scaleDown:
      stabilizationWindowSeconds: 300
```

---

## Interview Points

* **CPU-based autoscaling** is preferred for most production workloads because CPU utilization closely follows workload changes.
* **Memory-based autoscaling** should be used carefully since memory often remains high even after traffic decreases.
* **Custom metrics** allow applications to scale based on business-specific metrics such as queue length, Kafka lag, or requests per second.
* Custom metrics require **Prometheus**, **Prometheus Adapter**, and the appropriate metrics pipeline.
* **Thrashing (Flapping)** occurs when HPA repeatedly scales up and down due to temporary metric fluctuations.
* A **Stabilization Window** delays scale-down operations, making autoscaling more stable and efficient in production.
# Vertical Pod Autoscaler (VPA)

Horizontal scaling means **adding more pods**.

Vertical scaling means **making the existing pods bigger** by increasing their **CPU and memory resources**.

Instead of creating additional pods, **Vertical Pod Autoscaler (VPA)** increases the resources allocated to the existing pods.

---

## Real-World Example

Imagine your application is running with:

* CPU Request: **200m**
* Memory Request: **256Mi**

After monitoring the application in production, you notice:

* Continuous CPU throttling
* Out Of Memory (OOM) errors
* Performance degradation

Instead of increasing the number of pods, VPA increases the CPU and memory allocated to each pod, allowing the application to handle the workload more efficiently.

---

## How VPA Works

VPA continuously monitors the application's actual resource consumption.

Based on historical CPU and memory usage, it recommends better resource values.

In **Auto mode**, VPA automatically updates the pod resources by recreating the pods with the new CPU and memory requests.

---

## Important Point

Container CPU and memory resources **cannot usually be resized while the container is running**.

Therefore, when VPA applies new resource values, it **restarts (recreates) the pods** with the updated configuration.

---

# Vertical Pod Autoscaler YAML

```yaml
apiVersion: autoscaling.k8s.io/v1
kind: VerticalPodAutoscaler
metadata:
  name: my-app-vpa
spec:
  targetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: my-app

  updatePolicy:
    updateMode: Auto
```

---

# HPA and VPA Interaction

Can we use **HPA** and **VPA** together?

**Yes, but carefully.**

Using both without proper planning can create resource conflicts.

---

## Why Conflicts Occur

HPA makes scaling decisions based on **CPU or memory utilization percentage**.

VPA changes the **CPU and memory Requests** of the pods.

Since HPA calculates utilization using the CPU Request value, changing that value affects HPA's calculations.

This can create unstable scaling behavior.

---

## Example

Imagine:

* VPA increases the CPU Request.
* CPU utilization percentage suddenly decreases because the request value is now larger.
* HPA assumes the application is under less load and scales down the pods.
* Traffic increases again.
* CPU utilization rises.
* HPA scales the pods back up.

This continuous scaling creates an unstable loop, also known as **scaling oscillation**.

---

## Safe Production Pattern

The recommended production approach is:

* **HPA controls the number of pod replicas.**
* **VPA controls resource recommendations** or **memory only**, depending on the use case.

The most common production pattern is:

* HPA → CPU-based autoscaling
* VPA → **Recommendation Mode**

In Recommendation Mode:

* VPA only suggests better CPU and memory values.
* It does not restart pods automatically.
* Teams review the recommendations and update resource requests during planned deployments.

This approach is widely used in production environments.

---

# VPA Recommendation Mode YAML

```yaml
apiVersion: autoscaling.k8s.io/v1
kind: VerticalPodAutoscaler
metadata:
  name: my-app-vpa
spec:
  targetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: my-app

  updatePolicy:
    updateMode: "Off"
```

---

# Cluster Autoscaler and HPA Coordination

Many beginners think HPA alone is enough for autoscaling.

However, HPA can only create **more pods**.

If the Kubernetes cluster has no available resources, those new pods cannot run.

This is where **Cluster Autoscaler (CA)** comes into the picture.

---

## Real-World Example

Imagine:

* HPA wants to increase the application from **2 pods to 10 pods**.
* All worker nodes are already fully utilized.
* Kubernetes creates the new pod objects.
* The scheduler cannot place them on any node.
* The pods remain in the **Pending** state.

Cluster Autoscaler detects these unschedulable pods.

It automatically adds new worker nodes to the cluster.

Once the new nodes become available, the scheduler places the pending pods onto those nodes, and the application continues serving traffic.

---

## Workflow

1. Traffic increases.
2. HPA creates additional pods.
3. Scheduler tries to schedule the new pods.
4. No node has enough resources.
5. Pods remain in **Pending** state.
6. Cluster Autoscaler detects unschedulable pods.
7. New worker nodes are created.
8. Pending pods are scheduled on the new nodes.

This is how **cloud-native autoscaling** works in Kubernetes.

---

## Important Difference

* **HPA scales Pods (Application Layer).**
* **Cluster Autoscaler scales Nodes (Infrastructure Layer).**

Both work together to handle increasing workloads efficiently.

---

# Scale Target Reference

HPA must know **which workload it should scale**.

This is defined using **scaleTargetRef**.

Without a **scaleTargetRef**, HPA has no idea which Kubernetes resource it should increase or decrease.

---

## Supported Workloads

`scaleTargetRef` can point to:

* Deployment
* StatefulSet
* ReplicaSet
* Any Kubernetes workload that supports the Scale subresource

When HPA detects increased load, it updates the **replica count** of the workload specified in `scaleTargetRef`.

---

# Example: scaleTargetRef

```yaml
scaleTargetRef:
  apiVersion: apps/v1
  kind: Deployment
  name: my-app
```

This tells HPA to monitor and scale the **my-app Deployment** by modifying its replica count.

---

## Interview Points

* **HPA (Horizontal Pod Autoscaler)** increases or decreases the **number of pods**.
* **VPA (Vertical Pod Autoscaler)** increases the **CPU and memory resources** of existing pods.
* VPA generally **restarts pods** when applying new resource values because container resources cannot usually be resized dynamically.
* Running HPA and VPA together requires careful planning to avoid scaling conflicts.
* The recommended production pattern is **HPA for replica scaling** and **VPA in Recommendation Mode**.
* **Cluster Autoscaler** adds or removes worker nodes based on pending pods and cluster resource availability.
* **HPA scales applications**, while **Cluster Autoscaler scales infrastructure**.
* **scaleTargetRef** tells HPA exactly which Kubernetes workload (Deployment, StatefulSet, ReplicaSet, etc.) it should scale.
# Role-Based Access Control (RBAC)

Imagine a developer accidentally deletes a production namespace.

Or a compromised pod reads all the Kubernetes Secrets and gains access to the entire cluster.

These incidents often happen because **proper permissions were not configured**.

This is exactly why Kubernetes provides **RBAC (Role-Based Access Control)**.

RBAC controls **who can perform what action on which Kubernetes resource**.

---

## What is RBAC?

**RBAC** stands for **Role-Based Access Control**.

It answers one simple question:

> **Who is allowed to do what on which resource?**

In Kubernetes, almost everything is performed through an **API call**.

Examples:

* Creating a Pod → API call
* Reading a Secret → API call
* Updating a Deployment → API call
* Deleting a Namespace → API call

Before any request reaches the Kubernetes API Server, RBAC checks whether the request is allowed.

If permission exists, the request is allowed.

Otherwise, Kubernetes rejects the request.

---

## Three Things RBAC Checks

RBAC evaluates every request based on three things:

### 1. Who is making the request?

The identity can be:

* Human User
* Service Account
* Group

---

### 2. What action is being performed?

This is called the **Verb**.

Common verbs include:

* get
* list
* watch
* create
* update
* patch
* delete

---

### 3. Which resource is being accessed?

Examples include:

* Pods
* Secrets
* Deployments
* ConfigMaps
* Namespaces
* Services

Only if all these conditions match an RBAC rule is the request allowed.

---

## Important Point

RBAC is **not optional**.

It is one of the most important security mechanisms in Kubernetes.

Without RBAC, any authenticated user or application could potentially modify or delete critical cluster resources.

---

# Role vs ClusterRole

Kubernetes provides two types of roles:

* **Role**
* **ClusterRole**

Although they look similar, they serve different purposes.

---

## Role

A **Role** is **namespace-scoped**.

It grants permissions **only within a specific namespace**.

For example:

* Read Pods in the **production** namespace.
* Cannot access resources outside that namespace.

Use a Role when access should be limited to a single namespace.

---

### Role YAML

```yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
  namespace: production
  name: pod-reader

rules:
- apiGroups: [""]
  resources: ["pods"]
  verbs: ["get", "list", "watch"]
```

**What this does:**

* Applies only inside the **production** namespace.
* Allows reading Pods.
* Cannot access Pods in any other namespace.

---

## ClusterRole

A **ClusterRole** is **cluster-wide**.

It can grant permissions across all namespaces.

Use a ClusterRole when permissions are required throughout the cluster.

---

### ClusterRole YAML

```yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRole
metadata:
  name: secret-reader

rules:
- apiGroups: [""]
  resources: ["secrets"]
  verbs: ["get", "list"]
```

**What this does:**

* Applies across the entire Kubernetes cluster.
* Allows reading Secrets in every namespace.
* No namespace needs to be specified.

---

## Important Difference

* **Role** → Namespace-specific permissions.
* **ClusterRole** → Cluster-wide permissions.

---

# RoleBinding vs ClusterRoleBinding

A Role or ClusterRole **does not grant permissions by itself**.

It only defines a set of rules.

To actually assign those permissions, Kubernetes uses **Bindings**.

---

## RoleBinding

A **RoleBinding** assigns a **Role** (or a ClusterRole) to a user, group, or service account **within a specific namespace**.

---

### RoleBinding YAML

```yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: RoleBinding
metadata:
  namespace: production
  name: read-pods

subjects:
- kind: User
  name: john

roleRef:
  kind: Role
  name: pod-reader
  apiGroup: rbac.authorization.k8s.io
```

**What this does:**

* Gives user **John** the **pod-reader Role**.
* Access is limited to the **production** namespace.
* John cannot read Pods in other namespaces.

---

## ClusterRoleBinding

A **ClusterRoleBinding** assigns a **ClusterRole** across the entire cluster.

---

### ClusterRoleBinding YAML

```yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRoleBinding
metadata:
  name: secret-reader-binding

subjects:
- kind: User
  name: sarah

roleRef:
  kind: ClusterRole
  name: secret-reader
  apiGroup: rbac.authorization.k8s.io
```

**What this does:**

* Gives user **Sarah** the **secret-reader ClusterRole**.
* Sarah can read Secrets in **every namespace**.

---

## Golden Rule

* **Role + RoleBinding** → Namespace-level access.
* **ClusterRole + ClusterRoleBinding** → Cluster-wide access.
* **ClusterRole + RoleBinding** → Uses ClusterRole permissions, but only within a specific namespace.

The third combination is very common in production because it allows reusable ClusterRoles while still restricting access to a namespace.

---

# Service Accounts

Human users authenticate using user credentials.

Applications running inside Pods need their own identity.

That identity is called a **Service Account**.

Whenever a Pod needs to communicate with the Kubernetes API Server, it uses a Service Account.

Think of it like this:

* A developer logs in using a user account.
* A Pod authenticates using a Service Account.

---

### Service Account YAML

```yaml
apiVersion: v1
kind: ServiceAccount
metadata:
  name: my-app-service
```

---

### Pod Using a Service Account

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: my-app

spec:
  serviceAccountName: my-app-service

  containers:
  - name: app
    image: nginx
```

**What this does:**

* The Pod runs with the identity of **my-app-service**.
* Any API request made by the Pod is authenticated as this Service Account.

---

## Granting Permissions to a Service Account

Just like users, Service Accounts require RBAC permissions.

You create a Role or ClusterRole and bind it to the Service Account.

---

### RoleBinding for Service Account

```yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: RoleBinding
metadata:
  namespace: production
  name: app-reader

subjects:
- kind: ServiceAccount
  name: my-app-service
  namespace: production

roleRef:
  kind: Role
  name: pod-reader
  apiGroup: rbac.authorization.k8s.io
```

**What this does:**

* Grants **my-app-service** permission to read Pods in the **production** namespace.

This is a very common production pattern.

Applications such as:

* Prometheus
* CI/CD tools
* Operators
* Monitoring agents

all use Service Accounts to communicate with the Kubernetes API.

---

# Default Service Account

Every namespace automatically contains a Service Account called **default**.

If you create a Pod without specifying a Service Account, Kubernetes automatically assigns the **default Service Account**.

---

### Example

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: nginx

spec:
  containers:
  - name: nginx
    image: nginx
```

Even though no Service Account is specified, this Pod runs using the **default Service Account**.

---

## Security Concern

By default, the default Service Account usually has **very limited permissions**.

However, in older clusters or poorly configured environments, it may have excessive privileges.

If an attacker compromises a Pod, they may use the Service Account token to access the Kubernetes API.

The token is automatically mounted inside the Pod.

Typical location:

```text
/var/run/secrets/kubernetes.io/serviceaccount/
```

---

## Best Practice

If a Pod **does not need Kubernetes API access**, disable automatic Service Account token mounting.

This reduces the attack surface.

---

### Disable Automatic Token Mounting

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: secure-app

spec:
  automountServiceAccountToken: false

  containers:
  - name: app
    image: nginx
```

**What this does:**

* Kubernetes does **not** mount the Service Account token inside the Pod.
* Even if the Pod is compromised, there is no API token available for an attacker to use.
* This significantly improves the security of the workload.

---

## Interview Points

* RBAC controls **who can perform what action on which Kubernetes resource**.
* RBAC evaluates **Who (User/Group/Service Account)**, **What (Verb)**, and **Which Resource**.
* **Role** provides namespace-level permissions.
* **ClusterRole** provides cluster-wide permissions.
* **RoleBinding** grants permissions within a namespace.
* **ClusterRoleBinding** grants permissions across the cluster.
* **ClusterRole + RoleBinding** is commonly used to reuse ClusterRoles while restricting access to a namespace.
* **Service Accounts** provide identities for Pods to access the Kubernetes API.
* Every namespace automatically has a **default Service Account**.
* If a Pod does not require API access, set **`automountServiceAccountToken: false`** to improve security.
