**Stateless Application:** A stateless application **doesn't store important data inside the pod**. If the pod restarts or is replaced, nothing important is lost. Data is stored externally, such as in a database or cache. Examples are **web servers, REST APIs, and frontend applications**. Kubernetes can freely create, delete, and replace these pods because all pods are **identical and interchangeable**. That's why **Deployment** is ideal for stateless applications.

**Stateful Application:** A stateful application **stores important data and maintains identity or role**. Each instance may have its own data and position in the cluster. **Databases** like MySQL are common examples. If a pod is recreated with a different identity or loses its associated storage, the application can face data or cluster-related issues.

The main problem is that Kubernetes normally treats pods as **disposable and interchangeable**. Deployment works well for stateless applications, but stateful applications need **stable identity, predictable names, and persistent storage**. That's where **StatefulSet** comes in.

**Deployment with MySQL:** Suppose we run MySQL using a Deployment with 3 replicas. Kubernetes creates three pods with auto-generated names. If one pod fails, Kubernetes creates a replacement pod with a **different name**. From Kubernetes' perspective, everything is fine because the desired replica count is maintained.

But from MySQL's perspective, this can be a problem because each instance may have **specific data, identity, and role**. The replacement pod is not necessarily the same MySQL instance.

Storage is another issue. With stateful workloads, each instance needs consistent access to its **own persistent storage**. StatefulSet provides mechanisms to maintain the relationship between the **pod identity and its storage**.

**Quick revision:**

```text
Stateless → Pods are interchangeable → Deployment → External Storage
```

```text
Stateful → Stable Identity + Stable Storage → StatefulSet → Databases
```

**Core difference:**
**Deployment treats pods as disposable replicas.**
**StatefulSet gives pods stable identity and persistent storage.**
Yes. Here is the **complete StatefulSet YAML** for a MySQL stateful application, including stable identity and persistent storage:

```yaml
apiVersion: apps/v1
kind: StatefulSet
metadata:
  name: mysql
spec:
  serviceName: mysql
  replicas: 3

  selector:
    matchLabels:
      app: mysql

  template:
    metadata:
      labels:
        app: mysql

    spec:
      containers:
        - name: mysql
          image: mysql:8.0

          ports:
            - containerPort: 3306

          env:
            - name: MYSQL_ROOT_PASSWORD
              value: "password"

          volumeMounts:
            - name: mysql-data
              mountPath: /var/lib/mysql

  volumeClaimTemplates:
    - metadata:
        name: mysql-data
      spec:
        accessModes:
          - ReadWriteOnce
        resources:
          requests:
            storage: 10Gi
```

### Horizontal Flow

```text
StatefulSet → Stable Pod Identity → Stable Storage → Pod Restart → Same Identity + Same Storage
```

For example:

```text
mysql-0 → mysql-data-mysql-0
mysql-1 → mysql-data-mysql-1
mysql-2 → mysql-data-mysql-2
```

So if `mysql-1` is recreated:

```text
mysql-1 deleted → mysql-1 recreated → Same PVC → Same Data
```
Absolutely. Here is the **same explanation in your revision format**, followed by a visual diagram.

**Pod Identity in StatefulSet:** A StatefulSet provides each pod with a **stable and predictable identity**. To make this identity discoverable through DNS, we commonly use a **Headless Service**.

The Headless Service is created by setting `clusterIP: None`. This tells Kubernetes **not to assign one virtual ClusterIP** to the Service. Instead, Kubernetes creates DNS records that allow clients to resolve **individual pods**.

Suppose our StatefulSet has three replicas:

```text
myapp-0
myapp-1
myapp-2
```

These pod names are predictable and remain the same even if a pod is deleted and recreated.

Once the Headless Service `myapp-headless` is created, each pod gets a predictable DNS name:

```text
myapp-0.myapp-headless
myapp-1.myapp-headless
myapp-2.myapp-headless
```

So another pod can directly communicate with a **specific StatefulSet pod** using its DNS name instead of depending on a random pod IP.

For example, if `myapp-1` crashes:

```text
myapp-1 deleted → myapp-1 recreated → Same hostname → Same DNS identity
```

