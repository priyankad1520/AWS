## Prometheus

**Definition:** Prometheus is an **open-source monitoring and alerting system** used to **collect and store time-series metrics** from applications, servers, containers, Kubernetes, and infrastructure.

**Main Purpose:** Prometheus is mainly used to **monitor system health and performance, identify problems, and trigger alerts when something goes wrong**.

**What does it collect?** CPU usage, memory usage, request count, error rate, response time, disk usage, network traffic, and application-specific metrics.

**How does it collect metrics?** Prometheus normally follows a **pull model**, where it periodically collects metrics from the target's `/metrics` endpoint.

**Target:** A target is the **application, server, container, or service from which Prometheus collects metrics**.

**Exporter:** An exporter is a **component that exposes metrics in Prometheus format**, for example Node Exporter exposes Linux server metrics.

**Storage:** Prometheus stores the collected metrics as **time-series data**, meaning metric values are stored along with timestamps.

**Query:** Prometheus provides **PromQL**, which is used to query, filter, calculate, and analyze metrics.

**Alerting:** Prometheus uses **alerting rules** to detect conditions such as high CPU, high error rate, or high latency.

**Alertmanager:** Alertmanager receives alerts from Prometheus and **routes notifications** to systems such as Slack, email, PagerDuty, or other notification channels.

**Grafana:** Grafana is commonly connected to Prometheus to **create dashboards and visualize the metrics**.

### Prometheus Flow

`Application/Server/Kubernetes → Metrics/Exporter → Prometheus → Store Metrics → PromQL → Grafana`

### Alert Flow

`Metrics → Prometheus → Alert Rule → Alertmanager → SRE/On-call Engineer`

### Simple Example

`Application → /metrics → Prometheus → CPU/Memory/Request/Error Metrics → Grafana`

`Error Rate > 5% → Prometheus detects → Alertmanager → SRE gets notification`

### Easy Interview Definition

> **Prometheus is an open-source monitoring and alerting system used to collect, store, query, and monitor time-series metrics from applications, servers, containers, Kubernetes, and infrastructure. It normally uses a pull-based model to collect metrics and can work with Grafana for visualization and Alertmanager for alert notifications.**

# PromQL

**Definition:** PromQL is the **query language of Prometheus** used to **retrieve, filter, calculate, and analyze time-series metrics**.

**Main Purpose:** PromQL is mainly used to **understand system performance, create dashboards, create alerting rules, and calculate SLI/SLO metrics**.

**What does it do?** It allows us to query metrics such as **CPU usage, memory usage, request rate, error rate, latency, and availability**.

**Where is it used?** PromQL is commonly used in **Prometheus, Grafana dashboards, recording rules, and alerting rules**.

**How does it work?** `Metric → PromQL Query → Prometheus evaluates the query → Result`

**Simple Example:** `up` → Shows whether the monitored target is **up or down**.

**Filter Example:** `up{job="node"}` → Shows the `up` metric only for targets where the job is `node`.

**Rate Example:** `rate(http_requests_total[5m])` → Calculates the **per-second request rate over the last 5 minutes**.

**Error Example:** `rate(http_requests_total{status="500"}[5m])` → Shows the **rate of HTTP 500 errors over the last 5 minutes**.

**Aggregation:** `sum(rate(http_requests_total[5m]))` → Calculates the **total request rate across matching time series**.

### PromQL Flow

`Application/Server → Metrics → Prometheus → PromQL Query → Result → Grafana/Alert`

### Real SRE Example

`Application → http_requests_total → Prometheus → PromQL → Error Rate → Alert Rule → Alertmanager → SRE`

### Why is PromQL important for SRE?

**Monitoring:** Query current system metrics.

**Troubleshooting:** Identify which service is having a problem.

**Alerting:** Create conditions such as high error rate or high CPU.

**SLO/SLI:** Calculate availability, success rate, latency, and error budget.

### Easy Interview Definition

> **PromQL is Prometheus's query language used to retrieve, filter, aggregate, and analyze time-series metrics. SRE engineers use PromQL to monitor applications and infrastructure, build Grafana dashboards, create alerts, and calculate reliability metrics such as SLIs and SLOs.**

### Easy way to remember

`Prometheus = Collects Metrics`

`PromQL = Queries/Analyzes Metrics`

`Grafana = Visualizes Metrics`

`Alertmanager = Sends/Manages Alerts`
# Alertmanager
**routing alerts to the right team, removing duplicate alerts, grouping related alerts, and silencing unnecessary alerts.**

**Definition:** Alertmanager is a **component of the Prometheus monitoring system** that **receives alerts from Prometheus and manages and sends notifications** to the appropriate teams or people.

**Main Purpose:** Alertmanager is mainly used to **route, group, silence, and manage alerts** so that SRE teams receive useful notifications without unnecessary alert noise.

**What does it do?** It receives alerts from Prometheus, groups related alerts, removes duplicate notifications, routes alerts to the correct team, and sends notifications through channels such as Slack, email, PagerDuty, or other integrations.

**How does it work?** `Prometheus → Alerting Rule → Alert Fires → Alertmanager → Group/Filter/Route → Notification`

**Alerting Rule:** Prometheus checks a condition, such as `CPU > 80% for 5 minutes`, and creates an alert.

**Grouping:** Alertmanager can combine multiple related alerts into a single notification, so engineers don't receive hundreds of separate messages for the same incident.

**Routing:** Alertmanager sends different alerts to different teams, for example `Database Alert → DBA Team` and `Kubernetes Alert → Platform/SRE Team`.

**Deduplication:** Alertmanager avoids sending repeated notifications for the same alert.

**Silencing:** An SRE can temporarily silence alerts during planned maintenance or a known incident.

