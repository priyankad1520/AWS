## ReplicaSet

- ReplicaSet = Controller that maintains the desired number of Pods.
- Purpose = High availability by ensuring required Pods are always running.
- If Pod crashes → Creates a new Pod.
- If extra Pods exist → Removes extra Pods.
- Main job = Maintain desired replica count.

## Deployment and ReplicaSet

- Deployment does not manage Pods directly.
- Deployment → Manages ReplicaSet.
- ReplicaSet → Manages Pods.
- Creating a Deployment → Kubernetes automatically creates a ReplicaSet.
- Updating a Deployment → Creates a new ReplicaSet with updated Pod template.
- Old ReplicaSet → Gradually scaled down.
- Supports = Rolling Update, Rollback, Version History.
- Remember: Deployment manages ReplicaSets, ReplicaSet manages Pods.

## Deployment YAML Quick Revision
```yaml
apiVersion: apps/v1              # API group and version for Deployment
kind: Deployment                 # Creates a Deployment object

metadata:
  name: my-app-deployment        # Name of the Deployment

spec:
  replicas: 3                    # Maintains 3 running Pods

  selector:
    matchLabels:
      app: my-app                # Selects Pods with this label

  template:                      # Pod template (blueprint)
    metadata:
      labels:
        app: my-app              # Must match selector.matchLabels

    spec:                        # Pod specification
      containers:
      - name: my-app             # Container name
        image: my-java-app:1.0   # Docker image to run
        ports:
        - containerPort: 8080    # Application listens on port 8080
```
## What Happens After `kubectl apply`

- Deployment created → ReplicaSet created automatically.
- ReplicaSet → Creates required Pods.
- Pods run application.
- If a Pod fails → ReplicaSet creates a replacement.
- If Deployment is updated → New ReplicaSet created → Old ReplicaSet scaled down gradually.

## Interview One-Liner

- Deployment → Manages ReplicaSets.
- ReplicaSet → Maintains desired number of Pods.
- Pods → Run the application.

# Rolling Update
- Rolling Update = Updates application gradually without downtime.
- Deployment update → Creates a new ReplicaSet.
- New Pods are created first → Old Pods are terminated gradually.
- Application remains available during the update.
- Supports = Zero downtime deployment.

## Rolling Update YAML Quick Revision

```yaml
spec:
  strategy:
    type: RollingUpdate             # Update Pods gradually

    rollingUpdate:
      maxUnavailable: 1             # Maximum 1 Pod can be unavailable
      maxSurge: 1                   # Maximum 1 extra Pod can be created temporarily
```

**Example (replicas = 3):**
- Initial → 3 Old Pods
- Step 1 → Create 1 New Pod = 4 Pods (3 Old + 1 New)
- Step 2 → Delete 1 Old Pod = 3 Pods (2 Old + 1 New)
- Step 3 → Repeat until all Old Pods are replaced.
- Result → 3 New Pods running (Zero Downtime)

# Rollback
- Rollback = Restores the previous stable version if the new deployment fails.
- Every Deployment update → Creates a new ReplicaSet.
- Deployment history is maintained automatically.
- If new version fails → Roll back to previous ReplicaSet.

### Rollback Command

```bash
# If **v2.0** fails →
kubectl rollout undo deployment my-app-deployment
```
Result → Kubernetes automatically restores **my-java-app:1.0**.

→ Restores the previous Deployment revision.
```yaml
# Example
image: my-java-app:1.0     # Old Image
image: my-java-app:2.0     # Updated Image
```

## Flow
- Deployment Updated → New ReplicaSet Created → New Pods Started → Old Pods Removed
- If Success → New ReplicaSet becomes active.
- If Failure → `kubectl rollout undo` → Previous ReplicaSet restored automatically.

## Interview One-Liner

**Rolling Update** → Gradually replaces old Pods with new Pods to achieve **zero downtime**.

**Rollback** → Restores the previous stable ReplicaSet if the new deployment fails.

# Revision History
- Revision History = Kubernetes stores every Deployment update as a new revision.
- Every Deployment update → New ReplicaSet + New Revision.
- Used for = Rollback to previous stable version.
- Kubernetes automatically keeps old ReplicaSets.

## Revision History Commands

```bash id="g6i8ra"
kubectl rollout history deployment my-app-deployment
# Shows all Deployment revisions

kubectl rollout history deployment my-app-deployment --revision=2
# Shows details of Revision 2
```