This is very useful for **databases and clustered applications**, where instances may need to reliably find one another. For example, a primary database can have a predictable identity, and replicas can consistently connect to it.

The important point is that **Deployment does not provide this stable pod identity**. Deployment pods have generated names and can be replaced with different identities. StatefulSet combined with a Headless Service provides **predictable pod names, hostnames, and DNS records**.

### Diagram

```text
                    StatefulSet
                         │
              ┌──────────┼──────────┐
              ↓          ↓          ↓
           myapp-0    myapp-1    myapp-2
              │          │          │
              └──────────┼──────────┘
                         ↓
              Headless Service
             myapp-headless
              clusterIP: None
                         │
          ┌──────────────┼──────────────┐
          ↓              ↓              ↓
myapp-0.myapp-headless  myapp-1.myapp-headless  myapp-2.myapp-headless
```

**Quick revision flow:**

```text
StatefulSet → Stable Pod Name → Headless Service → Stable DNS → Predictable Pod Identity
```

**Core point:**
**StatefulSet gives stable identity; Headless Service makes that identity discoverable through DNS.**
### Headless Service YAML

```yaml id="x4k7pn"
apiVersion: v1
kind: Service
metadata:
  name: myapp-headless
spec:
  clusterIP: None
  selector:
    app: myapp
  ports:
    - port: 3306
      targetPort: 3306
```

### Pod Identity

With a StatefulSet having 3 replicas:

```text id="f7m3qa"
StatefulSet → myapp-0 → myapp-0.myapp-headless
            → myapp-1 → myapp-1.myapp-headless
            → myapp-2 → myapp-2.myapp-headless
```

If `myapp-1` restarts:

```text id="r2d8vk"
myapp-1 deleted → myapp-1 recreated → Same Hostname → Same DNS Name
```

**Key point:** `clusterIP: None` makes the Service **headless**, so Kubernetes doesn't provide one virtual ClusterIP. Instead, DNS can resolve **individual StatefulSet pods**, giving each pod a predictable network identity.
### Stable Storage

StatefulSet uses **`volumeClaimTemplates`** to automatically create **one PersistentVolumeClaim (PVC) for each pod**.

For example, if we have 3 replicas, Kubernetes creates 3 pods and 3 PVCs:

```text
StatefulSet
    ↓
3 Pods + 3 PVCs
    ↓
mysql-0 → mysql-data-mysql-0
mysql-1 → mysql-data-mysql-1
mysql-2 → mysql-data-mysql-2
```

Each pod gets its **own dedicated storage**. The storage is associated with that pod's stable identity.

If `mysql-1` crashes or the node goes down:

```text
mysql-1 crashes → mysql-1 recreated → Same PVC attached → Data preserved
```

So `mysql-1` comes back with the same identity and gets its existing `mysql-data-mysql-1` PVC.

### Complete StatefulSet YAML

```yaml
apiVersion: apps/v1
kind: StatefulSet
metadata:
  name: mysql

spec:
  serviceName: mysql-headless
  replicas: 3

  selector:
    matchLabels:
      app: mysql

  template:
    metadata:
      labels:
        app: mysql

    spec:
      containers:
        - name: mysql
          image: mysql:8.0

          ports:
            - containerPort: 3306

          volumeMounts:
            - name: mysql-data
              mountPath: /var/lib/mysql

  volumeClaimTemplates:
    - metadata:
        name: mysql-data

      spec:
        accessModes:
          - ReadWriteOnce

        resources:
          requests:
            storage: 10Gi
```

### What Happens in This YAML

`serviceName` points to the **Headless Service**, which provides stable DNS for the StatefulSet pods.

```text
StatefulSet → Headless Service → Stable DNS
```

`replicas: 3` means Kubernetes maintains three pods:

```text
mysql-0
mysql-1
mysql-2
```

With the default `OrderedReady` pod management policy, StatefulSet creates them in order:

```text
mysql-0 → Ready → mysql-1 → Ready → mysql-2 → Ready
```

The `volumeMounts` section mounts the storage inside the MySQL container:

