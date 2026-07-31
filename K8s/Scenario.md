## Question:

**As a DevOps engineer, you are given a task to configure a Pod for a Spring Boot application that needs to run as a single-container Pod exposing port 8080. How would you define the Pod YAML?**

## Complete YAML

```yaml
# Step 1: Understand the requirement. The application is a **Spring Boot application**.
# It should run as **a single container**, so we need **one Pod** with **one container**.
# The application listens on **port 8080**, so Kubernetes should know that the container exposes **8080**.
 
# Step 2: Define the API version. `apiVersion: v1` : We use **v1** because **Pod** is a core Kubernetes resource.
apiVersion: v1

# Step 3: Define the resource type. `kind: Pod` : This tells Kubernetes that we are creating a **Pod**.
kind: Pod

# Step 4: Give the Pod a name. Every Kubernetes object needs a unique name. Here we are naming our Pod **spring-boot-app**.
metadata:
  name: spring-boot-app

# Step 5: Define the Pod specification. `spec:` The **spec** section describes what should run inside the Pod.
spec:

# Step 6: Define the container. Inside the Pod we have one container. Giving a meaningful name makes troubleshooting easier.
 containers:
  - name: spring-boot-app-container

# Step 7: Specify the container image `image: myrepo/spring-boot-app:1.0`
# This tells Kubernetes which Docker image to pull:  **myrepo** → Container registry. **spring-boot-app** → Image name.
# **1.0** → Image version. When the Pod starts, Kubernetes pulls this image and creates the container.
    image: myrepo/spring-boot-app:1.0 

# Step 8: Expose the application port: The Spring Boot application listens on **8080**.This tells Kubernetes that the container exposes this port.
# It is mainly used for documentation and by Kubernetes resources like Services.
    ports:
    - containerPort: 8080
```

> "First, I create a **Pod** resource using **apiVersion v1** because Pod is a core Kubernetes object. Then I give the Pod a meaningful name, for example **spring-boot-app**. Inside the **spec** section, I define one container since the requirement is to run a single-container Pod. I specify the container image, for example **myrepo/spring-boot-app:1.0**, so Kubernetes can pull the image from the registry. Finally, I define **containerPort 8080** because the Spring Boot application listens on port 8080. After applying the YAML using `kubectl apply -f`, Kubernetes creates the Pod and starts the application."
This is the format I would prepare from your audio.

---

# Question

**As a DevOps engineer, you are given a task where your Node.js application requires environment variables stored in a ConfigMap named `node-env-config`. How would you inject these variables into your Pod?**

## Complete YAML

```yaml
# Step 1: Understand the requirement. We have a Node.js application that requires environment variables.
# Instead of hardcoding them inside the Pod YAML, they are already stored in a ConfigMap named node-env-config.

# Step 2: Specify the Kubernetes API version. Pod is a core Kubernetes resource, so we use apiVersion v1.
apiVersion: v1

# Step 3: Specify the resource type. kind: Pod tells Kubernetes that we are creating a Pod.
kind: Pod

# Step 4: Give the Pod a meaningful name. Every Kubernetes object should have a unique name.
metadata:
  name: nodejs-app

# Step 5: Define the Pod specification. The spec section describes what should run inside the Pod.
spec:

  # Step 6: Define the container. The Pod contains a single Node.js container.
  containers:
    - name: app

      # Step 7: Specify the container image. Here we use the official Node.js image with version 18.
      image: node:18

      # Step 8: Inject environment variables from the ConfigMap.
      # envFrom imports all key-value pairs from the ConfigMap. configMapRef refers to the existing ConfigMap by name.
      # Every key in the ConfigMap becomes an environment variable. inside the container automatically.
      envFrom:
        - configMapRef:
            name: node-env-config
```

## Interview Answer (30–45 seconds)

> "First, I understand that the Node.js application requires environment variables, and they are already stored in a ConfigMap named **node-env-config**. I create a Pod using **apiVersion v1** and **kind Pod**, then give it a meaningful name. Inside the **spec** section, I define the Node.js container and use the official **node:18** image. To inject the environment variables, I use the **envFrom** field with **configMapRef** and specify the ConfigMap name as **node-env-config**. This tells Kubernetes to automatically load all the key-value pairs from the ConfigMap as environment variables inside the container, keeping the application configuration separate from the application image."

