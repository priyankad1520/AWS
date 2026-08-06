#### 1. Can you explain your Jenkins pipeline from the moment a developer pushes code to Git until the application is deployed to Kubernetes? Walk me through each stage and explain what happens.
> When a developer pushes code to GitHub, a webhook automatically triggers the Jenkins pipeline. First, Jenkins checks out the latest source code from the repository. Next, Maven compiles the Java application and runs JUnit unit tests. After successful testing, SonarQube performs static code analysis to check code quality and security issues. If all quality gates pass, Maven packages the application into a JAR file. Then Jenkins builds a Docker image and scans it using Trivy for vulnerabilities. If the scan passes, the image is pushed to Amazon ECR. Finally, Jenkins updates the Kubernetes deployment on Amazon EKS using Helm or kubectl, allowing the new Pods to roll out. In the post stage, we send email notifications if the pipeline succeeds or fails.
Git Webhook triggers Jenkins
* Checkout stage
* Build (Maven): We use Maven to compile the application and execute the build lifecycle.
* Unit Testing (JUnit)
* SonarQube analysis
* Package as JAR: In many organizations, after creating the JAR, it is uploaded to Nexus or JFrog Artifactory before building the Docker image.
* Docker image build
* Trivy image scanning
* Push image to Amazon ECR
* Deploy to Amazon EKS
* Email notification in the post section

#### 2. What is a Jenkins Shared Library? Why did your team use it, and what problem did it solve?
> A Jenkins Shared Library is a collection of reusable Groovy scripts and pipeline functions that allow us to avoid duplicating CI/CD logic across multiple projects. In our project, we had several microservices with almost identical pipeline stages such as checkout, build, unit testing, SonarQube analysis, Docker image creation, Trivy scanning, and deployment. Instead of maintaining the same Jenkinsfile in every repository, we moved the common pipeline logic into a Shared Library. Each microservice simply passed its own parameters, such as the application name, Docker image name, or deployment configuration. This improved code reusability, ensured consistency across all pipelines, and made maintenance much easier because any pipeline change only needed to be updated once in the Shared Library.

#### 3. One day, your Jenkins pipeline suddenly fails during the Docker image build stage, even though no code changes were made. How would you troubleshoot this issue? Walk me through your approach
First, I check the Jenkins console output to identify the exact failure point and error message. Since there were no code changes, I suspect an environment or infrastructure issue rather than an application issue. I verify that the Jenkins agent is healthy, the Docker daemon is running, and there is sufficient disk space on the build server. Next, I check whether the Dockerfile references a valid base image and whether the agent can pull it successfully. I also verify Docker registry or Amazon ECR connectivity and ensure the Jenkins credentials are still valid. If the image build depends on external repositories, I check for network or DNS issues as well. After identifying the root cause, I fix the issue, rerun the pipeline, and verify that the Docker image builds successfully.

A senior engineer should think about several possibilities, such as:

* You started with the Jenkins console logs. This should always be the first step.
* You considered that the issue might not be related to application code.
* You mentioned Docker-related causes such as an incorrect image/tag and credential issues.
* Docker daemon/service is down.
* The Jenkins agent doesn't have enough disk space.
* The Docker registry (ECR) is unavailable.
* The base image in the Dockerfile has changed or is no longer available.
* Network or DNS issues while pulling the base image.
* Jenkins credentials have expired.
* Docker version or plugin changes on the Jenkins agent.
* The build node itself has a problem.

#### 4. Suppose one of your Jenkins agents suddenly goes offline during a pipeline execution. How would you troubleshoot and resolve the issue?
> "First, I verify in the Jenkins dashboard whether the agent is marked as Offline and check the reason displayed. Next, I review the agent logs and the Jenkins controller logs to identify any connection or authentication errors. Then I verify that the agent machine is running and reachable over the network by checking SSH connectivity or the agent service, depending on how it is configured. I also confirm that Java is running on the agent, because Jenkins agents require Java. If the agent uses Docker or Kubernetes, I verify that the container or Pod is healthy. I also check disk space, CPU, and memory, since resource exhaustion can cause agents to disconnect. If the issue is related to credentials, network, or the agent service, I fix it, reconnect the agent, and rerun the pipeline to ensure it completes successfully."

