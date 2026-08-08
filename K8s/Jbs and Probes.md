# Jobs in Kubernetes

- What if you want a task to **run once, complete, and then stop**?
- For example: Take a database backup. Migrate data from one database to another. Generate a report. Clean up old files.
- A Deployment is **not suitable** for these tasks because Deployments are designed to keep Pods running continuously.
- This is where **Jobs** are used.

## What is a Job?

- A **Job** is a Kubernetes controller that runs a Pod **until the task is completed successfully**.
- Unlike a Deployment, which keeps Pods running forever, a Job is designed for tasks that: Start, Complete their work, Exit successfully
- Once the task finishes successfully, the Job marks it as **Completed**.

## How a Job Works

By default, Kubernetes Pods created by a Deployment run continuously. However, sometimes you need a Pod to perform a one-time task and then stop.
A Job guarantees that the task completes successfully.
* If the Pod fails, the Job automatically creates a new Pod and retries the task.
* If the Pod succeeds, the Job records the completion and stops creating new Pods.

## Real-World Use Cases. Jobs are commonly used for:

* Database backups
* Data migration
* Batch processing
* Report generation
* One-time cleanup tasks
* Data transformation
* Running scripts
* Sending one-time notifications
# Job YAML Structure

A Job contains a **Pod Template**, just like a Deployment. However, there are some important differences.

## Important Fields: restartPolicy: Never
```yaml
restartPolicy: Never
```

* This tells Kubernetes: If the application inside the Pod fails, **the Pod itself is not restarted**.
* Instead, the **Job controller creates a new Pod**.

The Job manages retries—not the Pod.
### backoffLimit

```yaml
backoffLimit: 3 #This specifies how many times Kubernetes should retry a failed Job.
```
For example: Retry 1, Retry 2, Retry 3: If all retries fail, the Job is marked as **Failed**.

### ttlSecondsAfterFinished

```yaml
ttlSecondsAfterFinished: 3600 # This automatically deletes the completed Job after **3600 seconds (1 hour)**.
```
It helps keep the cluster clean by removing old Job objects.
# Example Job YAML

```yaml
apiVersion: batch/v1
kind: Job
metadata:
  name: database-backup
spec:
  backoffLimit: 3
  ttlSecondsAfterFinished: 3600

  template:
    spec:
      restartPolicy: Never

      containers:
      - name: backup
        image: busybox
        command: ["sh", "-c", "echo Backup completed"]
```
# Job Completions and Parallelism

By default: One Pod runs.The Job completes when that Pod finishes successfully. Sometimes, however, multiple Pods are required to complete a task.

Kubernetes provides two fields for this: **completions, parallelism**
## completions

```yaml
completions: 5  # The Job is considered successful only after **5 Pods complete successfully**.
```

## parallelism

```yaml
parallelism: 2   # This controls **how many Pods run at the same time**.
```
## Example

Suppose:

```yaml
completions: 5
parallelism: 2
```

Kubernetes runs:

* Pod 1 and Pod 2 together
* After one finishes, Pod 3 starts
* Then Pod 4
* Finally Pod 5

Only **2 Pods** run simultaneously until all **5 completions** are finished.
## Real-World Use Case

This is commonly used for:

* Batch processing
* Image processing
* Video encoding
* Processing large datasets
* Parallel data transformation

It improves performance while preventing the cluster from being overloaded.
# Example YAML

```yaml
apiVersion: batch/v1
kind: Job
metadata:
  name: batch-processing
spec:
  completions: 5
  parallelism: 2

  template:
    spec:
      restartPolicy: Never

      containers:
      - name: worker
        image: busybox
        command: ["sh", "-c", "echo Processing..."]
```
# CronJob

- What if you want a task to run **automatically on a schedule**?
- For example: Every day at **2 AM**, Every Monday morning, Every hour, Every month
- Instead of manually creating Jobs every time, Kubernetes provides **CronJobs**.

## What is a CronJob?

- A **CronJob** is a Kubernetes controller that creates a **Job automatically based on a schedule**.
- It uses standard **Cron syntax** to define when the Job should run.
- CronJobs are the Kubernetes equivalent of **Unix cron jobs**.

