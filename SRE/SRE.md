## What is a Metric?

A **metric is a numerical measurement that tells us the current health or behavior of a system.**
- metrics help us answer: **“What is happening in my system?”**
- **We use metrics to:** `Collect data → Monitor system → Detect problems → Create alerts → Troubleshoot → Improve reliability`
- **1. CPU Utilization** — how much CPU is being used. `Server → CPU = 85%`
- **2. Memory Utilization** — how much memory is being used.
- **3. Request Rate** — how many requests the application receives. `Application → Requests = 10,000/min`
- **4. Error Rate** — how many requests are failing. `Application → Error Rate = 2%`
- **5. Latency** — how long the application takes to respond. `API → Response Time = 500 ms`
- **6. Disk Usage** — how much disk space is being consumed.
- **7. Network Traffic** — amount of data being sent/received. `Database → Connections = 450`

`Metrics → Numbers that tell you WHAT is happening` **Problem detected**

`Logs → Detailed records that help explain WHY it happened` **Problem investigated**

**In your SRE architecture** `Application/Server → Exporter → Prometheus → Grafana`

Prometheus **collects and stores metrics**, while Grafana **visualizes those metrics**.

### Interview answer

> **“A metric is a numerical measurement that represents the health or performance of a system. In SRE, we use metrics such as CPU, memory, request rate, error rate, and latency to monitor systems, detect problems, create alerts, and measure reliability.”**
