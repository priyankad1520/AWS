**1. "Can you explain your current project architecture?"**

> "So basically, I'm currently working on a **healthcare project for a European client**. When I joined the project, the applications were running on a **self-managed Kubernetes cluster**, and I was involved in migrating the platform to **Amazon EKS** to improve reliability, scalability, and operational management.
>
> From the architecture perspective, the **frontend applications are hosted on Amazon S3 and served through CloudFront**, with **AWS WAF** providing the security layer. The backend and microservices are running on **EKS**, where we use Kubernetes for container orchestration and scaling.
>
> For CI/CD, we use **Bitbucket Pipelines for the CI process**, where we build, test, scan, and prepare the application artifacts. For CD, we use **Argo CD with GitOps**, where the Kubernetes manifests or Helm charts are maintained in Git and Argo CD synchronizes them to the EKS cluster.
>
> The complete AWS infrastructure is managed through **Terraform**, including networking, EKS, IAM roles, security components, and other AWS resources. We also use **Datadog for monitoring, logging, and alerting**.
>
> Since the client operates in Europe, we follow **GDPR requirements**, and as they are expanding into the US, we're also working on architecture and security controls to meet **HIPAA requirements**. We have a **multi-region disaster recovery setup** as well, so if the primary region has an issue, we can recover the application from the secondary region.
>
> So overall, the architecture is **Users → CloudFront/WAF → S3 for frontend and EKS for backend → supporting AWS services**, with **Bitbucket Pipelines + Argo CD for CI/CD, Terraform for infrastructure, Datadog for observability, and multi-region DR for resilience**."


**2. "Assume you're joining a new company that wants to build its entire cloud platform from scratch. As a Senior Cloud Architect with 6+ years of experience, how would you approach the architecture and end-to-end implementation?"**

> "So basically, I would not start directly by creating AWS resources. My first step would be to understand the **business and application requirements**—traffic patterns, availability and performance requirements, security, compliance, RTO and RPO, expected growth, and budget.
>
> Once those requirements are clear, I would design the **AWS multi-account structure**, separating production, non-production, security, logging, and networking accounts where required. Then I would design the **networking layer**, including the VPC, public and private subnets, Availability Zones, routing, Internet Gateway, NAT Gateway, VPC endpoints, security groups, and network controls.
>
> Next, I would decide the appropriate **compute and application architecture** based on the workload—whether we should use EC2, ECS, EKS, Lambda, or a combination of services. I would also select the appropriate database, storage, load balancing, and caching services.
>
> From the beginning, I would implement everything using **Terraform**, including networking, compute, IAM, databases, monitoring, and security controls. This gives us version control, repeatability, and the ability to recreate environments consistently.
>
> Then I would build the **CI/CD and deployment architecture**, including source control, automated testing, security scanning, artifact or container management, deployment approvals, and rollback. For Kubernetes workloads, I could use Argo CD and GitOps.
>
> After that, I would implement **observability and security from day one**—CloudWatch, Prometheus, Grafana or Datadog, centralized logging, IAM least privilege, Secrets Manager, encryption, WAF, vulnerability scanning, and audit logging.
>
> Finally, I would design **high availability, autoscaling, backup, and disaster recovery**, and validate the architecture through testing and DR drills. So my approach would be **requirements → account strategy → networking → compute/application design → data layer → Terraform → CI/CD → security and monitoring → scaling and DR**, and then continuously improve the platform based on business needs."

This version sounds more like a **Senior Cloud Architect** because you're showing the interviewer that you start with requirements and business goals, then design the platform layer by layer rather than immediately talking about individual AWS services.


**3. "Your Lambda workload suddenly starts throttling and latency is increasing. How would you troubleshoot it?"**

> "So basically, first I'll check the **Lambda CloudWatch metrics**, especially **Invocations, Errors, Duration, Throttles, and ConcurrentExecutions**, to understand whether the issue is related to concurrency or the function itself.
>
> Then I'll check whether the function has reached its **reserved concurrency or account-level concurrency limit**. If throttling is happening because of concurrency, I'll review the configured limits and increase or tune them if required.
>
> At the same time, I'll check the **downstream dependencies** such as RDS, DynamoDB, other AWS services, or third-party APIs, because if those services are slow or rate-limiting requests, Lambda execution time can increase and cause concurrency to build up.
>
> I'll also review the function's **memory and timeout configuration**, because insufficient memory can increase execution time. Based on the bottleneck, I'll tune concurrency, memory, timeout, or the downstream integration.
>
> Finally, I'll monitor the Lambda metrics again to confirm that throttling and latency have returned to normal."

