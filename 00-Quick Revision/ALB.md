Great. Now let's move to **Question 2: How is traffic distributed?**

# **1. What do we mean by traffic distribution?**

> “Traffic distribution means distributing incoming application requests across multiple healthy servers or pods so that no single server becomes overloaded and the application remains highly available.”

**Flow:** `Users → Load Balancer → EC2/Pods`

---

# **2. Which AWS service do we use to distribute traffic?**

> “In AWS, we commonly use Elastic Load Balancing. For HTTP/HTTPS applications, I would generally use an Application Load Balancer, while for TCP/UDP and high-performance use cases, I would consider a Network Load Balancer.”

**Flow:** `Users → ALB/NLB → Application Targets`

---

# **3. What is ALB?**

> “ALB, or Application Load Balancer, is a Layer 7 load balancer that distributes HTTP and HTTPS traffic across multiple healthy targets such as EC2 instances, containers, or IP addresses. It can also make routing decisions based on host names and URL paths.”

---

# **4. Why do we use ALB?**

> “We use ALB to distribute application traffic, improve availability, prevent individual servers from becoming overloaded, perform health checks, and route requests to the appropriate backend service.”

For example:

**Flow:** `User → ALB → EC2-1 / EC2-2 / EC2-3`

If EC2-2 becomes unhealthy, ALB stops sending traffic to it.

---

# **5. How does ALB know which server is healthy?**

> “ALB uses health checks configured on the target group. It periodically checks the configured protocol, port, and path. If a target fails the health check, ALB stops routing new requests to that target.”

**Flow:** `ALB → Health Check → Target Healthy → Receive Traffic`

---

# **6. What is a Target Group?**

> “A target group is a collection of backend targets that receive traffic from the load balancer. Depending on the configuration, the targets can be EC2 instances, IP addresses, or other supported target types.”

**Flow:** `ALB → Listener → Target Group → Healthy Targets`

---

# **7. What is a Listener?**

> “A listener checks for incoming connection requests on a specific protocol and port, such as HTTP port 80 or HTTPS port 443, and then forwards the request according to the configured rules.”

Example:

**Flow:** `Client → ALB :443 → Listener → Target Group → EC2`

---

# **8. Why do we need a load balancer if we already have Route 53?**

> “Route 53 is responsible for DNS resolution and helps the client discover the application's endpoint. The load balancer handles the actual application traffic and distributes requests across healthy backend targets.”

This is a **very important interview distinction**.

**Flow:** `www.example.com → Route 53 DNS → ALB → EC2/EKS`

---

# **9. What happens when traffic suddenly increases?**

> “The load balancer continues distributing incoming requests across the available healthy targets. If the application is configured with Auto Scaling, additional EC2 instances can be launched when capacity is needed, and the new instances are automatically registered with the target group and begin receiving traffic after passing health checks.”

**Flow:** `Traffic ↑ → ALB → ASG → New EC2 → Health Check → ALB sends traffic`

For EKS:

> “In EKS, increased traffic can trigger HPA to increase the number of pods, and node autoscaling can add worker-node capacity when required.”

**Flow:** `Traffic ↑ → ALB → Service → HPA → More Pods → Node Autoscaling if required`

---

# **10. What is the difference between ALB and NLB?**

> “ALB operates at the application layer and is designed mainly for HTTP and HTTPS traffic. It supports features such as host-based and path-based routing. NLB operates at the transport layer and is designed for TCP, UDP, and high-performance, low-latency use cases.”

### Easy interview memory

**ALB → HTTP/HTTPS → Application-level routing**

**NLB → TCP/UDP → High performance / low latency**

---

# **11. When would you choose ALB?**

> “I would choose ALB for web applications, REST APIs, microservices, and other HTTP/HTTPS-based applications where I need application-level routing.”

Example:

**Flow:** `example.com/api → Service A`
**Flow:** `example.com/admin → Service B`

---

# **12. When would you choose NLB?**

> “I would choose NLB when the application needs TCP or UDP traffic, very high throughput, low latency, or transport-level load balancing.”

---

# **13. What happens if one EC2 server fails?**

> “The ALB health check detects that the target is unhealthy and stops routing traffic to it. If the instances are managed by an Auto Scaling Group, the unhealthy instance can be replaced automatically.”

**Flow:** `EC2 fails → ALB Health Check fails → Traffic stops → ASG replaces EC2`

---

# **14. What happens if all EC2 servers become unhealthy?**

> “The ALB will have no healthy targets to serve the request, so the application will become unavailable through that load balancer. I would then troubleshoot the target health, application status, networking, security groups, ports, and dependencies such as the database.”

This is a good place to demonstrate your **troubleshooting mindset** rather than simply saying “ALB will fix it.”

---

# **15. Can ALB distribute traffic based on URL path?**

> “Yes. ALB supports path-based routing, so different URL paths can be forwarded to different target groups.”

Example:

