#### **1. The team wants to use the Git branch as a parameter while triggering the build and use that parameter during the Git checkout. How would you implement this in Jenkins?**

> "Yes, we can achieve this using **Jenkins String Parameters**.
>
> By default, Jenkins pipelines usually check out a fixed Git branch like **main** or **develop**. But if the development team wants the flexibility to build different branches such as **feature**, **bugfix**, **release**, or **hotfix**, we don't need to create multiple Jenkins jobs.
>
> Instead, we define a **String Parameter**, for example **BRANCH_NAME**, in the Jenkinsfile. When someone clicks **Build with Parameters**, Jenkins asks them to enter the branch name.
>
> During the **Checkout** stage, instead of hardcoding the branch, we use **`params.BRANCH_NAME`** in the Git checkout step. Jenkins then checks out the branch entered by the user and continues with the remaining stages like Build, Test, and Deploy.
>
> This makes the pipeline reusable, reduces maintenance, and gives the development team the flexibility to build any branch using a single Jenkins job."

```groovy
pipeline {
    agent any

    parameters {
        string(
            name: 'BRANCH_NAME',
            defaultValue: 'main',
            description: 'Enter the Git branch to build'
        )
    }

    stages {
        stage('Checkout') {
            steps {
                git branch: "${params.BRANCH_NAME}",
                    credentialsId: 'github-creds',
                    url: 'https://github.com/company/myapp.git'
            }
        }

        stage('Build') {
            steps {
                sh 'mvn clean package'
            }
        }
    }
}
```
 **Q1. Why do we use a String Parameter?**
> "A String Parameter allows the user to provide input while triggering the build. In this case, the input is the Git branch name. It makes the pipeline dynamic instead of hardcoding a specific branch."

**Q2. Why not create separate Jenkins jobs for each branch?**
> "Creating separate jobs increases maintenance because every job needs the same pipeline changes. A single parameterized pipeline is easier to maintain and can build any branch."

**Q3. What happens if the user enters a branch that doesn't exist?**
> "The Git checkout stage will fail because Jenkins won't find that branch in the repository. The pipeline stops at the checkout stage, and the error is shown in the build logs."

**Q4. Can we use a Choice Parameter instead of a String Parameter?**
> "Yes. If the team has a fixed set of branches like **main**, **develop**, and **release**, a Choice Parameter is better because it prevents typing mistakes. If developers create branches frequently, a String Parameter provides more flexibility."

**Q5. What is the difference between a parameterized pipeline and a Multibranch Pipeline?**
> "A parameterized pipeline is a single Jenkins job where the user manually specifies the branch at build time. A Multibranch Pipeline automatically discovers branches from the Git repository and creates separate jobs for them. We use a parameterized pipeline when we want one reusable job, and a Multibranch Pipeline when we want Jenkins to automatically manage branch-specific jobs."

**Q6. Why do we use a parameter instead of hardcoding the branch?**
> "Because hardcoding means the pipeline can build only one branch. By using a parameter, the same pipeline can build any branch without modifying the Jenkinsfile or creating multiple jobs. It improves reusability and reduces maintenance."
Excellent. I understand exactly what you want.

---

#### **2. How would you design your Jenkins pipeline where three different environments like Dev, Stage, and Prod require three different Docker image tags?**

> "In our project, we had a similar requirement where the application was deployed to **Dev**, **Stage**, and **Production**, and each environment required a different Docker image tag.
>
> Instead of creating three separate Jenkins pipelines, we used a **Choice Parameter** to let the user select the target environment while triggering the build.
>
> Based on the selected environment, we used a **script block** with an **if-else** condition to assign the appropriate Docker image tag. For example, if the environment is **Dev**, we use **my-app-dev**. If it's **Stage**, we use **my-app-staging**. Otherwise, for **Production**, we use **my-app-latest**.
>
> Then we build, tag, and push the Docker image using that dynamically selected tag. This approach keeps a single pipeline reusable across all environments, reduces maintenance, and minimizes deployment errors."

