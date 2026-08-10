#### 1. Your Terraform pipeline was working fine earlier, but now terraform plan is showing unexpected changes to resources even though nobody intentionally changed the Terraform code. What could be the reason, and how would you troubleshoot and fix it?
This is usually a Terraform drift issue. It can happen when someone manually changes a resource from the AWS Console instead of using Terraform. First, I'll review the terraform plan output and identify exactly what changed. If the manual change is required, I'll update the Terraform code to match the desired configuration. If the change was not required, I'll run terraform apply so Terraform brings the resource back to the configuration defined in the code. Finally, I'll run terraform plan again and make sure there are no unexpected changes.

Remember this flow: Unexpected plan → Identify drift → Review change → Keep or revert → Update Terraform code if needed → Apply → Plan again → Validate

#### 2. Your Terraform apply fails because the state is locked by another process. What could be the reason, how would you troubleshoot it, and how would you safely resolve the state lock?
This issue occurs because Terraform state locking is enabled, and another Terraform process may already be using the same state file. First, I'll check whether another Terraform apply or pipeline is currently running and wait for it to complete. If no process is running and the lock is stale because a previous operation failed or was interrupted, I'll verify the lock information and safely remove the lock using terraform force-unlock <LOCK_ID>. I won't force-unlock it while another Terraform operation is running because it can cause state corruption. After removing a stale lock, I'll run terraform plan again and verify the state."

Remember the production flow: State locked → Check another Terraform run → Wait if active → Check stale lock → terraform force-unlock only if safe → terraform plan → Validate

The most important sentence to remember is: "I won't force-unlock the state until I confirm that no other Terraform operation is running."

### 3. Your Terraform plan is successful, but terraform apply fails halfway through. Some resources are created and some are not. How would you troubleshoot and recover from this situation?
If Terraform plan is successful but apply fails halfway, first I'll check the Terraform error message to identify which resource failed and why. Then I'll verify the AWS resource and permissions involved. Since Terraform maintains the state, the resources that were successfully created will normally already be recorded in the state file. I'll fix the root cause and run `terraform plan` again to see what is still pending, and then run `terraform apply` to complete the remaining changes. Finally, I'll verify the infrastructure and Terraform state are consistent.

* `terraform plan` tells us: **"Based on the current configuration and state, this is what Terraform intends to do."**
* `terraform apply` actually communicates with AWS and creates/changes the resources and can encounter runtime/API/permission/resource issues.. So `apply` can fail because of things that only become apparent when Terraform actually talks to AWS.
* For example: AWS API error, IAM permission denied, Resource limit/quota, Dependency failure, Invalid AWS configuration,  Network/API timeout, Resource already exists, Insufficient capacity
* You **don't normally delete everything and start again**.
* Think: **Plan successful → Apply partially fails → Check error → Fix root cause → Plan again → Apply again → Validate**

#### 4. You ran terraform apply, and it failed with an AccessDenied error while creating an AWS resource. How would you troubleshoot and fix it?
"I'll verify which IAM Role or credentials Terraform is using and check whether that identity has the required permissions."

If Terraform apply fails with an AccessDenied error, first I'll check the exact AWS API action mentioned in the error message. Then I'll identify which IAM user or role Terraform is using and verify whether it has permission for that action. I'll check the attached IAM policies and make sure we're following least privilege. If the required permission is missing, I'll update the IAM role or policy and run terraform plan and terraform apply again. Finally, I'll verify that the resource was created successfully.

#### 5. Your Terraform state file is stored in an S3 bucket. What will happen if two engineers run terraform apply at the same time, and how do you prevent this?
If two engineers run terraform apply at the same time using the same remote state, Terraform state locking prevents both operations from modifying the state simultaneously. One engineer gets the state lock and continues the apply, while the other receives a state lock error. To prevent this, we should allow only one Terraform operation at a time and wait for the first operation to complete before running the second. In our project, we also handle Terraform deployments through a CI/CD pipeline so we can control concurrent deployments

