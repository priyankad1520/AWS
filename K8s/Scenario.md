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