```bash
# Example
# Revision 1 → `image: my-java-app:1.0` and Revision 2 → `image: my-java-app:2.0`
# If Revision 2 fails
kubectl rollout undo deployment my-app-deployment     # Restores Revision 1 automatically.
```

## Flow

Deployment Updated → New Revision Created → Old ReplicaSet Saved → View History → Rollback if required.

# Pause & Resume Rollout
- Pause Rollout = Temporarily stops the rolling update.
- Resume Rollout = Continues the paused rolling update.
- Used for = Verify Pods, Logs, Metrics before completing deployment.

```bash id="e1tazt"
kubectl rollout pause deployment my-app-deployment
# Pauses the ongoing rollout

kubectl rollout resume deployment my-app-deployment
# Resumes the paused rollout
```

## Flow

Update Deployment → Rolling Update Starts → Pause Rollout → Verify Pods/Logs/Metrics → Resume Rollout → Deployment Completes.

## Interview One-Liner

**Revision History** → Stores every Deployment update as a revision, making rollback possible.

**Pause Rollout** → Temporarily stops a rolling update for verification.

**Resume Rollout** → Continues the rollout from where it was paused.

# Blue-Green Deployment
- Blue-Green Deployment = Two identical environments where only one serves traffic at a time.
- **Blue** = Current stable version (Live).
- **Green** = New version (Ready for testing).
- Service controls which environment receives traffic.
- If Green is successful → Switch traffic to Green.
- If Green fails → Switch traffic back to Blue instantly.
- Purpose = Zero downtime + Fast rollback.
```yaml
apiVersion: apps/v1
kind: Deployment

metadata:
  name: my-app-green             # New Deployment

spec:
  replicas: 3

  selector:
    matchLabels:
      app: my-app
      version: green/blue

  template:
    metadata:
      labels:
        app: my-app
        version: green/blue

    spec:
      containers:
      - name: my-app
        image: my-java-app:2.0   # New version/old 
```
```yaml id="slm6m8"
# Service (Initially Points to Blue)
apiVersion: v1
kind: Service

metadata:
  name: my-app-service

spec:
  selector:
    app: my-app
    version: blue                # Traffic goes to Blue
---
# Switch Traffic to Green
spec:
  selector:
    app: my-app
    version: green               # Traffic now goes to Green
```

→ Only the Service selector changes. No need to recreate Pods.

## Flow
- Blue (Live) → Deploy Green → Test Green → Change Service Selector → Traffic moves to Green.
- If Green fails → Change Service Selector back to Blue → Traffic immediately returns to Blue.

## Interview One-Liner

**Blue-Green Deployment** → Two identical environments (Blue & Green). Only one receives traffic. Traffic is switched by updating the **Service selector**, providing **zero downtime** and **instant rollback**.
# Blue-Green Deployment

**Definition**

* Two identical environments: **Blue (Current)** and **Green (New)**.
* Only **one environment receives traffic** at a time.
* Traffic switching is done by changing the **Service selector**.
* Purpose = **Zero downtime + Instant rollback**.

## Blue Deployment

```yaml id="q6fx1v"
metadata:
  name: my-app-blue

labels:
  app: my-app
  version: blue

image: my-java-app:1.0
```

## Green Deployment

```yaml id="5ljlwm"
metadata:
  name: my-app-green

labels:
  app: my-app
  version: green

image: my-java-app:2.0
```

## Service Switch

```yaml id="r6wq7m"
selector:
  app: my-app
  version: blue        # Current traffic
```

```yaml id="evj6ca"
selector:
  app: my-app
  version: green       # Switch traffic to Green
```

### Flow

* Blue (Live)
* Deploy Green
* Test Green
* Change Service selector → Traffic moves to Green
* If Green fails → Point Service back to Blue

**Interview One-Liner**
Blue-Green Deployment = Two identical environments. Traffic is switched by changing the **Service selector**, enabling **zero downtime** and **instant rollback**.

---

# Canary Deployment

**Definition**

* Gradually releases the new version to a **small percentage of users**.
* Old and New versions run **side by side**.
* Traffic split is controlled by **Replica count** (basic Kubernetes) or **Service Mesh/Ingress** (advanced).
* Purpose = **Reduce deployment risk**.

## Blue (Stable)

```yaml id="mffrkx"
metadata:
  name: my-app-blue

spec:
  replicas: 4          # Stable version

labels:
  app: my-app
  version: blue

image: my-java-app:1.0
```

## Canary (New)

```yaml id="bh8hy7"
metadata:
  name: my-app-canary

spec:
  replicas: 1          # New version

labels:
  app: my-app
  version: canary

image: my-java-app:2.0
```