**Why do we use `envFrom` instead of `env`?**
> "We use **envFrom** when we want to import **all the key-value pairs** from a ConfigMap as environment variables. If we only need specific variables, we use the **env** field and reference individual keys using **configMapKeyRef**."
Perfect. Based on your audio, here's the answer in the exact format you've been using.

---

# Question

**As a DevOps engineer, you are asked to securely pass database credentials into your Pod. Instead of hardcoding the password, how would you use a Kubernetes Secret to inject the database password into the container?**

## Complete YAML

```yaml
# Step 1: Understand the requirement.
# The application needs a database password.
# We should never hardcode sensitive information like passwords
# inside the Pod YAML.
# Instead, we store the password securely in a Kubernetes Secret.

# -----------------------------
# Step 2: Create the Secret.
# A Secret stores sensitive data such as passwords,
# API keys, or tokens.
# The password value must be Base64 encoded before storing.
apiVersion: v1
kind: Secret

metadata:
  name: db-secret

type: Opaque

data:
  password: cG9zdGdyZXNwYXNz
  # This is the Base64 encoded value of "postgrespass".
  # Example:
  # echo -n "postgrespass" | base64

---

# Step 3: Create the Pod.
# Pod is a core Kubernetes resource.
apiVersion: v1
kind: Pod

# Step 4: Give the Pod a meaningful name.
metadata:
  name: postgres-client

# Step 5: Define the Pod specification.
spec:

  # Step 6: Define the container.
  containers:
    - name: db-client

      # Step 7: Use the PostgreSQL image.
      image: postgres:16

      # Step 8: Inject the password securely.
      # We create an environment variable named DB_PASSWORD.
      # Instead of writing the password directly,
      # we use secretKeyRef to fetch it from the Secret.
      env:
        - name: DB_PASSWORD
          valueFrom:
            #  allows us to retrieve a specific key from a Kubernetes Secret and expose it as an environment variable inside the container, without hardcoding the value in the Pod YAML.
            secretKeyRef:
              name: db-secret
              key: password
```
# Interview Answer (30–45 seconds)

> "First, I understand that database passwords are sensitive information, so I never hardcode them inside the Pod YAML. Instead, I create a Kubernetes **Secret** named **db-secret**, where the password is stored as a **Base64-encoded** value. Then I create the Pod and define the PostgreSQL container. Inside the **env** section, I create an environment variable called **DB_PASSWORD**. Instead of assigning the password directly, I use **valueFrom** with **secretKeyRef** to retrieve the **password** key from the **db-secret** Secret. This way, the password is securely injected into the container at runtime, keeping sensitive information separate from the application configuration."

---

### Can we mount a Secret as a volume instead of using environment variables?**
> "Yes. Kubernetes allows Secrets to be mounted as files inside the container using volumes. This is useful for certificates, private keys, or applications that read credentials from files instead of environment variables."
Excellent. Below are your notes in the **same format** as before.

---

# Question 1

**As a DevOps engineer, your application needs a guaranteed minimum CPU of 250m and memory of 256Mi, but it should not exceed a CPU limit of 500m and memory limit of 512Mi. How would you configure this in your Pod YAML?**

## Complete YAML

```yaml
# Step 1: Understand the requirement.
# The application should always get at least
# 250m CPU and 256Mi memory.
# However, it should never use more than
# 500m CPU and 512Mi memory.

apiVersion: v1

# Step 2: We are creating a Pod.
kind: Pod

# Step 3: Give the Pod a meaningful name.
metadata:
  name: resource-demo

# Step 4: Define the Pod specification.
spec:

  # Step 5: Define the container.
  containers:
    - name: app
      image: nginx

      # Step 6: Configure CPU and Memory resources.
      # requests -> Minimum resources guaranteed by Kubernetes.
      # limits -> Maximum resources the container can consume.
      resources:

        requests:
          cpu: "250m"
          memory: "256Mi"

        limits:
          cpu: "500m"
          memory: "512Mi"
```

---

## Interview Answer (30–45 seconds)

> "First, I understand that the application requires guaranteed minimum resources while preventing excessive resource usage. Inside the container definition, I use the **resources** section. Under **requests**, I configure **250m CPU** and **256Mi memory**, which are the minimum resources guaranteed by Kubernetes during scheduling. Under **limits**, I configure **500m CPU** and **512Mi memory**, which prevents the container from consuming more than these values. This ensures efficient resource allocation and prevents one container from affecting other workloads running in the cluster."

---

## Interview Follow-up

