# **4. How does the application scale?**
> “I would choose the scaling mechanism based on where the application is running. For EC2, I would use an Auto Scaling Group. For ECS, I can use Service Auto Scaling. For EKS, I would use HPA to scale pods and Karpenter or Cluster Autoscaler to add or remove nodes. For Lambda, AWS automatically scales the number of function executions based on incoming requests, subject to concurrency limits.”

---

## **1. What is Auto Scaling?**
> “Auto Scaling means automatically increasing or decreasing application capacity based on demand. The goal is to handle increased traffic while avoiding unnecessary infrastructure cost when traffic is low.”

**Flow:** `Traffic ↑ → Capacity ↑`
**Flow:** `Traffic ↓ → Capacity ↓`

---

# **2. How does EC2 scale?**
> “For EC2-based applications, I would use an Auto Scaling Group. It maintains the desired number of instances and can launch or terminate instances based on configured scaling policies and metrics such as CPU utilization, request count, or other CloudWatch metrics.”

**Flow:** `ALB → Auto Scaling Group → EC2-1 / EC2-2 / EC2-3`

If traffic increases: **Flow:** `Traffic ↑ → CloudWatch metric ↑ → ASG launches EC2 → Health Check → ALB adds new instance`

---

# **3. What is an Auto Scaling Group?**
> “An Auto Scaling Group is a service that maintains a desired number of EC2 instances and automatically replaces unhealthy instances and adjusts capacity according to scaling policies.”

Important concepts:

**Minimum capacity** → minimum number of instances

**Desired capacity** → normal number of instances

**Maximum capacity** → maximum number of instances

Example: `Min = 2 → Desired = 2 → Max = 6`

Traffic increases: `2 → 3 → 4 → 5`

Traffic falls: `5 → 4 → 3 → 2`

---

# **4. What happens when an EC2 instance fails?**
> “The Auto Scaling Group can detect that the instance is unhealthy and terminate and replace it to maintain the desired capacity. If the application is behind an ALB, the load balancer also performs health checks and stops sending traffic to unhealthy targets.”

**Flow:** `EC2 fails → ALB marks unhealthy → ASG replaces instance → New EC2 → Health Check passes → Traffic resumes`

---

# **5. What is horizontal scaling?**
> “Horizontal scaling means increasing or decreasing the number of application instances rather than increasing the size of one instance.”

**Flow:** `2 EC2 → 4 EC2 → 6 EC2`

This is usually what people mean by **scale out / scale in**.

---

# **6. What is vertical scaling?**
> “Vertical scaling means increasing or decreasing the capacity of an existing instance, such as moving from a smaller EC2 instance type to a larger one.”

**Flow:** `t3.medium → t3.large → t3.xlarge`

Easy memory: **Horizontal = more machines**. **Vertical = bigger machine**

---

# **7. Which is generally preferred for highly available applications?**
> “For highly available stateless applications, horizontal scaling is generally preferred because we can distribute traffic across multiple instances and Availability Zones and replace individual instances without taking the entire application offline.”

---

# **8. How does ECS scale?**
> “In ECS, Service Auto Scaling adjusts the desired number of running tasks based on metrics such as CPU utilization, memory utilization, or application load. With Fargate, AWS manages the underlying compute capacity for the tasks.”

**Flow:** `Traffic ↑ → ECS Service Auto Scaling → More Tasks`

For example: `2 tasks → 4 tasks → 6 tasks`

---

# **9. How does EKS scale?**
There are **two different levels of scaling**.

### Pod scaling
> “HPA, or Horizontal Pod Autoscaler, increases or decreases the number of pods based on metrics such as CPU, memory, or custom metrics.”

**Flow:** `Traffic ↑ → HPA → More Pods` Example: `3 Pods → 6 Pods → 10 Pods`

### Node scaling
> “If the existing worker nodes don't have enough capacity for the new pods, node autoscaling such as Karpenter or Cluster Autoscaler can add additional nodes.”

**Flow:** `Pods need capacity → Node Autoscaler → More Nodes`

---

# **10. What is HPA?**
> “HPA, or Horizontal Pod Autoscaler, automatically adjusts the number of Kubernetes pod replicas based on configured metrics.”

Example: `CPU > target → increase pods` `CPU < target → decrease pods`

---

# **11. What is Karpenter?**
> “Karpenter is a Kubernetes node provisioning and autoscaling tool that can automatically launch and terminate worker nodes based on the scheduling requirements of pending pods.”

The important distinction: **HPA → Pods** **Karpenter → Nodes**

---

# **12. What is Cluster Autoscaler?**
> “Cluster Autoscaler adjusts the number of nodes in a Kubernetes cluster when pods cannot be scheduled because of insufficient node capacity, or when nodes can be safely removed.”