#### 6. What is the difference between terraform plan and terraform apply, and what happens internally when you run each command?
The main difference is that `terraform plan` is a preview, while `terraform apply` actually makes the changes. When I run `terraform plan`, Terraform compares the configuration, state, and current infrastructure and shows what resources will be created, modified, or deleted. When I run `terraform apply`, Terraform communicates with AWS, performs those changes, and updates the Terraform state with the new infrastructure information."**

`terraform plan` compares the **configuration + current state + real infrastructure** and generates an execution plan.

`terraform apply` uses that plan and makes the required changes to the infrastructure, then **updates the Terraform state**.

#### 7. "What is Terraform state, why is it required, and what would happen if you accidentally delete the Terraform state file?"
* The Terraform configuration is stored in your .tf files. The state file stores information about the resources Terraform manages, including their IDs, attributes, and the relationship between your configuration and the real infrastructure.
* Also, if the state file is deleted, Terraform doesn't necessarily create everything blindly. It will lose its knowledge of the existing resources, so it may propose creating them again, and some resources may fail because they already exist.
"Terraform state keeps track of the resources that are managed by Terraform, including their resource IDs and current attributes. Terraform uses this state along with the Terraform code and actual infrastructure to identify changes and detect drift. If the state file is accidentally deleted, Terraform loses track of the existing resources and may try to create them again during the next plan or apply. In our project, we store the state remotely in S3 with state locking and enable versioning, so we can recover the state if it's accidentally deleted or corrupted."
#### 8. What is Terraform drift? How do you identify it, and how would you handle it in production?
Terraform drift happens when a resource managed by Terraform is manually changed outside Terraform, for example from the AWS Console. When I run terraform plan, Terraform compares the configuration, state, and actual infrastructure and shows the difference. First, I'll review the drift and understand whether the manual change was intentional. If we want to keep the change, I'll update the Terraform code to match it. If the change was not required, I'll run terraform apply to bring the resource back to the configuration defined in Terraform. Finally, I'll run terraform plan again to confirm there is no remaining drift.

* If someone changed a resource manually and we want to revert the manual change, we generally run: `terraform apply`
* Terraform will bring the resource back to what is defined in the Terraform configuration.
* If we want to keep the manual change, we should update the Terraform code to reflect that desired configuration and then apply it.

#### 9. What is the difference between count and for_each in Terraform? When would you use each one in your project?
**"In our project, we use `count` and `for_each` when we need to create multiple similar resources without duplicating the Terraform code. I use `count` when I simply need a specific number of similar resources. I use `for_each` when each resource needs different values or configuration, because each instance gets a unique key. For example, if I need three similar EC2 instances, I can use `count`. If I need EC2 instances with different names, instance types, or configurations, I prefer `for_each`."**
* Don't say `count` can **only** create resources with the same values. You can technically use `count.index` to vary values, but `for_each` is generally better when each resource has a distinct identity or configuration.
* **`count`** → How many?.  creates multiple instances based on a **number/index**.
* **`for_each`** →   Which ones / what values?. creates instances based on a **map or set of values**, giving each instance a stable key.

#### 10. What is a Terraform module? How do you create and use a module in your project?
**"In our project, Terraform modules are reusable blocks of Terraform code that help us avoid writing the same infrastructure code repeatedly. For example, instead of writing the EC2 configuration separately for Dev, QA, and Production, we created a reusable EC2 module with `main.tf`, `variables.tf`, and `outputs.tf`. From the root module, we call it using `source = \"./modules/ec2\"` and pass the required values through variables. This makes our infrastructure reusable, consistent, and easier to maintain."**

```hcl
# The syntax is:
module "ec2" {
  source = "./modules/ec2"
}

# And you don't put the reusable code in one single "module file."
# A module is generally a **directory containing Terraform files**, such as:
modules/
├── ec2/
│   ├── main.tf
│   ├── variables.tf
│   └── outputs.tf
├── vpc/
│   ├── main.tf
│   ├── variables.tf
│   └── outputs.tf
```
#### 11."You have created a Terraform module for EC2. How would you pass different values like instance type, AMI ID, and subnet ID from the root module to the EC2 module?"**
**"In our project, we pass values from the root module to the EC2 module using a module block. We specify the module path using `source`, and then pass values like `instance_type`, `ami_id`, and `subnet_id` as input variables. For example, we can pass `instance_type = \"t3.micro\"`, `ami_id = \"ami-xxxx\"`, and `subnet_id = \"subnet-xxxx\"`. Inside the EC2 module, we define these variables in `variables.tf` and use them in `main.tf` to create the EC2 instance."**