**what is a Jenkins Agent?**: A **Jenkins Agent** (previously called a **Slave**) is a machine where Jenkins executes the pipeline.
* **Jenkins Controller (Master)** → Manages jobs and schedules builds.
* **Jenkins Agent** → Actually executes the build steps like `git checkout`, `mvn package`, `docker build`, `kubectl apply`, etc.

> Real Project Example: Suppose you have: 50 developers and 100 Jenkins jobs If the Jenkins Controller runs every build, it will become overloaded. Instead, Jenkins sends jobs to different agents.
* Linux Agent → Builds Java applications.
* Docker Agent → Builds Docker images.
* Kubernetes Agent → Deploys to EKS. This distributes the workload.

**Common Reasons an Agent Goes Offline**

* Agent machine is powered off.
* Network issue between the controller and the agent.
* SSH connection failure.Java process stopped.
* Disk space is full. CPU or memory exhausted.
* Jenkins agent service stopped. Credentials changed or expired.
* Kubernetes agent Pod crashed (if using dynamic agents).

1. **Is the machine reachable?** (Network)
2. **Is the required service running?** (Jenkins agent, Java)
3. **Does it have enough resources?** (CPU, memory, disk)
4. **Are credentials and connectivity correct?**
5. **Fix the issue and verify the build.**

**Commands You Might Use**
```bash
# On the agent machine:
systemctl status jenkins-agent
# Check Java:
java -version
# Check disk usage:
df -h
# Check memory:
free -m
# Check CPU:
top
# Check if the machine is reachable:
ping <agent-ip>
```

#### "What is the difference between a Declarative Pipeline and a Scripted Pipeline in Jenkins? Which one did you use in your project, and why?"
"The main difference between a Declarative Pipeline and a Scripted Pipeline is that Declarative Pipeline provides a structured and simplified syntax, whereas Scripted Pipeline offers more flexibility and is written entirely in Groovy. Declarative Pipeline follows a predefined structure using blocks like `pipeline`, `agent`, `stages`, and `post`, making it easier to read, maintain, and troubleshoot. Scripted Pipeline, on the other hand, allows complex programming logic such as loops, conditions, and custom functions, but it is more difficult to write and maintain.**

Declarative Pipeline also provides built-in features like `post`, `environment`, `parameters`, `options`, and `triggers`, which make pipeline development simpler. Scripted Pipeline requires developers to implement much of this logic manually using Groovy code.**

In our project, we used Declarative Pipelines because they were easier to understand, maintain, and standardize across multiple microservices. Since our CI/CD workflow was common for all applications, we combined Declarative Pipelines with a Jenkins Shared Library to reuse common stages like build, SonarQube scan, Docker image creation, Trivy scanning, pushing the image to Amazon ECR, and deploying to Amazon EKS. This approach reduced code duplication, improved consistency, and made the pipelines easier to manage."**

#### 5. How do you securely store and use sensitive information such as AWS access keys, Docker registry credentials, GitHub tokens, or passwords in a Jenkins pipeline?
we never hardcoded sensitive information in the Jenkinsfile. Instead, we stored secrets in Jenkins Credentials, such as AWS access keys, Docker registry credentials, GitHub tokens, and SSH keys. Each credential is stored with a unique ID. In the pipeline, we use the withCredentials block to securely inject those credentials only during execution. This keeps passwords and tokens out of the source code and prevents accidental exposure in Git. For some cloud resources, we also integrated AWS Secrets Manager as a centralized secret store. This approach improves security, simplifies credential management, and allows us to rotate secrets without changing the pipeline code.
Jenkins supports different credential types, for example:

Username & Password
Secret Text (GitHub token, API token)
Secret File
SSH Private Key
AWS Credentials (through plugins or username/secret combinations)
#### 6. Your Jenkins build is stuck in the 'Pending' state and never starts. What are the possible reasons, and how would you troubleshoot it?

> **"The Jenkins build is in the Pending state and never starts."**

But your answer focused on **a build that has already started and failed**.

Those are two different scenarios.

---

# ❌ What You Missed

If a build is **Pending**, Jenkins has **not started executing the pipeline yet**.

So the problem is **before the first stage**.

The Docker build, SonarQube, Maven, Trivy, etc., haven't even started.

---

## What the interviewer expects

When a Jenkins build is **Pending**, think about:

### 1. No available Jenkins Agent ⭐⭐⭐⭐⭐

This is the **most common answer**.

Example:

* Agent is offline
* Agent disconnected
* Agent is busy
* Wrong agent label

