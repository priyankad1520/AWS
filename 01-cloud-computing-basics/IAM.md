# IAM

AWS IAM (Identity and Access Management) is a service provided by Amazon Web Services (AWS) that helps you manage access to your AWS resources. It's like a security system for your AWS account.

IAM allows you to create and manage users, groups, and roles. Users represent individual people or entities who need access to your AWS resources. Groups are collections of users with similar access requirements, making it easier to manage permissions. Roles are used to grant temporary access to external entities or services.

With IAM, you can control and define permissions through policies. Policies are written in JSON format and specify what actions are allowed or denied on specific AWS resources. These policies can be attached to IAM entities (users, groups, or roles) to grant or restrict access to AWS services and resources.

IAM follows the principle of least privilege, meaning users and entities are given only the necessary permissions required for their tasks, minimizing potential security risks. IAM also provides features like multi-factor authentication (MFA) for added security and an audit trail to track user activity and changes to permissions.

By using AWS IAM, you can effectively manage and secure access to your AWS resources, ensuring that only authorized individuals have appropriate permissions and actions are logged for accountability and compliance purposes.

Overall, IAM is an essential component of AWS security, providing granular control over access to your AWS account and resources, reducing the risk of unauthorized access and helping maintain a secure environment.

## Components of IAM 

Users: IAM users represent individual people or entities (such as applications or services) that interact with your AWS resources. Each user has a unique name and security credentials (password or access keys) used for authentication and access control.

Groups: IAM groups are collections of users with similar access requirements. Instead of managing permissions for each user individually, you can assign permissions to groups, making it easier to manage access control. Users can be added or removed from groups as needed.

Roles: IAM roles are used to grant temporary access to AWS resources. Roles are typically used by applications or services that need to access AWS resources on behalf of users or other services. Roles have associated policies that define the permissions and actions allowed for the role.

Policies: IAM policies are JSON documents that define permissions. Policies specify the actions that can be performed on AWS resources and the resources to which the actions apply. Policies can be attached to users, groups, or roles to control access. IAM provides both AWS managed policies (predefined policies maintained by AWS) and customer managed policies (policies created and managed by you).

# Interview Questions

Q: What is AWS IAM, and why is it important?

A: AWS IAM (Identity and Access Management) is a service provided by Amazon Web Services that helps you control access to your AWS resources. It allows you to manage user identities, permissions, and policies. IAM is important because it enhances security by ensuring that only authorized individuals or entities have access to your AWS resources, helping you enforce the principle of least privilege and maintain a secure environment.

Q: What is the difference between IAM users and IAM roles?

A: IAM users represent individual people or entities that need access to your AWS resources. They have their own credentials and are typically associated with long-term access. On the other hand, IAM roles are used to grant temporary access to AWS resources, usually for applications or services. Roles have associated policies and can be assumed by trusted entities to access resources securely.

Q: What are IAM policies, and how do they work?

A: IAM policies are JSON documents that define permissions. They specify what actions are allowed or denied on AWS resources and can be attached to IAM users, groups, or roles. Policies control access by matching the actions requested by a user or entity with the actions allowed or denied in the policy. If a requested action matches an allowed action in the policy, access is granted; otherwise, it is denied.

Q: What is the principle of least privilege, and why is it important in IAM?

A: The principle of least privilege states that users should be granted only the permissions necessary to perform their tasks and nothing more. It is important in IAM because it minimizes the risk of unauthorized access and limits the potential damage that could be caused by a compromised account. Following the principle of least privilege helps maintain a secure environment by ensuring that users have only the permissions they need to perform their job responsibilities.

Q: What is an AWS managed policy?

A: An AWS managed policy is a predefined policy created and managed by AWS. These policies cover common use cases and provide predefined permissions for specific AWS services or actions. AWS managed policies are maintained and updated by AWS, ensuring they stay up to date with new AWS services and features. They can be attached to IAM users, groups, or roles in your AWS account.

# AWS IAM — Practical Interview Answers

## 1. What is IAM?

**Interview answer:**

> “IAM is the AWS service we use to control access to AWS resources. In our project, whenever a user, EC2 instance, EKS workload, or Jenkins pipeline needed to access an AWS service, we used IAM to control what it could access and what actions it could perform. We followed least privilege, so we gave only the permissions required for that particular task.”