If the interviewer asks, **"What is the fixed Lambda concurrency limit?"**, don't give a hard number unless you're certain, because AWS quotas can vary by **Region/account and can be increased**.
> "There is an **account-level concurrent execution quota**, and Lambda also supports **reserved concurrency and provisioned concurrency** at the function level. I would verify the current quota for that AWS account and Region rather than assuming a fixed number."


**4. "The infrastructure looks healthy, but your website is slow and Time to First Byte (TTFB) is increasing. How would you investigate that properly?"**

> "So basically, if the website is slow even though the infrastructure looks healthy, I'll troubleshoot the **complete request path**, starting from DNS and CDN or load balancer, then the application, database, and any external dependencies.
>
> First, I'll compare the **latency, error rate, traffic patterns, and recent deployments** to identify when the issue started. Then I'll check the application logs and, if available, **APM traces** to find which part of the request is taking more time.
>
> I'll also check the **database performance**, especially slow queries, connection issues, or resource contention. If the database is the bottleneck, we can optimize the queries, introduce caching, or use read replicas depending on the requirement.
>
> At the same time, I'll check any **third-party or downstream services** the application depends on, because a slow external API can also increase the overall response time.
>
> Finally, I'll identify exactly which layer is causing the latency, fix or optimize that component, and monitor **TTFB, latency, and error rate** to confirm that the application performance has returned to normal."

### Interview Question

**"Your production workload is spread across multiple AWS accounts. How would you manage access and secure cross-account deployments?"**

> "So basically, in our current project we have **10 to 15 plus AWS accounts** across different environments like development, staging, and production. I avoid using long-lived IAM users and access keys for cross-account access.
>
> Instead, I create **IAM roles with cross-account trust relationships**, and the CI/CD pipeline assumes the required role in the target account for deployment. I also follow the **least-privilege principle**, so each role gets only the permissions required for that particular environment.
>
> For production, I add additional **approval controls** before deployment. And to maintain visibility and compliance, I enable **CloudTrail** and audit all cross-account activities.
>
> So the overall approach is **IAM Roles → Cross-Account AssumeRole → Least Privilege → CI/CD-based Access → Production Approval → CloudTrail Auditing**."
### Interview Question

**"We have an internal application in one AWS account, and we want another AWS account to access it. We don't want to expose it publicly. How would you design the networking?"**

> "So basically, I would keep the application completely **private** and expose it only through private AWS networking. Depending on the requirement, I would evaluate options like **VPC Peering, Transit Gateway, or AWS PrivateLink**. For a simple one-to-one connection, VPC Peering can work, while for multiple VPCs and accounts, Transit Gateway is more scalable. If I only want to expose a specific application or service without giving access to the entire VPC, I would prefer **PrivateLink**.
>
> Then I would configure the required **route tables, security groups, and network ACLs** so that only the necessary traffic and ports are allowed. I would follow the least-privilege approach and make sure the application is not reachable from the public internet.
>
> Finally, I would enable **VPC Flow Logs and other network logging** so that we can monitor, troubleshoot, and audit the connectivity."
### Interview Question

**"You need private connectivity between two AWS VPCs, but you discover that their CIDR ranges are overlapping. How would you approach this?"**

> "So basically, if both VPCs have **overlapping CIDR ranges**, direct **VPC Peering will not work** because AWS requires the VPC CIDR ranges to be non-overlapping for peering.
>
> First, I'll understand whether we need connectivity to the **entire VPC or only a specific application**. If we only need to expose a specific service privately, I'll prefer **AWS PrivateLink**, because it allows private access to that service without requiring full VPC-to-VPC routing.
>
> If broader connectivity is required, I'll evaluate whether we can **renumber or migrate one of the VPC CIDR ranges** as a long-term solution, especially if we control both environments. For example, if both are using `10.0.0.0/16`, we could migrate one VPC to a non-overlapping range.
>
> So my approach would be **PrivateLink for service-level connectivity, CIDR renumbering for long-term broader connectivity**, while avoiding direct VPC Peering with overlapping CIDRs."
### Interview Question

