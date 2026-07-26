# Amazon AMI — Complete Guide

## Table of Contents
1. [What is an AMI?](#1-what-is-an-ami)
2. [AMI Components](#2-ami-components)
3. [Types of AMIs](#3-types-of-ami)
4. [Finding the Right AMI](#4-finding-the-right-ami)
5. [Creating a Custom AMI](#5-creating-a-custom-ami)
6. [Copying and Sharing AMIs](#6-copying-and-sharing-amis)
7. [AMI Deregistration and Cleanup](#7-ami-deregistration-and-cleanup)
8. [AMI Lifecycle and Best Practices](#8-ami-lifecycle-and-best-practices)
9. [Cheat Sheet](#9-cheat-sheet)
10. [Common Interview Questions](#10-common-interview-questions)

---

## 1. What is an AMI?

An **AMI (Amazon Machine Image)** is a **template** used to launch an EC2 instance. It contains everything needed to boot a virtual machine:

- The **operating system** (Linux, Windows)
- **Application software** (if baked in)
- **Launch permissions** (who can use it)
- **Block device mappings** (which volumes to attach)

```
AMI = Blueprint for an EC2 Instance

AMI                                  EC2 Instance
┌───────────────────┐               ┌───────────────────┐
│ OS: Amazon Linux  │               │ Running OS        │
│ Apps: nginx       │──── Launch ──►│ Running nginx     │
│ Config: custom    │               │ Config applied    │
│ Size: 8GB root    │               │ 8GB EBS attached  │
└───────────────────┘               └───────────────────┘
         ↑
    Template only — can launch
    as many instances as you want
```

**Key facts:**
- AMIs are **region-specific** — an AMI in us-east-1 cannot be used in ap-south-1 directly (need to copy)
- AMIs are backed by **EBS snapshots** (for EBS-backed AMIs)
- Multiple instances can be launched from the same AMI
- You can create AMIs from running or stopped instances

---

## 2. AMI Components

An AMI consists of:

```
AMI: ami-xxxxxxxxxxxx
  ├── Root Volume Snapshot (snap-xxxx)
  │     └── Contains OS + applications
  ├── Additional Volume Snapshots (optional)
  │     └── Data volumes baked in
  ├── Launch Permissions
  │     ├── Private (only your account)
  │     ├── Explicit (specific AWS accounts)
  │     └── Public (anyone can launch)
  └── Block Device Mapping
        ├── /dev/xvda → 8 GB gp3 (root)
        └── /dev/xvdf → 50 GB gp3 (data)
```

---

## 3. Types of AMI

### By Source

| Type | Description | Example |
|------|-------------|---------|
| **AWS-provided** | Maintained by AWS, regularly patched | Amazon Linux 2023, Windows Server |
| **Marketplace AMIs** | Third-party vendors, may cost extra | WordPress by Bitnami, Kali Linux |
| **Community AMIs** | Public AMIs shared by other users | Use with caution |
| **Custom (your own)** | Created from your configured instance | Your golden image |

### By Storage Type

| Type | Description |
|------|-------------|
| **EBS-backed** | Root volume on EBS. Can stop/start. Most common. |
| **Instance store-backed** | Root volume on ephemeral storage. Cannot stop, only terminate. Rare. |

> **Always use EBS-backed AMIs** unless you have a very specific reason. Instance store-backed AMIs are a legacy option.

---

## 4. Finding the Right AMI

### Via Console
1. EC2 → Launch Instance → Browse AMIs
2. Filter by OS, architecture, region
3. Check "Free tier eligible" for learning

### Via CLI

```bash
# Find latest Amazon Linux 2023 AMI
aws ec2 describe-images \
  --owners amazon \
  --filters \
    "Name=name,Values=al2023-ami-*" \
    "Name=architecture,Values=x86_64" \
    "Name=state,Values=available" \
  --query 'sort_by(Images, &CreationDate)[-1].[ImageId,Name,Description]' \
  --output table

# Find latest Ubuntu 22.04 LTS
aws ec2 describe-images \
  --owners 099720109477 \
  --filters \
    "Name=name,Values=ubuntu/images/hvm-ssd/ubuntu-jammy-22.04-amd64-server-*" \
    "Name=state,Values=available" \
  --query 'sort_by(Images, &CreationDate)[-1].[ImageId,Name]' \
  --output table

# List YOUR own AMIs
aws ec2 describe-images --owners self --output table

# Get AMI details by ID
aws ec2 describe-images --image-ids ami-xxxxxxxxxxxxxxxxx
```

### Using SSM Parameter Store for Latest AMIs (Best Practice)

```bash
# Get latest Amazon Linux 2023 AMI via SSM (always current)
aws ssm get-parameter \
  --name /aws/service/ami-amazon-linux-latest/al2023-ami-kernel-default-x86_64 \
  --query 'Parameter.Value' \
  --output text

# Get latest Ubuntu 22.04 LTS
aws ssm get-parameter \
  --name /aws/service/canonical/ubuntu/server/22.04/stable/current/amd64/hvm/ebs-gp2/ami-id \
  --query 'Parameter.Value' \
  --output text
```

> **Use SSM parameter paths for AMI IDs in your scripts** — they always return the current AMI so you don't have to manually update AMI IDs when new ones are released.

---

## 5. Creating a Custom AMI

The workflow for creating a custom (golden) AMI:

```
1. Launch base EC2 instance
         │
         ▼
2. SSH in and configure:
   - Install packages (nginx, python, etc.)
   - Apply security hardening
   - Configure monitoring agents
   - Set system settings
         │
         ▼
3. Create AMI from the instance
   (AWS takes a snapshot of all EBS volumes)
         │
         ▼
4. AMI available in your account
         │
         ▼
5. Launch new instances from this AMI
   (Each instance starts pre-configured)
```

### Step-by-Step: Create a Golden AMI

**Step 1: Launch and configure a base instance**
```bash
# Launch a fresh instance
AMI_BASE=$(aws ssm get-parameter \
  --name /aws/service/ami-amazon-linux-latest/al2023-ami-kernel-default-x86_64 \
  --query 'Parameter.Value' --output text)

BASE_INSTANCE=$(aws ec2 run-instances \
  --image-id $AMI_BASE \
  --instance-type t2.micro \
  --key-name my-learning-key \
  --tag-specifications 'ResourceType=instance,Tags=[{Key=Name,Value=golden-image-builder}]' \
  --query 'Instances[0].InstanceId' --output text)

aws ec2 wait instance-running --instance-ids $BASE_INSTANCE
BASE_IP=$(aws ec2 describe-instances --instance-ids $BASE_INSTANCE --query 'Reservations[0].Instances[0].PublicIpAddress' --output text)
```

**Step 2: Install your software**
```bash
ssh -i ~/.ssh/my-learning-key.pem ec2-user@$BASE_IP << 'REMOTE'
  # System updates
  sudo dnf update -y

  # Install applications
  sudo dnf install -y nginx python3 python3-pip git curl wget htop

  # Configure nginx to start on boot
  sudo systemctl enable nginx

  # Install monitoring agent
  sudo dnf install -y amazon-cloudwatch-agent

  # Create application directory
  sudo mkdir -p /var/www/myapp
  sudo chown ec2-user:ec2-user /var/www/myapp

  # Security hardening
  sudo sed -i 's/#PermitRootLogin yes/PermitRootLogin no/' /etc/ssh/sshd_config
  sudo sed -i 's/PasswordAuthentication yes/PasswordAuthentication no/' /etc/ssh/sshd_config

  # Clean up to reduce image size
  sudo dnf clean all
  sudo rm -rf /tmp/*
  history -c
  
  echo "Configuration complete!"
REMOTE
```

**Step 3: Create the AMI**
```bash
# Stop the instance first for a clean snapshot (optional but recommended for databases)
# For stateless apps, you can create AMI from running instance
aws ec2 stop-instances --instance-ids $BASE_INSTANCE
aws ec2 wait instance-stopped --instance-ids $BASE_INSTANCE

# Create the AMI
MY_AMI=$(aws ec2 create-image \
  --instance-id $BASE_INSTANCE \
  --name "my-golden-image-$(date +%Y-%m-%d)" \
  --description "Golden image with nginx, python3, monitoring agent" \
  --no-reboot \
  --tag-specifications 'ResourceType=image,Tags=[{Key=Name,Value=my-golden-image},{Key=Version,Value=1.0}]' \
  --query 'ImageId' --output text)

echo "AMI being created: $MY_AMI"

# Wait for AMI to be available (takes a few minutes)
aws ec2 wait image-available --image-ids $MY_AMI
echo "AMI is ready: $MY_AMI"
```

**Step 4: Launch from Your AMI**
```bash
# Launch a new instance using your golden AMI
NEW_INSTANCE=$(aws ec2 run-instances \
  --image-id $MY_AMI \
  --instance-type t2.micro \
  --key-name my-learning-key \
  --tag-specifications 'ResourceType=instance,Tags=[{Key=Name,Value=from-golden-image}]' \
  --query 'Instances[0].InstanceId' --output text)

aws ec2 wait instance-running --instance-ids $NEW_INSTANCE
NEW_IP=$(aws ec2 describe-instances --instance-ids $NEW_INSTANCE --query 'Reservations[0].Instances[0].PublicIpAddress' --output text)

# Verify the software is already installed (no bootstrapping needed!)
ssh -i ~/.ssh/my-learning-key.pem ec2-user@$NEW_IP "nginx -v && python3 --version"
```

---

## 6. Copying and Sharing AMIs

### Copy AMI to Another Region

```bash
# Copy AMI from us-east-1 to ap-south-1 (Mumbai)
COPIED_AMI=$(aws ec2 copy-image \
  --source-region us-east-1 \
  --source-image-id $MY_AMI \
  --name "my-golden-image-mumbai-copy" \
  --region ap-south-1 \
  --query 'ImageId' --output text)

echo "Copied AMI in ap-south-1: $COPIED_AMI"

# Wait for it to be available in the new region
aws ec2 wait image-available --image-ids $COPIED_AMI --region ap-south-1
```

### Share AMI with Another AWS Account

```bash
# Share with a specific account (they can launch from it)
aws ec2 modify-image-attribute \
  --image-id $MY_AMI \
  --launch-permission "Add=[{UserId=123456789012}]"

# Make AMI public (NOT recommended for custom AMIs with any config/secrets)
aws ec2 modify-image-attribute \
  --image-id $MY_AMI \
  --launch-permission "Add=[{Group=all}]"

# Make AMI private again
aws ec2 modify-image-attribute \
  --image-id $MY_AMI \
  --launch-permission "Remove=[{Group=all}]"
```

---

## 7. AMI Deregistration and Cleanup

Deleting an AMI is a two-step process: deregister the AMI, then delete the underlying snapshots.

```bash
# Step 1: Find snapshots associated with the AMI
aws ec2 describe-images \
  --image-ids $MY_AMI \
  --query 'Images[0].BlockDeviceMappings[*].Ebs.SnapshotId' \
  --output text

# Step 2: Deregister the AMI
aws ec2 deregister-image --image-id $MY_AMI

# Step 3: Delete the underlying snapshots
aws ec2 delete-snapshot --snapshot-id snap-xxxxxxxxxxxxxxxxx
# Repeat for each snapshot found in step 1
```

---

## 8. AMI Lifecycle and Best Practices

| Practice | Why |
|----------|-----|
| **Version your AMIs** | Use date or version in the name: `my-app-v1.2-2026-05-01` |
| **Automate AMI creation** | Use EC2 Image Builder or AWS CodePipeline |
| **Clean up before imaging** | Remove logs, temp files, history to reduce size and cost |
| **Don't bake secrets** | Never put passwords or API keys in an AMI |
| **Tag everything** | Add tags: environment, version, creator, expiry date |
| **Retire old AMIs** | Deregister AMIs older than X months to reduce snapshot costs |
| **Test your AMI** | Always launch a test instance and verify before using in prod |

---

## 9. Cheat Sheet

```bash
# List your AMIs
aws ec2 describe-images --owners self --output table

# Create AMI from instance
aws ec2 create-image --instance-id <i-id> --name "my-ami-$(date +%Y%m%d)" --no-reboot

# Copy AMI to another region
aws ec2 copy-image --source-region us-east-1 --source-image-id <ami-id> --name "copy" --region eu-west-1

# Share AMI with account
aws ec2 modify-image-attribute --image-id <ami-id> --launch-permission "Add=[{UserId=<account-id>}]"

# Deregister AMI
aws ec2 deregister-image --image-id <ami-id>

# Delete associated snapshot
aws ec2 delete-snapshot --snapshot-id <snap-id>

# Find latest Amazon Linux AMI
aws ssm get-parameter --name /aws/service/ami-amazon-linux-latest/al2023-ami-kernel-default-x86_64 --query 'Parameter.Value' --output text
```

---

## 10. Common Interview Questions

**Q: What is an AMI and what does it contain?**
> An AMI is a template for launching EC2 instances. It contains the operating system (via EBS snapshots of the root volume), any baked-in software and configuration, launch permissions (who can use it), and block device mappings specifying which volumes to attach and their sizes.

**Q: How would you create a "golden image" and why would you use one?**
> Launch a base instance, configure it fully (install packages, security hardening, monitoring agents), create an AMI from it, then use that AMI for all future instance launches. The benefit is consistent, pre-configured instances that launch faster (no bootstrapping needed), reducing risk from configuration drift and speeding up auto-scaling.

**Q: Are AMIs region-specific?**
> Yes. An AMI exists only in the region where it was created. To use it in another region, you must copy it using `copy-image`. After copying, the AMI has a different ID in the destination region.

**Q: What is the difference between an AMI and a snapshot?**
> A snapshot is a point-in-time backup of a single EBS volume. An AMI is built from one or more snapshots plus metadata (launch permissions, block device mapping). An AMI references snapshots but is the complete blueprint for launching an instance, while a snapshot is just raw data storage.

**Q: How do you share an AMI with another AWS account?**
> Use `modify-image-attribute` to add launch permissions for a specific account ID. The other account can then see and launch the AMI. Note: if the AMI uses encrypted snapshots with a customer-managed KMS key, you also need to share the KMS key with the other account.

Absolutely. Here are the **most common interview questions** on **Golden AMIs** with **simple, interview-ready answers**.

---

# 1. What is a Golden AMI?

> **"A Golden AMI is a pre-configured Amazon Machine Image that contains the operating system, required software like Java and Docker, security patches, monitoring agents, and company-standard configurations. It helps us launch EC2 instances with a consistent configuration."**

---

# 2. Why do we create a Golden AMI?

> **"We create a Golden AMI to reduce server provisioning time, maintain consistency across all EC2 instances, eliminate manual installation, and ensure every server follows the company's standard configuration."**

---

# 3. How do you create a Golden AMI?

> **"First, we launch a base EC2 instance. Then we install the required software such as Java, Docker, CloudWatch Agent, and security patches. After validating everything, we create an AMI from that EC2 instance. We then use this AMI to launch new EC2 instances."**

---

# 4. What do you install before creating the Golden AMI?

> **"We install the operating system updates, Java, Docker, monitoring agents like CloudWatch Agent, the SSM Agent, security patches, and any standard software required by the project."**

---

# 5. Where do you use a Golden AMI?

> **"We use Golden AMIs in Launch Templates, Auto Scaling Groups, and whenever we need to launch new EC2 instances with a standard configuration."**

---

# 6. Can one Golden AMI be used to create multiple EC2 instances?

> **"Yes. Once the Golden AMI is created, we can launch any number of EC2 instances using the same AMI ID."**

---

# 7. Can you modify a Golden AMI?

> **"No. An AMI is immutable. If we need changes, we launch an EC2 instance from the existing AMI, make the required updates, and create a new version of the Golden AMI."**

---

# 8. What happens if you upgrade Docker in the Golden AMI?

> **"The updated Golden AMI is used only for new EC2 instances. Existing EC2 instances are not updated automatically."**

---

# 9. How do you update existing EC2 instances?

> **"We can use tools like Ansible or AWS Systems Manager to update existing EC2 instances. Alternatively, we can replace the old instances with new ones launched from the latest Golden AMI."**

---

# 10. Why not use only Ansible instead of a Golden AMI?

> **"Ansible is used to manage and update existing servers, whereas a Golden AMI provides a standard base image for launching new servers. In production, we typically use both together."**

---

# 11. What is the difference between a normal AMI and a Golden AMI?

> **"A normal AMI contains only the basic operating system, whereas a Golden AMI includes the operating system along with pre-installed software, security patches, monitoring agents, and company-standard configurations."**

---

# 12. How do Auto Scaling Groups use a Golden AMI?

> **"The Auto Scaling Group uses the AMI ID configured in the Launch Template. Whenever scaling occurs, it launches new EC2 instances from the Golden AMI."**

---

## ⭐ Most Important Interview Answer (Remember This)

If an interviewer asks:

> **"Why do companies create Golden AMIs?"**

Say:

> **"To standardise server provisioning. Every EC2 instance launches with the same operating system, software, security patches, and configurations, which reduces provisioning time, avoids manual errors, and ensures consistency across environments."**

This one answer alone covers the main purpose of Golden AMIs and is one of the most frequently asked interview questions.

---

*Notes by ITkannadigaru | AWS Certification Series 2026*