---

### 2. Executor is Busy

Suppose your Jenkins has:

```
2 Executors
```

Both are already running builds.

Your new build waits in **Pending**.

---

### 3. Wrong Agent Label

Example:

Pipeline:

```groovy
agent { label 'docker' }
```

But there is **no agent** with the label `docker`.

The job will remain Pending forever.

---

### 4. Agent Offline

Go to

```
Manage Jenkins
→ Nodes
```

Check whether the agent is Offline.

---

### 5. Queue

Go to

```
Build Queue
```

See why Jenkins is waiting.

---

### 6. Resources

Sometimes

* CPU
* Memory
* Disk

are exhausted on the Jenkins agent.

---

# Interview-Ready Answer (10/10)

> "If a Jenkins build remains in the Pending state, first I check the Build Queue to understand why it hasn't started. Then I verify whether the required Jenkins agent is online and available. I also confirm that the pipeline is requesting the correct agent label and that a matching agent exists. Next, I check whether all executors are busy, which can cause new builds to wait in the queue. I also review the agent logs and verify that the agent has sufficient CPU, memory, and disk space. If the agent is disconnected or the label is incorrect, I fix the issue and rerun the build. Once the build starts successfully, I monitor the pipeline to ensure it completes without errors."

---

# Interviewer's Verdict

⚠️ **Needs Improvement**

This wasn't because your Jenkins knowledge is weak.

It happened because you answered a **different problem**.

A very common interview mistake is missing one keyword.

---

## 🔥 Interview Tip

Whenever you're asked a troubleshooting question, first identify **which stage** the issue is in.

For example:

| Question             | Think About                   |
| -------------------- | ----------------------------- |
| Build is **Pending** | Queue, Agents, Executors      |
| Build **Failed**     | Console logs, pipeline stages |
| Docker build failed  | Docker daemon, Dockerfile     |
| SonarQube failed     | Quality Gate, Scanner         |
| Deployment failed    | Kubernetes, Helm, EKS         |
| Pod CrashLoopBackOff | Logs, application             |

This habit will help you answer much more accurately.

---
#### 7. What is the difference between `agent any`, `agent none`, and `agent { label 'docker' }` in a Declarative Jenkins Pipeline?"agent any means Jenkins can execute the pipeline on any available agent, so Jenkins automatically selects one. agent none means no agent is allocated for the entire pipeline. Instead, each stage must define its own agent, which is useful when different stages require different environments. agent { label 'docker' } tells Jenkins to run the pipeline or a specific stage only on an agent that has the label docker. In our project, we mainly used labeled agents to ensure Docker builds and Kubernetes deployments ran on machines with the required tools installed.
agent any means Jenkins can execute the pipeline on any available agent, so Jenkins automatically selects one. agent none means no agent is allocated for the entire pipeline. Instead, each stage must define its own agent, which is useful when different stages require different environments. agent { label 'docker' } tells Jenkins to run the pipeline or a specific stage only on an agent that has the label docker. In our project, we mainly used labeled agents to ensure Docker builds and Kubernetes deployments ran on machines with the required tools installed.
```groovy
pipeline {
    agent none

    stages {
        stage('Build') {
            agent { label 'java' }             # Build runs on the Java agent.
            steps {
                sh 'mvn package'
            }
        }

        stage('Docker') {
            agent { label 'docker' }           # Docker build runs on the Docker agent
            steps {
                sh 'docker build -t app .'
            }
        }
    }
}
```
#### 8. What is the difference between withCredentials and the Jenkins Credentials store? Why do we need both?
The Jenkins Credentials Store is a secure location where we save sensitive information such as passwords, API tokens, AWS access keys, and SSH keys. Each credential is stored with a unique Credential ID. The withCredentials step is used inside the Jenkins pipeline to retrieve a specific credential using that ID. It temporarily injects the secret into environment variables only for the duration of that block, allowing the pipeline to use it securely without hardcoding sensitive values in the Jenkinsfile. So, the Credentials Store is responsible for securely storing the secrets, while withCredentials is responsible for securely accessing them during pipeline execution."

withCredentials temporarily injects the stored secret into the pipeline as environment variables for the duration of that block.

