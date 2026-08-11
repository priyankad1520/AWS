#### You have an EC2 instance running in a private subnet. The application needs to access the internet to download packages and updates, but it should not be directly accessible from the internet. How would you configure this?
For an EC2 instance in a private subnet to access the internet, we create a NAT Gateway in a public subnet and configure the private subnet's route table with a default route to the NAT Gateway. The NAT Gateway then uses the Internet Gateway to access the internet. This allows the private EC2 instance to download packages and updates, while the instance itself doesn't have a direct route from the internet."

Private EC2 → Private Route Table → NAT Gateway → Internet Gateway → Internet

#### Your EC2 instance in a private subnet cannot access the internet even though a NAT Gateway has been created. How would you troubleshoot this issue?
"If a private EC2 instance cannot access the internet even though the NAT Gateway exists, first I'll check the private subnet's route table and verify that 0.0.0.0/0 points to the NAT Gateway. Then I'll check whether the NAT Gateway is in a public subnet, is in the Available state, and has an Elastic IP. I'll verify that the public subnet route table has a route to the Internet Gateway. After that, I'll check the Security Group, Network ACL, and DNS configuration. This helps me identify exactly where the connectivity path is breaking."

EC2 → Private Route Table → NAT Gateway → Public Route Table → Internet Gateway → Internet

* Check the private route table: Verify 0.0.0.0/0 → NAT Gateway.
* Check NAT Gateway: It should be in a public subnet.
* Verify it's in Available state.: Verify it has an Elastic IP.
* Check the public subnet route table: Verify 0.0.0.0/0 → Internet Gateway.
* Check Network ACLs: Make sure traffic isn't being blocked.
* Check Security Group: Verify the EC2 outbound rules allow the required traffic.
* Check DNS: If the instance can reach an IP but cannot resolve google.com, investigate DNS configuration.

#### 3. "What is the difference between a Security Group and a Network ACL? Where have you used each in your project?"
Both Security Groups and Network ACLs are used to control network traffic, but they work at different levels. A Security Group is attached to resources like EC2 and is stateful, so when traffic is allowed in one direction, the return traffic is automatically allowed. A Network ACL is associated with a subnet and is stateless, so we need to configure both inbound and outbound rules explicitly. In our project, we mainly use Security Groups for EC2 and load balancers, and NACLs when we need subnet-level network control."
* Security Group → Resource → Stateful
* NACL → Subnet → Stateless

#### 4. An EC2 instance is running, but you cannot connect to it using SSH. How would you troubleshoot this issue?
**"If I cannot SSH to an EC2 instance, first I'll check whether the instance is running and its status checks are healthy. Then I'll verify I'm connecting to the correct IP and check the Security Group to make sure TCP port 22 is allowed from my source IP. I'll also check the subnet route table and Network ACL. If the network path is fine, I'll verify the SSH key, correct OS username, and whether the SSH service is running. If the instance is private, I'll use a bastion host, VPN, or SSM instead of trying to connect directly from the internet."**

**Client → Network → EC2 → SSH service → Authentication**

**EC2 status → IP → Route → SG → NACL → SSH port → Key/User → SSH service**

#### Troubleshooting approach
```bash
# 1. Check EC2 status: Make sure the instance and system status checks are healthy.
aws ec2 describe-instance-status

# 2. Check whether you're connecting to the correct IP
# If using a public IP, verify it hasn't changed.

# 3. Check Security Group: Verify inbound TCP **22** is allowed from your source IP.
# 4. Check Network ACL: Make sure inbound and return traffic isn't being blocked.
# 5. Check subnet routing: For a public EC2:
# Public Subnet → Internet Gateway
# For a private EC2, you normally **cannot directly SSH from the internet**. You may need a bastion host, VPN, or AWS Systems Manager Session Manager.
# 6. Check SSH key and username
ssh -i key.pem ec2-user@<public-ip>
# 7. Check the SSH service: If you have console/SSM access:
systemctl status sshd
```
#### 5. An EC2 instance is running at 100% CPU and the application is becoming slow. How would you troubleshoot and resolve it?
If an EC2 instance is running at 100% CPU and the application is slow, first I'll check CloudWatch metrics and identify whether the high CPU is due to increased traffic or a specific application process. I'll also check the application logs and CPU-consuming processes on the instance. If the issue is genuine high traffic, I'll use an Auto Scaling Group behind a load balancer to add more EC2 instances and distribute the traffic. If it's an application or process issue, I'll fix the root cause instead of simply adding more instances. Finally, I'll monitor the CPU and application response time to confirm the issue is resolved."