**"A production service has lost connectivity to a private service in another AWS account, but both sides appear healthy. How would you troubleshoot it?"**

> "So basically, first I'll identify whether the issue is limited to **one service or the entire network**, because that helps narrow down where the problem could be.
>
> Then I'll check the **cross-account networking configuration**, including route tables, security groups, network ACLs, and the connectivity mechanism such as VPC Peering, Transit Gateway, or PrivateLink.
>
> I'll also verify **DNS resolution** and make sure the application is resolving to the correct private IP, because an incorrect DNS record can also cause connectivity issues.
>
> Next, I'll check **VPC Flow Logs** to determine whether the traffic is reaching the destination and whether it's being accepted or rejected. I'll also review any **recent infrastructure, networking, or security changes** that could have introduced the issue.
>
> Once I identify where the packet is being dropped, I'll fix that layer and validate the connectivity end to end."
### Interview Question

**"A critical application component, such as a payment gateway, goes down during peak traffic. How would you make sure the application remains highly available?"**

> "So basically, first I'll identify whether that component is a **single point of failure**. If it is, I'll remove that dependency by running **multiple instances or replicas across multiple Availability Zones**.
>
> I'll configure proper **health checks and load balancing**, so if one instance becomes unhealthy, the load balancer automatically removes it from traffic and routes requests to the healthy instances.
>
> If the component depends on a database, I'll also make sure the database is highly available using the appropriate **Multi-AZ or replication strategy**, depending on the workload.
>
> For applications running on Kubernetes, I would use multiple pod replicas, proper readiness and liveness probes, and pod distribution across Availability Zones.
>
> Finally, I'll configure **monitoring and alerting** so we detect failures quickly and verify that traffic is automatically shifted to healthy components and the application continues to serve users during peak traffic."
### Interview Question

**"Your infrastructure is running, but one component is costing much more than expected even though CPU and memory utilization are only around 10%. How would you approach cost optimization?"**

### Better interview answer

> "So basically, I would start with **AWS Cost Explorer** to identify which service and resource are contributing the most to the cost. Then I'll compare the cost against the actual **CPU, memory, storage, network traffic, and utilization patterns** to understand whether we are over-provisioned or whether the cost is coming from something other than compute.
>
> I'll look for **over-sized instances, idle resources, unused EBS volumes, unnecessary NAT Gateway or data-transfer costs, old snapshots, and resources running outside business hours**. For non-production environments, I can schedule resources to stop when they are not required.
>
> For **EKS**, I'll review pod **CPU and memory requests and limits**, node utilization, and scaling configuration because over-provisioned requests can result in unnecessary nodes. I'll also evaluate **Cluster Autoscaler or Karpenter** to improve node utilization.
>
> For predictable production workloads, I'll evaluate **Savings Plans or Reserved Instances**, and for suitable fault-tolerant workloads, especially non-production, I'll consider **Spot Instances**.
>
> I'll make the changes gradually, starting with non-production, and continuously monitor both **cost and application performance**. The goal is not simply to reduce the bill, but to remove waste while maintaining the required reliability and performance."
### Question

**"It's Friday night, you deployed a new version to production, and after some time you find that the new version has an issue affecting only a small percentage of users. What would you do?"**

### Answer

> "So basically, since it's Friday night and only a small percentage of users are affected, first I will **stop the rollout** rather than continuing with the deployment. Then I will check whether the issue is related to a **specific region, instance, user group, or traffic pattern**.
>
> Since we prefer **Canary deployment**, I will compare the old and new versions using **metrics, logs, error rate, and latency**. For example, if we have deployed the new version to around 10% of the traffic and the error rate is increasing, I will quickly **shift the traffic back to the stable version** and make sure the application is healthy.
>
> Once the stable version is restored, I will investigate and try to **reproduce the issue in a lower environment**. I will also check the recent code or configuration changes to identify the root cause.
>
> After fixing the issue, I will test it properly and redeploy using the same controlled **Canary approach**. Finally, I will continue monitoring the application to make sure the issue doesn't happen again."
### Question

**"We have multiple production AWS accounts, and our CI/CD pipeline needs to authenticate into those accounts. Security is a major concern. How would you design this securely?"**