**What is the difference between Requests and Limits?**

> "Requests determine the minimum resources guaranteed for a container and are used by the scheduler when placing Pods on nodes. Limits define the maximum amount of CPU and memory that the container is allowed to consume."

---

# Question 2

**The monitoring team reports that production dashboards are not showing any traffic or metrics for NGINX-based web servers, but the application team says the application is working fine. What would you do as a DevOps engineer?**

> "First, I verify whether the issue is with the monitoring setup or the application itself. I deploy a simple test NGINX Pod with the same labels that production monitoring expects, such as **app: nginx** and **environment: production**. Then I apply the Pod and check whether Prometheus discovers it and starts collecting metrics. If the test Pod appears in Prometheus but the original application still doesn't show any metrics, it indicates that the monitoring configuration is working correctly. At that point, I would investigate whether the original application is exposing metrics correctly or escalate the issue to the application team."

---

## Example Test Pod YAML

```yaml
# Step 1: Create a test Pod to verify monitoring.

apiVersion: v1
kind: Pod

metadata:
  name: nginx-test

  # Step 2: Add labels expected by Prometheus.
  labels:
    app: nginx
    environment: production

spec:

  # Step 3: Define the NGINX container.
  containers:
    - name: nginx
      image: nginx
```

**Why are labels important?**

> "Prometheus often discovers targets based on Kubernetes labels. If the required labels are missing, Prometheus may not scrape the application even though it is running successfully."

---

# Question 3

**In your DevOps interview, you are asked: What Kubernetes feature would you use to keep environment-specific settings separate without rebuilding the Docker image?**

## Complete ConfigMap YAML (Production)

```yaml
# Step 1: Understand the requirement.
# Environment-specific configuration should not be hardcoded
# inside the Docker image.
# We use a ConfigMap to store application configuration.

apiVersion: v1

# Step 2: We are creating a ConfigMap.
kind: ConfigMap

# Step 3: Give the ConfigMap a meaningful name.
metadata:
  name: app-config

# Step 4: Store environment-specific configuration.
data:
  APP_URL: https://prod.example.com
  DB_HOST: prod-db.example.com
  APP_MODE: production
  LOG_LEVEL: info
```

---

## Deployment YAML

```yaml
# Step 5: Inject ConfigMap values into the application.

apiVersion: apps/v1
kind: Deployment

metadata:
  name: nodejs-app

spec:
  replicas: 2

  selector:
    matchLabels:
      app: nodejs

  template:
    metadata:
      labels:
        app: nodejs

    spec:
      containers:
        - name: nodejs
          image: myrepo/nodejs:1.0

          # Step 6: Load all ConfigMap values
          # as environment variables.
          envFrom:
            - configMapRef:
                name: app-config
```

---

## Interview Answer (30–45 seconds)

> "To manage environment-specific settings, I use a **ConfigMap**. Instead of hardcoding values like the application URL, database host, or log level inside the Docker image, I keep them in separate ConfigMap files for each environment, such as **configmap-test.yaml** and **configmap-prod.yaml**. During deployment, I first apply the appropriate ConfigMap and then deploy the application. Inside the Deployment YAML, I use **envFrom** with **configMapRef** to load the configuration as environment variables. This allows us to change configuration without rebuilding the Docker image, making deployments faster and more efficient."

**Why use ConfigMaps instead of rebuilding the image?**

> "Configuration changes happen frequently, while the application code may remain the same. By storing configuration in ConfigMaps, we can update environment-specific settings independently of the application image, avoiding unnecessary image rebuilds and CI/CD executions."

Excellent. Here are your notes in the **same interview-preparation format**.

---

# Question 1

**As a DevOps engineer, what node-level change would you make to improve the fault tolerance of your Pods so that replicas are not scheduled on the same node?**

## Complete Deployment YAML

```yaml
# Step 1: Understand the requirement.
# We have multiple replicas of the same application.
# By default, Kubernetes may schedule multiple Pods
# on the same worker node.
# If that node fails, all those Pods become unavailable.
# To improve high availability, we use Pod Anti-Affinity.

apiVersion: apps/v1

# Step 2: We are creating a Deployment.
kind: Deployment

# Step 3: Give the Deployment a meaningful name.
metadata:
  name: backend-app

spec:
  replicas: 3

  selector:
    matchLabels:
      app: backend

  template:
    metadata:
      labels:
        app: backend

    spec:

      # Step 4: Configure Pod Anti-Affinity.
      # This tells Kubernetes to avoid scheduling
      # backend Pods on the same node whenever possible.
      affinity:
        podAntiAffinity:
          requiredDuringSchedulingIgnoredDuringExecution:
            - labelSelector:
                matchExpressions:
                  - key: app
                    operator: In
                    values:
                      - backend
              topologyKey: kubernetes.io/hostname

      # Step 5: Define the application container.
      containers:
        - name: backend
          image: myrepo/backend:1.0
```