**Simple example**

```hcl
# Root module:
module "ec2" {
  source        = "./modules/ec2"
  instance_type = "t3.micro"
  ami_id        = "ami-123456"
  subnet_id     = "subnet-123456"
}

# Child module — `variables.tf`:
variable "instance_type" {}
variable "ami_id" {}
variable "subnet_id" {}

# Child module — `main.tf`:
resource "aws_instance" "this" {
  ami           = var.ami_id
  instance_type = var.instance_type
  subnet_id     = var.subnet_id
}
```
* The flow is:**Root module → Module block → Input variables → Child module → AWS resource**
* We pass the values from the root module through the module block, and the child module receives those values through input variables.

#### 12."What are Terraform input variables and output variables, and how have you used them in your project?"**
**"In our project, we use input variables to pass values into our Terraform modules, such as AMI ID, instance type, VPC ID, or subnet ID, based on the environment. Output variables are used to expose values generated or returned by the resources, such as an EC2 public IP, private IP, or ALB DNS name. These outputs can be displayed using `terraform output` or passed to other modules."**

* **Input variable → values we provide to Terraform. /We give values to Terraform**
* **Output variable → values Terraform exposes after creating/managing resources./Terraform gives values back to us.**
* Also, outputs aren't only for displaying on the terminal. They can be **used by other Terraform modules** as well.
---

#### 13. "What is the difference between `terraform refresh`, `terraform plan`, and `terraform apply`?"
**"`terraform plan` shows what changes Terraform is going to make without actually changing the infrastructure. `terraform apply` communicates with the cloud provider and actually creates, updates, or deletes the resources. `terraform refresh` updates the Terraform state with the current information from the real infrastructure. In our project, we normally use `plan` and `apply`, because Terraform automatically refreshes the state during these operations."**

**`terraform refresh` updates the Terraform state to match the current real infrastructure.**

For example, if someone manually changes an EC2 instance in AWS, Terraform can refresh the state with the current AWS values. Also, in modern Terraform, you generally don't need to run `terraform refresh` separately. A normal:
```bash
terraform plan
# or. performs a refresh of the state as part of the operation.
terraform apply
```

* **Plan → What will change?**
* **Apply → Make the change.**
* **Refresh → Update state with what's actually in AWS.**

---

#### 14. What is the difference between Terraform `taint` and `terraform apply -replace`? When would you use them?
**"`terraform apply -replace` is used when I want Terraform to destroy and recreate a specific resource. For example, if an EC2 instance has an issue and I want to replace only that instance, I can use `terraform apply -replace=\"aws_instance.web\"`. The older `terraform taint` command was used for the same purpose, but `-replace` is the recommended approach now. It helps us target a specific resource instead of unnecessarily replacing other resources."**

* **`terraform plan` → Preview changes.**
* **`terraform apply -replace` → Force replacement of a specific resource.** **Replace = destroy + recreate that specific resource.**
* **`terraform taint` → Older way of marking a resource for replacement.**

#### 15. What is the difference between Terraform state stored locally and a remote backend like S3? Why did you use S3 for Terraform state in your project?
In our project, we store Terraform state remotely in an S3 bucket instead of keeping it locally because multiple engineers and our CI/CD pipeline need to work with the same state. With local state, the state file is available only on that engineer's machine, which makes team collaboration difficult. We use S3 as a centralized backend and enable versioning so we can recover an earlier version if the state is accidentally modified or deleted. We also use IAM policies to control who can access the state. This gives us centralized, secure, and recoverable Terraform state management.
* Local state → Individual machine
* S3 remote state → Centralized team access + versioning + access control + recovery
#### 16. You have a Terraform resource that was created manually in AWS, and now you want Terraform to manage it without recreating it. How would you do that?
If a resource already exists in AWS but is not managed by Terraform, we use `terraform import` to bring that existing resource into Terraform state without recreating it. First, I'll define the corresponding resource block in the Terraform code. Then I'll run the `terraform import` command with the resource address and the AWS resource ID. After importing, I'll run `terraform plan` and update the Terraform code to match the existing resource configuration so that there are no unexpected changes.

