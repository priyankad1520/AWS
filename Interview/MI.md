**"Your company has decided to migrate an application from EC2 to Kubernetes. How will you decide whether Kubernetes is the right choice?"**


> "Before moving to Kubernetes, first I will understand the current application and the problem we are trying to solve. Then I'll check whether the application can be containerized without major code changes. After that, I'll compare Kubernetes benefits like auto-scaling, self-healing, and zero-downtime deployments. Along with that, I'll also consider operational complexity and additional cost. If the benefits justify the cost, I'll perform a Proof of Concept with a non-production application. If the POC is successful, I'll prepare the documentation and recommend migrating to Kubernetes."


> "First, I won't assume Kubernetes is the right solution. I'll first understand the current application, its traffic pattern, availability requirements, deployment frequency, and the existing challenges on EC2.
>
> Then I'll evaluate whether the application is suitable for containerization. For example, I'll check its dependencies, whether it's stateless or stateful, how it handles sessions, storage requirements, and whether any code changes are required.
>
> Next, I'll compare the business benefits of Kubernetes. If the application requires automatic scaling, self-healing, rolling or blue-green deployments, better resource utilization, and supports a microservices architecture, then Kubernetes becomes a strong choice.
>
> At the same time, I'll evaluate the operational overhead. Kubernetes introduces additional complexity in cluster management, monitoring, networking, security, and cost. So the business benefits should clearly justify that investment.
>
> Before recommending migration, I'll perform a Proof of Concept on a non-production application, validate performance, deployment, monitoring, and rollback strategy. If the POC is successful and the expected benefits are achieved, I'll prepare a migration plan and recommend moving the application to Kubernetes."

**"When would you NOT recommend Kubernetes?"**
> "I wouldn't recommend Kubernetes for a small monolithic application with stable traffic, infrequent deployments, and a small team. In that case, EC2 with Auto Scaling would be simpler, cheaper, and easier to maintain. Kubernetes should be chosen only when its scalability, automation, and operational benefits outweigh its complexity and cost."

**Now you've decided Kubernetes is the right choice. How would you plan the migration to ensure there is no downtime for end users?**
> "First, I will containerize the application and test it thoroughly. Then I'll set up the Kubernetes infrastructure like EKS, AKS, or GKE, along with networking, ingress, and storage. Next, I'll deploy the application in a non-production environment and perform security and compliance testing. Then I'll configure the CI/CD pipeline for automated deployments. During production migration, I'll use Blue-Green or Canary deployment instead of switching all traffic at once. I'll continuously monitor logs, metrics, and application health, and I'll keep a rollback plan ready to redirect traffic back to the EC2 environment if any issues occur."Finally, I'll keep a tested rollback plan so that if any issue is detected, traffic can immediately be redirected back to the stable EC2 environment with minimal impact to users."

**After migration, deployments become slower than they were on EC2. How would you troubleshoot it?**
> "First, I'll identify where the delay is happening because Kubernetes itself doesn't make deployments slower.I'll start by checking the CI/CD pipeline to see whether the delay is during image build, image push, or Kubernetes deployment.

Next, I'll verify the Docker image size. Large images increase pull time, so I'll optimize the Dockerfile using multi-stage builds and lightweight base images.

Then I'll inspect the Kubernetes cluster. I'll check whether pods are stuck in Pending, whether nodes have sufficient CPU and memory, and whether the scheduler is waiting for resources.

I'll also review readiness probes because if they take too long to succeed, Kubernetes waits before marking pods as Ready.

Finally, I'll review cluster metrics, image pull times, events, and whether Cluster Autoscaler is scaling nodes quickly enough. Based on the findings, I'll optimize the specific bottleneck instead of assuming Kubernetes is the problem."

**During deployment, all old pods were terminated before the new pods became ready, causing downtime. How would you prevent this in the future?**

> "This usually happens because Kubernetes removes old pods before new pods are ready, often due to an incorrect RollingUpdate configuration.
>
> First, I'll configure a proper **readiness probe** so Kubernetes sends traffic only to healthy pods.
>
> Then I'll use the **RollingUpdate** strategy with appropriate `maxSurge` and `maxUnavailable` values. For example, I can set `maxUnavailable: 0` so Kubernetes never removes existing pods until replacement pods are ready.
>
> I'll also configure a **Pod Disruption Budget** to ensure a minimum number of pods remain available during deployments or node maintenance.
>
> For business-critical applications, I'll use **Canary** or **Blue-Green deployments** to gradually shift traffic while continuously monitoring the application.
>
> Finally, I'll validate the deployment in a staging environment and keep a rollback strategy ready so any issue can be reverted immediately."

---
If they ask, **"What values would you use?"**, give a concrete example:

```yaml
strategy:
  type: RollingUpdate
  rollingUpdate:
    maxUnavailable: 0
    maxSurge: 1
```
* **maxUnavailable: 0** → Never reduce the current number of available pods.
* **maxSurge: 1** → Create one extra pod before terminating an old one.


**Some applications should not run together on the same node because they consume too much CPU. How would you ensure proper placement across nodes?**

> "If we have multiple pods and we don't want two pods to be scheduled on the same node, we can use **Pod Anti-Affinity**. It ensures that when one pod is scheduled on a node, similar pods are scheduled on different nodes. If an application must run only on a specific node, I'll label that node and use **Node Selector** or **Node Affinity** in the pod specification."

> "The solution depends on the requirement.
>
> If I want to prevent certain application pods from running on the same node, I'll use **Pod Anti-Affinity**. This tells the Kubernetes scheduler to place matching pods on different nodes, which helps avoid CPU or memory contention.
>
> If an application must run only on specific nodes, for example GPU nodes or high-memory nodes, I'll label those nodes and use **Node Affinity** or **Node Selector** to schedule the pods there.
>
> If I want to prevent workloads from running on certain nodes completely, such as dedicated database nodes, I'll use **Taints** on the nodes and **Tolerations** only for the workloads that are allowed to run there.
>
> This combination gives me full control over workload placement while improving performance and resource utilization."