```text
mysql-data → /var/lib/mysql
```

The `volumeClaimTemplates` tells Kubernetes to automatically create a **separate PVC for every pod**:

```text
mysql-0 → mysql-data-mysql-0
mysql-1 → mysql-data-mysql-1
mysql-2 → mysql-data-mysql-2
```

So the three important StatefulSet features work together:

```text
Stable Pod Identity → Stable DNS → Stable Per-Pod Storage
       ↓                   ↓                ↓
    mysql-0          mysql-0.headless    PVC-0
    mysql-1          mysql-1.headless    PVC-1
    mysql-2          mysql-2.headless    PVC-2
```

### Scaling Up

If we scale from 3 to 5 replicas:

```text
mysql-0 → mysql-1 → mysql-2 → mysql-3 → mysql-4
                                      ↓
                                  New PVC
```

Kubernetes creates `mysql-3` first, waits for it to become ready, and then creates `mysql-4`. Each new pod gets its own PVC automatically.

### Scaling Down

If we scale from 5 back to 3:

```text
mysql-4 → Deleted
mysql-3 → Deleted
mysql-2 → Kept
mysql-1 → Kept
mysql-0 → Kept
```

The **PVCs are not automatically deleted**, helping protect the application's data.

### Rolling Update

If we change:

```yaml
image: mysql:8.0
```

to:

```yaml
image: mysql:8.5
```

the StatefulSet performs a controlled rolling update. With the default `RollingUpdate` strategy, StatefulSet updates pods from the **highest ordinal toward the lowest**, waiting for each updated pod to become ready before continuing:

```text
mysql-2 → Updated → Ready
                    ↓
mysql-1 → Updated → Ready
                    ↓
mysql-0 → Updated → Ready
```

**Quick revision flow:**

```text
StatefulSet → Stable Identity → Stable DNS → Stable Storage → Ordered Scaling → Controlled Rolling Update
```
**Node Labels:** Node labels are **metadata attached to nodes**. They describe what a node represents or what type of workload it is intended for. For example, we can label a node as a **database node** or assign it to a specific **availability zone**.

Labels themselves **do not affect scheduling**. Kubernetes only uses them when a pod explicitly references them through mechanisms such as **nodeSelector, nodeAffinity, or topology rules**.

### Node Label YAML

```yaml
metadata:
  labels:
    workload-type: database
    topology: zone-a
```

```text
Node → Labels Added → Labels Describe Node → Pod Uses Label → Scheduling Decision
```

---

**nodeSelector:** It is the **simplest way to control pod placement**. The pod says, "Schedule me only on a node with this exact label." If no matching node exists, the pod remains **Pending**.

### nodeSelector YAML

```yaml
spec:
  nodeSelector:
    workload-type: database
```

```text
Pod → nodeSelector → Exact Label Match → Matching Node → Pod Scheduled
                                      → No Match → Pod Pending
```

**nodeAffinity:** NodeAffinity is a more **advanced and flexible** version of node selection. It supports more complex rules and allows us to define both **hard requirements** and **soft preferences**.

### nodeAffinity YAML

```yaml
spec:
  affinity:
    nodeAffinity:
      requiredDuringSchedulingIgnoredDuringExecution:
        nodeSelectorTerms:
        - matchExpressions:
          - key: workload-type
            operator: In
            values:
            - database
```

```text
Pod → Node Affinity → Evaluate Rules → Rule Satisfied → Schedule
                                   → Rule Not Satisfied → Pending
```

---

**Required vs Preferred:**

**Required** means a **hard constraint**. The condition must be satisfied. If no node matches, the pod remains **Pending**.

### Required YAML

```yaml
requiredDuringSchedulingIgnoredDuringExecution:
  nodeSelectorTerms:
  - matchExpressions:
    - key: workload-type
      operator: In
      values:
      - database
```

```text
Pod → Required Rule → Must Match → Yes → Schedule
                                  → No → Pending
```

**Preferred** means a **soft constraint**. Kubernetes tries to follow the preference, but if no matching node is available, it can schedule the pod on another suitable node.

### Preferred YAML