---

## Interview Answer (30–45 seconds)

> "If my application has multiple replicas, I don't want all of them running on the same worker node because a single node failure could bring down the entire application. To improve fault tolerance, I use **Pod Anti-Affinity** in the Deployment YAML. I configure **requiredDuringSchedulingIgnoredDuringExecution**, along with a label selector and the topology key **kubernetes.io/hostname**. This tells Kubernetes not to schedule Pods with the same label on the same node. As a result, the replicas are distributed across different worker nodes, improving high availability and reducing the impact of node failures."

---

## Interview Follow-up

### **What does `requiredDuringSchedulingIgnoredDuringExecution` mean?**

> "It means Kubernetes must satisfy the anti-affinity rule when scheduling a Pod. Once the Pod is running, the rule is not re-evaluated, even if the cluster changes."

---

### **What is `topologyKey: kubernetes.io/hostname`?**

> "The topology key defines the scheduling boundary. `kubernetes.io/hostname` means each worker node is treated as a separate topology domain, so Pods are spread across different nodes."

---

# Question 2

**As a DevOps engineer, how would you securely handle sensitive information like database passwords, API keys, and access tokens in Kubernetes?**

## Method 1: Create the Secret using kubectl

```bash
# Step 1: Create a Secret using kubectl.
# Kubernetes automatically Base64 encodes the value
# when using --from-literal.

kubectl create secret generic db-secret \
  --from-literal=password=postgrespass
```

---

## Verify the Secret

```bash
# Step 2: Verify the Secret.
# The password is stored in Base64 format.

kubectl get secret db-secret -o yaml
```

Example output:

```yaml
apiVersion: v1
kind: Secret

metadata:
  name: db-secret

data:
  password: cG9zdGdyZXNwYXNz
```

---

## Deployment YAML

```yaml
# Step 3: Use the Secret inside the Deployment.

apiVersion: apps/v1
kind: Deployment

metadata:
  name: backend-app

spec:
  replicas: 2

  selector:
    matchLabels:
      app: backend

  template:
    metadata:
      labels:
        app: backend

    spec:
      containers:
        - name: backend
          image: myrepo/backend:1.0

          # Step 4: Inject the Secret as an environment variable.
          env:
            - name: DB_PASSWORD
              valueFrom:
                secretKeyRef:
                  name: db-secret
                  key: password
```

---

## Interview Answer (30–45 seconds)

> "Sensitive information such as database passwords, API keys, and access tokens should never be stored inside the Docker image, Deployment YAML, or Git repository. Instead, Kubernetes provides **Secrets** for securely storing this information. I can create a Secret using the **kubectl create secret** command with the **--from-literal** option. Kubernetes automatically stores the value in Base64-encoded format. Then, inside the Deployment YAML, I use **valueFrom** with **secretKeyRef** to inject the secret into the container as an environment variable. This keeps sensitive data separate from the application code and configuration."

---

## Interview Follow-up

### **Why shouldn't we store passwords in Git or Docker images?**

> "Anyone with access to the repository or image can retrieve the credentials, which creates a serious security risk. Secrets keep sensitive information separate from the application artifacts."

---

### **Is Base64 encoding secure?**

> "No. Base64 is only an encoding mechanism, not encryption. For stronger security, Kubernetes supports encrypting Secrets in etcd, and many organizations integrate external secret managers such as AWS Secrets Manager, HashiCorp Vault, or Azure Key Vault."

---

### **What happens when we use `--from-literal`?**

> "When we create a Secret using `kubectl create secret --from-literal`, Kubernetes automatically Base64-encodes the value before storing it. We don't need to encode it manually."
Excellent. Here are your notes in the **same interview format**.

---

# Question 1

**In your DevOps interview, you are asked: You updated a Kubernetes Secret, but your running Pod did not receive the new value. How would you resolve this issue?**

## Interview Explanation

