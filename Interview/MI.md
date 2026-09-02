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
