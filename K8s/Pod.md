### Kubernetes

* **Kubernetes** → open-source tool used to manage containerized applications.
* Automates deploying, scaling, and restarting containers.
* Needed in modern infrastructure to manage a large number of Docker containers efficiently.
* Ensures high availability, better resource utilization, smooth updates.
* Ideal for cloud environments.

### Containers vs Virtual Machines

* **Containers** → lightweight, portable units that package application, code, libraries, and dependencies.
* Share the host OS kernel, faster and more efficient.
* **Virtual Machines** → include a complete operating system and virtual hardware.
* Heavier, consume more resources, slower to start.
* **In short** → Containers share the host OS and are lightweight, Virtual Machines run separate OS instances and are heavier.
* Containers are preferred for faster development, testing, and deployment.

### Benefits of Kubernetes in Production

* Keeps applications highly available by restarting failed containers.
* Auto-scales based on traffic.
* Performs zero-downtime updates using rolling deployments.
* Self-heals by replacing unhealthy containers.
* Manages resources efficiently, reducing cloud cost.
### Docker vs Kubernetes

* **Docker** → used to create and run containers, packages application with its dependencies.
* **Kubernetes** → used to orchestrate and manage containers across multiple machines.
* **In simple terms** → Docker creates and runs containers, Kubernetes manages and scales containers in production.
* Docker builds the container, Kubernetes deploys and manages it.

### Main Components of Kubernetes Architecture

* **Two main parts** → Control Plane, Worker Nodes.
* **Control Plane** → manages the cluster, includes API Server, Scheduler, Controller Manager, etcd.
* **Worker Node** → runs the actual application, includes Kubelet, Kube-proxy, Container Runtime.
* Together, they keep the application running, healthy, and scalable.

### Pod

* **Pod** → smallest unit in Kubernetes.
* Like a wrapper around one or more containers that work together closely.
* Containers inside a pod share the same network namespace (IP, ports).
* Can communicate through localhost.
* Can share storage volumes.

### Kubernetes Cluster

* **Kubernetes Cluster** → group of machines that work together to run containerized applications.
* **Two main parts** → Control Plane, Worker Nodes.
* **Control Plane** → brain of the cluster, scheduling applications, monitoring health, handling updates.
* **Worker Nodes** → run the applications inside pods.
* Control Plane tells Worker Nodes what to do, Worker Nodes report back the status.
* Together, they keep the application running, scaled, and healthy.

### Deployment

* **Deployment** → controller that manages the application's lifecycle.
* Defines the desired state, like how many pods should run.
* Performs rolling updates without downtime by updating pods one by one.
* Allows rollback if something goes wrong.
* Makes it easy to update, scale, and maintain the application reliably.

### Kubernetes Scheduler

* **Scheduler** → assigns newly created pods to the best-fit worker node.
* Checks CPU, Memory, Node availability, Taints, Tolerations, Affinity rules.
* Picks the most suitable node and schedules the pod.
* Ensures efficient resource utilization and application performance.

### Labels and Selectors

* **Labels** → key-value pairs attached to objects like Pods and Deployments.
* Used to organize, group, and filter resources.
* **Selectors** → used to query or match labels.
* Example: Service uses a selector to route traffic to Pods with a specific label.
* Together, Labels and Selectors make it easy to manage and target specific resources in a large cluster.

### ConfigMaps and Secrets

* **ConfigMaps and Secrets** → manage configuration data separately from application code.
* **ConfigMap** → stores non-sensitive data like application settings, URLs, environment variables.
* **Secret** → stores sensitive data like passwords, tokens, keys in Base64 encoded form.
* Both can be injected into Pods as environment variables or mounted as files.
* Keeps applications flexible, secure, and easy to update without rebuilding images.

### ReplicaSet

* **ReplicaSet** → ensures a specific number of Pod replicas are always running.
* If a Pod crashes or is deleted, ReplicaSet automatically creates a new Pod.
* Ensures high availability and reliability.
* Usually managed by a **Deployment**, which provides version control and rolling updates.