**Practical flow:**
**User / EC2 / EKS / Jenkins → IAM Identity/Role → Permissions → AWS Resource**

---

## 2. What is the difference between IAM User, Group, Role, and Policy?

**Interview answer:**

> “An IAM user represents an individual identity, mainly for direct or legacy access. A group is used when multiple users need common permissions. An IAM role is an identity that can be assumed by users or AWS services and is mainly used when we want temporary access. A policy defines what actions that user or role is allowed or denied to perform. In our DevOps environment, we preferred roles for workloads instead of maintaining long-term access keys.”

**Easy memory:**
**User → Individual, Group → Collection, Role → Assumable identity, Policy → Permissions**

---

## 3. Why do you prefer IAM roles over access keys?

**Interview answer:**

> “For applications and AWS services, we avoid storing long-term access keys because it creates a credential-management and security risk. For example, if an EC2 application needs S3 access, we attach an IAM role to EC2 and the application gets temporary credentials automatically. This way we don't have to store or manually rotate access keys on the server.”

**Practical flow:**
**EC2 → IAM Role → Temporary Credentials → S3**

---

## 4. How does EC2 access S3 securely?

**Interview answer:**

> “First, we create an IAM role for EC2 and allow the EC2 service to assume that role through the trust policy. Then we attach a permissions policy to the role with only the required S3 actions, such as `s3:GetObject`, and restrict it to the required bucket. Finally, we attach the role to the EC2 instance. The application then uses the temporary credentials provided through the instance role.”

**Practical flow:**
**Create Policy → Create Role → Trust EC2 → Attach Policy → Attach Role to EC2 → Temporary Credentials → S3**

---

## 5. What is a trust policy?

**Interview answer:**

> “The trust policy tells AWS who is allowed to assume a role. For example, if the role is created for EC2, the trust policy allows the EC2 service to assume that role. In cross-account access, the trust policy can allow a principal from another AWS account to assume the role.”

**Easy memory:**
**Trust Policy → WHO can assume?**

---

## 6. What is a permissions policy?

**Interview answer:**

> “The permissions policy tells us what the role or user can actually do after authentication or role assumption. For example, we can give an EC2 role `s3:GetObject` permission only for one S3 bucket. So trust policy controls role assumption, while permissions policy controls resource access.”

**Easy memory:**
**Permissions Policy → WHAT can it do?**

---

## 7. Trust policy vs permissions policy?

**Interview answer:**

> “The trust policy and permissions policy solve two different problems. The trust policy tells AWS who is trusted to assume the role. The permissions policy tells AWS what that role can do after it gets access. For example, for EC2, the trust policy allows EC2 to assume the role, and the permissions policy might allow that role to read from S3.”

**Best line to remember:**
**Trust = Who, Permissions = What**

---

## 8. What is an identity-based policy?

**Interview answer:**

> “An identity-based policy is attached to an IAM user, group, or role and defines what that identity can do. For example, in our environment, we could attach a policy to an EKS workload role that allows `secretsmanager:GetSecretValue` for a specific secret.”

**Flow:**
**IAM Role → Identity Policy → AWS Service**

---

## 9. What is a resource-based policy?

**Interview answer:**

> “A resource-based policy is attached directly to the resource. For example, an S3 bucket can have a bucket policy that defines which principals can access the bucket. We use this when we need the resource itself to control access, especially in cases like cross-account access or additional resource-level restrictions.”

**Flow:**
**S3 Bucket → Bucket Policy → Principal → Access**

---

## 10. Identity-based policy vs resource-based policy?

**Interview answer:**

> “The main difference is where the policy is attached. If the policy is attached to the user, group, or role, it's identity-based. If it's attached to the resource, it's resource-based. For a normal EC2-to-S3 use case, I would normally start with an IAM role and identity-based policy. If I need additional control at the bucket level, I can use an S3 bucket policy.”

**Easy memory:**
**Identity-based → What can this identity do?**

**Resource-based → Who can access this resource?**

---

# 11. What is least privilege?

**Interview answer:**