#### 9. Your Jenkins pipeline successfully built the Docker image and pushed it to Amazon ECR, but the deployment to Amazon EKS failed. How would you troubleshoot this issue? Walk me through your approach.
If the pipeline successfully builds the Docker image and pushes it to Amazon ECR but fails during deployment to Amazon EKS, I first check the Jenkins console output to identify the exact deployment error. I verify whether the kubectl or Helm command failed and confirm that Jenkins is connected to the correct EKS cluster with a valid kubeconfig. If the deployment command succeeds but the application is still unavailable, I check the Deployment and Pods using kubectl get deployment, kubectl rollout status, kubectl get pods, and kubectl describe pod. I also verify whether the Pods are in states such as ImagePullBackOff, CrashLoopBackOff, or Pending. Then I check whether the image exists in Amazon ECR, verify the image tag, and ensure the ServiceAccount and IAM permissions are configured correctly. After fixing the root cause, I redeploy and confirm that all Pods are Running.
> 1. **Check the Jenkins Console Output:** First, identify where the deployment failed.
For example: kubectl apply failed, helm upgrade failed, Authentication error, Timeout, Manifest validation error

> 2. **Verify Cluster Connectivity:** Check whether Jenkins can communicate with EKS.
Possible issues:Incorrect kubeconfig, Expired AWS credentials, Wrong cluster context

> 3. **Check Kubernetes Resources:** Now check: kubectl get pods, kubectl describe pod, kubectl get events

> 4. **Check Deployment Status** A very common command is: kubectl rollout status deployment/<deployment-name>  or  kubectl describe deployment <deployment-name>

> 5. **Check Image Pull:** Sometimes the deployment succeeds, but Pods cannot start because: Wrong image tag, Image doesn't exist in ECR, ImagePullBackOff

> 6. **Check Service Account / IAM:** This is where your answer fits. If using IAM Roles for Service Accounts (IRSA), verify: Correct ServiceAccount, Correct IAM role, Required permissions

#### 10. Suppose your Jenkins pipeline has 10 stages, but you want the Docker build stage to run only when code changes are made to the Dockerfile. How would you implement this in Jenkins?
> "In Jenkins Declarative Pipelines, we can use the `when` condition to execute stages only when specific conditions are met. For example, if I want the Docker build stage to run only when the `Dockerfile` changes, I use the `changeset` condition. This avoids unnecessary Docker builds, reduces pipeline execution time, and saves compute resources. We also use `when` for conditions such as running deployments only on the `main` branch or only for release branches."

Suppose your repository contains:
```
application/
├── src/
├── pom.xml
├── Dockerfile
├── Jenkinsfile
```

A developer changes only: README.md. Should Jenkins rebuild the Docker image? No.There's no need. Building Docker images takes time. Instead, we can **skip** that stage.

**How do we do it?**: In a Declarative Pipeline, we use the **`when`** condition.
```groovy
stage('Docker Build') {
    when {
        changeset "Dockerfile"          # "Run this stage only if the `Dockerfile` changed."
    }
    steps {
        sh 'docker build -t myapp .'
    }
}

# or
when {
    changeset "docker/**"             # Run the stage only if anything under `docker/` changes: or 
    branch 'main'                  # Run deployment only from the `main` branch or
    branch 'release/*'      # Build Docker images only for release branches:
}
```
**Why do companies use this?**
Imagine you have:
* Build → 3 minutes
* Unit Test → 5 minutes
* SonarQube → 4 minutes
* Docker Build → 8 minutes
* Trivy → 5 minutes
> If only documentation changes, rebuilding the Docker image wastes time and compute resources. Conditional execution makes the pipeline faster and more efficient.
**No, it does not run only the Docker stage.**

```groovy
# Now imagine your Docker stage is written like:
stage('Docker Build') {
    when {
        changeset "Dockerfile"
    }
    steps {
        sh 'docker build -t myapp .'
    }
}
```
> **Case 1: Only `Dockerfile` changed:** Checkout --> Build --> Unit Test -->  SonarQube -->  Docker Build --> Trivy Scan --> Push to ECR --> Deploy to EKS
The **entire pipeline runs**, including the Docker Build stage, because the `when` condition is satisfied.

> **Case 2: Only `README.md` changed:** Checkout --> Build --> Unit Test --> SonarQube --> ⏭️ Docker Build (Skipped) -->  Trivy Scan (or skipped too, depending on your pipeline) --> Deploy (depends on your pipeline logic)
Only the **Docker Build stage** is skipped. The rest of the pipeline continues unless you've also added conditions to those stages.