## Real-World Use Cases

CronJobs are commonly used for:

* Daily database backups
* Weekly reports
* Hourly cleanup jobs
* Log rotation
* Cache cleanup
* Sending scheduled emails
* Running health checks

# CronJob YAML Structure

The schedule determines when the Job will run.

```yaml
schedule: "0 2 * * *"  # Run the Job **every day at 2:00 AM**.
```
### successfulJobsHistoryLimit

```yaml
successfulJobsHistoryLimit: 3  # Keep the last **3 successful Job records**.
```
### failedJobsHistoryLimit

```yaml
failedJobsHistoryLimit: 1    # Keep the last **1 failed Job record**.
```
## Example CronJob YAML

```yaml
apiVersion: batch/v1
kind: CronJob
metadata:
  name: daily-backup

spec:
  schedule: "0 2 * * *"

  successfulJobsHistoryLimit: 3
  failedJobsHistoryLimit: 1

  jobTemplate:
    spec:
      template:
        spec:
          restartPolicy: Never

          containers:
          - name: backup
            image: busybox
            command: ["sh", "-c", "echo Daily Backup"]
```
## How CronJob Works

1. CronJob waits for the scheduled time.
2. At the scheduled time, it creates a Job.
3. The Job creates a Pod.
4. The Pod completes its work.
5. The Job finishes.
6. CronJob waits for the next scheduled time and repeats the process.

Each Job created by a CronJob is independent.

# Jobs vs CronJobs

Both Jobs and CronJobs execute tasks, but they are used for different purposes.

| Feature    | Job                           | CronJob                          |
| ---------- | ----------------------------- | -------------------------------- |
| Execution  | Runs once                     | Runs automatically on a schedule |
| Trigger    | Manual or another application | Cron schedule                    |
| Repetition | No                            | Yes                              |
| Purpose    | One-time task                 | Recurring task                   |
| Example    | Data migration                | Daily backup                     |

## When to Use

Use a **Job** when:

* The task needs to run only once.
* The task should complete and stop.
* Examples: Data migration, one-time backup, cleanup script.

Use a **CronJob** when:

* The task must run repeatedly.
* The task follows a schedule.
* Examples: Daily backup, weekly reports, hourly cleanup.

## Interview Points

* A **Job** runs a Pod until the task completes successfully.
* Jobs are used for **one-time or batch processing tasks**.
* If a Job fails, Kubernetes retries it based on the **backoffLimit**.
* **restartPolicy: Never** means the Job controller creates a new Pod instead of restarting the existing one.
* **ttlSecondsAfterFinished** automatically deletes completed Jobs after a specified time.
* **completions** defines how many successful Pod executions are required.
* **parallelism** defines how many Pods can run simultaneously.
* A **CronJob** creates Jobs automatically according to a cron schedule.
* Use **Jobs** for one-time tasks and **CronJobs** for recurring scheduled tasks.
# ActiveDeadlineSeconds (Time Limit for Jobs)

Sometimes a Job may run forever because of an application issue, infinite loop, or unexpected delay.

To prevent a Job from consuming cluster resources indefinitely, Kubernetes provides **activeDeadlineSeconds**.

It sets a **maximum execution time** for the entire Job.

If the Job does not finish within the specified time, Kubernetes terminates it automatically.

---

## How It Works

Suppose:

```yaml
activeDeadlineSeconds: 600
```
This means:
* The Job must complete within **600 seconds (10 minutes)**.
* If the Pod is still running after 10 minutes, Kubernetes terminates it.
* The Job is marked as **Failed**.

This prevents long-running or stuck Jobs from wasting cluster resources.

---

## Real-World Use Cases

* Batch processing
* Database migration
* Report generation
* Data import/export
* Any task that should finish within a fixed time

---

## Example Job YAML

```yaml
apiVersion: batch/v1
kind: Job
metadata:
  name: batch-job

spec:
  activeDeadlineSeconds: 600

  template:
    spec:
      restartPolicy: Never

      containers:
      - name: worker
        image: busybox
        command: ["sh", "-c", "sleep 700"]
```

## Important Point

