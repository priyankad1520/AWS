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

## SLI vs SLO vs SLA
`Real System Performance → SLI → SLO → SLA` `Measure it → Set a target → Make a customer commitment`

---

**1. SLI — Service Level Indicator**: **SLI is the actual measurement of how the service is performing.**
> **“How is my service performing right now?”**
Examples:`Successful requests = 99.95%`, `API latency = 200 ms`, `Availability = 99.9%`

**SLI = What we measure**: Suppose our website received 100,000 requests and 99,900 succeeded. `SLI = 99,900 / 100,000 = 99.9%`

**2. SLO — Service Level Objective**: **SLO is the reliability target we want to achieve.**
> **“How reliable do we want our service to be?”** **SLO = What we Target**
Example: `SLI = Current availability = 99.95%`, `SLO = Target availability = 99.9%`
`Availability SLO = 99.9%` `Latency SLO = 95% of requests must be < 300 ms`

**Why do we use SLO?**: To define a **clear reliability goal** for the engineering team.

---

**3. SLA — Service Level Agreement: SLA is a formal agreement with the customer about the service level.**
> **“What level of service are we contractually promising the customer?”** **SLA = What we promise or Customer/Business Commitment**
For example: `SLA = 99.9% availability`

If the company fails to meet the SLA, there may be **service credits, refunds, penalties, or other contractual consequences**, depending on the agreement.

## Real-world case study

Imagine an e-commerce website.

We measure: `Successful requests = 99.95%` → **SLI**

Our engineering team sets: `Target = 99.9%` → **SLO**

The company promises customers: `Availability = 99.9%` → **SLA**

So: `Actual Performance (SLI) → Reliability Target (SLO) → Customer Commitment (SLA)`

`SLI → SLO → Error Budget → SLA`

### Interview answer

> **“SLI is the actual measurement of service reliability, such as availability, latency, or error rate. SLO is the target reliability we want to achieve, such as 99.9% availability. SLA is the formal commitment made to customers, usually with business consequences if we don't meet it. In simple terms, SLI is what we measure, SLO is what we target, and SLA is what we promise.”**

## Error Budget & Error-Budget Policy

These two concepts are closely connected to **SLO**.

### 1. Error Budget

**Error budget is the amount of failure or unreliability we are allowed to have while still meeting our SLO.**

Simple formula: `Error Budget = 100% − SLO`

For example: `SLO = 99.9% availability` So: `100% − 99.9% = 0.1%`. That **0.1% is the error budget**.

For a 30-day month, 99.9% availability allows about **43 minutes 12 seconds** of unavailability.

**Why do we use Error Budget?** Because **100% reliability is usually expensive or unrealistic**.

We need to balance: `New Features ↔ Reliability`. The error budget gives engineering a measurable way to decide how much risk is acceptable.

### 2. Error-Budget Policy

**Error-budget policy is the set of rules that tells the engineering team what to do when the error budget is healthy, being consumed quickly, or exhausted.**
> **“What action should we take based on how much error budget is left?”**

Example policy:

`Error Budget Healthy → Normal development + releases`

`Error Budget Low → Increase monitoring + prioritize reliability work`

`Error Budget Exhausted → Stop/pause risky releases → Focus on fixing reliability`

So the policy converts the budget into **engineering decisions**.


### Interview answer

> **“Error budget is the amount of unreliability we can tolerate while still meeting our SLO. For example, with a 99.9% availability SLO, we have a 0.1% error budget. Error-budget policy defines what actions the engineering team should take depending on how much of that budget remains. When the budget is healthy, we can continue normal development. When the budget is nearly exhausted or exhausted, we prioritize reliability work and may pause risky deployments. This helps balance feature velocity with system reliability.”**