* **Node Selector** → Simple scheduling.
* **Node Affinity** → Advanced scheduling with rules.
* **Pod Affinity** → Keep pods together.
* **Pod Anti-Affinity** → Separate pods.
* **Taints & Tolerations** → Keep unwanted pods away.

**A developer requests shell access to a production pod for debugging. Would you allow it?**

> "No, I wouldn't allow direct shell access by default because of security and compliance risks. First, I'd ask the developer to use logs, metrics, Prometheus, Grafana, or Datadog. If shell access is absolutely required, I'd provide temporary access after approval, audit all activities, and revoke the access once debugging is complete."


> "By default, I wouldn't allow shell access to production pods because it introduces security, compliance, and operational risks.
>
> First, I'd ask the developer to troubleshoot using application logs, Kubernetes events, metrics, and monitoring tools like Prometheus, Grafana, CloudWatch, or Datadog.
>
> If that's not sufficient and interactive debugging is genuinely required, I'd follow the organization's access control process. After obtaining the necessary approvals, I'd provide time-bound, least-privilege access, ensure all actions are audited, and revoke the access immediately after debugging is complete.
>
> This approach balances operational needs with production security."


**Your Docker registry becomes unavailable during a production deployment. What impact would you expect?**

> "First, I'll check whether the required Docker image already exists on the worker nodes. If it's already cached, the existing pods continue running. However, if Kubernetes needs to start new pods or deploy a new version, the deployment fails because it can't pull the image. To reduce this risk, I'll use a highly available registry like ECR, enable image caching where possible, and maintain a disaster recovery strategy with registry replication across regions."

> "The impact depends on whether the required container image is already available on the worker nodes.
>
> Existing running pods won't be affected because the image has already been pulled.
>
> However, any new pod creation, rolling deployment, autoscaling event, or pod restart that requires pulling the image will fail with an **ImagePullBackOff** or **ErrImagePull** error.
>
> To minimize this risk, I'd use a highly available private registry such as Amazon ECR, enable cross-region replication for disaster recovery, and rely on image caching on worker nodes where appropriate.
>
> I'd also monitor registry availability and keep rollback procedures ready so that production deployments aren't blocked during a registry outage."


**Interviewer:** *"If the registry is down, why are the existing pods still running?"*

> "Because the container image has already been downloaded to the node and the container is already running. Kubernetes doesn't need to contact the registry again unless it has to start a new pod or pull a different image."

**One of your teammates accidentally deleted the production namespace. What will you do?**
> "First, I'll stop any ongoing deployments or changes to avoid further impact. Then I'll check whether we have a backup solution like Velero. If a backup exists, I'll restore the production namespace and its resources. If no backup is available, I'll recreate the namespace and redeploy the workloads from the Git repository using Argo CD since all Kubernetes manifests are version-controlled. After restoration, I'll verify that all applications are healthy. Finally, I'll perform an RCA and implement RBAC, approval workflows, and backup policies to prevent the same incident."


> "First, I'll treat it as a production incident and immediately stop any ongoing deployments or manual changes to prevent further impact.
>
> Then I'll assess the impact by identifying which applications and services are affected and inform the stakeholders.
>
> If we have a backup solution like **Velero**, I'll restore the deleted namespace and Kubernetes resources from the latest backup.
>
> If a backup isn't available, I'll recreate the namespace and restore the workloads from Git because our Kubernetes manifests and Helm charts are stored in Git and synchronized through Argo CD. That allows us to rebuild the environment quickly.
>
> After the restoration, I'll verify that all pods, services, ingress resources, ConfigMaps, Secrets, and application health are working correctly.
>
> Finally, I'll perform an RCA and strengthen preventive controls by implementing stricter RBAC permissions, namespace deletion protection, regular backup validation, and approval processes for production changes."


**Six months after migration, management asks whether Kubernetes delivered value. What KPIs would you present?**

> "I'll compare deployment time before and after migration. I'll measure application availability, resource utilization, infrastructure cost, traffic handling capability, deployment success rate, rollout frequency, and MTTR."


> "I'll present both technical and business KPIs.
>
> From a deployment perspective, I'll compare deployment frequency, deployment duration, deployment success rate, and rollback frequency before and after migration.
>
> From an operations perspective, I'll present application availability, MTTR, incident count, and production stability.
>
> I'll also compare infrastructure utilization by looking at CPU and memory efficiency, autoscaling performance during traffic spikes, and overall infrastructure cost.
>
> Finally, I'll highlight business outcomes such as faster release cycles, reduced downtime, improved scalability, and better customer experience. If these metrics have improved after migration, it clearly demonstrates that Kubernetes has delivered value to the organization."

---

# KPIs to remember for interviews

A simple way to organize them is into four groups:

### 1. Delivery Metrics

* Deployment frequency
* Deployment time
* Deployment success rate
* Rollback frequency

### 2. Reliability Metrics

* Availability (uptime)
* MTTR
* MTBF
* Incident count

### 3. Infrastructure Metrics

* CPU utilization
* Memory utilization
* Autoscaling effectiveness
* Infrastructure cost

### 4. Business Metrics

* Faster feature delivery
* Improved customer experience
* Reduced downtime
* Better scalability during peak traffic

---

**"Which KPI is the most important?"**

> "It depends on the business objective. If the goal was faster software delivery, I'd focus on deployment frequency and deployment time. If the goal was improving reliability, I'd highlight availability, MTTR, and incident reduction. If the goal was cost optimization, I'd present infrastructure utilization and cloud cost savings. I always align the KPIs with the original migration objectives."


**Your CI/CD pipeline shows the deployment was successful, but some users still see the old version of the application. What could be the reason?**