```bash
# For example:
terraform import aws_instance.web i-1234567890abcdef
```
The important flow is: **Existing AWS resource → Terraform resource block → `terraform import` → State → `terraform plan` → Match code with actual resource**

---

#### 17. What happens if you run `terraform destroy` in production by mistake? How would you prevent this from happening?
If someone accidentally runs terraform destroy in production, Terraform can delete the infrastructure resources managed by that state, so we should prevent this at the process level. In our project, we protect production using CI/CD approvals, restricted IAM permissions, separate workspaces or state, and manual approval before destructive changes. We also review the terraform plan before applying any production changes. If resources are accidentally deleted, we recover them based on our backups and disaster-recovery process rather than using terraform import.

#### 18. How do you protect your production Terraform infrastructure from accidental terraform destroy or other destructive changes?
In our project, we protect production Terraform infrastructure by using CI/CD approval, restricted IAM permissions, and separate production state. Before applying any production change, we review the terraform plan and require manual approval for destructive changes. We also restrict who can run Terraform against production and keep S3 state versioning and backups enabled. This helps us prevent accidental resource deletion and recover the Terraform state if required

#### 19. What is the difference between Terraform workspace and separate Terraform state files? When would you use each?
Terraform workspaces allow us to maintain multiple separate state files using the same Terraform configuration. For example, we can have Dev, QA, and Production workspaces, and each workspace maintains its own state. Separate state files or separate Terraform configurations provide stronger isolation when environments have significantly different configurations, AWS accounts, or permissions. In our project, we prefer separate state for Production because we want stronger isolation and don't want a change in Dev or QA to affect the Production state."

* Workspace → Same code, different state.
* Separate configuration/state → Stronger environment isolation.

#### 20. What happens if two different Terraform configurations try to manage the same AWS resource?
If two different Terraform configurations try to manage the same AWS resource, it can cause conflicting changes and state management issues. Both configurations may think they own the same resource, so one configuration can overwrite or revert changes made by the other. To avoid this, we make sure each resource has a single Terraform owner and keep separate state files for different environments or components

#### 21. What is the difference between terraform state list, terraform state show, and terraform state rm? When would you use each?
**terraform state list** shows all the resources currently tracked in the Terraform state. **terraform state show** displays detailed information about a specific resource in the state, such as its ID and attributes. **terraform state rm** removes a specific resource from the Terraform state without deleting the actual AWS resource. We use it when we want Terraform to stop managing a particular resource."
* state list → What resources are tracked?
* state show → Show details of one resource.
* state rm → Stop Terraform tracking it; don't delete AWS resource.

#### 22. What is Terraform dependency? What is the difference between implicit and explicit dependencies?"
Dependency means one resource depends on another resource to be created or exist first. For example, an EC2 instance depends on a subnet, and the subnet is part of a VPC. When there is a direct resource reference, Terraform automatically understands the dependency; this is called an implicit dependency. If there is no direct reference but one resource still needs another resource to be created first, we explicitly define it using the depends_on argument. That's called an explicit dependency.
Absolutely. This is an important Terraform concept, and I'll explain it in a simple way before you answer.

#### What does "dependency" mean?

**Dependency means one resource needs another resource to exist or be created first.**

* For example, suppose we create: VPC → Subnet → EC2
* The **EC2 instance depends on the Subnet**, and the Subnet depends on the VPC.
* Terraform needs to understand this order so it doesn't try to create the EC2 before the subnet exists.

#### 1. Implicit Dependency

Terraform automatically understands the dependency when one resource **references another resource**.