**Flow:** `example.com/api → Target Group API`

**Flow:** `example.com/web → Target Group Web`

---

# **16. Can ALB distribute traffic based on domain name?**

> “Yes. ALB supports host-based routing, so different domain names can be routed to different target groups.”

Example:

**Flow:** `api.example.com → API Target Group`

**Flow:** `admin.example.com → Admin Target Group`

---

# **17. How does traffic distribution work in a production architecture?**

> “I would place the ALB across multiple Availability Zones and register application targets distributed across those Availability Zones. The ALB receives incoming HTTP/HTTPS requests, performs health checks, and forwards traffic to healthy targets.”

**Architecture flow:**
`Users → Route 53 → ALB → Target Group → EC2/EKS across multiple AZs`

---

# **18. What is the complete traffic flow?**

> “The user first resolves the application domain through Route 53. The request then reaches the ALB. The ALB listener accepts the request and applies the routing rules. The request is forwarded to the appropriate target group, and the target group sends it to a healthy application target.”

**Flow:** `User → Route 53 → ALB → Listener → Target Group → Healthy EC2/Pod → Application`

---

## The 6 things to memorize for traffic distribution

**Load Balancer → distributes traffic**

**ALB → HTTP/HTTPS**

**NLB → TCP/UDP, high performance**

**Listener → accepts incoming traffic**

**Target Group → contains backend targets**

**Health Check → decides which targets can receive traffic**

The main mental picture is:

**`Route 53 → ALB → Listener → Target Group → Healthy EC2/EKS`**

And when traffic increases:

**`Traffic ↑ → Load Balancer → Autoscaling → More Targets → Load Balancer distributes traffic`**

**when do we use CloudFront + S3, and when do we use ALB/NLB?**

Think of them as solving different problems:

**CloudFront = CDN/caching**
**S3 = object/static-file storage**
**ALB = HTTP/HTTPS application traffic distribution**
**NLB = TCP/UDP/high-performance traffic distribution**

---

# **1. What is CloudFront?**

> “Amazon CloudFront is a CDN service that caches and delivers content from edge locations closer to users. It improves performance and reduces the number of requests reaching the origin server.”

**Flow:** `User → Route 53 → CloudFront → Cache/Origin → User`

The origin can be S3, ALB, or another supported HTTP origin.

---

# **2. Why do we use CloudFront?**

> “We use CloudFront when users are geographically distributed or when we have content that can be cached, such as images, CSS, JavaScript, videos, documents, or static web content. It improves response time and reduces load on the origin.”

For example:

`User in India → nearest CloudFront edge → cached image`

instead of:

`User in India → application server in US → image`

---

# **3. Why do we use S3 with CloudFront?**

> “S3 is commonly used to store static objects such as images, CSS, JavaScript, videos, and documents, while CloudFront provides cached delivery of those objects from edge locations.”

**Flow:** `User → CloudFront → S3`

This is a very common AWS architecture for static content.

---

# **4. What kind of application uses CloudFront + S3?**

A **static website** is the simplest example.

Suppose you have:

```text
index.html
style.css
app.js
images/
```

You can store those files in S3.

**Flow:** `User → Route 53 → CloudFront → S3`

Here you don't necessarily need an ALB or EC2 because S3 is serving the static content.

---

# **5. What about a dynamic application?**

Suppose your application has:

`Login → Cart → Wishlist → Payment → User Account`

The application needs backend processing.

You could have:

**Flow:** `User → Route 53 → CloudFront → ALB → EC2/EKS → RDS`

CloudFront handles **cacheable content**, while ALB sends dynamic requests to the application.

For example:

`/images/product1.jpg → CloudFront → cached`

`/api/cart → CloudFront → ALB → Application`

The exact CloudFront cache/origin behavior depends on how you configure distributions and behaviors.

---

# **6. How do you configure CloudFront with S3?**

Interview answer:

> “First, I create an S3 bucket and upload the static content. Then I create a CloudFront distribution and configure the S3 bucket as the origin. I configure the appropriate origin access controls so users access the objects through CloudFront rather than directly exposing the bucket. Then I configure the required cache behavior and associate the domain through Route 53.”

**Flow:** `S3 Bucket → CloudFront Origin → Cache Behavior → Route 53 → www.example.com`

For modern AWS designs, **Origin Access Control (OAC)** is preferred for securing an S3 origin, so the bucket can remain private while CloudFront accesses it.

---

# **7. How do you connect CloudFront to Route 53?**

Interview answer:

> “After creating the CloudFront distribution, AWS provides a CloudFront distribution domain name. In Route 53, I create an Alias record for my domain and point it to the CloudFront distribution.”

For example:

`www.example.com → Route 53 Alias → CloudFront → S3`

---

# **8. How do you connect CloudFront to an ALB?**

Interview answer:

> “I create the CloudFront distribution and configure the ALB as the origin. CloudFront receives requests from users and forwards cacheable or dynamic requests to the ALB based on the configured cache behaviors. Route 53 then points the application domain to the CloudFront distribution.”