> "First, I'll verify whether the rollout has completed and whether all pods have been updated. Then I'll check whether the Kubernetes Service is routing traffic correctly to the new pods. Next, I'll check browser cache, CDN cache, or any caching layer because users might still be receiving cached content. Finally, if we're using Canary or Blue-Green deployment, it's expected that some users see the old version until the traffic migration is complete."

> "A successful CI/CD pipeline only confirms that the deployment process completed successfully; it doesn't guarantee that every user is already using the new version.
>
> First, I'll verify whether the Kubernetes rollout has completed successfully by checking that all new pods are running and Ready.
>
> Next, I'll confirm that the Service or Ingress is routing traffic to the updated pods correctly.
>
> Then I'll check whether we're using a Canary or Blue-Green deployment, because during a gradual rollout it's expected that some users still access the previous version.
>
> I'll also investigate caching layers such as the browser cache, CDN, reverse proxy, or application cache, since stale cached content can cause users to see the old version.
>
> Finally, I'll verify DNS, load balancer health, and pod versions to ensure traffic is reaching the intended application version."



**How would you design your CI/CD pipeline so a bad deployment never reaches production directly?**

> "We can't guarantee that a bad deployment will never reach production, but we can minimize the risk. I'll add unit tests, security testing, image scanning, validate deployments in lower environments, require manual approval before production if needed, and use Canary or Blue-Green deployments."


> "It's practically impossible to guarantee that a faulty deployment will never reach production, but we can significantly reduce the risk by introducing multiple quality gates.
>
> First, the pipeline should run automated unit tests, integration tests, and static code analysis.
>
> Next, I'll perform container image scanning and dependency vulnerability scanning before publishing the image.
>
> After that, the application will be deployed to development or staging environments where functional and smoke tests are executed automatically.
>
> Before production, I'll include a manual approval step for critical applications, followed by a progressive deployment strategy such as Canary or Blue-Green.
>
> Finally, I'll continuously monitor the deployment, and if any health checks fail, the pipeline should automatically trigger a rollback."


**You have 50+ microservices. Would you create a separate CI/CD pipeline for each one?**


> "Yes, generally I create a separate pipeline for each microservice because they should be deployed independently. To avoid duplication, I use a reusable pipeline template so every service shares the same pipeline logic with different configurations. This follows the DRY principle."


> "Yes. In most projects, each microservice has its own CI/CD pipeline because every service has an independent lifecycle, different release schedule, and separate rollback requirements.
>
> However, I wouldn't duplicate the pipeline logic across all repositories. Instead, I'd create a reusable pipeline template or a Jenkins Shared Library that contains the common stages such as checkout, build, test, image creation, image scanning, and deployment.
>
> Each microservice pipeline simply calls the shared template while passing service-specific parameters like the repository, Docker image name, or deployment configuration.
>
> This approach keeps the pipelines consistent, easier to maintain, and follows the DRY principle while still allowing each service to be deployed independently."

**Interviewer:** *"Why not use one pipeline for all 50 microservices?"*

> "Using a single pipeline for all microservices creates unnecessary dependencies. If one service fails to build or deploy, it can block the release of unrelated services. It also makes rollbacks, troubleshooting, and release management more difficult. Independent pipelines allow teams to build, test, deploy, and roll back each service without affecting the others."


**Your company decided to migrate CI/CD pipelines from Jenkins to GitHub Actions. How would you ensure a smooth migration without affecting existing deployments?**
> "First, I'll understand the existing Jenkins pipelines, plugins, integrations, and deployment process. Then I'll recreate the same pipeline in GitHub Actions. I'll migrate one non-critical application first as a POC. After that, I'll run Jenkins and GitHub Actions in parallel for some time and compare the results. Once the new pipeline is stable, I'll gradually migrate the remaining applications while keeping Jenkins as a rollback option."

> "I'll approach the migration incrementally rather than migrating all pipelines at once.
>
> First, I'll analyze the existing Jenkins pipelines, including stages, plugins, credentials, shared libraries, deployment process, and external integrations.
>
> Next, I'll recreate the same workflow in GitHub Actions using reusable workflows and GitHub Secrets while ensuring feature parity.
>
> Before migrating production applications, I'll select a low-risk service for a proof of concept and validate that the build, test, artifact creation, and deployment behave exactly like Jenkins.
>
> During the transition, I'll run Jenkins and GitHub Actions in parallel and compare their outputs. Only after the new pipeline proves stable will I migrate the remaining services in phases.
>
> Throughout the migration, I'll monitor deployments closely and keep Jenkins available as a rollback option until all applications are successfully migrated."


**Your application is deployed to both AWS and Azure. The AWS deployment succeeds, but Azure fails. How should the pipeline handle this?**

> "I'll stop the pipeline and identify why Azure failed. I won't mark the deployment as successful until both deployments succeed. If AWS is already running the new version, I'll either roll it back or keep it based on business requirements. After fixing Azure, I'll rerun the deployment and verify both environments are healthy."


> "The release shouldn't be considered successful until both cloud environments are in the expected state.
>
> First, the pipeline should immediately stop when the Azure deployment fails and report the failure.
>
> Then I'll investigate the Azure issue using deployment logs, application logs, and infrastructure events.
>
> If both environments are required to run the same application version, I'll roll back the successful AWS deployment to maintain version consistency.
>
> If the business allows temporary version differences, I'll keep AWS running the new version while fixing Azure, but only after stakeholder approval.
>
> Once Azure is fixed, I'll redeploy, validate both environments through health checks, and only then mark the release as successful."


**Your organization wants to manage manually created AWS resources using Terraform. How would you migrate them?**

> "First, I'll identify the existing AWS resources. Then I'll write Terraform code for those resources. I'll use `terraform import` to import them into the Terraform state instead of recreating them. After that, I'll repeatedly run `terraform plan` and update the code until it shows 'No changes'. Finally, Terraform becomes the source of truth."