### Namespaces

* **Namespaces** → virtual clusters within a physical Kubernetes cluster.
* Used to isolate resources like Pods, Services, and ConfigMaps.
* Example: Run **Dev**, **Test**, and **Production** in the same cluster using separate namespaces.
* Keeps resources organized, secure, and easy to manage.
* Useful for large teams and multi-tenant environments.

### Taints and Tolerations

* **Taints** → applied to nodes to prevent Pods from being scheduled.
* A tainted node says, **don't schedule Pods unless they tolerate this taint**.
* **Tolerations** → added to Pods to allow them to run on tainted nodes.
* Used for dedicated nodes like GPU workloads or high-security applications.
### Persistent Volumes (PV) and Persistent Volume Claims (PVC)

* **Persistent Volume (PV)** → storage resource in the cluster, created by an admin or dynamically provisioned.
* **Persistent Volume Claim (PVC)** → request for storage by a Pod, specifying size and access mode.
* Pods use **PVC** to access **PV**.
* Data remains safe even if the Pod is deleted or rescheduled.
* Storage is managed independently of the Pod lifecycle.

### Rolling Updates and Rollbacks

* **Deployment** handles rolling updates.
* Updates Pods gradually, one by one, without downtime.
* Keeps the application running during updates.
* If something goes wrong, roll back to the previous stable version using a single command.
* Ensures zero downtime, controlled rollout, and safe recovery.

---

### Ingress

* **Ingress** exposes Services outside the cluster using HTTP or HTTPS.
* Acts like a smart router.
* Routes traffic based on URL path or hostname.
* Supports SSL termination.
* Provides load balancing.
* Allows multiple Services to use a single external IP.
* Ideal for web applications and APIs.

### Autoscaling

* **Autoscaling** automatically adjusts the number of Pods based on workload.
* **Horizontal Pod Autoscaler (HPA)** scales Pods up and down based on CPU, memory, or custom metrics.
* Ensures better performance during high traffic.
* Saves cost during low traffic.
* Eliminates manual scaling.
* Kubernetes continuously monitors metrics and adjusts Pod count.

### Stateful vs Stateless Applications

* **Stateless Applications** → do not store data between sessions, every Pod is identical and replaceable.
* Managed using **Deployment**.
* Easy to scale and perform rolling updates.
* **Stateful Applications** → retain data and require stable identities.
* Managed using **StatefulSet**.
* Provides persistent storage, stable Pod names, ordered deployment, predictable network identity.
* **Examples** → Deployment: Web servers, StatefulSet: MySQL, Kafka, Redis.

## Job

* **Job** → used to run a task **only once** or until it completes successfully.
* Creates one or more Pods to complete the task.
* If a Pod fails, Kubernetes creates another Pod until the Job succeeds.
* Commonly used for database migration, backup, batch processing, or one-time scripts.
* After completion, the Job stops automatically.

## CronJob

* **CronJob** → used to run Jobs on a schedule.
* Works like the Linux **cron** scheduler.
* Creates a new Job automatically at the specified time.
* Used for scheduled backups, report generation, log cleanup, health checks.
* Runs repeatedly based on the cron schedule.

## DaemonSet

* **DaemonSet** → ensures one Pod runs on every worker node in the cluster.
* When a new node joins, Kubernetes automatically creates the Pod on that node.
* When a node is removed, the Pod is also removed.
* Commonly used for log collection, monitoring agents, security agents, and networking components.
* **Examples** → Fluentd, Prometheus Node Exporter, Datadog Agent, AWS VPC CNI.

## Kubernetes

* **Kubernetes** → platform for automating deployment, scaling, and management of containerized applications.
* Manages multiple containers across many machines.
* Ensures applications run smoothly.

## Kubernetes Architecture

* **Two main parts** → Control Plane (Master Node), Worker Node.

### Control Plane (Master Node)