### Answer

> "So basically, I will **not hardcode or store long-lived AWS access keys and secret keys** anywhere in the CI/CD pipeline. Instead, I will configure an **OIDC trust relationship between the CI/CD platform and AWS**.
>
> The CI/CD platform will obtain a short-lived OIDC token and use it to **assume a specific IAM role** in the target AWS account. I would maintain separate IAM roles for different accounts and environments, such as development, staging, and production, and follow the **least-privilege principle**, so each role has only the permissions required for that particular deployment.
>
> For production, I can also add additional controls such as **approval gates** before assuming the production deployment role. I would enable **CloudTrail** and other audit logging to track which role was assumed, by whom, and what changes were made.
>
> So the overall approach is **OIDC → short-lived credentials → IAM role assumption → least privilege → environment-specific roles → production approval → CloudTrail auditing**."
### Question 1

**"We discovered a critical vulnerability in a Docker image that is already deployed across 50 services. How would you handle it without impacting production?"**

### Answer

> "So basically, first I will identify **exactly which services and image versions are affected** and understand the severity and exploitability of the vulnerability.
>
> Then I will **rebuild the base image with the patched dependencies** and run the required security and vulnerability scans to make sure the issue is completely resolved.
>
> Instead of manually changing all 50 services, I will update the **common image reference or base image** and trigger the automated CI/CD process for the affected services.
>
> Since this is a critical vulnerability, I will prioritize the production rollout, but I will use a **controlled deployment strategy like Canary or Rolling Update** so that we don't impact all users at once. I will monitor the application health, error rate, and logs during the rollout.
>
> Finally, I will verify that **no production workload is still running the vulnerable image**, and I'll document the remediation and perform a root-cause review."

---

### Question 2

**"The same application works successfully in one Kubernetes cluster but keeps failing in production. How would you isolate the issue?"**

### Answer

> "So basically, if the same application works in one cluster but fails in production, first I will compare the **pod status, exit codes, events, and application logs** in both clusters to understand where the failure starts.
>
> Then I'll compare the important configuration between both environments, such as **image versions, ConfigMaps, Secrets, environment variables, resource requests and limits, and deployment configuration**.
>
> After that, I'll check the **networking layer**, including DNS, Ingress, Services, RBAC, Network Policies, and node-level differences. I'll also verify whether production has any additional dependencies, security policies, or external services that are different from the working cluster.
>
> If everything still looks similar, I'll try to **reproduce the production conditions in the lower environment** and isolate the difference step by step. Once I identify the configuration or infrastructure difference causing the failure, I'll fix that specific layer and validate the application again in production."
### Question 1

**"Have you faced a situation where Kubernetes pods restart randomly, but there is nothing useful in the application logs? How would you troubleshoot it?"**

### Answer

> "So basically, yes, I've faced this kind of issue multiple times. First, I'll check the **pod status and restart count** using `kubectl get pods`, and then I'll use `kubectl describe pod` to check the events and termination reason.
>
> One of the common causes is **OOMKilled**, so I'll check the CPU and memory usage of both the pod and the node. I'll also check whether there is any **process failure, probe failure, node issue, or Kubernetes cluster event** causing the restart.
>
> If the container has already restarted, the normal logs may not show the previous failure, so I'll use **`kubectl logs --previous`** to check the logs from the previous container instance.
>
> I'll also check **kubelet and node-level events** to identify whether the restart is caused by the node or cluster itself. Once I identify the termination reason, I'll fix that specific issue and monitor the pod to confirm that the restarts have stopped."

### Question 2

**"Pods and nodes are healthy, but service-to-service latency inside Kubernetes is increasing. How would you troubleshoot it?"**

### Answer

> "So basically, if the pods and nodes are healthy but service-to-service latency is increasing, first I'll identify **which services are experiencing the latency** and whether the issue is within the same cluster, across namespaces, or across clusters.
>
> Then I'll check the **application metrics and distributed traces** to identify where the request is spending most of its time. On the Kubernetes networking side, I'll check the **CNI**, because it manages pod networking, and I'll verify **Network Policies** to make sure traffic isn't being restricted or delayed unexpectedly.
>
> I'll also check service and DNS resolution, network-level metrics, and any recent deployment or configuration changes that could have introduced the latency.
>
> Finally, I'll use **distributed tracing and network monitoring** to pinpoint the exact layer causing the delay, fix that component, and validate the service-to-service latency again."
### Question