> "I'll start by discovering and documenting the existing AWS resources that need to be managed.
>
> Then I'll write Terraform configuration that accurately represents the current infrastructure.
>
> Instead of recreating the resources, I'll use `terraform import` to associate each existing resource with the Terraform state file.
>
> After importing, I'll run `terraform plan` to identify configuration differences. If Terraform proposes unexpected changes, I'll update the code until the plan shows **No changes**, confirming that the configuration matches the actual infrastructure.
>
> Once validation is complete, Terraform becomes the single source of truth, and all future infrastructure changes are managed through code."


**Interviewer:** *"Why do you run `terraform plan` multiple times after import?"*

> "Because `terraform import` only adds the resource to the Terraform state. It doesn't generate the Terraform configuration. After writing the configuration, I run `terraform plan` repeatedly to identify differences between the code and the existing infrastructure. I continue refining the configuration until the plan shows **No changes**, ensuring Terraform won't modify production resources unexpectedly."

**How do you prevent multiple engineers from making Terraform changes to the same environment simultaneously?**
> "I'll use a remote backend like S3 to store the Terraform state file and enable state locking using DynamoDB so only one Terraform operation can run at a time. I'll make all Terraform changes through the CI/CD pipeline instead of manual execution. Different environments will have separate state files or workspaces, and production changes will require code review and approval."

> "The first step is to use a remote backend, such as an S3 bucket, to store the Terraform state centrally, and enable **DynamoDB state locking** so only one Terraform operation can modify the state at a time.
>
> Next, I avoid running Terraform manually on engineers' laptops. Instead, all changes go through a CI/CD pipeline, ensuring consistent execution and preventing concurrent applies.
>
> I also maintain separate state files or workspaces for different environments like Development, QA, and Production to isolate changes.
>
> Finally, every infrastructure change goes through pull requests, code reviews, and approval before `terraform apply` is executed. This combination prevents conflicts and protects production infrastructure."

**Interviewer:** *"What happens if two engineers run `terraform apply` at the same time?"*
> "The first engineer acquires the state lock in DynamoDB. When the second engineer runs `terraform apply`, Terraform detects that the state is locked and waits or fails with a state-lock message. This prevents simultaneous modifications and protects the state file from corruption."


**You need to provision infrastructure across AWS, Azure, and GCP using Terraform. How would you organize the codebase?**

> "I'll separate the code by cloud provider while maintaining a common repository structure. I'll create reusable Terraform modules for common components such as networking, security, compute, and storage. Environment-specific values will be managed using variable files. Each cloud and environment will have its own remote state file with state locking, and deployments will be handled through the CI/CD pipeline."

> "I'll organize the repository with a modular structure.
>
> Common infrastructure components such as VPCs, networking, IAM, storage, and compute will be implemented as reusable Terraform modules.
>
> Then I'll create separate environment folders for AWS, Azure, and GCP, each containing the provider configuration, backend configuration, and environment-specific variable files.
>
> Every cloud and every environment will have its own remote state to avoid conflicts, and deployments will be executed through a CI/CD pipeline with state locking and code review.
>
> This structure maximizes code reuse while keeping cloud-specific configurations isolated and easy to maintain."

**How would you prevent a developer from accidentally deleting production resources using Terraform?**

> "I'll follow the least-privilege principle using IAM roles, require all changes to go through the CI/CD pipeline with code reviews and approvals, and use the Terraform lifecycle block with `prevent_destroy = true` for critical resources."

> "I'll protect production resources using multiple layers of control.
>
> First, I'll enforce least-privilege IAM permissions so only authorized users or pipelines can modify production.
>
> Second, all Terraform changes must go through pull requests, code reviews, and approval workflows before deployment.
>
> For critical resources such as production databases, EKS clusters, or load balancers, I'll use the Terraform lifecycle block with `prevent_destroy = true`, which prevents accidental deletion even if someone modifies the code.
>
> Finally, I'll review the Terraform plan before every apply and execute production changes only through the CI/CD pipeline."


**Interviewer:** *"What is `prevent_destroy`?"*
> "`prevent_destroy` is a Terraform lifecycle setting. When it's enabled, Terraform refuses to destroy that resource. Even if someone runs `terraform destroy` or removes the resource from the configuration, Terraform returns an error instead of deleting it."


**Your company wants to reduce AWS costs by 40% without affecting application performance. Where would you start?**

> "I'll analyze AWS Cost Explorer to identify the biggest cost contributors. Then I'll right-size EC2 instances, EKS nodes, RDS, and storage. I'll remove idle resources, configure autoscaling, use Cluster Autoscaler or Karpenter for Kubernetes, use Spot Instances for non-production workloads, consider Savings Plans or Reserved Instances, and continuously monitor cost and performance."

> "I'll start with a data-driven approach rather than making changes immediately.
>
> First, I'll use AWS Cost Explorer and CloudWatch to identify the services contributing the most to the monthly bill.
>
> Then I'll look for over-provisioned resources such as EC2 instances, EKS worker nodes, RDS databases, EBS volumes, and load balancers, and right-size them based on actual CPU and memory utilization.
>
> Next, I'll remove unused resources such as unattached EBS volumes, idle Elastic IPs, old snapshots, and unused load balancers.
>
> For Kubernetes workloads, I'll optimize resource requests and limits, enable Cluster Autoscaler or Karpenter, and use Spot Instances for suitable non-production or fault-tolerant workloads.
>
> Finally, I'll evaluate Savings Plans or Reserved Instances for predictable workloads and continuously monitor both cost and application performance to ensure optimization doesn't impact users."

---

# FinOps framework to remember
1. **Analyze** – Cost Explorer, CUR, CloudWatch.
2. **Optimize** – Right-size, remove waste.
3. **Automate** – Auto Scaling, Cluster Autoscaler, Karpenter.
4. **Purchase optimization** – Savings Plans, Reserved Instances, Spot Instances.
5. **Govern** – Tagging, budgets, alerts, continuous monitoring.