* **Control Plane** → brain of Kubernetes, makes all important decisions.
* **API Server** → control centre, receives and processes all requests, gateway to the cluster.
* **Scheduler** → decides which worker node should run the Pod based on available resources.
* **Controller Manager** → keeps the cluster in the desired state, restarts or replaces failed Pods.
* **etcd** → highly reliable key-value database, stores cluster state and configuration.

### Worker Node

* **Worker Node** → runs the actual applications inside containers.
* **Kubelet** → agent on each worker node, ensures Pods are running and healthy, communicates with the API Server.
* **Container Runtime** → pulls container images and runs containers inside Pods.
* **Kube-proxy** → manages networking rules and load balances traffic across Pods.

## Pod

* **Pod** → smallest deployable unit in Kubernetes.
* Holds one or more containers.
* Containers share the same network and storage.
* Pods are where containers actually run.

## Kubernetes Workflow

1. User sends a deployment request using **kubectl** or a **YAML** file.
2. **API Server** receives and processes the request.
3. **Scheduler** selects the best worker node.
4. **Kubelet** starts the container inside a Pod.
5. **Kube-proxy** manages networking and routes traffic.
6. **Controller Manager** continuously monitors the cluster and fixes issues if needed.

# Kubernetes Analogy (Easy to Remember)

### Control Plane = Head Office

* **API Server** → Project Coordinator, receives every request and sends it to the right team.
* **Scheduler** → Task Assigner, assigns work to the best branch office.
* **Controller Manager** → Operations Supervisor, monitors work and fixes failures.
* **etcd** → Company Database, stores all project and system information.

### Worker Node = Branch Office

* Runs the actual application.

* **Kubelet** → Team Lead, receives instructions from the API Server and ensures work is completed.

* **Container Runtime** → Developer's computer/toolkit, runs the application.

* **Pod** → Workstation where one or more developers (containers) work together.

### Summary

* **Control Plane (Head Office)** → plans, manages, monitors.
* **Worker Nodes (Branch Offices)** → execute the work.
* **Pods (Workstations)** → where containers actually run.
## Kubernetes Architecture – Top 15 Interview Notes

### 1. What happens when you run `kubectl apply -f <file>.yaml`?

* Request goes to the **API Server**.
* API Server stores the desired state in **etcd**.
* **Scheduler** selects the best worker node.
* **Kubelet** pulls the image and starts the container inside a Pod.

### 2. What if the Scheduler is down?

* New Pods cannot be scheduled.
* Existing Pods continue running.
* New deployments and autoscaling won't work.

### 3. What happens if etcd crashes?

* Kubernetes cannot read or write cluster state.
* Control Plane becomes unstable.
* Cluster won't function properly until etcd is restored.

### 4. Can a Pod be scheduled without Kubelet?

* **No.**
* Kubelet runs and manages Pods on the node.
* If Kubelet is down, the Pod won't start even if Scheduler assigns it.

### 5. Role of Kube-proxy

* Handles network traffic between Pods and Services.
* Configures IP rules.
* Performs load balancing to the correct Pod.

### 6. How does API Server authenticate requests?

* **Authentication** → Who are you?
* **Authorization** → What can you do?
* **Admission Controllers** → Validate the request before accepting it.

### 7. How do Control Plane and Worker Nodes communicate?

* Use **TLS certificates**.
* Communication happens through the **API Server endpoint**.
* Kubelet securely communicates with the API Server.

---

### 8. Can one node run both Control Plane and Worker components?

* **Yes**, in Minikube or development environments.
* **Production** → keep them separate for better performance and security.

---

### 9. What happens if a Worker Node goes down?

* Controller Manager detects the failure.
* Node becomes **NotReady**.
* Pods are rescheduled to healthy nodes if possible.

### 10. What stores the Kubernetes cluster state?

* **etcd**.
* Distributed key-value database.
* Stores complete cluster configuration and state.

### 11. What happens during a Rolling Update?

