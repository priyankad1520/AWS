1. Have you worked with enterprise-level Terraform deployments?
2. How would you build a testing framework to validate Terraform infrastructure before deployment?
3. How would you validate Terraform code before deployment?
4. How would you design an automated remediation/self-healing system for an unhealthy EC2 instance?
5. If someone manually changes Terraform-managed infrastructure from the AWS console, how would you remediate it?
6. Have you worked with Kubernetes for several years?
7. Pods are running and readiness probes are passing, but customers are getting HTTP 503. How would you troubleshoot it?
8. What do error codes like exit code 0 and exit code 1 mean in pod logs?
9. Pods are getting evicted from one worker node while other nodes have enough capacity. What could be the root cause?
10. How would you check why a pod was evicted?
11. What is an Ingress file?
12. What is the Kubernetes pod lifecycle?
13. Have you designed any self-healing systems?
14. Have you worked on production troubleshooting and RCA?
15. An upstream service is getting many retries because a downstream service is slow. The retries make the whole platform unavailable. How would you handle it?
16. What experience do you have with monitoring tools like Grafana and Prometheus?
17. What are the types of telemetry in monitoring?
18. A developer adds customer ID and transaction ID as Prometheus labels and memory usage increases. How would you fix it?
19. What types of labels do you see in a Grafana/Prometheus dashboard?
20. A service generated 2,000–3,000 alerts/calls during a weekend but automatically recovered. How would you prevent this?
21. Have you worked on performance and latency troubleshooting?
22. What is the difference between P50 and P99 latency?
23. If P50 latency is 100 ms but P99 is 8 seconds, what does that indicate?
24. After enabling distributed tracing, P99 latency increased. What could be the reason?
25. Have you worked in an L3/support role involving RCA?
26. What would be your action items during the first 15 minutes of a P1 incident?
27. A deployment caused an outage, but even after rollback the issue persists. What could be the reason?
28. Cloud services need to connect to an on-premises database, but some services connect successfully while others get timeout errors. How would you troubleshoot it?
29. Have you done end-to-end enterprise pipeline configuration?
30. What are the stages of an enterprise CI/CD pipeline?
31. What is sli slo sla
### EPAM
1. **What is the difference between NAT Gateway and VPC Endpoint?**

2. **What kind of packages are installed in a NAT Gateway?**

3. **What is AWS Lambda and how does it work?**

4. **What is a Jenkins Shared Library? How do you create and configure it? Explain the folder structure.**

5. **If you use a Shared Library and need a change only for one application, how do you manage it?**

6. **Can you explain a normal Jenkins CI/CD pipeline?**

7. **How would you run integration tests for a Node.js application across multiple Node versions and operating systems?**

8. **How do you handle a monorepo where only the changed microservice should be built instead of the entire repository?**

9. **What is an ephemeral Jenkins agent?**

10. **How do you archive artifacts only for the main/release branch and not for feature branches?**

11. **How do you connect Jenkins to AWS using short-lived/session-based credentials instead of access keys?**

12. **What scripting languages have you used?**

13. **How have you used Python with AWS Lambda?**

14. **How do you establish connectivity between VPCs across multiple AWS accounts?**

15. **How do you establish communication when two VPCs have overlapping CIDRs?**

16. **How do you protect S3 audit logs from accidental deletion, even by the root user?**

17. **How do you prevent developers from attaching AdministratorAccess to IAM roles across AWS Organization accounts?**

18. **How do you troubleshoot an Auto Scaling Group that isn't scaling out during a traffic spike?**

19. **What if CPU utilization never reaches the 80% scaling threshold even though traffic has increased significantly?**

20. **How do you manage patching of multiple EC2 instances?**

21. **How do you troubleshoot AccessDenied when an EC2 instance in Account A needs to upload data to an S3 bucket in Account B?**

22. **What should you check if the EC2 IAM role already has S3 permissions but you're still getting AccessDenied?**

23. **How do you configure the S3 bucket policy to allow cross-account access?**

24. **How do you manage database passwords/API keys on EC2 without hardcoding them, while rotating credentials every 60 days without application downtime?**

25. **How do you make sure secret rotation doesn't bring the application down?**

26. **How do you manage secrets at runtime in Kubernetes using Secrets Manager/SDK/sidecar approaches?**

27. **Have you handled Kubernetes cluster-level patching or version upgrades?**

