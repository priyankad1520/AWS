### **1. How is the Kubernetes (EKS) cluster setup done?**

> **In our project, we use Terraform to create the complete EKS infrastructure.**
>
> **First,** we create the **VPC**, **public and private subnets**, **Internet Gateway**, **NAT Gateway**, **route tables**, and **security groups** across multiple Availability Zones.
>
> **Next,** we create the **EKS cluster** using Terraform. AWS automatically provisions the **managed control plane**, so we don't manage the master nodes.
>
> **Then,** we create **EKS Managed Node Groups** in the **private subnets**. We attach the required **IAM roles** and install the **Amazon VPC CNI**, **CoreDNS**, and **kube-proxy** add-ons.
>
> **After that,** we install the required components like the **AWS Load Balancer Controller**, **Metrics Server**, **Cluster Autoscaler**, **Fluent Bit**, **Prometheus**, and **Grafana**.
>
> **Finally,** we deploy applications using **Helm** through the **Jenkins CI/CD pipeline**, verify the pods and services, and test application access through the **ALB Ingress**.
>
> **The best practice is to automate the entire cluster setup using Terraform so the environment is consistent, repeatable, and easy to manage.**


> **In our project, we worked on Kubernetes migration and cost optimization together.**
>
> **First,** we analyzed the existing application to understand its dependencies, resource usage, and whether it was suitable for Kubernetes. Then, we containerized the application using **Docker** and stored the images in **Amazon ECR**.
>
> **Next,** we created the Kubernetes infrastructure on **Amazon EKS** using **Terraform** and deployed the application using **Helm**. We configured **ConfigMaps**, **Secrets**, **Ingress**, and **Horizontal Pod Autoscaler (HPA)** to make the application production-ready. After testing in the staging environment, we migrated production using a **rolling update** to avoid downtime.
>
> **Then,** for cost optimization, we analyzed CPU and memory usage using **Prometheus** and **Grafana**. We **right-sized** the pod resource requests and limits, enabled **Cluster Autoscaler** to add or remove worker nodes based on demand, and used **Spot Instances** for non-production workloads. We also cleaned up unused EBS volumes, old ECR images, and idle resources, and used **S3 lifecycle policies** to move old data to cheaper storage classes.
>
> **Finally,** we continuously monitored resource utilization and adjusted configurations based on actual usage.
>
> **The best practice is to migrate only after proper testing and optimize costs continuously by monitoring real usage instead of overprovisioning resources.**

## **1. What is AWS Lambda, and how does it work?**

> **In our project, we use AWS Lambda to run small automation tasks without managing servers. For example, automating EC2 start/stop, cleaning old snapshots, or triggering infrastructure-related tasks.**
>
> **First,** we create a Lambda function in the **AWS Lambda Console** or using **Terraform**. Then we choose the runtime, such as **Python**, and write the function code or upload a ZIP file.
>
> **Next,** we attach an **IAM Role** so the Lambda function has permission to access AWS services like **EC2**, **S3**, or **CloudWatch**.
>
> **Then,** we configure a trigger, such as an **EventBridge schedule**, **S3 upload event**, or **API Gateway** request. When the event occurs, AWS automatically starts the Lambda function, executes the code, and returns the result.
>
> **Finally,** we monitor the execution using **CloudWatch Logs** and configure retries or error handling if required.
>
> **The best practice is to use Lambda for short-running, event-driven automation tasks and give it only the minimum IAM permissions it needs.**

---

## **2. How do you invoke a Lambda function, and where do you configure it?**

> **In our project, we configure Lambda triggers from the AWS Lambda Console under the function's "Triggers" section, or we define them using Terraform.**
>
> **First,** we create the Lambda function and attach the required IAM role.
>
> **Next,** we configure how the function should be invoked. Common triggers include:
>
> * **EventBridge** – for scheduled jobs (cron)
> * **S3** – when a file is uploaded
> * **API Gateway** – when an API request is received
> * **SNS or SQS** – for messages
> * **CloudWatch Alarms** – for operational events
>
> **Then,** whenever the configured event occurs, AWS automatically invokes the Lambda function. We can also invoke it manually from the AWS Console, using the **AWS CLI**, or through an AWS SDK.
>
> **The best practice is to use event-based triggers instead of polling because it is more efficient and cost-effective.**

---

## **3. Can you describe how Lambda handles scaling and event-based invocations?**

> **In our project, one of the main advantages of Lambda is that AWS automatically manages scaling.**
>
> **First,** whenever an event is received, AWS creates an execution environment and runs the Lambda function. If one request comes, one execution starts.
>
> **Next,** if hundreds or thousands of events arrive at the same time, AWS automatically creates multiple Lambda instances to process them in parallel. We do not need to provision servers or configure an Auto Scaling Group.
>
> **Then,** when the workload decreases, AWS automatically scales the Lambda executions back down, and we pay only for the execution time.
>
> **Finally,** because Lambda is event-driven, it runs only when an event occurs, such as an S3 upload, API Gateway request, EventBridge schedule, or an SQS message.
>
> **The best practice is to design Lambda functions to be stateless and idempotent, because multiple executions can run concurrently.**

## **1. How do you attach an SSL certificate to an S3 bucket?**

This is a trick interview question.

> **In AWS, we cannot attach an SSL certificate directly to an S3 bucket because S3 does not support custom SSL certificates.**
>
> **In our project,** if we want users to access S3 securely using our own domain, **first** we create an SSL certificate in **AWS Certificate Manager (ACM)**.
>
> **Next,** we create an **Amazon CloudFront** distribution and configure the **S3 bucket as the origin**.
>
> **Then,** we attach the ACM SSL certificate to the **CloudFront distribution**, configure our custom domain in **Route 53**, and point it to CloudFront.
>
> **Finally,** users access the application through **HTTPS**, and CloudFront securely retrieves the content from the S3 bucket.
>
> **The best practice is to use CloudFront with ACM for custom HTTPS access to S3 instead of trying to attach a certificate directly to the bucket.**

---

## **2. What type of encryption have you implemented in your project?**

> **In our project, we implemented encryption both at rest and in transit.**
>
> **First,** for **encryption at rest**, we enabled **AWS KMS-managed encryption (SSE-KMS)** for services like **S3**, **EBS**, and **RDS** to protect stored data.
>
> **Next,** for **encryption in transit**, we used **HTTPS with TLS certificates** from **AWS Certificate Manager (ACM)** for applications behind the **Application Load Balancer (ALB)** or **CloudFront**, so data is encrypted while traveling over the network.
>
> **We also** stored sensitive information such as passwords and API keys in **AWS Secrets Manager** instead of hardcoding them in the application.
>
> **The best practice is to encrypt data both at rest and in transit and manage encryption keys securely using AWS KMS.**

---

## **3. If an S3 bucket has a read-only policy, can you modify objects in the bucket?**

> **No. If a user has only read-only permissions, they cannot modify, upload, or delete objects in the bucket.**
>
> **In our project,** read-only access means the IAM policy allows actions like **`s3:GetObject`** and **`s3:ListBucket`**, but it does **not** allow actions such as **`s3:PutObject`** or **`s3:DeleteObject`**.
>
> If someone needs to update an object, they must have additional write permissions through an **IAM policy** or **bucket policy**.
>
> **The best practice is to follow the principle of least privilege by giving users only the permissions they need to perform their job.**