**Your primary AWS region suddenly becomes unavailable. How will your application recover?**

> "We'll already have a Disaster Recovery setup in another AWS region. If the primary region fails, traffic will be redirected using Route 53 or AWS Global Accelerator. I'll verify that the application, database, and dependencies are healthy in the DR region. If required, I'll restore the latest backup or rely on cross-region replication. Once the primary region is restored, I'll validate it and perform a controlled failback."

> "Disaster recovery should already be planned before a failure occurs.
>
> We'll maintain a secondary AWS region with the required infrastructure, application, and database replication.
>
> If the primary region becomes unavailable, Route 53 failover routing or AWS Global Accelerator will redirect user traffic to the secondary region automatically.
>
> I'll verify that the application, databases, and supporting services are healthy in the DR region and confirm that data replication is up to date. If necessary, I'll restore from the latest backup or use cross-region replicas to minimize data loss.
>
> After the primary region is stable again, I'll validate it thoroughly and perform a controlled failback during a maintenance window."

---

**Walk me through your first 30 minutes after receiving a P1 production incident.**

> "I'll acknowledge the alert, assess the impact, join the incident bridge, notify the required teams, check dashboards, logs, metrics, and recent deployments. If a recent deployment caused the issue, I'll roll it back. Once the service is restored, I'll continue RCA and implement preventive actions."


> "During the first 30 minutes, my priority is service restoration rather than finding the root cause.
>
> First, I'll acknowledge the alert, assess the business impact, and identify which applications or customers are affected.
>
> Next, I'll join the incident bridge, notify the relevant teams such as developers, infrastructure, database, and management, and assign clear ownership.
>
> Then I'll review dashboards, logs, metrics, Kubernetes events, CloudWatch alerts, and any recent deployments or infrastructure changes.
>
> If a recent deployment is identified as the cause, I'll immediately roll it back to restore service as quickly as possible.
>
> Once the application is stable, I'll continue investigating the root cause, monitor the platform closely, and later conduct a formal RCA with preventive actions."

---

## Interview tip

For any **P1/P0 incident**, remember this order:

1. Acknowledge
2. Assess impact
3. Communicate
4. Mitigate/Restore
5. Investigate
6. RCA
7. Prevention


**If you join as a Senior DevOps Engineer and are given ownership of the platform, what are the first three improvements you would look for?**

> "First, I'll understand the existing platform, architecture, CI/CD, monitoring, security, backup, and disaster recovery. Then I'll identify pain points, technical debt, automation gaps, cost optimization opportunities, performance bottlenecks, and gather feedback from developers. Finally, I'll prioritize improvements based on business impact."

> "Before making any changes, my first priority is to understand the current platform thoroughly.
>
> First, I'll review the architecture, CI/CD pipelines, Kubernetes environment, monitoring, security, backup strategy, and disaster recovery process to understand how the platform operates today.
>
> Second, I'll identify operational pain points such as recurring incidents, manual processes, technical debt, performance bottlenecks, security risks, and cost optimization opportunities. I'll also gather feedback from developers and operations teams.
>
> Finally, I'll prioritize improvements based on business impact, reliability, and risk. Rather than making immediate changes, I'll create a roadmap so that improvements are implemented in a controlled and measurable way."


**Do you have any questions for me?**
> "Yes, I have a couple of questions. Since I understand the team is working on Kubernetes migration, I'd like to know what the biggest technical challenge is today. Is it application modernization, operational complexity, or something else? Also, what would success look like for the person joining this role in the first six months?"


## 38. What is your expertise in AWS? Which AWS services and tools have you worked on?

“I have hands-on experience with **AWS**, mainly in infrastructure provisioning, deployment, containerization, and monitoring. I have worked with **VPC, EC2, IAM, S3, ECR, ECS, EKS, RDS, Lambda, ALB, CloudWatch, Internet Gateway, NAT Gateway, Route 53, Security Groups, and NACLs**. On the DevOps side, I have worked with **Terraform, Jenkins, Docker, Kubernetes, Helm, Argo CD, and Git**. My main focus is infrastructure maintenance, CI/CD, Kubernetes deployments, and Infrastructure as Code.”

**Simple flow:** `Terraform → AWS Infrastructure → Jenkins CI/CD → Docker → ECR → EKS/ECS → CloudWatch`

---

## 39. Have you provisioned any VPC?

“Yes, I have provisioned **VPCs using Terraform**. I create the **VPC CIDR**, **public and private subnets** across multiple **Availability Zones**, **route tables**, **Internet Gateway**, **NAT Gateway**, **Security Groups**, and **NACLs**. For production, I focus on **high availability**, network segmentation, and secure access to private resources.”

**Simple flow:** `Terraform → VPC → Public/Private Subnets → Route Tables → IGW/NAT Gateway → Security Groups/NACLs`

---

## 40. What exactly do we use an Internet Gateway and NAT Gateway for?

“An **Internet Gateway (IGW)** provides internet connectivity for resources in a **public subnet**. A **NAT Gateway** provides **outbound internet access** to resources in a **private subnet** without allowing direct inbound internet connections to those resources. The NAT Gateway is deployed in a public subnet.”

**Simple flow:** `Public Subnet → Route Table → IGW → Internet` | `Private Subnet → Route Table → NAT Gateway → IGW → Internet`

---

## 41. Why do we use a route table?

“A **route table** controls how **network traffic** is routed within a VPC. It contains **destination CIDR blocks** and their corresponding **targets**. Depending on the requirement, the target can be an **Internet Gateway, NAT Gateway, VPC Peering Connection, or Transit Gateway**. Each subnet is associated with a route table that determines its routing behavior.”

**Simple flow:** `Subnet → Route Table → Destination CIDR → Target → Destination`