> Usually, if the Docker Build is skipped, we also skip the stages that depend on it, such as: Docker Build, Trivy Scan, Push to ECR, Deploy to EKS. because there's no new image to scan, push, or deploy.
That way, all Docker-related stages are skipped together when the `Dockerfile` hasn't changed.
```groovy
# So a production pipeline might look like:
stage('Docker Build') {
    when { changeset "Dockerfile" }
}

stage('Trivy Scan') {
    when { changeset "Dockerfile" }
}

stage('Push to ECR') {
    when { changeset "Dockerfile" }
}

stage('Deploy to EKS') {
    when { changeset "Dockerfile" }
}
```
* **`when` only controls the stage where it is defined.**
* **It does not automatically skip the rest of the pipeline.**
* If you want multiple stages to be conditional, you need to apply a `when` condition to each of those stages (or structure your pipeline accordingly).


#### 11. **"What is the difference between `post { always }`, `post { success }`, `post { failure }`, and `post { cleanup }` in a Jenkins Declarative Pipeline?"**
**"The `post` section in a Jenkins Declarative Pipeline** defines the actions that run after the pipeline or a stage completes. `post { always }` executes every time, regardless of whether the build is successful, failed, or aborted. We typically use it for tasks like archiving logs, publishing reports, sending metrics, or any cleanup activity that should always happen.

**`post { success }`** runs only when the pipeline completes successfully. We commonly use it to send success email notifications, trigger downstream jobs, or notify the deployment team that the deployment was successful.

**`post { failure }`** runs only when the pipeline fails. It is generally used to send failure notifications, create Jira incident tickets, send Slack alerts, or trigger a rollback process if required.**

**`post { cleanup }`** runs at the very end, after all the other `post` conditions have finished. It is mainly used to delete temporary files, clean the Jenkins workspace, remove unused Docker images, and free up disk space so that the agent remains clean for future builds.

we used `success` and `failure` to send email notifications based on the build result, and `cleanup` to remove temporary files and clean the workspace, ensuring the Jenkins agent was always ready for the next pipeline execution."

#### 12. In your project, how did Jenkins know which branch to build? For example, if a developer pushed code to the dev branch, how did Jenkins build only the dev branch and not main or feature branches?
> **"If a developer pushes code to the `dev` branch, how does Jenkins know to build the `dev` branch instead of `main`?"**
This has nothing to do with **image tags** or **deployment parameters**. It's about **Git branch configuration**.
> "In our project, Jenkins was integrated with GitHub using webhooks. Whenever a developer pushed code, GitHub automatically triggered the Jenkins job. The Jenkins job was configured with the Git repository and the target branch, such as `dev`, so it checked out only that branch and executed the pipeline. In projects using Multibranch Pipelines, Jenkins can automatically detect and build the branch that triggered the webhook, such as `main`, `dev`, or a feature branch, without requiring manual configuration."
 **Real Project Flow**: Suppose your Git repository has these branches:

```text
main
dev
feature/login
feature/payment
```

A developer pushes code to:dev. --> GitHub sends a **webhook** to Jenkins. Now Jenkins needs to know: "Which branch should I check out?"

**Method 1: Pipeline Job (Most Common):** When creating the Jenkins job, you configure: **Source Code Management → Git**
```text
# Repository:
https://github.com/company/project.git

# Branch Specifier: Always build the **dev** branch.
*/dev                  
```
**Method 2: Multibranch Pipeline** : Many companies use **Multibranch Pipeline**.

```text
# Jenkins automatically discovers branches such as:
main
dev
feature/login
feature/payment

# When someone pushes to:
feature/login          # Jenkins automatically builds **only** that branch. No manual branch selection is needed.
```
**Method 3: Build with Parameters** 


```text
# Sometimes we create:
BRANCH_NAME

# The user chooses:
dev or main
# The pipeline checks out that branch.This approach is also valid, but it's **manual**. Most CI pipelines triggered by webhooks don't rely on a user selecting the branch every time.
```
---

## Interview Tip

When you hear:

* **Branch** → Think **Git**.
* **Environment** → Think **Dev/UAT/Prod**.
* **Image Tag** → Think **Docker**.
* **Deployment Target** → Think **Kubernetes/EKS**.