High CPU → Check CloudWatch → Identify cause → High traffic? → Scale out → Monitor

100% CPU does not always mean high traffic. It could be:
* High traffic
* Application CPU-intensive process
* Memory pressure causing CPU activity
* Infinite loop/application bug
* Background process
* Poorly optimized code
```bash
# So first investigate, then decide whether scaling is the correct fix.
# You can check:
top
# or:
ps aux --sort=-%cpu | head
# And from AWS, check CloudWatch CPUUtilization and application metrics/logs.
```
#### 6. Your EC2 instance is healthy, but users are still getting 503 Service Unavailable from the Application Load Balancer. How would you troubleshoot this?
If users are getting 503 from an ALB while the EC2 instance itself is healthy, first I'll check the ALB Target Group and verify whether the EC2 target is healthy. I'll check the health-check path, port, protocol, and the failure reason. Then I'll verify that the ALB Security Group can reach the EC2 Security Group on the application port. I'll also test the application directly from the EC2 using curl and check the application logs. Finally, I'll verify the ALB listener is forwarding traffic to the correct target group. Once the target becomes healthy, I'll test the application again from the ALB endpoint.

* User → ALB → Listener → Target Group → Health Check → EC2 SG → Application → Logs
* And remember the distinction: ALB 503 → Check Target Group/EC2
* Kubernetes Ingress 503 → Check Service/Endpoints/Pods

#### 7. An EC2 instance is showing as healthy in the Target Group, but users are getting 502 Bad Gateway from the ALB. What would you check?
If the EC2 target is healthy but users are getting 502 from the ALB, first I'll check whether the application is actually listening on the configured target port. Then I'll verify the ALB listener and target group port configuration. I'll check the EC2 Security Group to make sure it allows traffic from the ALB Security Group. After that, I'll test the application directly from the EC2 using curl and check the application logs for connection or application errors. I'll also verify whether the application is closing the connection or returning an invalid response to the ALB. Once I identify and fix the issue, I'll test the application again through the ALB.

#### 8. Your application is running on multiple EC2 instances behind an ALB, but one EC2 instance is receiving much more traffic than the others. What could be the reason, and how would you troubleshoot it?
> If one EC2 instance is receiving much more traffic than the others, first I'll check whether all the targets are healthy in the ALB Target Group. Then I'll verify the target registration, listener rules, and whether any targets were recently added or removed. I'll also check whether sticky sessions are enabled, because the ALB may keep a user's requests going to the same instance. Then I'll compare the application and network metrics across all instances using CloudWatch. If there's no configuration issue, I'll check whether the traffic distribution is affected by connection patterns or long-lived connections. After identifying the cause, I'll fix the ALB or application configuration and monitor the traffic distribution again."**

**Troubleshooting flow: ALB → Target Group → Target Health → Listener Rules → Sticky Sessions → Connection Pattern → CloudWatch → Fix → Validate**
#### 9. Your EC2 instance is running normally, but the application suddenly becomes unreachable. What would you check first, and how would you troubleshoot it?
If the EC2 instance is running but the application suddenly becomes unreachable, first I'll check CloudWatch metrics and logs to identify when the issue started and whether there is any CPU, memory, network, or application error. Then I'll check the application service on the EC2 and verify whether it's listening on the expected port. I'll test the application locally using curl. If the application is working locally, I'll check the ALB target health, Security Group, Network ACL, and routing. I'll also check whether the application has any dependency issue with the database or external service. After identifying the root cause, I'll fix it and monitor the application to confirm it's accessible again."

CloudWatch → EC2 → Application → Port → ALB → SG/NACL → Dependencies → Fix → Validate