```groovy
pipeline {
    agent any

    parameters {
        choice(
            name: 'ENVIRONMENT',
            choices: ['Dev', 'Stage', 'Prod'],
            description: 'Select the deployment environment'
        )
    }

    environment {
        IMAGE_NAME = "my-app"
    }

    stages {

        stage('Select Image Tag') {
            steps {
                script {
                    if (params.ENVIRONMENT == "Dev") {
                        env.IMAGE_TAG = "my-app-dev"
                    } else if (params.ENVIRONMENT == "Stage") {
                        env.IMAGE_TAG = "my-app-staging"
                    } else {
                        env.IMAGE_TAG = "my-app-latest"
                    }
                }
            }
        }

        stage('Build Docker Image') {
            steps {
                sh "docker build -t ${IMAGE_NAME}:${IMAGE_TAG} ."
            }
        }

        stage('Push Docker Image') {
            steps {
                sh "docker push ${IMAGE_NAME}:${IMAGE_TAG}"
            }
        }
    }
}
```

**Q1. Why do we use a Choice Parameter instead of a String Parameter?**
> "A Choice Parameter provides a predefined list of environments like Dev, Stage, and Prod. It prevents users from entering invalid values and reduces deployment mistakes."

**Q2. Why don't we create three separate Jenkins pipelines?**
> "Maintaining three pipelines increases duplication and effort. A single parameterized pipeline is easier to maintain and ensures the same deployment logic is used across all environments."

**Q3. Why do we use a script block here?**
> "We use a script block because the Docker image tag needs to be decided dynamically based on the environment selected by the user. Declarative syntax alone cannot handle this conditional logic."

**Q4. Why do we store the image tag in an environment variable?**
> "Storing it in an environment variable allows us to reuse the same value across multiple stages, such as Docker build, Docker push, and Kubernetes deployment, without repeating the logic."

**Q5. What happens if the user selects the Production environment?**
> "The pipeline assigns the Production image tag, such as **my-app-latest**, builds the image with that tag, pushes it to the registry, and continues with the Production deployment process."

---

#### **3. How would you configure a Jenkins pipeline to run only if the previous build was successful?**


> "In Jenkins, we can achieve this by adding a **pre-check stage** at the beginning of the pipeline. Inside that stage, we use a **script block** to check the status of the previous build.
>
> Jenkins provides the variable **`currentBuild.previousBuild`**, which gives information about the last execution of the same job. First, I check whether a previous build exists. Then I verify whether its result is **SUCCESS**.
>
> If the previous build exists and its status is anything other than **SUCCESS**, such as **FAILURE**, **ABORTED**, or **UNSTABLE**, I stop the pipeline using the **`error()`** step with a meaningful message like *'Previous build failed, so skipping the current build.'*
>
> This prevents unnecessary builds from running after a failed pipeline and ensures that issues are resolved before the next execution. It's useful in production pipelines where we want to maintain build stability."

```groovy
pipeline {
    agent any

    stages {

        stage('Pre-Check') {
            steps {
                script {
                    if (currentBuild.previousBuild != null &&
                        currentBuild.previousBuild.result != 'SUCCESS') {

                        error("Previous build failed, so skipping this build.")
                    }
                }
            }
        }

        stage('Checkout') {
            steps {
                git url: 'https://github.com/company/myapp.git',
                    branch: 'main'
            }
        }

        stage('Build') {
            steps {
                sh 'mvn clean package'
            }
        }
    }
}
```

**Q1. What is `currentBuild.previousBuild`?**
> "It is a Jenkins built-in object that provides information about the previous execution of the same Jenkins job."

**Q2. What does `currentBuild.previousBuild.result` return?**
> "It returns the status of the previous build, such as **SUCCESS**, **FAILURE**, **ABORTED**, or **UNSTABLE**."

**Q3. Why do we check `currentBuild.previousBuild != null`?**
> "Because during the first execution of a Jenkins job, there is no previous build. This null check prevents a runtime error."

**Q4. Why do we use the `error()` step?**
> "The `error()` step immediately stops the pipeline execution and displays a custom error message in the Jenkins console."

**Q5. In what scenarios would you use this approach?**
> "I would use it in production or release pipelines where I want to ensure that a failed build is fixed before allowing the next build to execute. This helps maintain pipeline stability and avoids propagating failures."

**Q6. What happens if the previous build was successful?**
> "The pre-check passes, and the pipeline continues normally with stages like Checkout, Build, Test, and Deploy."