#### 13. **"What is the difference between a Freestyle Job, a Pipeline Job, and a Multibranch Pipeline in Jenkins? Which one did you use in your project, and why?"**
A Freestyle Job is the simplest Jenkins job where the build steps are configured directly through the Jenkins UI. It is suitable for simple tasks but is difficult to maintain because the configuration is not stored as code. A Pipeline Job defines the CI/CD workflow in a Jenkinsfile using Groovy. Since the Jenkinsfile is stored in Git, it supports version control, code reviews, and reusable pipeline logic, making it ideal for modern CI/CD. A Multibranch Pipeline extends this concept by automatically discovering branches in the Git repository and creating a separate pipeline for each branch. Whenever code is pushed to a branch, Jenkins builds only that branch. In my project, we used Pipeline Jobs because our entire CI/CD process was defined in a Jenkinsfile, making it easier to maintain and version-control.

We used Pipeline Jobs because our CI/CD pipeline was defined in a Jenkinsfile, which allowed us to version-control the pipeline along with the application code. It also made the pipeline easier to maintain and supported reusable stages through Shared Libraries.

#### 14. Suppose your team has 15 microservices, and all of them use the same Jenkins Shared Library. One day, you make a change in the Shared Library, and after that, all 15 pipelines start failing. How would you troubleshoot and resolve this issue?
> "If all pipelines start failing immediately after a Shared Library change, the first thing I do is check the Jenkins console logs to identify the exact error. Since all 15 pipelines are failing after the same change, I suspect the issue is in the Shared Library rather than in the individual applications. I compare the recent changes in the Shared Library repository to identify what was modified. If the new change introduced the problem, I immediately revert or roll back to the last working version so that all pipelines can resume successfully. After restoring the pipelines, I fix the issue in a separate branch, test it with one application in a development environment, and only then merge it into the main Shared Library. This reduces the impact on all microservices."

**1. Check Jenkins Console Logs:** Find the exact error.

**2. Since All Pipelines Failed...** "This is probably not an application issue.", "The Shared Library change caused it."

**3. Compare the Recent Changes**: Check Git history. `git log, git diff`. Find what changed in the Shared Library.

**4. Roll Back**: If yesterday everything worked, go back to the previous commit. This is the fastest way to restore all pipelines.

**5. Test Before Merging**: Never push Shared Library changes directly to production. Instead: Test with one pipeline. Verify it works. Then merge.

```groovy
# Suppose your Shared Library has versions: v1.0, v1.1, v1.2
# Instead of every application always using the latest version, many teams pin the version:

@Library('shared-library@v1.1') _

# Now, if `v1.2` has a bug: Only the applications that choose `v1.2` are affected.
# The rest continue using `v1.1`. This is considered a best practice in larger organizations.
```

> **"All 15 pipelines failed after one change..."**
Immediately think: Shared component. Rollback. Git history. Test before merge

#### 15. **"What happens internally when a Jenkins pipeline starts? From the moment the webhook is received until the pipeline finishes, explain the complete flow."**
When a developer pushes code to GitHub, a webhook notifies Jenkins about the new commit. Jenkins receives the webhook, identifies the configured job, and places the build in the queue. Once an appropriate Jenkins agent is available, Jenkins allocates the agent and checks out the source code from the repository. It then reads the Jenkinsfile and executes each stage in sequence, such as build, unit testing, code quality analysis, Docker image creation, vulnerability scanning, pushing the image to Amazon ECR, and deploying to Amazon EKS. After all stages complete, Jenkins executes the post actions, such as sending email notifications, archiving artifacts, and updating the build status as Success or Failure.

#### 16. What is the difference between archiveArtifacts and stash/unstash in Jenkins? When would you use each one?
The main difference is their purpose and lifetime. stash and unstash are used to temporarily transfer files between different stages or agents within the same pipeline execution. For example, if I build a JAR file on one agent and deploy it from another agent, I use stash to save the JAR and unstash to retrieve it on the second agent. Once the pipeline finishes, the stashed files are removed.

archiveArtifacts, on the other hand, is used to permanently store build artifacts after the pipeline completes. These artifacts can be downloaded later from the Jenkins build history and are useful for auditing, debugging, or sharing build outputs like JARs, WARs, logs, or reports.

So, in short, I use stash/unstash for temporary file sharing between pipeline stages or agents, and archiveArtifacts to preserve build outputs after the pipeline has finished.

Suppose your pipeline is:

Stage 1 (Agent A): Build the application → app.jar
Stage 2 (Agent B): Deploy the application

