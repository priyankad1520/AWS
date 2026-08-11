#### 1. Your Docker container is running, but the application inside the container is not accessible from outside. How would you troubleshoot and fix the issue?
If the container is running but the application is not accessible from outside, first I'll check the port mapping using docker ps or docker port. Then I'll verify that the application is actually listening on the expected port inside the container. I'll test it from inside the container using curl, and I'll check the container logs for application errors. I'll also verify whether the application is bound to 0.0.0.0 instead of only localhost. If the port mapping or application configuration is wrong, I'll correct it and test the application again."

External request → Host port → Container port → Application listening port → Logs → Fix → Validate

```bash
# What should you check? First:
docker ps
# Check whether the container has a **port mapping**, for example:0.0.0.0:8080 → 80/tcp. Then check:

docker port <container-name>

# Then verify whether the application is actually listening inside the container:
docker exec -it <container-name> ss -lntp

# You can also test from inside:
docker exec <container-name> curl localhost:80

# Then check the container logs:
docker logs <container-name>
```
#### 2. Your Docker image is 2 GB in size, and the team wants to reduce the image size significantly. How would you optimize the Docker image?
To reduce the Docker image size, in our project we use multi-stage builds. In the first stage, we use the required build tools and dependencies to compile the application. In the final stage, we use a smaller runtime or slim base image and copy only the required application artifact from the build stage. This removes the build tools, source code, and unnecessary dependencies from the final image, which significantly reduces the image size and attack surface.
* Build stage → Build everything
* Runtime stage → Copy only what is required
#### 3. A Docker container is continuously restarting. How would you troubleshoot and find the root cause?
If a Docker container is continuously restarting, it usually means the application inside the container is starting and then exiting or crashing. First, I'll check the container status using `docker ps -a`. Then I'll check the container logs using `docker logs <container-name>` to identify the application error. I'll also use `docker inspect` to verify the CMD, ENTRYPOINT, environment variables, restart policy, and health check. Once I identify the root cause, I'll fix the application or configuration and start the container again. Finally, I'll verify that the container remains in the Running state."**

* **Container restarting → Check logs first.**
* **Container starts → Application/process exits or crashes → Docker restarts it → Container starts again → crashes again**
* **`docker ps -a` → `docker logs` → `docker inspect` → Identify root cause → Fix → Restart → Validate**

Common reasons include:

* Application is crashing.
* Incorrect `CMD` or `ENTRYPOINT`.
* Application exits immediately.
* Missing environment variables/configuration.
* Dependency connection failure.
* Health check failure.
* Incorrect application command.

### How I would troubleshoot it
```bash
# First, check the container status:
docker ps -a

# Then check the container logs:
docker logs <container-name>

# This is usually the **first important place** to find the application error.Then inspect the container:
docker inspect <container-name>

# Check the configured `CMD`, `ENTRYPOINT`, environment variables, restart policy, and health check. You can also check the container's exit code:
docker inspect <container-name> --format='{{.State.ExitCode}}'
# Then identify the root cause and fix the configuration/application issue.
```

#### What is the difference between `CMD` and `ENTRYPOINT` in a Dockerfile? When would you use each?"**

CMD and ENTRYPOINT are both used to define what runs when the container starts. In our project, we use ENTRYPOINT for the main application executable and CMD for default arguments that we may want to override at runtime. For example, if the ENTRYPOINT is java -jar app.jar and CMD is --server.port=8080, we can override the port while running the container without changing the image. So, ENTRYPOINT defines the main process, while CMD provides the default command or arguments.

JAR = Java ARchive. It's a packaged Java application containing compiled Java classes and usually dependencies/resources required by the application.
#### What is the difference between Docker COPY and ADD? Which one do you prefer in your project and why?
COPY and ADD are both used to copy files from the build context into the Docker image. In our project, we prefer COPY because it has simple and predictable behavior. ADD provides some additional features, such as automatically extracting local tar archives and supporting URLs. We use ADD only when we actually need those features; otherwise, COPY is the recommended choice."

#### What is Docker volume? Why do we use volumes, and what happens to the data when a container is deleted?
By default, data written inside a container's writable layer is lost when the container is removed. To persist application data, we use Docker volumes. The volume exists separately from the container, so even if the container is deleted or recreated, the data remains available. For example, for a database container, we can mount a volume to the database data directory so the database data persists across container restarts or recreation.

#### What is the difference between Docker volume and bind mount? When would you use each?
A Docker volume is storage managed by Docker, whereas a bind mount maps a specific directory or file from the host machine into the container. In our project, I prefer volumes when we need persistent application data because Docker manages the storage and it's easier to manage across containers. We use bind mounts when we specifically need to share or modify files from a particular host path, such as configuration or development files. Volumes are generally more portable and easier to manage than bind mounts.
* Database data — MySQL, PostgreSQL
* Application-generated files
* Uploaded files
* Persistent logs, if the application requires file-based logs
* **Container → /var/lib/mysql → Docker Volume → Database data**
* For a bind mount, we commonly use a specific host file/directory when we need direct access from the host, such as: Host: /opt/app/config --. Container: /app/config
* For production application configuration, though, we would usually prefer a proper configuration/secrets mechanism rather than depending heavily on host paths.