---

#### **4. How do you configure a Jenkins pipeline so that the Production deployment stage runs only when the code is merged into the `main` branch?**


> "In Jenkins Declarative Pipeline, we can achieve this using the **`when`** condition.
>
> For the **Deploy to Production** stage, I add **`when { branch 'main' }`**. This tells Jenkins to execute that stage only when the pipeline is running for the **main** branch.
>
> If a developer pushes code to a **feature**, **bugfix**, or **release** branch, the pipeline can still perform stages like Checkout, Build, Test, and Docker Image creation, but the Production deployment stage is automatically skipped.
>
> This is a simple and effective way to protect the Production environment from accidental deployments while allowing developers to work freely on their branches."

```groovy id="4x71kt"
pipeline {
    agent any

    stages {

        stage('Build') {
            steps {
                sh 'mvn clean package'
            }
        }

        stage('Test') {
            steps {
                sh 'mvn test'
            }
        }

        stage('Deploy to Production') {

            when {
                branch 'main'
            }

            steps {
                sh './deploy-prod.sh'
            }
        }
    }
}
```

**Q1. What is the purpose of the `when` directive?**
> "The `when` directive is used to execute a stage only when a specified condition is true. If the condition is not met, Jenkins skips that stage."

**Q2. Why do we deploy only from the `main` branch?**
> "The `main` branch usually contains stable and approved code. Restricting Production deployments to this branch prevents accidental deployments from feature or development branches."

**Q3. What happens if the pipeline runs from a feature branch?**
> "The Build and Test stages run normally, but the Production deployment stage is skipped because the branch condition is not satisfied."

**Q4. Can we deploy from multiple branches?**
> "Yes. We can modify the `when` condition to allow multiple branches using expressions or logical conditions, depending on the deployment requirement."

**Q5. Does `when { branch 'main' }` work in every Jenkins pipeline?**
> "It works with **Multibranch Pipelines** or pipelines where Jenkins knows the branch name through SCM. Jenkins uses the branch information to evaluate the condition."

**Q6. What is the benefit of using `when` instead of writing an `if-else` block?**
> "The `when` directive is cleaner, easier to read, and is the recommended Declarative Pipeline approach for controlling whether an entire stage should execute."

---

#### **5. As a DevOps engineer, how would you configure a Jenkins pipeline to trigger automatically every weekday (Monday to Friday) at 9:00 AM and 5:00 PM?**

> "In Jenkins, we can schedule automatic builds using the **`triggers`** block with a **cron expression**.
>
> For this requirement, I would configure the cron schedule as **`0 9,17 * * 1-5`**.
>
> Here, **0** represents the 0th minute, **9,17** means the job runs at **9:00 AM** and **5:00 PM** in 24-hour format, the two asterisks represent **every day of the month** and **every month**, and **1-5** represents **Monday to Friday**.
>
> This configuration is commonly used for scheduled CI/CD health checks, automated testing, report generation, monitoring jobs, or any recurring operational tasks without requiring manual intervention."
> 

```groovy id="fh2d7k"
pipeline {
    agent any

    triggers {
        cron('0 9,17 * * 1-5')
    }

    stages {

        stage('Build') {
            steps {
                sh 'mvn clean package'
            }
        }

        stage('Test') {
            steps {
                sh 'mvn test'
            }
        }
    }
}
```

**Q1. What is the purpose of the `triggers` block in Jenkins?**
> "The `triggers` block is used to automatically start a Jenkins pipeline based on a schedule or an external event, such as a cron schedule or SCM polling."

**Q2. What does the cron expression `0 9,17 * * 1-5` mean?**
> "It runs the job at **9:00 AM** and **5:00 PM**, every day of the month, every month, from **Monday to Friday**."

 **Q3. What do the five fields in a Jenkins cron expression represent?**
> "The five fields represent **Minute**, **Hour**, **Day of Month**, **Month**, and **Day of Week**."

**Q4. What is the difference between Jenkins cron and Linux cron?**
> "The syntax is very similar, but Jenkins also supports the **`H`** symbol, which distributes job execution times automatically to avoid multiple jobs starting at the same time."

