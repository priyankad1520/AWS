# **3. Where does the application run?**
> “The application can run on EC2, ECS, EKS, or Lambda depending on the application's architecture, containerization requirements, scalability, and operational requirements. I choose the service based on how much infrastructure control we need and how the application is packaged and executed.”

**Architecture:** `User → Route 53 → CloudFront/WAF → ALB → EC2/ECS/EKS → Database`

For serverless: `User → Route 53 → CloudFront/WAF → API Gateway → Lambda → Database`

---

# **4. What is EC2?**

> “Amazon EC2 provides virtual servers in AWS. We use EC2 when we need full control over the operating system, installed software, networking, and application environment. We are responsible for managing the server, including patching, configuration, and scaling.”

**Flow:** `ALB → EC2 → Application`

---

# **5. When would you choose EC2?**


> “I would choose EC2 when the application requires operating-system-level control, has specific software or runtime requirements, is a traditional application, or cannot easily be migrated to a containerized or serverless architecture.”

### Real-world example:

A company has an old Java application that requires a particular OS configuration and custom software.

**Choice:** `EC2` Why? > “We need more control over the underlying server.”

---

# **6. What is ECS?**

> “Amazon ECS is a managed container orchestration service used to run and manage Docker containers. AWS manages the orchestration layer, while we define how our containers should run.”

**Flow:** `ALB → ECS Service → Docker Containers`. ECS can run containers using: **EC2 capacity** or **AWS Fargate**

---

# **7. When would you choose ECS?**

> “I would choose ECS when the application is containerized but we don't need Kubernetes-specific features. ECS provides simpler container orchestration and integrates well with AWS services. It is a good choice when we want to run Docker containers without the complexity of managing Kubernetes.”

### Easy memory: > **Docker container + AWS-native orchestration + simpler than Kubernetes → ECS**

---

# **8. What is EKS?**

**Interview answer:**

> “Amazon EKS is AWS's managed Kubernetes service. I would use EKS when the organization requires Kubernetes for container orchestration, advanced deployment strategies, Kubernetes APIs, portability, or a large microservices environment.”

**Flow:**
`ALB → EKS → Kubernetes Service → Pods`

---

# **9. When would you choose EKS instead of ECS?**

**Interview answer:**

> “I would choose EKS when Kubernetes is a specific requirement of the organization or application, especially when we need Kubernetes features such as advanced scheduling, custom controllers, Helm, operators, Kubernetes-native tooling, or portability across environments. If those capabilities are not required, ECS is generally simpler to operate.”

### Easy memory:

**ECS → simpler AWS container orchestration**

**EKS → Kubernetes required**

---

# **10. What is Lambda?**

**Interview answer:**

> “AWS Lambda is a serverless compute service that runs code without requiring us to manage servers. We provide the function code and configuration, and AWS manages the underlying infrastructure. Lambda is especially useful for event-driven, short-running, and request-based workloads.”

**Flow:**
`API Gateway → Lambda → Database`

or:

`S3 Event → Lambda → Processing`

---

# **11. When would you choose Lambda?**

**Interview answer:**

> “I would choose Lambda when the workload is event-driven or request-based, doesn't require a continuously running server, and can work within Lambda's execution limits. It is useful for APIs, automation, file processing, scheduled jobs, and event-driven applications.”

### Real-world examples:

**Image uploaded to S3 → Lambda processes image**

**API request → Lambda executes business logic**

**CloudWatch/EventBridge event → Lambda performs automation**

---

# **12. When should you NOT choose Lambda?**

**Interview answer:**

> “I would avoid Lambda when the application requires long-running processes, specialized server-level configuration, persistent workloads, or execution characteristics that don't fit the Lambda model. In those cases, EC2 or containers may be more appropriate.”

---

# **13. How do you choose between EC2, ECS, EKS, and Lambda?**

This is a **very important interview question**.

**Interview answer:**

> “I choose based on the application's requirements. If I need maximum server control, I use EC2. If the application is containerized and I want simpler AWS-native orchestration, I use ECS. If Kubernetes is required, I use EKS. If the workload is event-driven or request-based and doesn't require server management, I use Lambda.”

### Remember this:

`Maximum server control → EC2`

`Docker + simpler orchestration → ECS`

`Docker + Kubernetes → EKS`

`Event-driven/serverless → Lambda`

---

# **14. What is WAF?**

**WAF = Web Application Firewall**

**Interview answer:**

> “AWS WAF is a web application firewall that protects web applications from common application-layer attacks and unwanted HTTP/HTTPS traffic. We can create rules based on IP addresses, HTTP headers, URI paths, query strings, geographic conditions, and managed rule groups.”