> “Least privilege means giving only the permissions required for a specific task. For example, if our application only needs to read files from one S3 bucket, I would give `s3:GetObject` for that bucket instead of giving `s3:*` or access to all S3 buckets. We follow this to reduce the impact if credentials or the workload are compromised.”

**Practical example:**
**Required → `s3:GetObject` on one bucket**
**Avoid → `s3:*` on `*`**

---

# 12. What is STS?

**Interview answer:**

> “STS, or Security Token Service, is what we use when temporary credentials are required. For example, when a Jenkins server needs to deploy into another AWS account, Jenkins can assume a role using STS and get temporary credentials. We don't need to maintain a permanent access key for that deployment.”

**Flow:**
**Jenkins → STS AssumeRole → Temporary Credentials → Target AWS Account**

---

# 13. What happens when a role is assumed?

**Interview answer:**

> “When a trusted principal assumes a role, AWS verifies the trust relationship and then provides temporary security credentials for that role. The permissions of that role determine what the caller can do. For example, Jenkins assumes a production deployment role and gets temporary credentials, then uses those credentials to deploy to EKS.”

**Flow:**
**Principal → AssumeRole → Trust Check → Temporary Credentials → Role Permissions → AWS API**

---

# 14. What is an Instance Profile?

**Interview answer:**

> “An instance profile is the mechanism through which an IAM role is made available to an EC2 instance. In practical terms, when I attach an IAM role to EC2, the instance profile provides that role to the instance, and the application can then use the role's temporary credentials.”

**Flow:**
**IAM Role → Instance Profile → EC2 → Temporary Credentials**

---

# 15. What is a Permission Boundary?

**Interview answer:**

> “A permission boundary is used to define the maximum permissions an IAM user or role can have. It doesn't grant the permissions by itself. For example, even if a developer creates a role with broader permissions, the permission boundary can limit the maximum permissions that role is allowed to use.”

**Easy memory:**
**Policy → What is allowed**

**Boundary → Maximum it can have**

---

# 16. What is an SCP?

**Interview answer:**

> “SCP, or Service Control Policy, is used at the AWS Organizations level. It acts as a guardrail for accounts or organizational units. For example, our organization can use an SCP to prevent certain actions in production accounts. SCP doesn't grant permissions; it limits what permissions are available.”

**Flow:**
**Organization → OU → AWS Account → IAM Principal → Resource**

---

# 17. Permission Boundary vs SCP?

**Interview answer:**

> “The main difference is the scope. A permission boundary limits an individual IAM user or role, while an SCP applies at the AWS account or organizational level. So I think of a permission boundary as an identity-level restriction and an SCP as an organization or account-level guardrail.”

**Easy memory:**
**Boundary → Role/User level**

**SCP → Account/OU level**

---

# 18. Managed Policy vs Inline Policy?

**Interview answer:**

> “A managed policy is a separate policy that can be reused and managed independently, while an inline policy is directly embedded into a specific user, group, or role. In enterprise environments, we generally prefer reusable customer-managed policies where possible because they are easier to maintain and standardize.”

**Easy memory:**
**Managed → Reusable**

**Inline → Attached directly to one identity**

---

# 19. AWS Managed Policy vs Customer Managed Policy?

**Interview answer:**

> “AWS managed policies are created and maintained by AWS, while customer managed policies are created and controlled by our organization. If we need very specific permissions for our application, I prefer a customer-managed policy because we control the exact actions and resources.”

---

# 20. What is explicit deny?

**Interview answer:**

> “An explicit deny means a policy specifically denies the requested action. Even if another policy allows that action, the explicit deny takes precedence. When troubleshooting AccessDenied issues, I always check for explicit deny conditions in bucket policies, SCPs, permission boundaries, and other applicable policies.”

**Remember:**
**Explicit Deny > Allow**

---

# 21. What is IAM Identity Center?

**Interview answer:**

> “IAM Identity Center is used for centralized workforce access to multiple AWS accounts. Instead of creating separate IAM users for every account, employees can sign in through the company identity system and get different permission sets for different AWS accounts. For example, a DevOps engineer might have admin access in Dev, limited access in QA, and read-only or approved access in Production.”

**Flow:**
**Employee → Corporate IdP/Identity Center → AWS Account → Permission Set → Role → AWS**

---