* **backoffLimit** controls **how many retry attempts** Kubernetes makes.
* **activeDeadlineSeconds** controls **how long the entire Job is allowed to run**.

Both are independent settings.

# Suspend and Resume CronJobs

Sometimes you need to temporarily stop a CronJob without deleting it.

For example:

* Maintenance window
* Application deployment
* Database upgrade
* System maintenance

Instead of deleting the CronJob, Kubernetes allows you to **pause** it using the **suspend** field.
## How Suspend Works

### Active CronJob

```yaml
suspend: false
# CronJob is active. Jobs are created according to the schedule.
```
### Suspended CronJob
```yaml
suspend: true
# CronJob is paused. No new Jobs are created. Existing running Jobs are **not affected**. To resume scheduling, simply change it back to **false**.
```

 
## Example CronJob YAML

```yaml
apiVersion: batch/v1
kind: CronJob
metadata:
  name: daily-backup

spec:
  schedule: "0 2 * * *"
  suspend: true

  jobTemplate:
    spec:
      template:
        spec:
          restartPolicy: Never

          containers:
          - name: backup
            image: busybox
            command: ["sh", "-c", "echo Backup"]
```
## Real-World Use Cases

* Maintenance windows
* Cluster upgrades
* Database migration
* Temporary business shutdowns
* Preventing scheduled tasks during deployments

## Important Point

Suspending a CronJob **does not delete it**.

The CronJob configuration remains intact and can be resumed anytime by setting:

```yaml
suspend: false
```

---

# Job Failure Handling (restartPolicy)

When a Job Pod fails, Kubernetes needs to decide what should happen next.

This behavior is controlled by the **restartPolicy** field.

The two commonly used restart policies are: **Never**,  **OnFailure**

---

## restartPolicy: Never

```yaml
restartPolicy: Never
```

If the Pod fails:

* Kubernetes does **not restart the failed Pod**.
* Instead, the **Job controller creates a brand-new Pod**.
* Retries continue until the **backoffLimit** is reached.

Example:

```yaml
backoffLimit: 3
```

Means:

* Kubernetes creates up to **3 new Pods** before marking the Job as Failed.

This is the **most commonly used restart policy** for Jobs.

---

## restartPolicy: OnFailure

```yaml
restartPolicy: OnFailure
```

If the Pod fails:

* Kubernetes restarts the **container inside the same Pod**.
* A new Pod is **not created immediately**.
* Retries continue until the **backoffLimit** is reached.

Example:

```yaml
backoffLimit: 5   # Kubernetes retries up to **5 times** before the Job fails.
```
This policy is useful when failures are expected to be temporary.

---

## Important Difference

| restartPolicy | What Happens on Failure                |
| ------------- | -------------------------------------- |
| Never         | Creates a new Pod                      |
| OnFailure     | Restarts the container in the same Pod |

---

# CronJob History Limits

- Every time a CronJob runs, Kubernetes creates a new Job.
- Over time, many completed Jobs accumulate.
- Keeping too many old Job records consumes cluster resources.
- Kubernetes provides two fields to automatically clean up old Job history.

## successfulJobsHistoryLimit
```yaml
successfulJobsHistoryLimit: 3
# Keep the **last 3 successful Job records**. Older successful Jobs are deleted automatically.
```

## failedJobsHistoryLimit
```yaml
failedJobsHistoryLimit: 1
# Keep only the **last failed Job record**. Older failed Jobs are deleted automatically.
```

## Example YAML
```yaml
successfulJobsHistoryLimit: 3
failedJobsHistoryLimit: 1
# This keeps the cluster clean while still allowing recent Job history for troubleshooting.
```
# CronJob Concurrency Policy

Sometimes a CronJob is still running when the next scheduled execution time arrives.

The **concurrencyPolicy** field controls what Kubernetes should do in this situation.

There are **three concurrency policies**.
## 1. Allow (Default)
```yaml
concurrencyPolicy: Allow
```
- This allows multiple Job instances to run at the same time.
- If the previous Job is still running and the next schedule arrives: Kubernetes starts another Job. Both Jobs run simultaneously.
- Suitable for: Independent tasks, Parallel processing, Jobs that do not interfere with each other