**Q5. Why do many teams prefer using `H` instead of a fixed time like `0`?**
> "Using **`H`** helps distribute the load across the Jenkins server. Instead of multiple jobs starting exactly at the same minute, Jenkins calculates a stable hashed time for each job, reducing resource contention."

 **Q6. In which real-world scenarios have you used scheduled Jenkins builds?**
> "I've used scheduled builds for nightly regression testing, dependency updates, CI/CD health checks, security scans, backup jobs, and generating daily reports and metrics."

---

#### **6. As a DevOps engineer, how would you configure a Jenkins pipeline to run every hour but skip the 1:00 PM execution?**

> "In Jenkins, I would use the **`triggers`** block with a **cron expression** to schedule the job.
>
> Since the requirement is to run the pipeline every hour except **1:00 PM**, I would configure the cron expression as **`0 0-12,14-23 * * *`**.
>
> Here, **0** means the job runs at the **0th minute** of every hour. **0-12** schedules the job from **12:00 AM to 12:00 PM**, and **14-23** schedules it from **2:00 PM to 11:00 PM**. This automatically skips the **1:00 PM** execution. The remaining asterisks indicate **every day of the month**, **every month**, and **every day of the week**.
>
> This type of scheduling is useful when we want to avoid running CI jobs during a maintenance window or when developers are performing testing on shared environments."

```groovy id="6z5h2p"
pipeline {
    agent any

    triggers {
        cron('0 0-12,14-23 * * *')
    }

    stages {

        stage('Build') {
            steps {
                sh 'mvn clean package'
            }
        }

        stage('Test') {
            steps {
                sh 'mvn test'
            }
        }
    }
}
```
**Q1. Why did you exclude hour `13` in the cron expression?**
> "Because `13` represents **1:00 PM** in the 24-hour format, and the requirement is to skip that specific execution."

**Q2. What does the cron expression `0 0-12,14-23 * * *` mean?**
> "It runs the job at the **0th minute** of every hour from **12:00 AM to 12:00 PM** and from **2:00 PM to 11:00 PM**, skipping **1:00 PM**."

 **Q3. Why do we use the `triggers` block?**
> "The `triggers` block is used to schedule automatic pipeline execution without requiring manual intervention."

**Q4. Can we use the `H` symbol instead of `0`?**
> "Yes. Using **`H`** distributes the job start time across different minutes, which helps reduce load on the Jenkins controller when many jobs are scheduled."

**Q5. In what real-world scenarios would you skip a scheduled build?**
> "We might skip builds during maintenance windows, production deployments, backup activities, security scans, or when developers are using a shared environment for testing."

**Q6. What is the advantage of using cron scheduling instead of manually triggering builds?**
> "Cron scheduling ensures builds run consistently at predefined times, reduces manual effort, and is ideal for recurring CI jobs, health checks, regression testing, and report generation."

---

#### **7. How would you configure a Jenkins pipeline in a monorepo so that the Backend build runs only when Java files change, the Frontend build runs only when JavaScript files change, both run if both change, and both are skipped if neither changes?**

> "In a monorepo, we don't want to build every component for every commit because it increases the pipeline execution time. Instead, we can use the **`when`** directive with the **`changeset`** condition.
>
> For the **Backend Build** stage, I use **`changeset 'backend/**/*.java'`**, which tells Jenkins to execute that stage only if any **.java** file has changed inside the **backend** directory or its subdirectories.
>
> Similarly, for the **Frontend Build** stage, I use **`changeset 'frontend/**/*.js'`**, so the stage runs only when **.js** files are modified inside the **frontend** directory.
>
> If both Java and JavaScript files are changed, both stages execute. If neither pattern matches, Jenkins automatically skips both stages. This approach improves pipeline performance by building only the components affected by the latest changes."

```groovy id="1d7x9m"
pipeline {
    agent any

    stages {

        stage('Backend Build') {

            when {
                changeset "backend/**/*.java"
            }

            steps {
                sh 'cd backend && mvn clean package'
            }
        }

        stage('Frontend Build') {

            when {
                changeset "frontend/**/*.js"
            }

            steps {
                sh 'cd frontend && npm install && npm run build'
            }
        }
    }
}
```