---

## 42. What is a load balancer? What are the types and what are they used for?

“An AWS **Load Balancer** distributes incoming traffic across multiple **healthy targets**, which improves **availability, scalability, and fault tolerance**.

An **Application Load Balancer (ALB)** works at **Layer 7** and is mainly used for HTTP/HTTPS applications. It supports **path-based and host-based routing**.

A **Network Load Balancer (NLB)** works at **Layer 4** and is used for TCP, UDP, and TLS traffic where we need **high performance and low latency**.

A **Gateway Load Balancer (GWLB)** is used to deploy and scale **network virtual appliances**, such as firewalls.

**Classic Load Balancer (CLB)** is a legacy option and is generally not preferred for new applications.”

**Simple flow:** `Client → Load Balancer → Healthy Target` | `ALB → Layer 7` | `NLB → Layer 4` | `GWLB → Network Appliances`

---

## 43. For a banking application, which load balancer would be more feasible?

“For a typical web-based **banking application using HTTP/HTTPS**, I would prefer an **Application Load Balancer** because it provides **Layer 7 routing**, **host-based/path-based routing**, **TLS termination**, and integration with **AWS WAF**. If the application requires high-performance TCP/UDP connectivity at Layer 4, then I would consider an **NLB**.”

**Simple flow:** `User → HTTPS → ALB → AWS WAF → Backend Services`

---

## 44. Have you provisioned an EKS cluster?

“Yes, I have provisioned **EKS clusters using Terraform**. I configure the **EKS control plane**, **VPC**, public/private subnets, **IAM roles**, **managed node groups**, and **Security Groups**. I also configure the **Amazon VPC CNI**, verify the cluster using **kubectl**, and deploy applications using **Helm or Kubernetes manifests**. For production, I focus on **high availability** across multiple Availability Zones.”

**Simple flow:** `Terraform → VPC → EKS Control Plane → IAM/Security Groups → Managed Node Groups → VPC CNI → kubectl/Helm`

---

## 45. What are the components of the control plane and worker node in EKS?

“In EKS, AWS manages the **control plane**. Its main components include the **API Server, etcd, Scheduler, and Controller Manager**.

The **worker node**, typically an EC2 instance in a managed node group, runs the **kubelet, kube-proxy, container runtime, and Amazon VPC CNI plugin**. The kubelet communicates with the API Server and manages the Pods running on the node.”

**Simple flow:** `Control Plane → API Server → Scheduler/Controllers → Worker Node → kubelet/kube-proxy/Container Runtime/VPC CNI → Pods`

---

## 46. When you run a kubectl command, what happens and where does it fetch data from?

“When I run a **kubectl** command, `kubectl` reads the **kubeconfig** file to identify the EKS cluster and authentication configuration. It sends the request to the Kubernetes **API Server**. The API Server performs **authentication and authorization**, and then retrieves or updates the required cluster state. Persistent Kubernetes state is stored in **etcd**. For example, `kubectl get pods` sends the request to the API Server, which returns the Pod information to kubectl.”

**Simple flow:** `kubectl → kubeconfig → API Server → Authentication → Authorization → etcd/Cluster State → Response`

---

## 47. What are Authentication, Authorization, and Admission Control?

“**Authentication** verifies **who you are**. In EKS, this can involve an **AWS IAM identity**. **Authorization** determines **what that identity is allowed to do**, commonly using **RBAC**. **Admission Control** evaluates the request after authentication and authorization and can **validate or mutate** the request before it is persisted.”

**Simple flow:** `Request → Authentication → Authorization → Admission Control → Accept/Reject → etcd`

---

## 48. What exactly does Admission Control do?

“**Admission Control** is a stage in the Kubernetes **API Server** request process. After authentication and authorization, admission controllers can **validate or modify** the request before the object is stored in **etcd**. They can enforce **security policies**, required configurations, resource rules, or other cluster policies. If a request violates a policy, it can be **rejected**.”

**Simple flow:** `Request → Authentication → Authorization → Admission Control → Validate/Mutate → Accept/Reject → etcd`

---

## 49. If a Pod needs to connect to S3, do we need PVCs and volumes?

“No, if the application only needs to **read from or write to Amazon S3**, we don't need a **PVC or PersistentVolume**. S3 is an **object storage service**, so the application can access it through the **AWS SDK/API**.

In EKS, I would use a **ServiceAccount** associated with an **IAM Role** using **EKS Pod Identity or IRSA**, and provide only the required **S3 permissions**. If the Pod is running in a private subnet, we can use an **S3 VPC Endpoint** for private connectivity.”

**Simple flow:** `Pod → ServiceAccount → IAM Role → AWS SDK/API → S3` | `Private Subnet → S3 VPC Endpoint → S3`

---

## 50. Can we use an S3 endpoint in the Kubernetes Deployment file?

“We can configure the **S3 VPC Endpoint** at the AWS VPC/networking level, but normally we don't put the endpoint directly into the Kubernetes **Deployment YAML**. For an S3 Gateway Endpoint, we associate it with the appropriate **route tables**. The Pod accesses S3 normally through the **AWS SDK/API**, and VPC routing sends the traffic through the endpoint.

The endpoint provides the **network path**, while the Pod's **IAM Role** provides authorization.”

**Simple flow:** `Pod → AWS SDK → VPC Routing → S3 VPC Endpoint → S3` | `Pod → IAM Role → S3 Permissions`

---

## 51. Which DevOps tools have you worked with?

“I have worked with **Terraform** for **Infrastructure as Code**, **Jenkins** for **CI/CD**, **Docker** for containerization, **Amazon ECR** for container image storage, **Amazon EKS** for container orchestration, and **Helm** for Kubernetes application packaging and deployment. I have also worked with **Argo CD** for **GitOps-based continuous delivery** and monitoring application synchronization.”