## 2. Forbid
```yaml
concurrencyPolicy: Forbid
```
- Only one Job is allowed at a time.
- If the previous Job is still running: The next scheduled execution is skipped. No new Job is created.
- Suitable for: Database backup, Shared file processing, Tasks that cannot run concurrently

## 3. Replace
```yaml
concurrencyPolicy: Replace
```
- If a Job is still running: Kubernetes terminates the currently running Job. A new Job starts immediately.
- Suitable for: Monitoring tasks, Cache refresh, Tasks where only the latest execution matters

## Important Difference

| Concurrency Policy | Behavior                                               |
| ------------------ | ------------------------------------------------------ |
| Allow              | Multiple Jobs run simultaneously (Default).            |
| Forbid             | Skip the new Job if the previous one is still running. |
| Replace            | Stop the running Job and start a new one.              |

## Interview Points

* **activeDeadlineSeconds** sets the maximum time a Job is allowed to run.
* If the deadline is exceeded, Kubernetes terminates the Job and marks it as Failed.
* **suspend: true** pauses a CronJob without deleting it.
* **restartPolicy: Never** creates a new Pod when a Job fails.
* **restartPolicy: OnFailure** restarts the failed container inside the same Pod.
* **successfulJobsHistoryLimit** controls how many successful Job records Kubernetes keeps.
* **failedJobsHistoryLimit** controls how many failed Job records are retained.
* **concurrencyPolicy: Allow** permits multiple Jobs to run simultaneously.
* **concurrencyPolicy: Forbid** skips new Jobs while a previous Job is still running.
* **concurrencyPolicy: Replace** terminates the current Job and starts a new one immediately.
---
# Liveness Probe

Jobs and CronJobs are used for one-time and scheduled tasks.

But what about **long-running applications** like web servers, APIs, or microservices?

How does Kubernetes know whether an application is actually healthy or just running?

This is where **Probes** come into the picture.

A **Liveness Probe** checks whether your application is **alive and functioning correctly**.

If the application becomes unhealthy, Kubernetes automatically restarts the container.

---

## Real-World Example

Imagine your application is running, but its **database connection pool is exhausted**.

The container is still running, but it cannot process any user requests.

Without a Liveness Probe:

* Kubernetes thinks the Pod is healthy because the process is still running.
* Users continue sending requests to a broken application.

With a Liveness Probe:

* Kubernetes detects that the health check is failing.
* The container is restarted automatically.
* The application starts fresh and begins serving requests again.

This improves application availability without manual intervention.

---

## Example YAML

```yaml
livenessProbe:
  httpGet:
    path: /health          # Kubernetes checks the /health endpoint
    port: 8080             # Port on which the application is running

  periodSeconds: 10        # Perform the health check every 10 seconds
  failureThreshold: 3      # Restart the container after 3 consecutive failures
```

---

## What This YAML Does

* Every **10 seconds**, Kubernetes sends an HTTP request to the **/health** endpoint.
* If the health check fails **3 consecutive times**, Kubernetes considers the container unhealthy.
* The container is automatically restarted.

---

## Important Point

Use **Liveness Probes carefully**.

If your application:

* Takes a long time to start
* Needs time to initialize
* Experiences temporary slowdowns

then an aggressive Liveness Probe may restart the application unnecessarily, causing a **restart loop (CrashLoopBackOff)**.

In such cases, combine a **Startup Probe** or configure appropriate delays like **initialDelaySeconds**.

---

## Interview Points

* A **Liveness Probe** checks whether the application is **alive**.
* If the health check fails repeatedly, Kubernetes **restarts the container**.
* It helps recover applications that are stuck, deadlocked, or unable to serve requests.
* It is commonly implemented using **HTTP**, **TCP**, or **Exec** probes.
* Incorrect Liveness Probe configuration can lead to unnecessary container restarts.
**Readiness Probe:** It checks whether the **container is ready to receive traffic**. The container may be running, but the application could still be initializing, loading data, or connecting to a database. In that case, the readiness probe fails, and Kubernetes **removes the pod from the Service endpoints**, so traffic is not sent to it. The pod stays running and is **not restarted**. Once the probe succeeds, Kubernetes adds the pod back to traffic. This is very important during deployments because new pods can initialize without receiving traffic, helping achieve **zero-downtime deployments**.