**Flow:** `User → Route 53 → CloudFront → ALB → EC2/EKS`

This is useful when you want **CDN benefits in front of a dynamic web application**.

---

# **9. Why put CloudFront in front of ALB?**

Interview answer:

> “We put CloudFront in front of an ALB when we want global content delivery, caching, TLS termination at the edge, and reduced traffic to the origin. Static or cacheable content can be served from CloudFront, while requests that require the application can be forwarded to the ALB.”

For example:

**Flow:** `User → CloudFront → /images → Cache`

**Flow:** `User → CloudFront → /api → ALB → Application`

---

# **10. Does every application need CloudFront?**

> “No. CloudFront is not mandatory. I would use it when the application benefits from CDN caching, global distribution, reduced origin traffic, or edge delivery. For a simple internal application with users in one location, CloudFront may not provide enough benefit to justify adding it.”

---

# **11. Does every application need S3?**

> “No. S3 is used when the application needs object storage, such as images, videos, documents, backups, static assets, or other files. It is not a replacement for a relational database such as RDS.”

---

# **12. Now the important question: Which application needs which load balancer?**

This is the decision table I want you to remember.

| Application requirement            | Choose                                          |
| ---------------------------------- | ----------------------------------------------- |
| Normal website using HTTP/HTTPS    | **ALB**                                         |
| REST API using HTTP/HTTPS          | **ALB**                                         |
| Microservices using HTTP/HTTPS     | **ALB**                                         |
| Path-based routing                 | **ALB**                                         |
| Host-based routing                 | **ALB**                                         |
| Kubernetes HTTP/HTTPS application  | **ALB** commonly                                |
| TCP application                    | **NLB**                                         |
| UDP application                    | **NLB**                                         |
| Very high throughput / low latency | **NLB**                                         |
| Static website                     | **S3 + CloudFront**                             |
| Images/CSS/JS/videos/documents     | **S3 + CloudFront**                             |
| Global dynamic web application     | **CloudFront + ALB**                            |
| Internal/simple application        | **ALB or internal LB depending on requirement** |

---

# **13. Real-world example: E-commerce application**

Imagine Amazon-like application:

`www.shop.com`

It has product images, product pages, cart, login, and payment.

You might design:

**Flow:** `User → Route 53 → CloudFront → ALB → EKS → RDS`

And static files:

**Flow:** `CloudFront → S3`

So conceptually:

```text
                         CloudFront
                       ↙           ↘
                 Static content   Dynamic requests
                       ↓                ↓
                      S3               ALB
                                         ↓
                                        EKS
                                         ↓
                                        RDS
```

The important thing is:

> **CloudFront does not replace ALB. S3 does not replace your application servers.**

They have different responsibilities.

---

# **14. Real-world example: Company portfolio website**

Suppose your company website contains:

`index.html`
`about.html`
`logo.png`
`style.css`
`company-video.mp4`

There is no backend processing.

You can use:

**Flow:** `User → Route 53 → CloudFront → S3`

You don't need EC2, EKS, or ALB just to serve these static files.

---

# **15. Real-world example: Online banking/API application**

Suppose your application has:

`/login`
`/accounts`
`/transfer`
`/transactions`

These requests require backend processing and database access.

You might use:

**Flow:** `User → Route 53 → CloudFront → ALB → Application → RDS`

CloudFront can accelerate suitable content, while the ALB handles application traffic.

---

# **16. Real-world example: Gaming/TCP application**

Suppose the application needs persistent TCP connections or other transport-level traffic.

Then you would consider:

**Flow:** `Client → NLB → Application`

Here ALB isn't the right first choice because the requirement isn't ordinary HTTP/HTTPS application-layer routing.

---

# **17. The interview decision rule**

When the interviewer gives you an application, **don't immediately say ALB**.

Ask yourself:

> **What kind of traffic?**

**HTTP/HTTPS → ALB**

**TCP/UDP → NLB**

Then:

> **Does the content need global caching?**

**Yes → CloudFront**

Then:

> **Is the content static/object-based?**

**Yes → S3 + CloudFront**

Then:

> **Does the application need backend processing?**

**Yes → ALB/NLB → EC2/EKS**

So your mental architecture becomes:

**`User → Route 53 → CloudFront (if CDN needed) → ALB (if HTTP/HTTPS backend) → EC2/EKS → RDS`**

or, for static content:

**`User → Route 53 → CloudFront → S3`**

or, for transport-level applications:

**`Client → NLB → Application`**

### The key sentence for your interview

> **“I choose the load balancer based on the traffic protocol and application requirement. For HTTP/HTTPS applications I generally use ALB, while for TCP/UDP and high-performance transport-level workloads I use NLB. CloudFront is added when CDN caching and global content delivery are required, and S3 is commonly used as the origin for static content.”**
