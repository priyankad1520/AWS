#### esyasoft

1. **What is a Golden AMI, what goes into it, and how do you prevent it from becoming stale?**
2. **Explain your current CI/CD flow/architecture.**
3. **How do you push Docker images to Elastic Container Registry (ECR)?**
4. **You're using EKS — what GitOps tool do you use, and how does Argo CD work?**
5. **What is a Readiness Probe?**
6. **What are Taints and Tolerations?**
7. **How do GuardDuty, Security Hub, and Inspector differ? What does each detect that the others don't?**
8. **How do you identify and remove unused IAM permissions from a role?**
9. **What failure does Terraform remote-state locking with DynamoDB prevent?**
10. **You migrated workloads from ECS to EKS. What was the biggest operational difference?**
11. **For a stateful service with a database migration, would you choose Blue-Green or Canary, and why?**
12. **Write shell logic to count EC2-related log lines containing `error` in the last hour.**
13. **What is the `lsblk` command?**
14. **What is the risk of making a Terraform module too generic/reusable across every environment?**
---
#### KPM
1. Do you only deploy applications, or do you also create and administer EKS clusters?
2. How do you access an EKS cluster?
3. If I give you AWS Access Key and Secret Key, how do you identify and connect to the correct EKS cluster?
4. If there are multiple EKS clusters, how do you switch to a specific cluster?
5. How do you give a developer read-only access to specific namespaces?
6. If the developer's name is Srinivas, what do you put in the RoleBinding? Do you use Kubernetes users or IAM Roles?
7. Tell me about your application. What does it do?
8. What is your role in that application?
9. Explain the application architecture and deployment flow.
10. How is the database designed? How do you maintain redundancy in RDS?
11. Which tool are you most confident in?
12. How do you recover deleted data/commits in Git?
13. Difference between git reset and git revert.
14. Dockerfile best practices.
15. How does a multi-stage build reduce image size?
16. Difference between ENTRYPOINT and CMD.
17. What is EXPOSE?
18. If you change EXPOSE from 8080 to 8081, will the application run on 8081?
19. If you really want to change the application's port, what do you do?
20. A pod needs to restart another workload every day at 10 AM. How do you implement it?
21. Why do you need a ServiceAccount? What is its purpose?
22. How do you create public and private subnets?
23. How do you determine whether a subnet is public or private?
24. nat gateway
--- 
#### betatestsolution
1. What is a VPC?
2. Why do we distinguish between public and private subnets?
3. How can a private EC2 instance download Linux updates or patches?
4. What is NAT and what does it actually do?
5. Why do we use a NAT Gateway instead of an Internet Gateway or Transit Gateway?
6. How does a NAT Gateway allow a private EC2 instance to communicate with the internet?
7. How do you connect two VPCs together?
8. What happens if two VPCs have the same CIDR range during VPC peering?
9. What type of applications have you deployed on Kubernetes/EKS?
10. Which framework was used for the Java applications?
11. What is the difference between ConfigMap and Secret?
12. How did you integrate AWS Secrets Manager with EKS?
13. What is IRSA and how did you implement it?
14. What is the difference between Ingress, Service, and Deployment?
15. Can a Pod have multiple containers?
16. What are the different types of Kubernetes Services?
17. How would you expose an application to the internet without ALB or NLB for testing?
18. Have you worked on an EKS cluster version upgrade? How did you perform it?
19. What is etcd?
20. What happens to Pods when only a ConfigMap is changed and Helm is upgraded?
21. What is a PersistentVolume and PersistentVolumeClaim?
22. How would you establish a private connection between AWS and Azure?
23. What is the difference between an IAM policy and a trust policy?
24. Where is the trust policy defined?
25. How did you set up IRSA using IAM roles and IAM policies?
26. What happens if two engineers execute Terraform at the same time?
27. What is the difference between terraform init, terraform plan, and terraform destroy?
28. How do you implement namespace-based RBAC in EKS?
29. Which AWS services have you worked with?
30. For a production e-commerce application, which AWS services would you recommend?
31. Where would you deploy the frontend?
32. Where would you deploy the backend APIs—EC2, ECS, or Kubernetes?
33. What replication/scaling strategy would you use for a high-traffic e-commerce application?
34. How would you configure HPA/autoscaling for festive-season traffic?
35. Why would you use Karpenter, and can we avoid it?
36. What would you use for Redis?
37. How would you handle background workers for payments and order processing?
38. Can Lambda be used for background workers, and what are its disadvantages?
39. What would you use for CI/CD?
40. How would you secure secrets in Jenkins?
41. What would you use for monitoring?
42. How would you configure a custom domain for the website?
43. A Pod suddenly goes into CrashLoopBackOff after working fine for a week with no deployment. What would you check?
---
**Accion_labs**
1. Explain your CI/CD process.
2. You migrated workloads from ECS to EKS. What was the business problem with ECS? (You can answer that your project was already on EKS and not ECS.)
3. The application was working perfectly on ECS, but after moving to EKS it started failing. How would you investigate?
4. During a blue-green deployment, everything looks successful, but after 30 minutes customers report failures. What could have gone wrong?
5. In Kubernetes, all pods are running and all nodes are healthy, but customers are getting 503 Service Unavailable. How would you investigate?
6. One pod receives high traffic while another healthy pod receives very little traffic. What would you check?
7. Tell me about a complex issue that was difficult to troubleshoot and resolve.
8. Give another complex issue example.
9. How would you prevent that issue from happening again?
10. A user reports that records are not visible in the application. It could be a UI issue, API issue, or database issue. How would you isolate and troubleshoot it?
11. A deployment works fine in Dev and QA, but after production deployment the application crashes due to real-time/live data. Have you faced such a scenario?
12. Give another example of a production-only issue after deployment.
13. Give a simple example of a production issue.
14. Have you done SQL debugging? Give an example.
15. A customer is very angry, management is on the bridge call, there is no ETA, and technical teams are struggling. How would you handle the customer and communication?
16. Terraform apply succeeded yesterday, but today Terraform plan shows unexpected changes even though nobody changed the code. How would you investigate?
17. What are the specific checks you would perform when Terraform plan shows unexpected changes?
18. Only 3% of requests are failing. Pods, nodes, database, CPU, memory, and deployments all look normal. How would you investigate?
19. What tools would you use when only a small percentage of requests are failing?
20. Explain your troubleshooting approach from start to end for the 3% request failure scenario.
21. AI is becoming popular in DevOps. How are you using AI tools in your current project or company?