You would:

Use stash in Stage 1 to save app.jar.
Use unstash in Stage 2 to retrieve app.jar and deploy it.

After deployment, if you want to keep app.jar so anyone can download it from Jenkins later, you use archiveArtifacts.

#### 17. Rollback
> "If a Shared Library change causes all pipelines to fail, I first identify the issue through the Jenkins console logs. Then I check the Shared Library Git history, revert the problematic commit to the last known working version, and push the rollback. After verifying one pipeline, I allow the remaining pipelines to use the restored version."
There is **no direct "rollback" button for a Jenkins pipeline.**

**Scenario 1: Roll Back a Jenkins Shared Library (Most Common)**

Suppose: Yesterday you modified the Shared Library. Today all 15 pipelines are failing.

**Steps**

1. Check the Jenkins console logs.
2. Confirm that all pipelines started failing after the Shared Library change.
3. Go to the Shared Library Git repository.
4. Identify the last working commit using `git log`.
5. Revert the bad commit or check out the previous version.
6. Push the rollback commit.
7. Trigger one pipeline and verify it works.
8. Once confirmed, allow the remaining pipelines to run.

**Scenario 2: Roll Back the Jenkinsfile**

Suppose someone modified the Jenkinsfile and the pipeline is failing.
1. Open the Git repository.
2. Review the Jenkinsfile changes.
3. Revert the bad commit.
4. Push the corrected Jenkinsfile.
5. Trigger the pipeline again.

Since the Jenkinsfile is stored in Git, you use **Git rollback**, not a Jenkins rollback feature.

**Scenario 3: Roll Back the Application Deployment:** Sometimes the pipeline succeeds, but the new application version has issues.

```bash
kubectl rollout undo deployment/<deployment-name>       # If you're deploying to Kubernetes, you would roll back the deployment.

helm rollback <release-name> <revision>       # if you use Helm:
```

> "Jenkins itself doesn't have a rollback feature for pipelines. Since the Jenkinsfile and Shared Library are stored in Git, we roll back by reverting the problematic commit and restoring the last working version. If the issue is only with the application deployment, we use Kubernetes or Helm rollback commands to restore the previous application version. After the rollback, we verify that the pipeline and deployment are working correctly before continuing."

#### Key Points to Remember
When an interviewer says **"rollback"**, first think:
* **Pipeline code?** → Roll back in Git.
* **Shared Library?** → Revert the Shared Library commit.
* **Application deployment?** → `kubectl rollout undo` or `helm rollback`.


#### 18. Your Jenkins agent suddenly goes offline, and all builds are stuck in the queue. How would you troubleshoot and resolve the issue?
> "If a Jenkins agent goes offline and builds are stuck in the queue, I first check the Jenkins controller to see the agent's status and any error messages. Then I review the agent logs to identify the root cause. Next, I verify that the agent machine is up, the agent process is running, and there are no network connectivity issues between the controller and the agent. I also check CPU, memory, and disk usage because resource exhaustion can make the agent unresponsive. If required, I restart the agent service or reconnect it to Jenkins. Once the agent is back online, I verify the connection and rerun the queued builds. To prevent this in the future, I monitor agent health and ensure sufficient resources are allocated."

* Check Jenkins logs.
* CPU or memory exhaustion can cause an agent to go offline.
* Is the **agent machine** (VM/EC2/Kubernetes pod) running?
* Is the **agent process** (`java -jar agent.jar`) still running?
* Is there a **network issue** between the Jenkins controller and the agent?
* Is the **disk full** on the agent?
* Did the **SSH/JNLP connection** drop?
* Check the **agent logs** in addition to the Jenkins controller logs.
* After fixing the issue, reconnect or restart the agent and rerun the queued builds.
#### Key Points to Remember
Whenever you hear **"Jenkins agent is offline"**, think in this order:
1. **Jenkins controller** – Is there an error message?
2. **Agent logs** – What is the root cause?
3. **Machine health** – CPU, memory, disk.
4. **Agent process** – Is it running?
5. **Network/SSH/JNLP** – Is the controller able to communicate with the agent?
6. **Restart/reconnect** the agent.
7. **Verify and rerun** the builds.

---