**Q1. What is the purpose of the `changeset` condition?**
> "The `changeset` condition checks the files modified in the current commit and executes the stage only if they match the specified file pattern."

**Q2. What does `backend/**/*.java` mean?**
> "It matches all **.java** files inside the **backend** directory and all of its subdirectories."

**Q3. What does the `**` symbol represent in the file pattern?**
> "The `**` wildcard matches all subdirectories recursively, allowing Jenkins to check files in nested folders."

 **Q4. What happens if both Java and JavaScript files are modified?**
> "Both `changeset` conditions evaluate to true, so Jenkins executes both the Backend Build and Frontend Build stages."

**Q5. What happens if only a README file is changed?**
> "Neither file pattern matches, so Jenkins skips both stages because there are no relevant source code changes."

**Q6. What is the benefit of using `changeset` in a monorepo?**
> "It reduces unnecessary builds, saves pipeline execution time, optimizes resource usage, and speeds up feedback by building only the components affected by the latest changes."

---

#### **8. Can we define multiple triggers in a Jenkins pipeline? If yes, how would you configure a pipeline to run every 30 minutes when there are SCM changes, and also run every day at 3:00 AM regardless of changes?**

> "Yes, Jenkins allows us to configure multiple triggers in the same pipeline.
>
> In this scenario, I would use the **`triggers`** block with both **`cron`** and **`pollSCM`**.
>
> The **`cron('0 3 * * *')`** trigger runs the pipeline every day at **3:00 AM**, irrespective of whether there are any code changes. This is useful for scheduled jobs like health checks, backups, or nightly builds.
>
> The **`pollSCM('H/30 * * * *')`** trigger checks the source code repository every **30 minutes**. If Jenkins detects new commits since the last build, it automatically triggers the pipeline.
>
> By combining both triggers, we ensure that the pipeline runs on a fixed daily schedule and also responds automatically whenever new code changes are available."

```groovy id="8j4m2n"
pipeline {
    agent any

    triggers {
        cron('0 3 * * *')
        pollSCM('H/30 * * * *')
    }

    stages {

        stage('Build') {
            steps {
                sh 'mvn clean package'
            }
        }

        stage('Test') {
            steps {
                sh 'mvn test'
            }
        }
    }
}
```

**Q1. What is the difference between `cron` and `pollSCM`?**
> "The `cron` trigger runs the pipeline at a fixed schedule regardless of code changes, whereas `pollSCM` checks the source repository periodically and triggers the pipeline only if it detects new commits."

**Q2. What does `cron('0 3 * * *')` mean?**
> "It schedules the pipeline to run every day at exactly **3:00 AM**."

**Q3. What does `pollSCM('H/30 * * * *')` mean?**
> "It tells Jenkins to poll the source code repository approximately every **30 minutes**. If changes are detected, Jenkins starts the pipeline."

**Q4. Why do we use `H/30` instead of `0/30`?**
> "The `H` stands for **Hash**. Jenkins automatically assigns a stable minute value for each job, helping distribute the load and preventing multiple jobs from starting at the exact same time."

**Q5. Can both triggers execute the same pipeline?**
> "Yes. Either trigger can start the same pipeline independently. The pipeline will execute whenever any configured trigger condition is satisfied."

**Q6. In what real-world scenarios would you use both triggers together?**
> "I would use this approach for projects that require immediate builds after code changes using `pollSCM`, while also running a scheduled nightly build for regression testing, security scans, backups, or health checks, even if there are no new commits."

---

#### **9. How do you automatically trigger a Jenkins pipeline whenever code is pushed to a Git repository?**

> "The recommended approach is to use a **Git webhook**.
>
> Instead of scheduling the pipeline using **cron** or **pollSCM**, we configure a webhook between **GitHub** and **Jenkins**.
>
> In Jenkins, I enable the option **'GitHub hook trigger for GITScm polling'** in the job configuration. Then, in the GitHub repository, I go to **Settings → Webhooks**, add a new webhook, and provide the Jenkins webhook URL as the **Payload URL**. I also set the content type to **application/json** and select the **Push** event.
>
> After this configuration, whenever a developer pushes code to the repository, GitHub immediately sends an HTTP POST request to Jenkins, which automatically triggers the pipeline.
>
> This is more efficient than polling because Jenkins doesn't repeatedly check the repository. Instead, GitHub notifies Jenkins only when there is a new commit."