```hcl
resource "aws_instance" "web" {
  subnet_id = aws_subnet.app.id
}
# Because the EC2 references `aws_subnet.app.id`, Terraform automatically knows:
# Create the subnet first, then create the EC2.
```
#### 2. Explicit Dependency

Sometimes one resource depends on another, but there is **no direct reference** between them. We tell Terraform explicitly using: **depends_on**

```hcl
resource "aws_instance" "web" {
  depends_on = [
    aws_iam_role_policy.app
  ]
}
# Now Terraform knows:**Create the IAM policy first, then create the EC2 instance.**
# Terraform IAM Role/User → Permission to create/manage AWS resources: ec2:RunInstances, ec2:DescribeInstances, ec2:CreateTags
# EC2 IAM Role → Permission for the application running on EC2 to access AWS services: EC2 → IAM Role → IAM Policy → S3
```
**Implicit dependency:** Terraform automatically understands the dependency from the resource reference.

**Explicit dependency:** We manually tell Terraform about the dependency using `depends_on`.

#### 23. What is Terraform data source? How is it different from a Terraform resource, and where have you used data sources in your project?
A Terraform data source is used to read information about an existing resource instead of creating or managing that resource. For example, in our project, if a VPC already exists and we need its VPC ID while creating another resource, we can use an AWS VPC data source to retrieve that information and reference it in our Terraform code. A resource is used to create or manage infrastructure, whereas a data source is mainly used to read existing infrastructure information.
* Resource → Creates/manages something.
* Data source → Reads something that already exists.

#### 24. In your Terraform project, you have a VPC module and an EC2 module. How would you pass the VPC ID created by the VPC module to the EC2 module?
In our project, we pass the VPC ID between modules using Terraform outputs and input variables. The VPC module exposes the VPC ID through an output variable, and the root module passes that output to the EC2 module as an input variable. This creates an implicit dependency, so Terraform knows that the VPC needs to be created before the dependent resources.

**VPC module creates VPC → VPC module outputs VPC ID → Root module receives it → EC2 module uses it**
```hcl
# VPC module: `modules/vpc/outputs.tf`:
output "vpc_id" {
  value = aws_vpc.main.id
}

# Root module
module "vpc" {
  source = "./modules/vpc"
}

module "ec2" {
  source = "./modules/ec2"

  vpc_id = module.vpc.vpc_id
}
# EC2 module: `modules/ec2/variables.tf`:
variable "vpc_id" {
  type = string
}
# Then the EC2 module can use:
vpc_id = var.vpc_id
# However, in a real EC2 resource, you normally provide a **subnet ID**, rather than a VPC ID directly:
subnet_id = var.subnet_id
# The subnet itself belongs to that VPC.
```
---

#### 24. What is the difference between an IAM role attached to an EC2 instance and the IAM role used by Terraform to create that EC2 instance?"**
The Terraform IAM role and EC2 IAM role have different purposes. The IAM role used by Terraform gives Terraform permission to create and manage AWS resources, such as EC2, VPC, and S3. The IAM role attached to the EC2 instance gives the application running on that instance permission to access other AWS services, such as S3 or Secrets Manager. So, one role is for infrastructure management, and the other is for the workload running on the EC2 instance.

#### 25. What is Terraform locals? Why would you use local values instead of variables in your project?
In our project, we use Terraform locals to define and reuse common or calculated values inside the Terraform configuration. For example, we can define common tags, naming conventions, or environment-specific expressions in a `locals` block and reuse them across multiple resources. We use variables when we want to accept values as input, whereas locals are mainly used for internal reusable values."**

* **`variable` → value comes from outside. Someone gives Terraform the value.**
* **`local` → value is calculated or defined inside Terraform. Terraform defines and reuses the value internally.**

### What is Terraform `locals`?

**Local values** are values that you define **inside your Terraform configuration** and reuse multiple times.

```hcl
# For example, suppose you repeatedly use the same naming format:
locals {
  environment = "production"
  name_prefix = "myapp-production"
}

# Then you can reuse it:
resource "aws_instance" "app" {
  tags = {
    Name        = "${local.name_prefix}-server"
    Environment = local.environment
  }
# Instead of writing `"myapp-production"` repeatedly, you define it once in `locals`.
```