#### 19. **"In your project, why did you use separate Jenkins agents instead of running all builds on the Jenkins controller?"**
we used separate Jenkins agents because the Jenkins controller is responsible for managing jobs, scheduling builds, and maintaining the Jenkins UI. Running all builds on the controller would consume a lot of CPU and memory, affecting its performance. By using separate agents, the build execution happens on dedicated machines, which reduces the load on the controller. It also allows multiple pipelines to run in parallel and lets us configure different agents with different tools or environments, such as Java, Maven, Node.js, or Docker. This makes the CI/CD pipeline more scalable, reliable, and easier to maintain.

When asked "Why Jenkins agents?", remember these 5 keywords: Reduce load on the controller. Parallel builds. Scalability. Isolation (different tools/environments). Better performance and reliability.

#### 20. Create shared library
> "A Jenkins Shared Library is a separate Git repository that contains reusable pipeline code. First, we create a Git repository for the Shared Library. Inside it, we organize the code using the standard Jenkins directory structure, such as `vars` for reusable pipeline functions, `src` for Groovy classes, and `resources` for static files if required. Then we configure the repository in Jenkins under **Manage Jenkins → System → Global Pipeline Libraries** by providing the library name, Git repository URL, credentials, and default branch. Finally, in the Jenkinsfile, we import the library using the `@Library` annotation and call the reusable functions, allowing multiple pipelines to share the same code."
#### How to Create a Shared Library

#### Step 1: Create a Git Repository

Example: jenkins-shared-library --> This repository contains only reusable pipeline code.

#### Step 2: Create the Standard Directory Structure

```
jenkins-shared-library/
│
├── vars/              # This contains reusable pipeline functions.  Think of `vars/` as the place for **common pipeline steps**.
|   #These are directly callable from a Jenkinsfile.
│   ├── buildApp.groovy
│   ├── dockerBuild.groovy
│   ├── deployEKS.groovy
│
├── src/                  # This contains reusable **Groovy classes**.
│   └── com/company/
│       └── Utils.groovy
| Example use cases: This is used when the logic becomes more complex than a simple pipeline step.
|
| * Utility methods, Validation logic, String formatting, API helper classes
│
├── resources/            # The library can load these files when needed. Static files like YAML, JSON, HTML templates
│   └── config.yaml
│   └── deployment.json
│   └── email-template.html
│
└── README.md
```
```groovy
@Library('shared-library') _

pipeline {
    agent any

    stages {
        stage('Build') {
            steps {
                buildApp()
            }
        }

        stage('Docker') {
            steps {
                dockerBuild()
            }
        }
    }
}
                   or
stages {
        stage('CI/CD') {
            steps {
                buildApp()
                dockerBuild()
                deployEKS()
        }
}
```

      
#### Step 3: Configure Jenkins
Go to: Manage Jenkins --> System --> Global Pipeline Libraries
shared-library       # Configure: Library Name
https://github.com/company/shared-library.git   # Repository
Git Credentials         # Credentials
main           # Default Branch

#### Step 4: Import the Library. At the top of the Jenkinsfile:
```groovy
@Library('shared-library') _

# Now all reusable functions become available.
buildApp()
dockerBuild()
deployEKS()
```
**Example:** Suppose you have **15 microservices**.

Without a Shared Library, each Jenkinsfile contains:

* Git checkout
* Maven build
* SonarQube
* Docker build
* Trivy scan
* Push to ECR
* Deploy to EKS

The same code is duplicated 15 times. With a Shared Library: Each Jenkinsfile becomes very small:

#### 21. **"Which folder did you use most?"**

> "We primarily used the **`vars/`** directory because it contained reusable pipeline functions for build, Docker image creation, security scanning, and deployment. We used `src/` only for more complex reusable Groovy logic when required."

This aligns well with how Shared Libraries are commonly used in real-world CI/CD pipelines.

**How do you collect logs from 15 microservices?**

"In production, we don't usually use Jenkins to collect application logs. We configure Fluent Bit or Fluentd as a DaemonSet to collect logs from all Kubernetes nodes and forward them to Elasticsearch, Splunk, Datadog, or CloudWatch. Jenkins may be used only for scheduled maintenance or archival tasks, not as the primary log collection mechanism."

**If they specifically ask about a Shared Library**


"We created a reusable collectLogs() function in the Shared Library. A single scheduled Jenkins job called this function. The function executed a shell script that discovered all deployments or namespaces, collected logs using kubectl logs, and stored them in the required location. This avoided duplicating the same log collection logic across multiple Jenkins jobs."


