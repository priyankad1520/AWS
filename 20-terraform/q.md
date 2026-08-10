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