---

# **15. Why do we use WAF?**

**Interview answer:**

> “We use WAF to protect web applications from malicious HTTP and HTTPS requests, such as SQL injection, cross-site scripting, malicious bots, and unwanted traffic. It allows us to inspect requests and allow, block, or count them based on configured rules.”

---

# **16. Where do we configure WAF?**

This is **very important**.

AWS WAF can be associated with supported application endpoints such as:

**CloudFront**

**Application Load Balancer**

**API Gateway**

**AppSync**

For your architecture, think:

### Without CloudFront

`User → WAF → ALB → EC2/ECS/EKS`

### With CloudFront

`User → CloudFront + WAF → ALB → EC2/ECS/EKS`

### Serverless API

`User → WAF → API Gateway → Lambda`

So WAF is generally placed **in front of the web application entry point**.

---

# **17. Where would you put WAF in a production architecture?**

**Interview answer:**

> “For a public web application, I would typically associate AWS WAF with CloudFront when CloudFront is being used, or directly with the Application Load Balancer when CloudFront is not being used. For APIs using API Gateway, WAF can also be associated with API Gateway.”

**Flow:**
`User → Route 53 → CloudFront/WAF → ALB → Application`

---

# **18. Why put WAF before ALB?**

**Interview answer:**

> “WAF allows us to inspect and filter malicious HTTP/HTTPS requests before they reach the application infrastructure. This prevents unwanted traffic from reaching the ALB and backend application.”

For example:

`Attacker → malicious request → WAF → Block ❌`

Normal:

`User → valid request → WAF → ALB → Application ✅`

---

# **19. What kind of attacks can WAF help protect against?**

**Interview answer:**

> “WAF can help protect web applications against common application-layer attacks such as SQL injection and cross-site scripting, as well as unwanted IP addresses, malicious bots, and other patterns defined through WAF rules.”

Remember:

> **WAF protects the web/application layer.**

It is not a replacement for Security Groups, NACLs, IAM, or other security controls.

---

# **20. WAF vs Security Group**

Very common interview question.

**Interview answer:**

> “A Security Group controls network-level access to an AWS resource such as an EC2 instance or load balancer, mainly based on IP addresses, ports, and protocols. WAF operates at the web application layer and inspects HTTP/HTTPS requests based on application-level rules.”

### Easy memory:

**Security Group → Who can connect to the resource and on which port?**

**WAF → Is this HTTP/HTTPS request allowed or malicious?**

---

# **21. Does WAF replace ALB?**

**Interview answer:**

> “No. WAF and ALB have different responsibilities. WAF filters and protects HTTP/HTTPS requests, while ALB distributes valid application traffic across healthy targets.”

**Flow:**
`User → WAF → ALB → EC2/ECS/EKS`

---

# **22. Does every application need WAF?**

**Interview answer:**

> “No. WAF is mainly useful for public-facing web applications and APIs where we need application-layer protection. For a private internal application without public web exposure, WAF may not be necessary depending on the security architecture.”

---

# **23. Does every application need EC2?**

**Interview answer:**

> “No. EC2 is only one compute option. Depending on the application, we may use ECS, EKS, or Lambda instead.”

---

# **24. Complete architecture decision**

Suppose the interviewer says:

> **“Design a public e-commerce application.”**

You can think:

`User → Route 53 → CloudFront → WAF → ALB → EKS/ECS → RDS`

Static content:

`CloudFront → S3`

Now suppose they ask:

> **“Why EKS?”**

You answer:

> “The application is containerized and the organization requires Kubernetes-based orchestration.”

If they ask:

> **“Why WAF?”**

> “To inspect and block malicious HTTP/HTTPS requests before they reach the application.”

If they ask:

> **“Why CloudFront?”**

> “To cache and deliver content closer to users and reduce traffic to the origin.”

If they ask:

> **“Why ALB?”**

> “To distribute HTTP/HTTPS traffic across healthy application targets.”

---

# **Your complete Question 3 mental map**

### **Where does the application run?**

`Traditional application → EC2`

`Containerized application → ECS`

`Kubernetes application → EKS`

`Event-driven/serverless workload → Lambda`

### **Where does security happen?**

`User → Route 53 → CloudFront/WAF → ALB → Application`

And remember the responsibility of each:

`Route 53 → DNS`

`CloudFront → CDN/cache`

`WAF → HTTP/HTTPS security`

`ALB → HTTP/HTTPS traffic distribution`

`EC2 → Virtual server`

`ECS → Container orchestration`

`EKS → Kubernetes orchestration`

`Lambda → Serverless execution`

`S3 → Object/static storage`

`RDS → Relational database`