**Jenkins Configuration: In Jenkins:**
* Go to **Job → Configure**
* Under **Build Triggers**
* Enable **GitHub hook trigger for GITScm polling**

**In GitHub:**
* Go to **Repository → Settings → Webhooks**
* Click **Add webhook**
* Enter the **Jenkins Payload URL**
* Select **Content-Type: application/json**
* Choose the **Push** event
* Save the webhook

**Q1. What is a webhook?**
> "A webhook is an HTTP callback mechanism where one application automatically sends a request to another application when a specific event occurs, such as a Git push."

**Q2. Why do we prefer webhooks over `pollSCM`?**
> "Webhooks trigger the pipeline immediately after a code push and avoid continuous repository polling, which reduces unnecessary network traffic and improves efficiency."

**Q3. What happens when a developer pushes code to GitHub?**
> "GitHub sends an HTTP POST request to the Jenkins webhook URL, and Jenkins receives the event and starts the pipeline automatically."

**Q4. Do we need a `triggers` block in the Jenkinsfile when using webhooks?**
> "No. When using GitHub webhooks, the pipeline is triggered by the webhook event, so a `triggers` block like `cron` or `pollSCM` is not required."

**Q5. What information does the webhook send to Jenkins?**
> "The webhook sends details about the Git event, such as the repository, branch, commit information, and the type of event, allowing Jenkins to trigger the appropriate build."

**Q6. What would you check if the webhook is not triggering Jenkins?**
> "I would verify the webhook URL, ensure Jenkins is reachable from GitHub, check the GitHub webhook delivery logs, confirm that the GitHub webhook trigger is enabled in Jenkins, and review the Jenkins system and job logs for any errors."

---

#### **10. How would you configure a Jenkins pipeline to run automatically every weekday (Monday to Friday) at 8:00 AM?**

> "In Jenkins, I would use the **`triggers`** block with a **cron expression** to schedule the pipeline.
>
> For this requirement, I would configure the cron expression as **`0 8 * * 1-5`**.
>
> Here, **0** represents the minute, **8** represents **8:00 AM** in 24-hour format, the two asterisks mean **every day of the month** and **every month**, and **1-5** represents **Monday to Friday**.
>
> This configuration ensures the pipeline runs automatically every weekday at **8:00 AM**, while skipping weekends. It's commonly used for daily health checks, automated testing, scheduled builds, and report generation."

```groovy id="j9m3wp"
pipeline {
    agent any

    triggers {
        cron('0 8 * * 1-5')
    }

    stages {

        stage('Build') {
            steps {
                sh 'mvn clean package'
            }
        }

        stage('Test') {
            steps {
                sh 'mvn test'
            }
        }
    }
}
```

**Q1. What is the purpose of the `triggers` block?**
> "The `triggers` block is used to schedule automatic execution of a Jenkins pipeline based on a cron schedule or other supported trigger types."

**Q2. What does the cron expression `0 8 * * 1-5` mean?**
> "It runs the pipeline at **8:00 AM**, every **Monday to Friday**, every month."

**Q3. Why do we use `1-5` for weekdays?**
> "In cron syntax, **1** represents **Monday** and **5** represents **Friday**, so `1-5` schedules the job only on weekdays."

**Q4. What values represent Saturday and Sunday in cron?**
> "Saturday is **6**, and Sunday can be represented as **0** or **7**, depending on the cron implementation."

**Q5. Can we use `H` instead of `0` for the minute field?**
> "Yes. Using **`H`** distributes job execution times across different minutes, which helps balance the load on the Jenkins server."

**Q6. In which real-world scenarios would you schedule a weekday-only Jenkins job?**
> "I would use it for daily CI builds, health checks, automated regression tests, security scans, report generation, or any business-hour automation that doesn't need to run on weekends."

---

#### **11. How would you configure a Jenkins pipeline to check the Git repository every 15 minutes and trigger a build only when there is a new commit?**