**Why use `locals`?** We use locals when we have a **calculated value, common value, or expression that we want to reuse** within the Terraform configuration.

```hcl
locals {
  common_tags = {
    Environment = "production"
    Project     = "payment-app"
    ManagedBy   = "Terraform"
  }
}
# Then multiple resources can use:
tags = local.common_tags
```
This avoids **repeating the same values** throughout the code.

---

#### 26. What is the difference between `variable`, `local`, and `output` in Terraform?
In our project, we use Terraform `dynamic` blocks when we need to create multiple nested configuration blocks based on a variable or collection, instead of writing the same block repeatedly. For example, if a security group needs multiple ingress rules, we can use a dynamic block to generate those rules from a list or map. This makes the Terraform code reusable and avoids duplicate configuration.

* Dynamic block → Generate repeated nested blocks dynamically instead of writing them manually.
* For example: **Multiple ingress rules → `dynamic "ingress"` → Generate the required ingress blocks.**

```hcl
dynamic "ingress" {
  for_each = var.ingress_rules

  content {
    from_port   = ingress.value.from_port
    to_port     = ingress.value.to_port
    protocol    = ingress.value.protocol
    cidr_blocks = ingress.value.cidr_blocks
  }
}
```
#### 27. What is Terraform provider, and why do we need to configure a provider in Terraform?
The provider is a plugin that allows Terraform to communicate with the cloud provider's APIs and manage its resources. we use the AWS provider because it allows Terraform to communicate with AWS APIs and create and manage AWS resources like EC2, VPC, S3, and RDS. When we initialize Terraform, it downloads the required provider plugin based on the provider configuration

Terraform → Provider → Cloud API → AWS resources

#### 28. What is the difference between terraform init and terraform validate? When do you use each command?
`terraform init` initializes the Terraform working directory and downloads the required providers and modules. `terraform validate` checks whether the Terraform configuration is syntactically valid and internally consistent before we run plan or apply.
#### 29. What is the Terraform .terraform directory, and what is the purpose of the .terraform.lock.hcl file?
> **"`terraform init` creates the `.terraform` directory and downloads the required providers and modules. The `.terraform.lock.hcl` file records the selected provider versions and checksums, so the same provider versions are used consistently across our local environment and CI/CD pipeline. We commit the lock file to Git, but normally we don't commit the `.terraform` directory."**

**`.terraform` directory** When you run: terraform init

Terraform creates the **`.terraform` directory**.

It contains things such as:
* Downloaded provider plugins
* Downloaded modules
* Terraform's local working information

```text
For example:
.terraform/
├── providers/
└── modules/
```

You normally **don't manually modify this directory**, and it is generally not committed to Git.

---

### `.terraform.lock.hcl`

This file is very important.

It records the **specific provider versions and checksums** that Terraform selected.

For example, if your project uses AWS provider version `5.x`, the lock file helps ensure that another engineer or CI/CD pipeline uses the **same provider version/checksums** rather than unexpectedly downloading a different provider version.


> **`.terraform` → Downloaded providers/modules and working files**

> **`.terraform.lock.hcl` → Locks provider versions and verifies provider packages**


#### 30. What is Terraform moved block, and when would you use it?

> **"A Terraform `moved` block is used when we change the address or structure of a resource in our Terraform code but want Terraform to understand that it is still the same existing resource. For example, if we move an EC2 resource from the root module into an EC2 module, we can use a `moved` block so Terraform updates the state address instead of destroying and recreating the EC2 instance. We use it mainly during Terraform code refactoring to avoid unnecessary resource replacement."**

Example:

```hcl
moved {
  from = aws_instance.web
  to   = module.ec2.aws_instance.web
}
```

**Simple flow:**

**Old resource address → `moved` block → New resource address → Same AWS resource**

The important point is:

> **`moved` changes the Terraform state address; it does not recreate the actual AWS resource.**