# 22. How do you provide access to multiple AWS accounts?

**Interview answer:**

> “In a multi-account environment, we normally use centralized identity management. Users authenticate through the company identity provider or IAM Identity Center, then select the AWS account they need and receive the appropriate role or permission set. This allows us to maintain one corporate identity while giving different access levels in Dev, QA, and Production.”

---

# 23. How does cross-account access work?

**Interview answer:**

> “For cross-account access, we normally create a role in the target account. The target role has a trust policy that allows the source account or specific principal to assume it. The source user or workload needs permission to call `sts:AssumeRole`. After assuming the role, AWS issues temporary credentials, and the permissions policy attached to the target role defines what the caller can do.”

**Flow:**
**Dev Account → `sts:AssumeRole` → Prod Role → Temporary Credentials → Prod Resource**

---

# 24. Would you create an IAM user in Production for a developer from Dev?

**Interview answer:**

> “Normally, no. I would prefer cross-account role assumption instead of creating another long-term IAM user in Production. The developer can authenticate through the normal corporate access mechanism, assume the required Production role, and receive temporary credentials. This gives better control and avoids maintaining another permanent credential.”

---

# 25. How do you give Jenkins access to AWS?

**Interview answer:**

> “I prefer role-based access instead of storing a permanent AWS access key in Jenkins. Depending on the setup, Jenkins can assume a deployment role in the target account. For example, Jenkins can assume a Production deployment role that has only the permissions required to deploy the application to EKS.”

**Flow:**
**Jenkins → AssumeRole → Prod Deployment Role → EKS**

---

# 26. How does an EKS application access AWS services?

**Interview answer:**

> “We don't normally store AWS access keys inside the container. We associate the workload with an IAM role using an EKS workload identity mechanism such as IRSA or EKS Pod Identity. The pod gets temporary credentials and can then access services such as S3, Secrets Manager, or DynamoDB according to the IAM policy.”

**Flow:**
**EKS Pod → Workload Identity → IAM Role → Temporary Credentials → AWS Service**

---

# 27. How do you troubleshoot AccessDenied?

**Interview answer:**

> “First, I identify which identity is actually making the request. I usually check that using `aws sts get-caller-identity`. Then I verify the correct role is attached or assumed, check the identity-based policy, confirm the action and resource ARN are correct, and check for a resource-based policy. After that I look for explicit denies, permission boundaries, SCPs, policy conditions, and KMS permissions if encryption is involved. I also check application credentials because sometimes the application is using a different credential than expected.”

**Troubleshooting flow:**
**Caller Identity → Role → Policy → Resource ARN → Resource Policy → Explicit Deny → KMS → Boundary → SCP → Conditions**

---

# 28. How do you check which AWS identity is being used?

**Interview answer:**

> “I use `aws sts get-caller-identity`. This is one of the first things I check when there is a permission issue because it tells me which user or role is actually making the request.”

```bash
aws sts get-caller-identity
```

---

# 29. An EC2 instance has S3 permission but still gets AccessDenied. What do you check?

**Interview answer:**

> “I first confirm the correct IAM role is attached to the EC2 instance. Then I check whether the role policy allows the required S3 action on the correct bucket or object ARN. Next I check the bucket policy for an explicit deny or restrictive condition. If the object is KMS encrypted, I also check `kms:Decrypt`. After that I check whether the application is using the EC2 role credentials or some different credentials, and finally I check SCPs and permission boundaries.”

---

# 30. What is IAM Access Analyzer?

**Interview answer:**

> “IAM Access Analyzer helps us review and validate IAM policies and identify unintended access, such as public or cross-account access. It can also help us refine permissions toward least privilege. In a real project, this is useful when we want to review whether a role has more access than the application actually needs.”

---

# 31. What is the difference between authentication and authorization?

**Interview answer:**

> “Authentication is verifying who the user or workload is. Authorization is deciding what that identity is allowed to do. For example, when a DevOps engineer signs in through corporate SSO, authentication verifies the identity, and IAM permissions determine whether that person can access a Production EKS cluster.”

**Memory:**
**Authentication → Who are you?**

**Authorization → What can you do?**

---

# 32. How do you secure IAM in a production environment?

**Interview answer:**

