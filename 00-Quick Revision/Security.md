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