> "In Jenkins, I would use the **`pollSCM`** trigger inside the **`triggers`** block.
>
> I would configure it as **`pollSCM('H/15 * * * *')`**, which tells Jenkins to check the Git repository approximately every **15 minutes**.
>
> If Jenkins detects a new commit since the last successful build, it automatically triggers the pipeline. If there are no changes, the build is not triggered.
>
> The **`H`** stands for **Hash**. Jenkins uses it to distribute polling times across different jobs so that multiple pipelines don't check the repository at the exact same minute, helping reduce the load on the Jenkins server.
>
> This approach is useful when webhooks are not available or cannot be configured."


```groovy id="n7v2qx"
pipeline {
    agent any

    triggers {
        pollSCM('H/15 * * * *')
    }

    stages {

        stage('Checkout') {
            steps {
                git url: 'https://github.com/company/myapp.git',
                    branch: 'main'
            }
        }

        stage('Build') {
            steps {
                sh 'mvn clean package'
            }
        }
    }
}
```

**Q1. What is `pollSCM` in Jenkins?**
> "The `pollSCM` trigger periodically checks the source code repository and starts the pipeline only if it detects new commits."

**Q2. What does `H/15 * * * *` mean?**
> "It tells Jenkins to poll the Git repository approximately every **15 minutes** using a hashed schedule to distribute the load across jobs."

**Q3. What is the purpose of the `H` in the cron expression?**
> "The `H` stands for **Hash**. It distributes polling times across different jobs so they don't all execute at the same minute."

**Q4. Will Jenkins trigger a build every 15 minutes with `pollSCM`?**
> "No. Jenkins checks the repository every 15 minutes, but it triggers a build only if it detects new changes."

**Q5. What is the difference between `pollSCM` and a Git webhook?**
> "With `pollSCM`, Jenkins periodically checks the repository for changes. With a Git webhook, the Git server immediately notifies Jenkins whenever a new commit is pushed, making it more efficient."

**Q6. When would you choose `pollSCM` instead of a webhook?**
> "I would use `pollSCM` when webhooks cannot be configured due to network restrictions, firewall limitations, or repository permissions. Otherwise, webhooks are generally the preferred approach because they trigger builds immediately after a commit."

---

#### **12. How would you configure a Jenkins pipeline to trigger automatically every day at exactly 2:00 AM?**

> "In Jenkins, I would use the **`triggers`** block with a **cron expression** to schedule the pipeline.
>
> For this requirement, I would configure the cron expression as **`0 2 * * *`**.
>
> Here, **0** represents the **0th minute**, **2** represents **2:00 AM** in 24-hour format, and the three asterisks indicate **every day of the month**, **every month**, and **every day of the week**.
>
> This configuration automatically triggers the pipeline every day at **2:00 AM**. It's commonly used for nightly builds, backups, security scans, database maintenance, and automated regression testing when system usage is low."


```groovy id="k3v8pq"
pipeline {
    agent any

    triggers {
        cron('0 2 * * *')
    }

    stages {

        stage('Build') {
            steps {
                sh 'mvn clean package'
            }
        }

        stage('Test') {
            steps {
                sh 'mvn test'
            }
        }
    }
}
```

**Q1. What does the cron expression `0 2 * * *` mean?**
> "It schedules the Jenkins pipeline to run every day at exactly **2:00 AM**."

**Q2. Why do teams often schedule jobs at 2:00 AM?**
> "Because system usage is usually low during that time, making it ideal for resource-intensive tasks like backups, regression tests, security scans, and maintenance jobs."

**Q3. What is the purpose of the `triggers` block?**
> "The `triggers` block is used to automatically start a Jenkins pipeline based on a schedule or other supported trigger mechanisms."

**Q4. Can we use `H` instead of `0` in the minute field?**
> "Yes. Using **`H`** allows Jenkins to distribute job execution across different minutes, reducing the chance of multiple jobs starting simultaneously."

**Q5. What is the difference between `cron` and `pollSCM`?**
> "The `cron` trigger runs the job at a fixed schedule regardless of code changes, whereas `pollSCM` checks the repository periodically and triggers the build only when new commits are detected."

**Q6. In which real-world scenarios have you used a 2:00 AM scheduled job?**
> "I've used scheduled jobs at **2:00 AM** for nightly builds, automated regression testing, backup tasks, security vulnerability scans, log cleanup, and generating daily operational reports."