**"Have you worked on upgrading Kubernetes clusters? What do you consider during a Kubernetes/EKS upgrade to minimize production impact and risk?"**

### Answer

> "So basically, yes, I've worked on upgrading Kubernetes clusters, including EKS and self-managed clusters. The first thing I would do is **check the supported upgrade path and version compatibility**, especially deprecated APIs, Kubernetes resources, addons, and application dependencies. I would avoid making a big version jump without validating the supported upgrade path.
>
> Then I would first test the complete upgrade process in a **non-production environment** and validate the workloads, APIs, ingress, networking, monitoring, and other addons.
>
> For EKS, I would **upgrade the control plane first**, because AWS manages the control plane, and then upgrade the worker nodes or node groups in a controlled manner. For self-managed Kubernetes, I would handle the control plane and worker-node upgrades myself.
>
> During the worker-node upgrade, I would use a **rolling approach**, drain nodes gradually, maintain sufficient pod capacity, and make sure replicas are distributed across Availability Zones. I would also verify **Pod Disruption Budgets, readiness probes, and resource capacity** so applications continue serving traffic.
>
> Finally, I would monitor the cluster and application after each stage, keep a **rollback or recovery plan**, and only proceed to the next stage after validating that everything is healthy."
### Question

**"Security has discovered that a few pods in a namespace are compromised and are communicating with other namespaces and external endpoints. How would you handle the incident?"**

### Answer

> "So basically, first I will **isolate the affected pod or workload** to contain the incident and prevent further communication. I will use **Kubernetes Network Policies** to restrict its communication with other namespaces and external endpoints.
>
> Then I will investigate the **pod logs, Kubernetes events, container image, and workload configuration** to understand what happened and whether there was any data exfiltration or suspicious activity.
>
> Since the pod may have been compromised, I will also identify and **rotate any credentials, Secrets, or tokens** that may have been exposed. At the same time, I will check whether any other workloads or namespaces have been affected.
>
> After containment, I will redeploy the affected workload using a **trusted and verified image** rather than continuing to use the compromised pod. Then I will perform the root-cause analysis and strengthen the security controls.
>
> For prevention, I can use **image-signing or admission policies** to allow only approved images, and tools like **Falco** for runtime threat detection and monitoring. I would also review RBAC, Network Policies, and pod security controls to prevent the same type of lateral movement in the future."
### Question 1

**"We want our Kubernetes pods to pull container images only from a specific approved repository. How would you enforce that?"**

### Answer

> "So basically, we can enforce this using an **admission control policy**. In our environment, we can configure a policy using a tool like **Kyverno** to allow images only from approved registries or repositories. For example, we can define a policy that allows images only from our approved ECR account or repository, and blocks images coming from any other registry.
>
> So even if someone tries to deploy an image like Alpine or Ubuntu directly from Docker Hub, the admission policy will reject that deployment unless it comes from the approved repository. This helps us enforce **image-source control, security, and compliance** across the cluster."

### Question 2

**"What are Terraform modules, and how would you structure Terraform to deploy the same infrastructure across 22 AWS accounts and multiple regions?"**

### Answer

> "So basically, a **Terraform module** is a reusable collection of Terraform resources that we can use across multiple environments instead of duplicating the same code. For example, if we have a common VPC design, I can create one reusable VPC module and call it from different accounts, regions, and environments.
>
> For 22 AWS accounts and multiple regions, I would keep the **common infrastructure logic inside reusable modules** and keep the **account- and region-specific configuration outside the modules**.
>
> Then I would have separate environment or account-level configurations that call those modules with the required variables, such as account ID, region, CIDR ranges, and environment-specific settings.
>
> I would maintain a **separate Terraform state for each account and region** to provide proper isolation. The CI/CD pipeline would assume the appropriate **IAM role in each target account** and execute Terraform for that specific environment.
>
> Everything would be deployed through Terraform and CI/CD rather than manually, which gives us **reusability, consistency, isolation, and centralized control** across all 22 accounts and multiple regions."
### Interview Question

**"Your Terraform state is stored in S3 and manages resources across multiple AWS accounts. How would you secure the Terraform state and access model?"**