> “We follow least privilege, avoid long-term credentials where possible, use IAM roles for workloads, use centralized identity and MFA for human access, restrict sensitive permissions, review unnecessary access, and use organization-level guardrails such as SCPs where required. For Production, we also separate access levels so not every engineer gets full administrator access.”

---

# 33. How would you give an application access to Secrets Manager?

**Interview answer:**

> “I would create or use an IAM role for the workload and give it only `secretsmanager:GetSecretValue` permission for the required secret. The application would assume the role and retrieve the secret at runtime rather than storing the secret in source code or a configuration file.”

**Flow:**
**Application → IAM Role → `GetSecretValue` → Secrets Manager**

---

# 34. How would you handle KMS permissions?

**Interview answer:**

> “If the application is accessing a KMS-encrypted resource, I make sure the workload role has the required KMS permissions, such as `kms:Decrypt`, in addition to the permission for the underlying service. For example, an application may have `s3:GetObject` but still get AccessDenied because it doesn't have permission to use the KMS key.”

**Flow:**
**Application → IAM Role → S3 GetObject + KMS Decrypt → Encrypted Object**

---

# 35. What is role chaining?

**Interview answer:**

> “Role chaining means one role assumes another role. It can be used in multi-account or delegated access designs, but I would keep the chain as simple as possible because it can make troubleshooting and permission management more complicated.”

**Flow:**
**Role A → AssumeRole → Role B → AWS Resource**

---

# 36. What is External ID?

**Interview answer:**

> “External ID is mainly used when a third-party service needs to assume a role in our AWS account. It helps protect against the confused-deputy problem. Instead of only trusting the third party, we can require a specific external ID as part of the role assumption.”

---

# 37. What is a service-linked role?

**Interview answer:**

> “A service-linked role is an IAM role that is created for a specific AWS service so that the service can perform actions required for its operation. AWS manages the role's relationship with that service. I mainly need to understand what it is and recognize it when troubleshooting service permissions.”

---

# 38. How would you access AWS from an on-premises workload without storing access keys?

**Interview answer:**

> “I would prefer a temporary-credential approach rather than hard-coding permanent access keys. Depending on the architecture, we can use federation, STS-based role assumption, or IAM Roles Anywhere for supported on-premises workloads. The exact solution depends on the identity and network architecture.”

---

# 39. How would you describe your IAM work honestly in an interview?

Since you've said you worked alongside a Cloud/Senior team, this is the safest strong answer:

“In our project, IAM was a shared responsibility between the Cloud and DevOps teams. The Cloud team handled the account-level IAM setup, centralized access, and security standards, while I worked more on the application and workload side. For example, when an application running on EKS or EC2 needed access to S3, Secrets Manager, or other AWS services, I worked with the required IAM roles and least-privilege policies, validated the access, and supported troubleshooting. I also worked with the team on CI/CD and cross-account access where deployment roles were required.”

That answer demonstrates experience **without claiming that you independently owned the entire IAM architecture**.

# Your IAM interview cheat sheet

**IAM → Authentication + Authorization**

**User → Individual identity**

**Group → Collection of users**

**Role → Assumable identity + temporary credentials**

**Policy → Permissions**

**Trust Policy → WHO can assume?**

**Permissions Policy → WHAT can it do?**

**Identity Policy → Attached to User/Group/Role**

**Resource Policy → Attached to Resource**

**STS → Temporary credentials**

**EC2 → Instance Profile → Role**

**Least Privilege → Minimum required access**

**Boundary → Maximum permissions for identity**

**SCP → Account/Organization guardrail**

**Explicit Deny → Overrides Allow**

**AccessDenied → Identify caller → Check role/policy/resource → Check Deny/boundary/SCP/KMS**

**EC2 → Role → Temporary Credentials → S3**

**EKS Pod → Workload Identity → Role → AWS Service**

**Jenkins → AssumeRole → Deployment Role → Target Account**

**Dev Account → AssumeRole → Prod Role → Temporary Credentials → Prod Resource**

The most important thing is that your answers should naturally include **“in our environment,” “we used,” “we configured,” “we validated,” and “we troubleshot”** where those statements are genuinely true. That makes your answer practical without exaggerating your level of ownership.