#### What is Docker networking? Explain the difference between bridge, host, and none network modes, and when would you use them?
* **Bridge network**:Container-to-container communication on same host/ It's the common/default network for containers on the **same Docker host**. Containers on the same user-defined bridge network can communicate with each other using container names.
* **Host network**:Container uses host's network/ The container **shares the host's network namespace**. It does **not** mean communication between two different hosts.
* **None network**: No network/The container gets essentially **no network connectivity** through Docker.
> **"Docker networking allows containers to communicate with each other and with external systems. The bridge network is commonly used when containers on the same Docker host need to communicate with each other. The host network removes the network isolation and allows the container to use the host's network directly, so we use it only when that behavior is specifically required. The none network provides network isolation, so we use it when the container doesn't need network connectivity."**
---

#### A Docker container can communicate with another container, but it cannot access the internet. What would you check first, and how would you troubleshoot it?"**
> **"If the container can communicate with another container but cannot access the internet, first I'll verify the container's network configuration and confirm whether the host itself has internet access. Then I'll enter the container and test connectivity to an external IP. If the IP works but domain names don't resolve, I'll check the container's DNS configuration. I'll also verify the Docker bridge network and the host's NAT or firewall configuration. Based on the result, I'll fix the DNS, network, or host NAT issue and test the connectivity again."**
* **Container → Docker bridge → Host → NAT → Internet**
* So if: Container A → Container B ✅ Container → Internet ❌ the Docker internal network is working, but the **external connectivity path** has a problem.
```bash
# What would you check?
# First check the container network:
docker inspect <container-name>

# Then enter the container:
docker exec -it <container-name> sh

# Check whether you can reach an IP:
ping 8.8.8.8

# If IP works but a domain doesn't:
ping google.com

# then it is likely a **DNS issue**. Also check:
cat /etc/resolv.conf

# Then check the Docker network:
docker network inspect bridge
# And verify the host itself has internet connectivity.
```
---

#### Your Docker container is running, but it exits immediately when you start it. What could be the reason, and how would you troubleshoot it?"**
If a Docker container exits immediately after starting, first I'll check it using docker ps -a because the container may already have stopped. Then I'll check docker logs <container> to identify the application error and use docker inspect to check the exit code, CMD, ENTRYPOINT, environment variables, and configuration. If the container is already stopped, I won't use docker exec; instead, I can start it interactively with a shell if I need to investigate inside the image. Common causes are application crashes, incorrect CMD or ENTRYPOINT, missing configuration, or the main process completing successfully. After fixing the root cause, I'll start the container again and validate it."

docker ps -a → docker logs → docker inspect → Identify root cause → Fix → Restart → Validate

#### What is the difference between docker stop, docker kill, and docker restart? When would you use each?
docker stop gracefully stops a running container by sending a termination signal and giving the application some time to shut down properly. docker kill forcefully terminates the container immediately, so I use it when the container isn't responding to a normal stop. docker restart stops and starts the same container again, and I use it when I need to restart the application without manually running separate stop and start commands. If I change environment variables, I normally recreate the container with the updated configuration rather than just restarting it."

docker stop → Graceful, docker kill → Forceful, docker restart → Stop + Start same container
#### What is Docker image layering, and how does it help with Docker image size and build performance?
Docker images are built in layers, and each filesystem-changing instruction can add a layer to the image. In our project, we optimize the Dockerfile by combining related RUN commands, removing unnecessary files in the same layer, and avoiding duplicate COPY instructions where possible. We also use multi-stage builds to keep build dependencies out of the final image. This helps reduce the final image size and improves build and deployment performance."
* This can reduce unnecessary image layers and also lets you clean up temporary package data in the same layer.
* Dockerfile instructions → Image layers → Larger image
* Combine RUN → Clean temporary files → Multi-stage build → Smaller image
#### Your Docker container is consuming very high CPU and memory. How would you identify the root cause and troubleshoot it?
If a Docker container is consuming very high CPU or memory, first I'll use docker stats to identify which container is consuming the most resources. Then I'll inspect that container using docker inspect and check the application logs. If required, I'll enter the container and use process-level commands to identify which application process is consuming the resources. I'll check whether it's due to high traffic, a memory leak, an application issue, or incorrect resource configuration. After fixing the root cause, I'll monitor the container again using docker stats to confirm CPU and memory usage are back to normal."
* docker stats → Identify container → docker logs / docker inspect → Check process → Find root cause → Fix → Monitor
