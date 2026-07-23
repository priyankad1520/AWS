1. How is the Kubernetes (EKS) cluster setup done?

In our project, we use Terraform to create the complete EKS infrastructure.

First, we create the VPC, public and private subnets, Internet Gateway, NAT Gateway, route tables, and security groups across multiple Availability Zones.

Next, we create the EKS cluster using Terraform. AWS automatically provisions the managed control plane, so we don't manage the master nodes.

Then, we create EKS Managed Node Groups in the private subnets. We attach the required IAM roles and install the Amazon VPC CNI, CoreDNS, and kube-proxy add-ons.

After that, we install the required components like the AWS Load Balancer Controller, Metrics Server, Cluster Autoscaler, Fluent Bit, Prometheus, and Grafana.

Finally, we deploy applications using Helm through the Jenkins CI/CD pipeline, verify the pods and services, and test application access through the ALB Ingress.

The best practice is to automate the entire cluster setup using Terraform so the environment is consistent, repeatable, and easy to manage.

In our project, we worked on Kubernetes migration and cost optimization together.

First, we analyzed the existing application to understand its dependencies, resource usage, and whether it was suitable for Kubernetes. Then, we containerized the application using Docker and stored the images in Amazon ECR.

Next, we created the Kubernetes infrastructure on Amazon EKS using Terraform and deployed the application using Helm. We configured ConfigMaps, Secrets, Ingress, and Horizontal Pod Autoscaler (HPA) to make the application production-ready. After testing in the staging environment, we migrated production using a rolling update to avoid downtime.

Then, for cost optimization, we analyzed CPU and memory usage using Prometheus and Grafana. We right-sized the pod resource requests and limits, enabled Cluster Autoscaler to add or remove worker nodes based on demand, and used Spot Instances for non-production workloads. We also cleaned up unused EBS volumes, old ECR images, and idle resources, and used S3 lifecycle policies to move old data to cheaper storage classes.

Finally, we continuously monitored resource utilization and adjusted configurations based on actual usage.

The best practice is to migrate only after proper testing and optimize costs continuously by monitoring real usage instead of overprovisioning resources.
