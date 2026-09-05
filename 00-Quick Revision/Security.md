# **6. How is the application secured?**

**Interview answer:**

> “I secure the application using multiple layers. I use VPC and private subnets to isolate the application, Security Groups to control network access, NACLs for subnet-level traffic control, IAM for AWS permissions, Secrets Manager for sensitive credentials, KMS for encryption, and AWS WAF to protect public web applications from malicious HTTP and HTTPS requests.”

### **What is VPC?**

> “VPC provides an isolated network environment in AWS where I define subnets, route tables, gateways, and network security controls for the application.”

**Flow:** `Internet → VPC → Public/Private Subnets → Application`

### **Why do we use Private Subnets?**

> “I keep backend application servers and databases in private subnets when they don't need to be directly accessible from the internet. This reduces their public exposure and allows access through controlled network paths.”

**Flow:** `Internet → ALB → Private Application → Private RDS`

### **What is a Security Group?**

> “A Security Group is a stateful virtual firewall that controls inbound and outbound traffic for resources such as EC2 instances, load balancers, and other supported resources.”

Example:

> “I would allow the EC2 security group to receive application traffic only from the ALB security group, rather than allowing traffic from the entire internet.”

**Flow:** `Internet → ALB SG → ALB → EC2 SG → EC2`

### **What is NACL?**

> “A Network ACL is a stateless firewall that operates at the subnet level. It controls inbound and outbound traffic for the subnet.”

**Easy memory:**
`Security Group → Resource level`
`NACL → Subnet level`

### **What is IAM?**

> “IAM controls who can access AWS resources and what actions they are allowed to perform. I follow the principle of least privilege and grant only the permissions required for a user, role, or application.”

### **What is Secrets Manager?**

> “AWS Secrets Manager is used to securely store and manage sensitive information such as database passwords, API keys, and other application secrets instead of hardcoding them in application code or configuration files.”

### **What is KMS?**

> “AWS KMS is used to create and manage encryption keys that can be used to encrypt data at rest and protect sensitive information.”

### **What is WAF?**

> “AWS WAF is a web application firewall that inspects HTTP and HTTPS requests and can allow, block, or count requests based on configured rules. I commonly associate it with CloudFront, ALB, or API Gateway for public-facing applications.”

**Flow:** `User → CloudFront/WAF → ALB → Application`

### **How would you secure a production application?**

> “I would use a layered security approach: public access only through the required entry point such as CloudFront or ALB, keep application and database resources in private subnets where appropriate, use Security Groups to restrict communication between layers, IAM with least privilege for AWS access, Secrets Manager for credentials, KMS for encryption, and WAF for application-layer protection.”

### **Most important security architecture to remember**

`Internet → CloudFront/WAF → ALB → Private EC2/ECS/EKS → Private RDS`

`IAM → AWS permissions`
`Security Group → Resource traffic`
`NACL → Subnet traffic`
`Secrets Manager → Secrets`
`KMS → Encryption`
`WAF → Web-request protection`
## **6. How is the application secured?**

**What do we use for network security?**: VPC, Security Groups, and NACLs.

**What is VPC?**: VPC is a logically isolated network in AWS where we place and control our AWS resources.

**Why do we use public and private subnets?**: Public subnets are used for resources that need direct internet-facing connectivity, while private subnets are used for application servers and databases that should not be directly accessible from the internet.

**Typical architecture flow**: Internet → Public ALB → Private EC2/ECS/EKS → Private RDS.

---

### **Security Group**

**What is a Security Group?**: A Security Group is a stateful virtual firewall that controls inbound and outbound traffic for resources such as EC2 instances and load balancers.

**Example**: ALB Security Group allows `443`, EC2 Security Group allows traffic only from the ALB Security Group, and RDS Security Group allows database traffic only from the application Security Group.

**Good architecture flow**: Internet → ALB SG → ALB → EC2 SG → EC2 → RDS SG → RDS.

**Why use Security Group references?**: To allow communication between specific application layers instead of allowing traffic from everywhere.

---

### **NACL**

**What is a NACL?**: A Network ACL is a stateless firewall that controls traffic at the subnet level.

**Security Group vs NACL**: Security Group → Resource-level and stateful, NACL → Subnet-level and stateless.

---

### **IAM**

**What is IAM?**: IAM manages authentication and authorization for AWS resources and services.

**Why do we use IAM?**: To control who can access AWS resources and what actions they are allowed to perform.

**Best practice**: Follow the principle of least privilege and give only the permissions that are required.

**Example**: An EC2 application should use an IAM role to access S3 instead of storing AWS access keys inside the application.

---

### **IAM Role**

**What is an IAM Role?**: An IAM Role provides temporary permissions to AWS services, applications, or users without requiring long-term access keys.

**Example**: EC2 → IAM Role → S3.

---

### **Secrets Manager**

**Why do we use Secrets Manager?**: To securely store sensitive information such as database passwords, API keys, and other application secrets.

**Why not store passwords in code?**: Credentials should not be hard-coded or committed to Git because that creates a security risk.

**Flow**: Application → Secrets Manager → Retrieve secret → Connect to database.

---

### **KMS**

**What is KMS?**: AWS Key Management Service is used to create and manage encryption keys.

**Why do we use KMS?**: To encrypt and protect sensitive data stored in services such as S3, RDS, EBS, and other AWS services.

**Encryption example**: Application data → KMS-managed encryption → Stored securely.

---

### **WAF**

**What is WAF?**: AWS WAF is a Web Application Firewall that filters HTTP/HTTPS requests and protects web applications from common application-layer attacks and unwanted traffic.

**Where do we configure WAF?**: Commonly with CloudFront, ALB, or API Gateway.

**Typical flow**: User → CloudFront/WAF → ALB → Application.

**Why use WAF?**: To block or allow requests based on rules such as IP address, URI, headers, geographic conditions, and managed security rules.

---

### **HTTPS / TLS**

**Why do we use HTTPS?**: To encrypt communication between the client and application and protect data while it is being transmitted.

**Where can TLS terminate?**: Commonly at CloudFront or an ALB, depending on the architecture.

**Typical flow**: User → HTTPS → CloudFront/WAF → HTTPS/HTTP → ALB → Application.

---

### **How would you secure a production application?**

**Answer**: VPC with private subnets → ALB as the public entry point → Security Groups between each layer → WAF for HTTP/HTTPS protection → IAM roles for AWS access → Secrets Manager for credentials → KMS for encryption → HTTPS for secure communication.

### **Most important interview memory**

**VPC**: Network isolation.

**Public/Private Subnet**: Control network exposure.

**Security Group**: Resource-level firewall.

**NACL**: Subnet-level firewall.

**IAM**: AWS permissions.

**Secrets Manager**: Store secrets.

**KMS**: Encryption keys.

**WAF**: Web/application-layer protection.

**HTTPS**: Encrypt traffic.