* Deployment gradually replaces old Pods with new Pods.
* Ensures zero downtime.
* Scheduler places new Pods.
* Kubelet starts them.

### 12. How does Scheduler choose a node?

* Checks CPU and Memory availability.
* Checks Taints and Tolerations.
* Checks Affinity and Anti-affinity rules.
* Selects the best-fit worker node.

### 13. Why is API Server the single source of truth?

* All Kubernetes components communicate through the API Server.
* Reads and writes cluster state to **etcd**.
* No operation happens without the API Server.

### 14. Can Kubelet restart a crashed container?

* **Yes.**
* Kubelet monitors container health.
* Restarts the container based on the Pod's **Restart Policy**.

### 15. What happens if you manually delete a Pod?

* **ReplicaSet** detects the missing Pod.
* Creates a new Pod automatically.
* Maintains the desired number of replicas.
These are the notes in the same style as your previous ones—short, interview-friendly, without adding extra information.

---

# Pod

* **Pod** → smallest and most basic deployable unit in Kubernetes.
* Represents one or more containers.
* Containers share the same network namespace, storage volumes, and lifecycle.
* Think of a Pod as a wrapper around the application's containers.

# Pod Lifecycle

### Pending

* Pod definition accepted, scheduling in progress.
* Kubernetes has received the Pod specification but has not scheduled or started it.
* Possible reasons → insufficient node resources, image pulling, PVC provisioning, YAML misconfiguration.

### Running

* Pod scheduled, containers are running.
* Suitable worker node assigned.
* Containers initialized and executing.
* Can check logs, port-forward, debug, and perform load testing.

### Succeeded

* Container completed successfully.
* Used mainly for Jobs and CronJobs.
* Examples → backup scripts, report generation, data migration.

### Failed

* Container terminated with an error.
* Possible reasons → application error, configuration issue, port conflict, failed Init Container.
* Troubleshooting → `kubectl logs`, `kubectl describe pod`.

### Unknown

* Node unreachable or state not reported.
* Control Plane cannot communicate with the Worker Node.
* Usually caused by network issues or node failure.

# Init Container

* **Init Container** → helper container that runs before the main application container.
* Runs only once.
* Used for setup tasks before the application starts.

# Why Init Container?

* Download configuration files.
* Wait for another service to become ready.
* Perform database migration.
* Execute setup tasks before starting the application.
* Keeps the main application container clean and lightweight.

# Init Container Workflow

* Kubernetes runs Init Containers one by one.
* Starts the first Init Container.
* Waits until it completes successfully.
* Starts the next Init Container.
* After all Init Containers finish, the main application container starts.
* Init Containers never run at the same time as the main container.

# Real-Time Example

* Java application depends on MySQL.
* Init Container waits until MySQL is reachable on port **3306**.
* After the database is ready, Kubernetes starts the main application container.
* Prevents the application from failing because the database is not yet available.

# Important Points

* If an **Init Container fails**, the main application container will not start.
* Kubernetes keeps retrying the Init Container until it succeeds or the issue is fixed.
## Multi-Container Pod

* **Multi-Container Pod** → single Kubernetes Pod running two or more containers.
* Containers share the same network, storage volumes, and lifecycle.
* Containers work together as one unit.
* Each container has a specific responsibility.
* Used to separate responsibilities into smaller, reusable parts.

## Sidecar Pattern

* One container runs the main application.
* Another container runs alongside it to assist.
* Shares the same network and storage.
* Runs as long as the main application is running.
* **Examples** → log collection, monitoring, backup, configuration sync.

## Ambassador Pattern

* Helper container acts as a proxy between the application and external services.
* Main application communicates with **localhost**.
* Ambassador handles communication with external services.
* Can manage security, failover, connection management, or request routing.
* Keeps the application simple by hiding external communication details.

# Basic Pod YAML Structure

**apiVersion:** Specifies the Kubernetes API version.

**kind:** Defines the Kubernetes object type, such as **Pod** or **Deployment**.