## Service

```yaml id="0lbd1s"
selector:
  app: my-app          # Selects both Blue and Canary Pods
```

### Traffic Split Example

* Blue = 4 Pods
* Canary = 1 Pod
* Total = 5 Pods
* Traffic ≈ **80% Blue + 20% Canary**

If Canary is successful:

* Increase Canary replicas.
* Decrease Blue replicas.
* Eventually Canary handles **100% traffic**.
* Delete Blue deployment.

If Canary fails:

* Delete Canary Pods.
* Blue continues serving **100% traffic**.

### Flow

* Deploy Blue (Stable)
* Deploy Canary (Few Pods)
* Monitor Logs, Metrics & Errors
* Scale Canary Up
* Scale Blue Down
* Canary becomes Stable
* Remove Blue

**Interview One-Liner**
Canary Deployment = Releases the new version to a **small percentage of users first**, monitors it, and gradually shifts all traffic if everything is stable.
# Image Updates

**Definition**

* Image update = Deploy a new container image version.
* Triggers a **Rolling Update** automatically.
* Kubernetes creates a **new ReplicaSet**.

## Method 1: Update via YAML

```yaml
containers:
- name: my-app
  image: my-java-app:3.0    # Updated image version
```

```bash
kubectl apply -f myapp-deployment.yaml
# Applies the updated Deployment
```

## Method 2: Update via CLI

```bash
kubectl set image deployment/myapp-deployment my-app=my-java-app:3.0
# Updates container image without editing YAML
```

**Command Breakdown**

* `deployment/myapp-deployment` → Deployment name.
* `my-app` → Container name.
* `my-java-app:3.0` → New image.

## Verification

```bash
kubectl rollout status deployment/myapp-deployment
# Checks rollout status
```

```bash
kubectl describe deployment myapp-deployment | grep Image
# Verifies running image
```

## Flow

* Update Image (YAML / CLI)
* New ReplicaSet Created
* New Pods Started
* Traffic Gradually Shifts
* Old Pods Removed

**Interview One-Liner**
Image update triggers a **Rolling Update**, where Kubernetes creates a **new ReplicaSet** and gradually replaces old Pods.

---

# Scaling Deployment

**Definition**

* Scaling = Increase or decrease the number of Pods.
* Scale Up → Handle more traffic.
* Scale Down → Save resources.
* ReplicaSet maintains the desired number of Pods.

## Method 1: Scale via YAML

```yaml
spec:
  replicas: 5      # Maintain 5 Pods
```

```bash
kubectl apply -f myapp-deployment.yaml
# Applies the new replica count
```

## Method 2: Scale via CLI

```bash
kubectl scale deployment myapp-deployment --replicas=5
# Scales Deployment to 5 Pods
```

## Verification

```bash
kubectl get pods
# Verify the number of running Pods
```

## Flow

* Set Replica Count
* Kubernetes Creates/Deletes Pods
* ReplicaSet Maintains Desired Count

**Interview One-Liner**
Scaling changes the number of running Pods, and the **ReplicaSet** ensures the requested replica count is always maintained.

---

# When to Use Which Deployment Strategy?

| Strategy           | Best Used When                     | Rollback | Resources |
| ------------------ | ---------------------------------- | -------- | --------- |
| **Rolling Update** | Regular releases, stable changes   | Moderate | Low       |
| **Canary**         | Risky changes, test with few users | Easy     | Medium    |
| **Blue-Green**     | Instant switching & rollback       | Instant  | High      |

## Rolling Update

* Default Kubernetes strategy.
* Gradually replaces old Pods.
* Best for regular feature releases.
* Simple and resource-efficient.

## Canary Deployment

* Releases to a small percentage of users first.
* Monitor Logs, Metrics, Errors.
* Gradually increase traffic.
* Best for risky or critical releases.

## Blue-Green Deployment

* Two identical environments (Blue & Green).
* Switch traffic instantly using the Service selector.
* Best when instant rollback is required.
* Requires double infrastructure.

## Zero Downtime

* **Rolling Update** → ✅ Zero Downtime (Gradual Pod replacement)
* **Canary** → ✅ Zero Downtime (Both versions run together)
* **Blue-Green** → ✅ Zero Downtime (Instant traffic switch)

## Interview One-Liner

* **Rolling Update** → Simple, gradual deployments.
* **Canary** → Test new version with a small group of users before full rollout.
* **Blue-Green** → Instant traffic switching and fastest rollback, but requires more resources.