**HPA → application pods** **Cluster Autoscaler/Karpenter → worker nodes**

---

# **13. How does Lambda scale?**
> “Lambda automatically creates additional concurrent function executions as request volume increases, so we don't manually add servers. We can control or reserve concurrency when we need to limit scaling or protect downstream systems.”

**Flow:** `Requests ↑ → Lambda Concurrent Executions ↑` You don't create EC2 instances for Lambda.

---

# **14. What happens when traffic suddenly increases?**

### EC2 application

> “The load balancer continues distributing traffic to healthy instances. If demand increases beyond the current capacity, the Auto Scaling Group launches additional EC2 instances according to the configured scaling policy. Once those instances pass health checks, the ALB can send traffic to them.”

**Flow:** `Traffic ↑ → ALB → CloudWatch → ASG → New EC2 → Health Check → ALB → New Traffic`

### EKS application

> “HPA increases the number of pods. If the cluster doesn't have enough node capacity, Karpenter or Cluster Autoscaler provisions additional nodes.”

**Flow:** `Traffic ↑ → ALB → Service → HPA → More Pods → Karpenter/CA → More Nodes`

### Lambda

> “Lambda automatically scales concurrent executions according to incoming demand, subject to concurrency limits and service quotas.”

---

# **15. What is Scale Out and Scale In?**

**Scale Out:** > “Increase the number of resources when demand increases.” `2 EC2 → 4 EC2`

**Scale In:** > “Decrease the number of resources when demand decreases.” **Flow:** `4 EC2 → 2 EC2`

---

# **16. What metrics can trigger scaling?**
> “Scaling can be based on metrics such as CPU utilization, memory utilization, request count, request rate, latency, queue depth, or custom application metrics, depending on the workload.”

For example:Manybe `CPU > 70% → scale out` `CPU < 30% → scale in`
> **“Scale based on an appropriate metric for the workload.”**

---

# **17. Why shouldn't we scale only based on CPU?**
> “CPU is not always the best indicator of application demand. For example, a web application may be limited by request rate, latency, memory, or database connections while CPU remains low. So I would choose a metric that represents the actual bottleneck.”
---

# **18. What is the difference between Auto Scaling and Load Balancing?**
> “A load balancer distributes traffic across available healthy targets, while Auto Scaling changes the number of targets based on demand. They work together but solve different problems.”

**Flow:** `Users → ALB → Existing EC2`

**Flow during scale-out:** `Traffic ↑ → ASG adds EC2 → ALB distributes traffic across old + new EC2`

Easy memory: **ALB = distribute** **ASG = add/remove capacity**

---

# **19. What if traffic increases faster than Auto Scaling can react?**
> “There can be a temporary capacity gap while new resources are launching. To handle sudden spikes, I would consider sufficient baseline capacity, appropriate scaling policies, cooldown or stabilization settings, predictive or scheduled scaling where applicable, and caching/CDN mechanisms such as CloudFront to reduce origin load.”

---

# **20. How does CloudFront help with scaling?**
> “CloudFront can cache static and cacheable content at edge locations, which reduces the number of requests reaching the origin. This reduces load on the ALB and backend application and can improve performance during traffic spikes.”

**Flow:** `Users → CloudFront Cache → Response`. Only requests that need the origin continue to: `CloudFront → ALB → Application`

---

# **21. What if the application is stateful?**
> “For horizontal scaling, I prefer keeping application servers stateless whenever possible. Session or shared state can be stored in external services such as ElastiCache or a database so that requests can be handled by any healthy application instance.”

**Flow:** `User → ALB → EC2-1 / EC2-2 → Shared Session Store` This avoids depending on one particular server.

---

# **22. What does a good scalable AWS architecture look like?**

For an EC2 application:

**Flow:** `Users → Route 53 → CloudFront/WAF → ALB → ASG/EC2 → RDS`

For an EKS application:

**Flow:** `Users → Route 53 → CloudFront/WAF → ALB → EKS → HPA → Karpenter → RDS`

For a serverless application:

**Flow:** `Users → Route 53 → CloudFront/WAF → API Gateway → Lambda → Database`

---

# **Your scaling cheat sheet**

| Application    | Scaling mechanism               |
| -------------- | ------------------------------- |
| **EC2**        | Auto Scaling Group              |
| **ECS**        | ECS Service Auto Scaling        |
| **EKS Pods**   | HPA                             |
| **EKS Nodes**  | Karpenter / Cluster Autoscaler  |
| **Lambda**     | Automatic concurrency scaling   |
| **CloudFront** | CDN caching reduces origin load |

### The most important distinction

> **EC2 → ASG**
> **ECS → Service Auto Scaling**
> **EKS → HPA for pods + Karpenter/Cluster Autoscaler for nodes**
> **Lambda → AWS automatically scales executions**

And the overall architecture becomes:

**`Traffic ↑ → Load Balancer → Application Scaling → More Capacity → Health Check → Traffic Distributed`**

That is the core answer for **Question 4: “How does the application scale?”**
## **4. How does the application scale?**

**What is scaling?**: Scaling means increasing or decreasing application resources based on workload or traffic.

**Why do we need scaling?**: To handle increased traffic, maintain performance, avoid overloading servers, and reduce unnecessary cost when traffic is low.

**What is vertical scaling?**: Increasing the capacity of the existing server, such as increasing CPU or memory.

**What is horizontal scaling?**: Adding more servers, containers, or pods to handle more traffic.

**Which scaling is commonly used in AWS applications?**: Horizontal scaling is commonly preferred for highly available applications because traffic can be distributed across multiple instances.

### **EC2 Scaling**

**What do we use for EC2 scaling?**: Auto Scaling Group (ASG).

**How does ASG work?**: It automatically adds or removes EC2 instances based on configured policies, metrics, or schedules.

**Traffic increase flow**: Traffic ↑ → ALB → CloudWatch metric → ASG → New EC2 instance → Health check → ALB sends traffic to new instance.

**Traffic decrease flow**: Traffic ↓ → ASG detects lower demand → Removes unnecessary EC2 instances.

**What is the benefit of ASG?**: Automatic scaling, high availability, and better cost management.

---

### **ECS Scaling**

**How do we scale ECS?**: We can increase or decrease the number of ECS tasks using Service Auto Scaling.

**What is an ECS task?**: A running instance of one or more containers defined by a task definition.

**Traffic increase flow**: Traffic ↑ → ALB → ECS Service → More tasks → ALB distributes traffic.

**What if more EC2 capacity is required in ECS?**: The underlying ECS capacity can also be scaled when using EC2-based ECS; with Fargate, AWS manages the underlying compute capacity.

---

### **EKS Scaling**

**How do we scale pods?**: Horizontal Pod Autoscaler (HPA).

**What does HPA do?**: It increases or decreases the number of pods based on configured metrics such as CPU, memory, or application metrics.

**How do we scale worker nodes?**: Karpenter or Cluster Autoscaler can add or remove nodes based on scheduling/capacity requirements.

**EKS scaling flow**: Traffic ↑ → ALB → Service → HPA → More Pods → Insufficient node capacity → Karpenter/Cluster Autoscaler → More Nodes.

**Important difference**: HPA → Pod scaling, Karpenter/Cluster Autoscaler → Node scaling.

---

### **Lambda Scaling**

**How does Lambda scale?**: Lambda automatically creates more concurrent function executions as requests increase, subject to concurrency limits and configuration.

**Lambda scaling flow**: Requests ↑ → Lambda → More concurrent executions.

**Do we manage EC2 servers for Lambda scaling?**: No, AWS manages the underlying compute infrastructure.

---

### **CloudFront and Scaling**

**Does CloudFront scale?**: CloudFront automatically handles large amounts of content-delivery traffic through its distributed edge network.

**Why does CloudFront reduce application load?**: Cached content is served from CloudFront instead of repeatedly requesting it from the origin.

**Flow**: User → CloudFront → Cache hit → Content returned.

**Cache miss flow**: User → CloudFront → Origin → CloudFront caches response → User.

---

### **Auto Scaling vs Load Balancer**

**Is ALB responsible for scaling?**: No, ALB distributes traffic; Auto Scaling adds or removes application capacity.

**Simple difference**: ALB → distributes traffic, ASG → changes the number of EC2 instances.

**Complete flow**: Users → Route 53 → CloudFront/WAF → ALB → Auto Scaling EC2/ECS/EKS → Application.

---

### **What happens when traffic suddenly increases?**

**EC2 application**: Traffic ↑ → ALB → ASG launches more EC2 instances → Health checks pass → ALB distributes traffic.

**ECS application**: Traffic ↑ → ALB → ECS Service Auto Scaling → More tasks.

**EKS application**: Traffic ↑ → ALB → HPA → More pods → Node autoscaling if required.

**Lambda application**: Traffic ↑ → More concurrent Lambda executions.

---

### **Most important scaling questions to remember**

**EC2 scaling**: ASG.

**ECS scaling**: Service Auto Scaling → More tasks.

**EKS pod scaling**: HPA.

**EKS node scaling**: Karpenter / Cluster Autoscaler.

**Lambda scaling**: Automatic concurrency scaling.

**CloudFront scaling**: Distributed caching and edge delivery.

**Horizontal scaling**: Add more instances/pods/tasks.

**Vertical scaling**: Increase CPU/memory of an existing resource.

### **Your architecture memory**

**Traffic ↑ → Load Balancer distributes → Scaling mechanism adds capacity → Health checks → New capacity receives traffic**.