**Simple flow:** `Git → Jenkins → Docker → ECR → Helm → EKS → Argo CD`

---

## 52. How does CI start automatically when a developer pushes code to GitHub?

“We configure a **GitHub webhook** to trigger the **Jenkins pipeline** whenever the developer pushes code. Jenkins receives the webhook, checks out the latest code, and starts the **CI pipeline**. The pipeline performs **build, testing, code quality/security scanning, and Docker image creation**. If successful, the image is pushed to **Amazon ECR** and the CD process continues.”

**Simple flow:** `Developer → GitHub Push → Webhook → Jenkins → Build → Test → Scan → Docker Build → ECR → CD`

---

## 53. What exactly have you worked on in Terraform?

“I have used **Terraform** mainly for **Infrastructure as Code** to provision and manage AWS infrastructure. I have worked with resources such as **VPC, subnets, route tables, Internet Gateway, NAT Gateway, Security Groups, IAM, EC2, ECR, and EKS**.

I use **Terraform modules** for reusability across environments and manage environment-specific values using **variables and tfvars**. I also use **remote state**, Git, and CI/CD to manage infrastructure changes in a controlled way.”

**Simple flow:** `Terraform Code → Git → Jenkins → Plan → Approval → Apply → AWS Infrastructure`

---

## 54. What is the Terraform state file, why is it important, and where should we keep it?

“The **Terraform state file** maintains the mapping between the **Terraform configuration** and the actual infrastructure. Terraform uses it to determine what resources already exist and what changes are required during `terraform plan` and `terraform apply`.

For a team or production environment, I would not keep it only locally. I would use a **remote S3 backend**, with **S3 Versioning**, encryption, and proper access control. This provides **centralized state management, team collaboration, recovery, and state isolation**.”

**Simple flow:** `Terraform Code → Remote S3 State → terraform plan/apply → AWS Resources`

---

## 55. If Terraform detects drift, how do you make sure it won't impact the current infrastructure?

“I would first run **`terraform plan`** and carefully review the detected **drift** before making any changes. I would identify whether the drift was caused by a manual AWS change or a Terraform configuration change.

In production, I would use **Git version control**, **remote state**, **Jenkins plan-and-approval**, and **least-privilege IAM**. I would fix the Terraform code or infrastructure according to the intended state and only then perform `terraform apply`. I would avoid automatically applying unexpected changes.”

**Simple flow:** `Terraform Code + State + AWS → terraform plan → Detect Drift → Review → Fix → Approval → terraform apply`

---

## 56. If 3–4 developers work on the same Terraform code, same workspace or different workspaces?

“For multiple developers working on the same Terraform project, I would use a **remote backend** so the team shares centralized state. For different environments, we need **state isolation**.

We can use **Terraform workspaces**, but for production environments I generally prefer separate **environment configurations/directories with separate state**, because it provides clearer isolation and easier environment-specific access control.”

**Simple flow:** `Common Modules → Dev/QA/Staging/Prod → Separate State → Git PR → Plan → Approval → Apply`

---

## 57. Where do you store the Terraform code?

“We store the **Terraform code in a Git repository**, such as GitHub, GitLab, or Bitbucket. Git acts as the **single source of truth** for the Infrastructure as Code. Developers work on branches, create **pull requests**, perform code reviews, and merge approved changes.

The Terraform **state file is separate** from the source code and is stored in the **remote S3 backend**.”

**Simple flow:** `Developer → Git Branch → Terraform Code → PR → Code Review → Main Branch → Jenkins → AWS`

---

## 58. Why do we need a Terraform provider and output?

“The **provider** tells Terraform which platform or cloud provider it needs to communicate with. For AWS, the **AWS provider** allows Terraform to communicate with AWS APIs and manage AWS resources.

The **output** exposes important values from Terraform resources, such as a **VPC ID, subnet ID, load balancer DNS name, or EKS endpoint**. Outputs can also be consumed by other Terraform modules or automation pipelines.”

**Simple flow:** `Provider → Terraform → AWS API → Resources` | `Resources → Output → Other Modules/CI-CD`

---

## 59. How do you provision two EKS clusters in different regions using only one module?

“I would create one **reusable EKS Terraform module** and configure separate **AWS provider aliases** for the two regions. Then I would call the same module twice and pass the appropriate **provider alias** to each module instance.

The module code remains the same, while the **region, cluster name, VPC configuration, and other variables** can be different. I would also maintain **separate state** for each cluster to provide proper isolation.”

**Simple flow:** `One EKS Module → Provider Alias Region 1 → EKS Cluster 1` | `One EKS Module → Provider Alias Region 2 → EKS Cluster 2`

---

## 60. How do you use Prometheus, Grafana, and CloudWatch for monitoring?

“In our **EKS/Kubernetes** environment, **Prometheus** is used to collect and store **metrics** from Pods, nodes, Kubernetes components, and applications. **Grafana** is used to visualize those metrics through **dashboards** and configure alerts for conditions such as high CPU/memory usage, Pod restarts, and application issues.

For AWS-level monitoring, we use **CloudWatch** for **AWS service metrics, logs, and alarms**, including services such as EC2, EKS, and load balancers.”

**Simple flow:** `EKS/Pods/Nodes → Prometheus → Metrics → Grafana → Dashboards/Alerts` | `AWS Services → CloudWatch → Metrics/Logs/Alarms`
## 21. How do you create a Golden AMI?

“We create a **Golden AMI** by starting with a base AMI and installing the required **OS packages, application dependencies, security patches, monitoring agents, and configurations**. We then apply **security hardening**, remove temporary or sensitive data, test and validate the instance, and finally create the AMI.

In production, I would prefer automating this using **Packer** or **EC2 Image Builder** so that the AMI is consistent, repeatable, and versioned.”

**Simple flow:** `Base AMI → Packages/Dependencies → Security Hardening → Monitoring/Configuration → Test & Validate → Golden AMI → EC2`