**Inhibition:** Alertmanager can suppress less-important alerts when a more important root-cause alert is already active.

### Alertmanager Flow

`Application/Server → Metrics → Prometheus → Alert Rule → Alertmanager → Slack/Email/PagerDuty → SRE`

### Simple Example

`CPU > 80% for 5 minutes → Prometheus creates HighCPU alert → Alertmanager receives it → Routes it to SRE team → Slack/PagerDuty notification`

### Why do we use Alertmanager?

**Without Alertmanager:** `Prometheus → Many Alerts → Alert Noise → SRE`

**With Alertmanager:** `Prometheus → Alertmanager → Group + Deduplicate + Route → Useful Notification`

### Easy Interview Definition

> **Alertmanager is a component of Prometheus used to manage and route alerts. It receives alerts generated by Prometheus and handles grouping, deduplication, silencing, inhibition, and notification routing to systems such as Slack, email, or PagerDuty.**

### Easy way to remember

`Prometheus = Detects the Problem`

`Alertmanager = Manages and Sends the Alert`

`Grafana = Shows the Metrics`

# Service Discovery
**`New Server/Pod/Service → Service Discovery automatically detects it → Prometheus gets the target information → Prometheus monitors it`**

The main benefit is **we don't have to manually add every new or changed monitoring target**, especially in dynamic environments like Kubernetes.

**Definition:** Service Discovery is a mechanism used to **automatically find and identify the applications, servers, containers, or services that Prometheus needs to monitor**.

**Main Purpose:** Service Discovery is mainly used to **automatically detect monitoring targets**, so we don't need to manually add every server, pod, or service to Prometheus configuration.

**What does it do?** It finds new or changed targets and provides their information to Prometheus, such as **IP address, port, service name, environment, and other labels**.

**Why do we use it?** In dynamic environments like Kubernetes, servers and pods can be **created, deleted, restarted, or have different IP addresses**. Service Discovery automatically keeps track of these changes.

**How does it work?** `Service Discovery Source → Finds Targets → Prometheus → Scrapes Metrics`

**Static Configuration:** `Prometheus → Manually configured targets → Scrape Metrics`

**Service Discovery:** `Kubernetes/Cloud → Automatically finds targets → Prometheus → Scrape Metrics`

### Kubernetes Example

`Kubernetes → Service Discovery → Prometheus discovers Pods/Services → /metrics → Prometheus`

Suppose today we have:

`3 Pods → Prometheus discovers 3 Pods`

Tomorrow Kubernetes scales to:

`10 Pods → Service Discovery discovers new Pods automatically → Prometheus scrapes them`

### Common Service Discovery Sources

**Kubernetes Service Discovery** → Automatically discovers Kubernetes pods, services, nodes, and other objects.

**AWS/EC2 Service Discovery** → Automatically discovers AWS instances.

**Consul Service Discovery** → Discovers services registered in Consul.

**File-based Discovery** → Targets are provided through a file that can be updated dynamically.

### Simple Example

Without Service Discovery:

`New Pod Created → SRE manually updates Prometheus → Prometheus monitors Pod`

With Service Discovery:

`New Pod Created → Kubernetes Discovery detects it → Prometheus automatically starts monitoring`

### Interview Definition

> **Service Discovery is a mechanism used by Prometheus to automatically discover monitoring targets in dynamic environments. It eliminates the need to manually configure every target and is especially useful in Kubernetes, where pods and services can frequently change.**

### Easy way to remember

`Service Discovery = Find Targets Automatically`

`Prometheus = Scrape Those Targets`
# Exporters
`Application/System → Exporter → Collects metrics → Exposes them in Prometheus-compatible format → Prometheus scrapes the metrics`

**Exporter’s main job = Collect/Expose metrics in a format Prometheus can scrape.**

Your understanding is correct.

**Definition:** Exporter is a **component that collects metrics from a system or application and exposes those metrics in a format that Prometheus can understand**.

**Main Purpose:** Exporters are mainly used when the application or system **does not provide Prometheus metrics directly**.

**What does it do?** It collects information from the target system, converts it into **Prometheus metric format**, and exposes it through a `/metrics` endpoint.

**How does it work?** `Server/Application → Exporter → /metrics → Prometheus`

**Example:** A Linux server does not directly provide Prometheus-formatted metrics → **Node Exporter** collects CPU, memory, disk, and network information → exposes `/metrics` → Prometheus scrapes it.

### Common Exporters

**Node Exporter** → Collects Linux server metrics such as `CPU, Memory, Disk, Network`.

**Blackbox Exporter** → Checks external endpoints such as `HTTP, HTTPS, DNS, TCP, ICMP`.

**Database Exporter** → Exposes database-related metrics for monitoring.

**kube-state-metrics** → Exposes metrics about the **state of Kubernetes objects**, such as Pods, Deployments, and StatefulSets.

### Simple Example

`Linux Server → Node Exporter → /metrics → Prometheus → Grafana`

Suppose:

`CPU = 85% → Node Exporter exposes CPU metric → Prometheus collects it → Grafana displays it`

### Why do we use Exporters?

**Without Exporter:** `System → No Prometheus-format metrics → Prometheus cannot directly scrape the required metrics`

**With Exporter:** `System → Exporter → /metrics → Prometheus`

### Interview Definition

> **Exporter is a component that collects metrics from a system or application, converts or exposes them in Prometheus format, and provides them through a metrics endpoint so that Prometheus can scrape and monitor them.**

### Easy way to remember

`Exporter = Collect + Expose Metrics`

`Prometheus = Scrape + Store + Query Metrics`

`Grafana = Visualize Metrics`

`/metrics = Metrics Endpoint`

`Prometheus → Service Discovery → Target → /metrics → Metrics`