```yaml
preferredDuringSchedulingIgnoredDuringExecution:
- weight: 80
  preference:
    matchExpressions:
    - key: workload-type
      operator: In
      values:
      - database
```

`weight` determines **how strongly Kubernetes prefers that condition**. A higher weight gives that preference more importance.

```text
Pod → Preferred Rule → Try Database Node → Available → Schedule There
                                      → Not Available → Schedule Elsewhere
```

### Quick Revision

```text
Node Label → Describes Node
nodeSelector → Simple Exact Match
nodeAffinity → Advanced Node Selection
Required → Must Match
Preferred → Try to Match
```
**Taint:** A taint is applied at the **node level**. It tells Kubernetes, **“Don't schedule pods on this node unless they explicitly tolerate this taint.”** Taints are useful for protecting nodes reserved for **database workloads, critical components, or special hardware**.

### Taint Command

```bash
kubectl taint nodes node1 workload-type=database:NoSchedule
```

* `workload-type=database` → taint key and value
* `NoSchedule` → prevents new pods from being scheduled unless they have a matching toleration

```text
Node → Taint Applied → Pod Without Toleration → Blocked
                                      ↓
                           Pod With Toleration → Allowed
```

---

**Toleration:** A toleration is defined at the **pod level**. It tells Kubernetes, **“This pod is allowed to run on a node having this taint.”**

Important point: **Toleration does not force the pod onto that node.** It only removes the taint restriction and allows the scheduler to consider that node.

### Toleration YAML

```yaml
spec:
  tolerations:
  - key: "workload-type"
    operator: "Equal"
    value: "database"
    effect: "NoSchedule"
```

```text
Taint on Node → Blocks Pod
       ↓
Toleration on Pod → Removes Restriction
       ↓
Scheduler Considers Node
       ↓
Other Scheduling Rules
       ↓
Pod Scheduled
```

### Quick Revision

```text
Taint → Node-side restriction
Toleration → Pod-side permission
Taint + No Toleration → Pod blocked
Taint + Matching Toleration → Pod allowed
```

**Key difference:** **Toleration allows placement; it does not guarantee placement.**
**Taint Effects:** Kubernetes has three main taint effects. They control **new pod scheduling** and, in the case of `NoExecute`, also affect **existing pods**.

### 1. NoSchedule

This is a **hard restriction**. New pods cannot be scheduled on the tainted node unless they have a matching toleration.

```yaml
spec:
  taints:
  - key: workload-type
    value: database
    effect: NoSchedule
```

```text
Node Taint → NoSchedule → New Pod → No Toleration → ❌ Blocked
                                      ↓
                               Toleration → ✅ Allowed
```

---

### 2. PreferNoSchedule

This is a **soft restriction**. Kubernetes tries to avoid scheduling pods on the node, but if there is no better option, it can still schedule them.

```yaml
spec:
  taints:
  - key: workload-type
    value: database
    effect: PreferNoSchedule
```

```text
Node Taint → PreferNoSchedule → Try Other Nodes → Available → Schedule Elsewhere
                                      ↓
                                No Better Option → Schedule Here
```

---

### 3. NoExecute

This is the **strongest restriction**. It affects both **new and existing pods**. Pods without a matching toleration can be evicted from the node.

```yaml
spec:
  taints:
  - key: workload-type
    value: database
    effect: NoExecute
```

```text
Node Taint → NoExecute → New Pod Without Toleration → ❌ Not Scheduled
                     → Existing Pod Without Toleration → ❌ Evicted
                     → Pod With Toleration → ✅ Can Stay
```

**Quick revision:**

```text
NoSchedule → Blocks new pods
PreferNoSchedule → Avoids new pods
NoExecute → Blocks new + Evicts existing pods
```

---

**Pod Anti-Affinity:** Anti-affinity answers a different question: **“Which pods should not run together?”**

For example, if we have multiple replicas of a web application, we don't want all replicas on the same node. If that node fails, all replicas could go down. Pod anti-affinity helps **spread replicas across different nodes**.

### Pod Anti-Affinity YAML