---

## 22. What kind of Python coding/scripting experience do you have, including Lambda functions?

“I have **basic to intermediate Python** experience, mainly focused on **DevOps automation and scripting** rather than application development. I have worked with **functions, loops, conditional statements, exception handling, JSON**, and API interactions. I have also started working with **Python Lambda functions** and **Boto3** for AWS automation.

My primary hands-on experience is in **AWS infrastructure, Jenkins CI/CD, Docker, Kubernetes, and deployment**, and I am improving my Python scripting skills to automate repetitive infrastructure and operational tasks.”

**Simple flow:** `Python Script → Boto3/API → AWS Resources → Automation`

---

## 23. How would you structure reusable Terraform code for multiple environments?

“I would create **reusable Terraform modules** for common infrastructure and maintain separate **environment-specific configurations** for Dev, QA, Staging, and Production. The common logic stays inside the module, while environment-specific values such as **CIDR ranges, instance types, and replica counts** are passed through **variables and tfvars**.

I would also maintain **separate state** for each environment and store the code in **Git** for version control and collaboration.”

**Simple flow:** `Reusable Modules → Dev/QA/Staging/Prod Config → Variables/tfvars → Separate State → Terraform Plan → Apply`

---

## 24. If the Terraform state file stored in S3 is deleted and S3 Versioning is not enabled, can it be recovered?

“If **S3 Versioning** was not enabled and the Terraform **state file** is deleted, S3 does not have a previous version available for restoration. Recovery would depend on another **backup, replication copy, or external recovery mechanism**.

For production, I would enable **S3 Versioning**, encryption, and proper access control so that accidental deletion or overwriting of the state can be recovered.”

**Simple flow:** `State Deleted → Versioning OFF → No Previous Version → Check Backup/Recovery`

---

## 25. Can the infrastructure be recreated if the Terraform state file is lost?

“Yes, but it depends on whether the existing infrastructure is still available. If the infrastructure still exists, I would not immediately run `terraform apply`, because Terraform may consider the resources unmanaged and try to create them again.

Instead, I would use **`terraform import`** to bring the existing resources back into Terraform management, rebuild the state, and then run **`terraform plan`** to verify everything.

If the infrastructure itself is lost, we can use the existing **Terraform code/modules** to create new infrastructure.”

**Simple flow:** `State Lost + Infrastructure Exists → terraform import → terraform plan` | `State Lost + Infrastructure Lost → Terraform Code → terraform apply`

---

## 26. If the state file is lost, what approach would you take to recover or recreate the infrastructure?

“First, I would check for **S3 Versioning, backups, replication, or other recovery mechanisms**. If no backup is available but the infrastructure still exists, I would reconstruct the state using **`terraform import`** and then use **`terraform plan`** to verify that the Terraform configuration matches the actual infrastructure.

If both the state and infrastructure are lost, I would use the existing **Terraform configuration and modules** to provision new infrastructure.”

**Simple flow:** `State Lost → Check Backup/Version → Existing Infrastructure? → Import & Recover State` | `Infrastructure Lost → Terraform Code → New Infrastructure`

---

## 27. How do you test Terraform code? What testing strategies have you used?

“I use multiple levels of **Terraform testing**. First, I run **`terraform fmt`** for formatting and **`terraform validate`** to verify the configuration. Then I use **`terraform plan`** to review the infrastructure changes before applying them.

For quality and security checks, I can use **TFLint** and **Checkov**. For reusable modules and infrastructure behavior, we can use **Terratest** for automated testing in a test environment.

These checks can also be integrated into the **CI/CD pipeline** so that Terraform changes are validated before production deployment.”

**Simple flow:** `fmt → validate → plan → TFLint/Checkov → Terratest → CI/CD → apply`

---

## 28. What do you work on in CI/CD, and what kind of pipeline have you defined?

“I have worked with **Jenkins** and mainly use **Declarative Pipelines**. Our pipeline starts with **Git checkout**, followed by **build, testing, code quality/security checks, Docker image creation, and pushing the image to Amazon ECR**.

For deployment, we use **Kubernetes/EKS** and **Helm**, and we also use **Argo CD** for GitOps-based continuous delivery and synchronization. Sensitive information is managed through **Jenkins Credentials** rather than hardcoding secrets.”

**Simple flow:** `Git → Jenkins → Build → Test → Scan → Docker Build → ECR → Helm/Argo CD → EKS`

---

## 29. Have you written a pipeline that deploys a backend onto ECS/ECS Cluster?

“Yes, I have written a **Jenkins Declarative Pipeline** for deploying a backend application to **ECS**. The pipeline checks out the code, builds the application, creates a **Docker image**, pushes it to **Amazon ECR**, and then updates the **ECS Task Definition** and **ECS Service** to deploy the new image.

We also use different environments and approvals where required, especially before production deployment.”

**Simple flow:** `Git → Jenkins → Build → Docker Image → ECR → ECS Task Definition → ECS Service → Deployment`

---

## 30. How do you connect Jenkins/CI-CD with the AWS account to deploy to ECS or EKS?

“I connect **Jenkins** to AWS using a dedicated **IAM Role** or securely managed **Jenkins Credentials**, following the **principle of least privilege**. I avoid hardcoding long-lived AWS access keys in the Jenkinsfile.

For deployment, Jenkins authenticates to AWS and uses the **AWS CLI/API**. For ECS, it pushes the image to **ECR** and updates the **ECS Task Definition/Service**. For EKS, it pushes the image to ECR, uses **`aws eks update-kubeconfig`** to connect to the cluster, and then uses **kubectl or Helm** to deploy the application. The Jenkins identity also needs the required **EKS access/RBAC permissions**.”

**Simple flow:** `Jenkins → IAM Role/Credentials → AWS Account → ECR → ECS/EKS → Deployment`