**metadata:** Stores identifying information.

**name:** Unique name of the Pod within the namespace.

**labels:** Key-value pairs used for grouping and selecting resources.

**spec:** Defines the desired state and configuration of the Pod.

**containers:** List of containers running inside the Pod.

**name:** Name of the container.

**image:** Docker image used by the container.

**ports:** Container ports to expose.

**env:** Environment variables for the container.

**volumeMounts:** Mount points for shared storage.

**resources:** CPU and memory requests and limits.

**initContainers (Optional)**: Helper containers that run before the main container starts.

**volumes *(Optional)**: Shared storage accessible by all containers in the Pod.

**restartPolicy:**

* Defines what happens when a container exits.

* **Always** *(Default)* → restarts the container every time it exits.

* **OnFailure** → restarts only if the container exits with a non-zero exit code.

* **Never** → never restarts the container.

## Pod Networking in Kubernetes

### Pod-to-Pod Communication

* Pods communicate directly using their IP addresses.
* No special configuration required.
* Default Kubernetes behaviour.
* **CoreDNS** resolves DNS names.

### Pod-to-Service Communication

* **Service** provides a stable endpoint for Pods.
* Pods communicate with the **Service**, not directly with Pod IPs.
* Service forwards traffic to the appropriate Pod.

### Pod-to-External Communication

* Pods can access external websites and APIs by default.
* Access can be restricted using **Network Policies**.

### CNI (Container Network Interface)

* **CNI** sets up Pod networking.
* Assigns Pod IP addresses.
* Configures routing.
* Enforces network policies.

# Pod Affinity

* **Pod Affinity** → schedules Pods on the same node as specific Pods.
* Used when Pods should stay together.
* Example → Logging Agent and Backend Pod on the same node.
* Uses **requiredDuringSchedulingIgnoredDuringExecution**.
* Scheduler places the Pod only where the matching Pod already exists.
* **Label Selector** identifies matching Pods.
* **Topology Key** decides the scheduling level, usually the node.

# Pod Anti-Affinity

* **Pod Anti-Affinity** → prevents Pods from running on the same node.
* Used to improve high availability.
* Example → Backend replicas distributed across different nodes.
* Uses **requiredDuringSchedulingIgnoredDuringExecution**.
* Scheduler avoids placing Pods on nodes with matching Pods.
* **Label Selector** identifies matching Pods.
* **Topology Key** ensures Pods are spread across different nodes.

# Real-Time Pod YAML Scenario

### Requirement

* Deploy a Java Order Service.
* Wait for MySQL before starting.
* Write logs to a shared volume.
* Stream logs using a Sidecar Container.
* Restart automatically on failure.
* Prefer running on the same node as **app=payment-service**.
* Debug using standard **kubectl** commands.

## Step 1 – Basic Pod Structure

* Define **apiVersion**, **kind**, **metadata**, **labels**, and **spec**.
* Foundation for adding containers, volumes, and affinity rules.

## Step 2 – Init Container

* Create **wait-for-db** Init Container.
* Uses **BusyBox** image.
* Continuously checks MySQL on port **3306**.
* Starts the main application only after the database is available.

## Step 3 – Shared Volume

* Create **log-volume** using **emptyDir**.
* Shared storage for log files between containers.

## Step 4 – Main Application Container

* Java application container.
* Runs on **port 8080**.
* Writes logs to **app.log**.
* Mounts the shared log volume.

## Step 5 – Sidecar Container

* Log forwarder using **BusyBox**.
* Continuously tails **app.log**.
* Streams logs to **stdout**.
* Uses the same shared log volume.

## Step 6 – Restart Policy

* **restartPolicy: Always**
* Automatically restarts containers if they crash.

## Step 7 – Pod Affinity

* Uses **preferredDuringSchedulingIgnoredDuringExecution**.
* Prefers scheduling on the same node as **app=payment-service**.
* **Topology Key** applies the preference at the node level.
* Improves performance and shared resource access.