28. **An application takes 45–50 seconds to start, but the pod restarts every 30 seconds and enters CrashLoopBackOff. How do you fix it?**

29. **How do you make sure three replicas of a deployment are scheduled on different nodes?**

30. **How do you prevent one pod from consuming all node resources?**

31. **How do you protect critical Kubernetes pods from eviction during node resource pressure?**

32. **Have you worked with Terraform modules?**

33. **How do you deploy the same Terraform VPC module across multiple AWS regions?**

34. **How do you differentiate AWS regions using Terraform provider aliases?**

35. **How do you prevent critical Terraform-managed resources such as VPC, EC2, RDS, and S3 from accidental deletion?**

36. **What is a circular dependency in Terraform, and how do you resolve it?**

37. **How do you manage secrets in Terraform without exposing them in logs or the Terraform state file?**

38. **Does `sensitive = true` prevent secrets from being stored in Terraform state?**

39. **Can you use a Terraform data block to retrieve secrets? Does it guarantee that the secret won't appear in state?**

40. **How do you get a specific commit from another developer's branch into your branch?**

41. **How do you temporarily save local Git changes without committing or pushing them?**

42. **For a production environment, would you prefer Git merge or Git rebase?**

43. **What is the difference between margin and markup?**

44. **You get "No space left on device," but `df -h` shows only 50% disk usage. Why?**

45. **How can a Linux filesystem have free disk space but still report "No space left on device"?**

46. **How do you troubleshoot and remove zombie processes from a Linux server?**

47. **Once you identify the parent PID of a zombie process, what commands do you use to handle it?**
#### FINEOS and client focus 
21. **How do you create a Golden AMI?**
22. **What kind of Python coding/scripting experience do you have, including Lambda functions?**
23. **How would you structure reusable Terraform code for multiple environments?**
24. **If the Terraform state file stored in S3 is deleted and S3 Versioning is not enabled, can it be recovered?**
25. **Can the infrastructure be recreated if the Terraform state file is lost?**
26. **If the state file is lost, what approach would you take to recover or recreate the infrastructure?**
27. **How do you test Terraform code? What different Terraform testing strategies have you used?**
28. **What do you work on in CI/CD, and what kind of pipeline have you defined?**
29. **Have you written a pipeline that deploys a backend onto ECS/ECS Cluster?**
30. **How do you connect Jenkins/CI-CD with the AWS account to deploy to EKS?**
31. **What is a CNI plugin in Kubernetes?**
32. **What is NetworkPolicy in Kubernetes?**
33. **What is ingress and egress?**
34. **What is network traffic?**
35. **What is DNS in Kubernetes?**
36. **How do you create a ServiceAccount?**
37. **What things should be mentioned inside a ServiceAccount?**
38. **What is your expertise in AWS? Which AWS services and tools have you worked on?**
39. **Have you provisioned any VPC?**
40. **What exactly do we use an Internet Gateway and NAT Gateway for?**
41. **Why do we use a route table?**
42. **What is a load balancer? What are the types of load balancers and what are they used for?**
43. **For a banking application, which load balancer would be more feasible to use?**
44. **Have you provisioned an EKS cluster?**
45. **What are the components of the control plane/master node and worker node in EKS?**
46. **When you run a `kubectl` command, what exactly happens and where does it fetch the data from?**
47. **What are Authentication, Authorization, and Admission Control in Kubernetes?**
48. **What exactly does Admission Control do?**
49. **If a Pod needs to connect to S3, do we need PVCs and volumes, or how do we provide connectivity?**
50. **Can we use an S3 endpoint in the Kubernetes Deployment file to connect a Pod to S3?**
51. **Which DevOps tools have you worked with?**
52. **How does CI start automatically when a developer pushes code to GitHub?**
53. **What exactly have you worked on in Terraform?**
54. **What is the Terraform state file, why is it important, and where should we keep it?**
55. **If Terraform detects drift, how do you make sure it won't impact the current infrastructure?**
56. **If three or four developers are working on the same Terraform code, should they use the same workspace or different workspaces?**
57. **Where do you store the Terraform code at the end of the day when multiple developers are working on it?**
58. **Why do we need a Terraform provider file and output file?**
59. **How do you provision two EKS clusters in different AWS regions using only one reusable Terraform module?**
60. **How do you use Prometheus, Grafana, and CloudWatch for monitoring?**
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