### Readiness Probe

```yaml
readinessProbe:
  httpGet:
    path: /ready
    port: 8080
  periodSeconds: 5
  failureThreshold: 2
```
**Readiness probe:** If `/ready` fails **2 consecutive times**, the pod is removed from traffic but **not restarted**.

**Example:** Kubernetes checks `/ready` every 5 seconds. If it fails twice, the pod becomes **NotReady** and stops receiving traffic. Once it recovers, it is added back automatically.

**Key difference:** Readiness failure means **stop traffic**, not restart the container.

**Startup Probe:** It is used when an application takes a **long time to start**. Without a startup probe, the liveness probe might think the application is unhealthy during startup and restart it continuously. The startup probe tells Kubernetes, **“Give the application time to start.”** Until the startup probe succeeds, Kubernetes doesn't perform liveness or readiness checks. Once it succeeds once, the **liveness and readiness probes take over**. If the startup probe never succeeds within the configured limit, Kubernetes kills and restarts the container.

### Startup Probe

```yaml
startupProbe:
  httpGet:
    path: /health
    port: 8080
  periodSeconds: 5
  failureThreshold: 30
```

**Startup probe:** `5 × 30 = 150 seconds` maximum startup time.
**Example:** If the startup probe runs every 5 seconds with `failureThreshold: 30`, Kubernetes allows up to **150 seconds** for the application to start.

There are **three common types of health probes**:

1. **HTTP Probe** – Kubernetes sends an HTTP request to an endpoint. A response between **200–399** is considered successful. Best for **web applications and REST APIs**.
2. **TCP Probe** – Kubernetes tries to establish a TCP connection to a port. If the connection succeeds, the probe passes. Best for **databases, caches, and services listening on a port**.
3. **Exec Probe** – Kubernetes runs a **command inside the container** and checks the exit code. Best for **custom or complex health checks**.

**Quick revision:**
**Readiness → Can I receive traffic?**
**Liveness → Am I alive or should I restart?**
**Startup → Have I finished starting yet?**
---
### Failure Threshold
The probe must fail **3 consecutive times** before Kubernetes takes action.
```yaml
failureThreshold: 3
```
### Success Threshold
For a **readiness probe**, one successful check is enough to mark the pod as ready again.
```yaml
successThreshold: 1
```
### Initial Delay, Period & Timeout

```yaml
initialDelaySeconds: 30
periodSeconds: 10
timeoutSeconds: 5
```
* `initialDelaySeconds: 30` → Wait **30 seconds** before the first probe.
* `periodSeconds: 10` → Run the probe every **10 seconds**.
* `timeoutSeconds: 5` → If the probe doesn't respond within **5 seconds**, consider it a failure.

```yaml
# Real Example
# Application startup = **30 seconds**
# Health endpoint response = **1 second**

initialDelaySeconds: 35
periodSeconds: 10
timeoutSeconds: 3
# This gives the application enough time to start, checks it regularly, and allows up to **3 seconds** for the health-check response.
```
---
### Post-Start Hook

```yaml
lifecycle:
  postStart:
    exec:
      command: ["/bin/sh", "-c", "echo 'Initializing application'"]
# Runs **immediately after the container starts**. Used for initialization, cache warm-up, or registering with service discovery.
```

### Pre-Stop Hook

```yaml
lifecycle:
  preStop:
    exec:
      command: ["/bin/sh", "-c", "sleep 60"]
# Runs **before the container is terminated**. Used for graceful cleanup, closing connections, or allowing requests to finish.
```



### Graceful Shutdown

```yaml
terminationGracePeriodSeconds: 60

lifecycle:
  preStop:
    exec:
      command: ["/bin/sh", "-c", "sleep 60"]
# 
`terminationGracePeriodSeconds` gives the application time to **shut down gracefully** before Kubernetes forcefully terminates it.
```

**Flow:** Pod Termination → SIGTERM → Pre-Stop Hook → Graceful Shutdown → Grace Period Ends → SIGKILL
