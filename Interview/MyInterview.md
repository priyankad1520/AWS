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