```yaml
affinity:
  podAntiAffinity:
    requiredDuringSchedulingIgnoredDuringExecution:
    - labelSelector:
        matchExpressions:
        - key: app
          operator: In
          values:
          - web
      topologyKey: kubernetes.io/hostname
```

```text
Web Pod 1 → Node 1
Web Pod 2 → Node 2
Web Pod 3 → Node 3
```

`topologyKey: kubernetes.io/hostname` means the rule is applied at the **node level**, so matching pods should not be placed on the same node.

---

**Zonal Pod Spread:** Anti-affinity can spread pods across nodes, but production clusters can have multiple **Availability Zones**. If all replicas are concentrated in one zone and that zone fails, the application can still be unavailable.

Pod topology spread constraints help distribute replicas **across zones**.

### Zonal Pod Spread YAML

```yaml
topologySpreadConstraints:
- maxSkew: 1
  topologyKey: topology.kubernetes.io/zone
  whenUnsatisfiable: DoNotSchedule
  labelSelector:
    matchLabels:
      app: web
```

* `maxSkew: 1` → Difference between zones should not be more than **1 pod**.
* `topologyKey` → Distribute based on **availability zone**.
* `DoNotSchedule` → Don't schedule if the required balance cannot be maintained.

```text
Zone A → 2 Web Pods
Zone B → 2 Web Pods
Zone C → 1 Web Pod
          ↓
      maxSkew = 1
```

**Quick revision:**

```text
Anti-Affinity → Spread pods across different nodes
Topology Spread → Spread pods across different zones
```
**DaemonSet:** A DaemonSet is a Kubernetes controller that ensures **one pod runs on every eligible node** in the cluster. Unlike a Deployment, where we specify the number of replicas, a DaemonSet automatically maintains one pod per matching node.

If a **new node joins**, Kubernetes automatically creates the DaemonSet pod on that node. If a **node is removed**, the pod on that node is also removed.

Common use cases are **log collectors, monitoring agents, security agents, network plugins, and node-level agents**.

```text id="8j8q2w"
Node Added → DaemonSet Detects Node → Creates Pod
Node Removed → DaemonSet Detects Node → Removes Pod
```

### DaemonSet YAML

```yaml id="j3n5hf"
apiVersion: apps/v1
kind: DaemonSet
metadata:
  name: log-collector
spec:
  selector:
    matchLabels:
      app: log-collector
  template:
    metadata:
      labels:
        app: log-collector
    spec:
      containers:
      - name: log-collector
        image: fluentd:latest
```

**Important:** There is **no `replicas` field** in a DaemonSet. Kubernetes automatically determines the number of pods based on the eligible nodes.

```text id="lq5l2k"
DaemonSet → Eligible Nodes → One Pod Per Node
```

---

### DaemonSet + Node Selector

Sometimes we don't want the DaemonSet on every node. We can use **nodeSelector** to restrict it to specific nodes.

```yaml id="g1av7f"
spec:
  template:
    spec:
      nodeSelector:
        hardware: gpu
```

Only nodes with `hardware=gpu` will get the DaemonSet pod.

```text id="0q4k9r"
DaemonSet → Check Node Label → hardware=gpu → Pod Created
                                → No Match → Node Skipped
```

---

### DaemonSet + Taints/Tolerations

Taints can prevent pods from running on certain nodes. A DaemonSet can use **tolerations** to allow its pods to run on tainted nodes.

```yaml id="6f2q4x"
spec:
  template:
    spec:
      tolerations:
      - key: node-role.kubernetes.io/control-plane
        operator: Exists
        effect: NoSchedule
```

This allows the DaemonSet pod to run on **control-plane nodes** that have the corresponding taint.

```text id="j1h3w9"
Tainted Node → Regular Pod → ❌ Blocked
                    ↓
              DaemonSet Pod
                    ↓
             Matching Toleration
                    ↓
                  ✅ Allowed
```

### Quick Revision

```text id="7s9c4e"
DaemonSet → One Pod Per Eligible Node
Deployment → Specified Number of Replicas
NodeSelector → Controls Which Nodes
Toleration → Allows DaemonSet on Tainted Nodes
```