When a Secret is updated, **Kubernetes does not automatically restart Pods** that consume the Secret as **environment variables**. The Pod continues using the old value because the environment variables are loaded only when the container starts.

To make the application use the updated Secret, we need to restart the Pod so that Kubernetes creates a new container and loads the latest Secret.

There are two common ways:

1. Restart the Deployment using `kubectl rollout restart`.
2. Delete the Pod manually. If the Pod is managed by a Deployment, ReplicaSet, or StatefulSet, Kubernetes automatically creates a new Pod with the updated Secret.

---

## Method 1: Rollout Restart

```bash
# Step 1: Restart the Deployment.
# Kubernetes terminates the old Pods and creates new Pods.
# The new Pods load the updated Secret values.

kubectl rollout restart deployment <deployment-name>
```

---

## Method 2: Delete the Pod

```bash
# Step 2: Delete the existing Pod.
# The Deployment automatically creates a new Pod,
# which loads the updated Secret.

kubectl delete pod <pod-name>
```

---

## Interview Answer (30–45 seconds)

> "If I update a Kubernetes Secret, the running Pods don't automatically receive the new value when the Secret is used as environment variables. This is because environment variables are loaded only during container startup. To apply the updated Secret, I restart the Pods. The recommended approach is to use **kubectl rollout restart deployment** so Kubernetes performs a rolling restart without downtime. Alternatively, I can delete the Pod, and if it is managed by a Deployment, Kubernetes automatically creates a new Pod that loads the latest Secret."

---

## Interview Follow-up

### **Why doesn't the Pod automatically get the updated Secret?**

> "Because environment variables are initialized only when the container starts. Updating the Secret changes the Secret object, but it does not restart existing containers."

---

### **Is this true for Secrets mounted as volumes?**

> "No. If a Secret is mounted as a volume, Kubernetes can update the mounted files automatically after a short delay. However, if the application reads the Secret only during startup, it may still require a restart to use the new value."

---

# Question 2

**In your DevOps interview, you are asked: How would you mount a JSON configuration file into a container at a specific path without rebuilding the Docker image? Which Kubernetes feature would you use?**

## Complete YAML

```yaml
# Step 1: Understand the requirement.
# The application needs a JSON configuration file.
# Instead of copying the file into the Docker image,
# we store it in a ConfigMap and mount it as a volume.

# -----------------------------
# Step 2: Create the ConfigMap.
# The ConfigMap stores the JSON configuration.

apiVersion: v1
kind: ConfigMap

metadata:
  name: app-config

data:
  config.json: |
    {
      "database": "mysql",
      "host": "db.example.com",
      "port": 3306
    }

---

# Step 3: Create the Deployment.

apiVersion: apps/v1
kind: Deployment

metadata:
  name: json-demo

spec:
  replicas: 1

  selector:
    matchLabels:
      app: json-demo

  template:
    metadata:
      labels:
        app: json-demo

    spec:

      # Step 4: Define the ConfigMap volume.
      volumes:
        - name: config-volume
          configMap:
            name: app-config

      containers:
        - name: app
          image: myrepo/app:1.0

          # Step 5: Mount the ConfigMap
          # at the required directory.
          volumeMounts:
            - name: config-volume
              mountPath: /app/config

              # Optional:
              # If only config.json should be mounted
              # as a single file, use subPath.
              # subPath: config.json
```

---

## Create the ConfigMap using kubectl

```bash
# Create the ConfigMap from an existing JSON file.

kubectl create configmap app-config \
  --from-file=config.json
```

---

## Interview Answer (30–45 seconds)

> "To mount an external JSON configuration file without rebuilding the Docker image, I use a **ConfigMap** with a **Volume Mount**. First, I create a ConfigMap from the JSON file using either a YAML manifest or the **kubectl create configmap --from-file** command. Then, in the Deployment YAML, I define a ConfigMap volume and mount it into the container using **volumeMounts** at the required path. This allows the application to access the JSON configuration file directly from the mounted directory while keeping configuration separate from the application image."

---

## Interview Follow-up

### **Why use a ConfigMap volume instead of copying the file into the image?**

> "Keeping configuration outside the Docker image allows us to update configuration independently of the application code. This avoids unnecessary image rebuilds and makes deployments more flexible."

---

### **When would you use `subPath`?**

> "I use `subPath` when I want to mount only a single file from the ConfigMap instead of mounting the entire ConfigMap directory. This prevents replacing an existing directory inside the container."