### Answer

> "So basically, I will store the Terraform state in a **centralized remote S3 backend** and enable **encryption** for the state file. I will restrict access to the bucket using **IAM roles and least-privilege permissions**, so only the required CI/CD role or authorized engineers can access it.
>
> Since we are managing multiple AWS accounts and environments, I would maintain **separate state files for each account and environment** to provide proper isolation and avoid one environment affecting another.
>
> I would also enable **S3 versioning** so that if the state is accidentally modified or deleted, we can recover a previous version. For state locking, I would use the supported Terraform locking mechanism so that concurrent Terraform operations don't modify the same state simultaneously.
>
> Finally, I would ensure Terraform operations go through the **CI/CD pipeline**, use short-lived or assumed IAM roles where possible, and enable **CloudTrail and S3 access logging** for auditing who accessed or modified the state."

### Interview Question

**"We have two Terraform modules with a circular dependency. How would you redesign them?"**

### Answer

> "So basically, if two Terraform modules have a **circular dependency**, it means both modules are depending on each other, so Terraform cannot determine a proper creation order. First, I will identify why the two modules are tightly coupled.
>
> Then I would **redesign the modules to keep the dependency flow one-directional**. If both modules need some common resource or value, I would extract that common dependency into a **separate module** and pass the required values between the modules through outputs and inputs.
>
> I would also avoid unnecessary `depends_on` just to force an execution order, because Terraform should normally determine dependencies automatically from resource references.
>
> Finally, I would run `terraform plan` and review the dependency graph to make sure the circular dependency is removed and the infrastructure can be created and updated in the correct order."
### Question 1

**"You just ran `terraform apply`, and it's taking around 45 minutes. What would be your first thought, and how would you troubleshoot it?"**

### Answer

> "So basically, first I would identify **which resource or operation is actually taking the most time**, rather than assuming Terraform itself is slow. I would check the Terraform output and the AWS resources being created or updated to see where the delay is happening.
>
> Then I would check whether any **AWS API throttling or dependency issue** is causing delays, and review the Terraform dependency graph to understand whether resources are being created sequentially because of unnecessary dependencies.
>
> I would also check whether we're creating too many resources in a single deployment and consider **splitting the deployment into smaller stacks or stages**. At the same time, I would check whether multiple Terraform pipelines are running against the same AWS account simultaneously.
>
> I would review the Terraform structure and parallelism settings, but I wouldn't simply increase retries or parallelism without understanding the bottleneck. The goal is to identify the actual slow resource or dependency and optimize that part."

### Question 2

**"How would you provide Databricks workloads access to an S3 bucket using Unity Catalog?"**

### Answer

> "So basically, with **Unity Catalog**, I would create a **storage credential** using an appropriate AWS IAM role that has the required S3 permissions. Then I would create an **external location** in Unity Catalog that points to the required S3 bucket or path and associates it with that storage credential.
>
> After that, I would grant the required permissions on the external location to the appropriate users, groups, or workloads. So the main components are **Storage Credential → IAM Role → External Location → S3 Bucket**, and then we control access through Unity Catalog permissions.
>
> Finally, I would validate that the required Databricks workload can access only the intended S3 location and doesn't have unnecessary permissions."

### Question 3

**"Your application runs in a single AWS Region, and the entire region goes down. Management expects the application to be available in another region within 30 minutes. How would you design the DR strategy?"**

### Answer

> "So basically, the first thing I would define is the required **RTO of 30 minutes and RPO**, because that determines the appropriate DR architecture.
>
> Then I would identify the critical components that need to be available in the secondary region, such as the application, database, storage, networking, and supporting services. I would manage the secondary infrastructure through **Terraform**, so it can be provisioned consistently and quickly.
>
> For data, I would use the appropriate **cross-region replication strategy**, such as database cross-region replication and S3 Cross-Region Replication. For compute-based workloads, I would maintain the required images or deployment artifacts in the DR region.
>
> During a regional failure, I would use **Route 53 failover or AWS Global Accelerator** to redirect traffic to the secondary region. We would regularly perform **DR drills**, validate the recovery process against the 30-minute RTO, and monitor the recovered application.
>
> Once the primary region is restored, I would validate it and perform a **controlled failback**."
