**ConfigMap:** A ConfigMap is used to store **non-sensitive application configuration outside the container image**. Instead of hardcoding values like environment, log level, or timeout inside the application or Docker image, we store them in a ConfigMap.

The main benefit is **separating configuration from application code**. We can change configuration without rebuilding the Docker image. ConfigMaps can be consumed as **environment variables** or **mounted as files**.

```text id="m8x3kp"
Application Code → ConfigMap → Environment Variables / Mounted Files → Container
```

### ConfigMap YAML

```yaml
apiVersion: v1                              # Kubernetes API version.
kind: ConfigMap                             # Creates a ConfigMap.
metadata:
  name: my-app-config                       # Name used by the Pod to reference this ConfigMap.
data:
  app_environment: production               # Non-sensitive configuration value.
  log_level: info                           # Log level configuration.
  timeout: "30"                             # ConfigMap values are stored as strings.
```

**Why do we need ConfigMap?**

```text id="q4n7zs"
Hardcoded Config → Rebuild Image → Redeploy
ConfigMap → Change Configuration → Reuse Same Image
```

**Important:** ConfigMaps are for **non-sensitive data**. Passwords, tokens, and credentials should go into **Secrets**.

---

### Create ConfigMap from Existing File

```bash id="w5k2rn"
kubectl create configmap my-app-config --from-file=app-config.properties   # Creates a ConfigMap using the file.
kubectl get configmap my-app-config -o yaml                              # Displays the complete ConfigMap YAML.
```

Important correction: `--from-file` normally creates a key based on the **filename**, with the file's contents as the value. It does **not automatically turn every line into separate key-value pairs**.

```text id="v3p8mx"
app-config.properties → ConfigMap Key → Complete File Contents
```

---

### Create ConfigMap from Literal Values

```bash id="k6r2qp"
kubectl create configmap my-app-config --from-literal=app_environment=production --from-literal=log_level=info   # Creates ConfigMap directly from key-value pairs.
kubectl get configmap my-app-config -o yaml                                                                       # Displays the stored configuration.
```

This is useful for **quick testing or small configurations**.

---

### Important ConfigMap Points

```text id="n7c4zk"
ConfigMap Values → Strings
ConfigMap Keys → Case-Sensitive
Sensitive Data → Use Secret
ConfigMap Update → Does Not Automatically Update Existing Environment Variables
```

If a ConfigMap is consumed as **environment variables**, changing the ConfigMap does not change the environment variables inside an already-running container. You normally need to **restart/recreate the Pod**.

If mounted as a **volume**, Kubernetes can update the mounted files after the ConfigMap changes, subject to Kubernetes' update mechanism and application behavior.

---

## ConfigMap as Environment Variables

You can inject a **specific ConfigMap key** into a container as an environment variable.

### ConfigMap

```yaml
apiVersion: v1                              # Kubernetes API version.
kind: ConfigMap                             # Creates a ConfigMap.
metadata:
  name: my-app-config                       # ConfigMap name.
data:
  app_environment: production               # Value for APP_ENVIRONMENT.
  log_level: info                            # Value for LOG_LEVEL.
```

### Pod

```yaml
env:
- name: APP_ENVIRONMENT                      # Environment variable available inside the container.
  valueFrom:
    configMapKeyRef:
      name: my-app-config                    # References the ConfigMap.
      key: app_environment                   # Reads this specific key from the ConfigMap.
- name: LOG_LEVEL                            # Another environment variable.
  valueFrom:
    configMapKeyRef:
      name: my-app-config                    # References the same ConfigMap.
      key: log_level                          # Reads the log_level key.
```

```text id="j8m4yc"
ConfigMap → app_environment=production → APP_ENVIRONMENT=production
ConfigMap → log_level=info → LOG_LEVEL=info
```

**Simple understanding:** `configMapKeyRef` means **“Take this particular key from this ConfigMap.”**

---

## Inject All ConfigMap Keys

If you want to inject **all keys** from a ConfigMap as environment variables, use `envFrom`.

```yaml
envFrom:
- configMapRef:
    name: my-app-config                      # Imports all keys from this ConfigMap as environment variables.
```

Suppose the ConfigMap contains:

```yaml
data:
  app_environment: production
  log_level: info
  timeout: "30"
```

Then the container receives:

```text id="r5k9wp"
app_environment=production
log_level=info
timeout=30
```

```text id="t2m6vx"
ConfigMap → envFrom → All Keys → Container Environment Variables
```

### `configMapKeyRef` vs `configMapRef`

```text id="x7p3qn"
configMapKeyRef → One Specific Key
configMapRef → All Keys
```

### Quick Revision

```text id="z9k4ws"
ConfigMap → Non-Sensitive Configuration
Secret → Sensitive Configuration
--from-file → Create ConfigMap from File
--from-literal → Create ConfigMap from CLI Key-Value
configMapKeyRef → Inject One Key
configMapRef → Inject All Keys
Environment Variable → ConfigMap Update Requires Pod Restart
Volume Mount → ConfigMap Can Be Reflected in Mounted Files
```

### Interview-Ready Answer

> **“Basically, ConfigMap is used to store non-sensitive application configuration separately from the application image.** For example, environment, log level, and timeout values can be stored in a ConfigMap instead of hardcoding them in the application or Docker image. We can consume ConfigMap values as individual environment variables using `configMapKeyRef`, or inject all keys using `envFrom`, and we can also mount ConfigMaps as files. The main benefit is that we can change application configuration without rebuilding the Docker image. However, ConfigMaps should not be used for passwords or sensitive information; for that, we use Kubernetes Secrets. One important point is that updating a ConfigMap does not automatically update environment variables in an already-running container, so the Pod normally needs to be restarted.”
**ConfigMap Volume Mount:** A ConfigMap can be mounted as **files inside a container**. This is useful when an application expects configuration files instead of environment variables, such as `.yaml`, `.properties`, or `.env` files.

Each ConfigMap **key becomes a file name**, and its **value becomes the file content**.

```text id="r6k2px"
ConfigMap → Volume → Container Directory → Application Reads Config Files
```

### Mount Entire ConfigMap

```yaml id="m8q4zn"
volumes:
- name: config-volume                         # Defines the volume.
  configMap:
    name: my-app-config                        # Gets the volume data from this ConfigMap.
containers:
- name: my-app
  volumeMounts:
  - name: config-volume                        # Uses the ConfigMap volume.
    mountPath: /etc/config                     # Mounts the ConfigMap files here inside the container.
```

Suppose the ConfigMap contains:

```yaml id="x3v7km"
data:
  app-environment: production
  log-level: info
```

The container will have:

```text id="q9n4ws"
/etc/config/app-environment → production
/etc/config/log-level       → info
```

```text id="p5k8zr"
ConfigMap Key → File Name
ConfigMap Value → File Content
```

**Why use it?** Some applications are designed to read configuration from **files**, not environment variables. Volume mounting allows us to use those applications without changing their configuration mechanism.

Also, when a ConfigMap mounted as a volume is updated, Kubernetes can **eventually reflect the updated content in the mounted files**. The application itself must still detect/reload those changes if required.

---

### Mount Specific ConfigMap Key

Sometimes we don't want the entire ConfigMap. We can mount **only a specific key**.

```yaml id="h2m6qx"
volumes:
- name: config-volume                         # Defines the volume.
  configMap:
    name: my-app-config                        # References the ConfigMap.
    items:
    - key: app-environment                     # Selects only this ConfigMap key.
      path: environment.txt                    # Creates this file name inside the volume.
containers:
- name: my-app
  volumeMounts:
  - name: config-volume                        # Uses the ConfigMap volume.
    mountPath: /etc/config                     # Mounts the selected file under /etc/config.
```

If the ConfigMap contains:

```text id="k7v3pm"
app-environment = production
```

The container gets:

```text id="s4n8wx"
/etc/config/environment.txt → production
```

```text id="v2m6kq"
ConfigMap → Select Key → Rename as environment.txt → /etc/config → Application
```

### Quick Revision

```text id="z8q3nw"
ConfigMap as Env → Configuration as Environment Variables
ConfigMap as Volume → Configuration as Files
Volume Mount All → Every Key Becomes a File
items → Select Specific Key
path → File Name Inside Volume
mountPath → Directory Inside Container
```
“Basically, **ConfigMap volume mount** is used when an application expects configuration as a **file instead of environment variables**. We can mount a ConfigMap as a volume, and Kubernetes converts each ConfigMap key into a file, with the value becoming the file content. For example, if the ConfigMap has `app-environment=production`, Kubernetes creates `/etc/config/app-environment` containing `production`. We can also use the `items` section when we want to mount only a **specific key** and give it a custom file name. The main advantage is that we can manage configuration outside the container image, and when the ConfigMap is updated, the mounted files can be updated without rebuilding the image. This is commonly useful for applications that read `.yaml`, `.properties`, or other configuration files.”

---
**Secret:** Basically, a Kubernetes Secret is used to store **sensitive information** such as passwords, API keys, tokens, and credentials. The main advantage is that we don't hardcode these values in application code or Docker images. Kubernetes Secrets are **base64-encoded by default, not encrypted by default**, so base64 should not be considered security by itself. Access can be controlled using **RBAC**, and Secrets can be injected into Pods as environment variables or mounted as files.

```text id="v8m3qx"
Secret → Kubernetes → Environment Variable / Volume → Application
```

### Basic Secret YAML

```yaml id="k4n7zp"
apiVersion: v1                              # Kubernetes API version.
kind: Secret                                 # Creates a Secret resource.
metadata:
  name: my-secret                            # Name used by Pods to reference the Secret.
type: Opaque                                 # Generic Secret type for arbitrary key-value data.
data:
  DB_PASSWORD: <base64-value>                # Base64-encoded password.
  API_KEY: <base64-value>                    # Base64-encoded API key.
```

To encode a value:

```bash id="q6r2wk"
echo -n "mypassword" | base64                 # Converts the value to base64.
```

**Important:** Base64 is **encoding, not encryption**.

---

### Create Secret from Literal Values

```bash id="x9p4mz"
kubectl create secret generic my-secret --from-literal=DB_PASSWORD=mypassword --from-literal=API_KEY=my-api-key   # Creates a Secret directly from raw values.
kubectl get secret my-secret -o yaml                                                                            # Displays the Secret YAML with encoded values.
```

With `--from-literal`, you provide the **raw values**. Kubernetes handles the encoding.

```text id="m7k3qx"
Raw Value → kubectl → Secret → Base64 Encoded Value
```

---

### Create Secret from File

```bash id="r5n8vc"
kubectl create secret generic my-secret --from-file=db_password.txt        # Creates a Secret using the file content as the value.
```

The filename becomes the Secret key.

```text id="z4q6hp"
db_password.txt → Secret Key → File Content → Secret Value
```

---

## Secret as Environment Variable

If the application expects credentials as environment variables, we can inject a **specific Secret key**.

```yaml id="c8m5wr"
env:
- name: DB_PASSWORD                          # Environment variable available inside the container.
  valueFrom:
    secretKeyRef:
      name: my-secret                         # References the Secret.
      key: DB_PASSWORD                        # Reads the DB_PASSWORD key from the Secret.
```

```text id="n3k7vx"
Secret → DB_PASSWORD → secretKeyRef → Container Environment Variable
```

Kubernetes provides the value to the container; the application receives the **decoded value**.

---

## Inject All Secret Keys

If we want to inject **all keys** from a Secret:

```yaml id="p6x2qm"
envFrom:
- secretRef:
    name: my-secret                           # Imports all keys from this Secret as environment variables.
```

If the Secret contains `DB_PASSWORD` and `API_KEY`:

```text id="w8m4zn"
my-secret → envFrom → DB_PASSWORD + API_KEY → Container Environment
```

### `secretKeyRef` vs `secretRef`

```text id="q2v7kx"
secretKeyRef → One Specific Secret Key
secretRef → All Secret Keys
```

### Why Do We Use Secrets?

```text id="j5n8wp"
Secret → Avoid Hardcoding → Protect Credentials → RBAC Access Control → Easy Credential Rotation
```

### Interview-Ready Answer

> **“Basically, Kubernetes Secret is used to store sensitive information like passwords, API keys, tokens, and credentials.** It helps us avoid hardcoding sensitive values in application code or Docker images. By default, Secret data is **base64 encoded, not encrypted**, so we should also use proper RBAC and encryption at rest where required. We can create Secrets using YAML, `--from-literal`, or `--from-file`. Once created, we can inject a specific key using `secretKeyRef`, or all keys using `secretRef`. Kubernetes makes the value available to the container in decoded form. This gives us a Kubernetes-native way to manage credentials separately from the application.”
## Secret as Volume Mount

Some applications expect sensitive data as **files instead of environment variables**, for example certificates, SSH keys, or configuration files. Kubernetes allows us to mount a Secret as a volume. Each Secret key becomes a file, and the file contains the **decoded Secret value**.

```text id="v7k3mx"
Secret → Volume → /etc/secret → Application Reads Sensitive Files
```

### Mount Entire Secret

```yaml id="k4m8qp"
volumes:
- name: secret-volume                         # Defines the Secret volume.
  secret:
    secretName: my-secret                     # Gets the data from this Secret.
containers:
- name: my-app
  volumeMounts:
  - name: secret-volume                       # Uses the Secret volume.
    mountPath: /etc/secret                    # Mounts Secret files inside this directory.
```

If the Secret has `DB_PASSWORD` and `API_KEY`:

```text id="r5n2wx"
/etc/secret/DB_PASSWORD → Decoded Password
/etc/secret/API_KEY → Decoded API Key
```

### Mount Specific Secret Key

```yaml id="p8q3zn"
volumes:
- name: secret-volume                         # Defines the Secret volume.
  secret:
    secretName: my-secret                     # References the Secret.
    items:
    - key: db-password                         # Selects only this Secret key.
      path: db-password.txt                    # Creates this file name.
containers:
- name: my-app
  volumeMounts:
  - name: secret-volume                        # Uses the Secret volume.
    mountPath: /etc/secret                     # Mounts the selected file here.
```

```text id="m6v9ks"
my-secret → db-password → db-password.txt → /etc/secret/db-password.txt
```

---

## Base64 Encoding / Decoding

Kubernetes Secret YAML commonly represents values under `data` using **base64 encoding**. Base64 is **not encryption**.

```bash id="x2n7qc"
echo -n "mypassword" | base64                  # Encodes the password.
echo -n "bXlwYXNzd29yZA==" | base64 --decode  # Decodes the base64 value.
```

```text id="c4k8wp"
Plain Value → Base64 Encoding → Secret data
Secret data → Base64 Decoding → Original Value
```

**Important:** Real security requires appropriate **RBAC and encryption at rest**, not just base64.

---

## Immutable ConfigMap

An immutable ConfigMap is a ConfigMap that **cannot be modified after creation**. It is useful when configuration should remain fixed and accidental production changes must be prevented.

### Immutable ConfigMap YAML

```yaml id="n5r8xm"
apiVersion: v1                              # Kubernetes API version.
kind: ConfigMap                             # Creates a ConfigMap.
metadata:
  name: immutable-config                     # Name of the ConfigMap.
immutable: true                              # Prevents modification after creation.
data:
  app_environment: production                # Fixed configuration value.
  log_level: info                            # Fixed configuration value.
```

```text id="q7m3vx"
Create ConfigMap → immutable=true → Configuration Locked → Cannot Edit
```

If you need a new value:

```text id="w8k4zn"
Old ConfigMap → Create New ConfigMap → Update Deployment Reference → New Pods → New Configuration
```

### Mount Immutable ConfigMap

```yaml id="f3q9kp"
volumes:
- name: config-volume                         # Defines the ConfigMap volume.
  configMap:
    name: immutable-config                     # References the immutable ConfigMap.
containers:
- name: my-app
  volumeMounts:
  - name: config-volume                        # Uses the ConfigMap volume.
    mountPath: /etc/config                     # Configuration files appear here.
```

---

## ConfigMap / Secret Update Strategy

The important difference is **how the configuration is consumed**.

### Environment Variable

Environment variables are loaded when the **Pod starts**. Updating the ConfigMap or Secret does not update the environment variable inside an existing container.

```text id="k6p2wm"
ConfigMap/Secret Updated → Existing Pod → Old Environment Value
                                      ↓
                                Pod Restart
                                      ↓
                                New Value Loaded
```

For a Deployment:

```bash id="v4n8qx"
kubectl rollout restart deployment my-app       # Restarts Pods so they load the updated configuration.
```

### Volume Mount

When ConfigMap or Secret data is mounted as a volume, Kubernetes can **refresh the mounted files** after the object changes. There can be a short propagation delay.

```text id="z5m7kc"
ConfigMap/Secret Updated → Kubernetes Refreshes Mounted Files → Application Reads New File
```

No Pod restart is normally required.

### Immutable ConfigMap / Secret

An immutable object cannot be changed. Create a **new version** and update the workload to reference it.

```text id="h4q8nx"
Old ConfigMap → New ConfigMap → Update Deployment → Rolling Update → New Pods → New Configuration
```

## Quick Revision

```text id="s8k3qp"
Secret Volume → Sensitive Data as Files
Base64 → Encoding, NOT Encryption
Immutable ConfigMap → Cannot Be Modified
Environment Variable → Restart Pod to Get Updated Value
Volume Mount → Files Can Refresh Automatically
Immutable Object → Create New Version + Update Workload
```

### Interview-Ready Answer

> **“Basically, Kubernetes Secrets can be mounted as files when an application expects sensitive configuration in file format, such as certificates, SSH keys, or configuration files.** Each Secret key becomes a file, and Kubernetes makes the decoded value available inside the container. We can mount the complete Secret or use `items` to mount only a specific key. Base64 is only an encoding mechanism, not encryption, so we should use RBAC and encryption at rest for proper security. For ConfigMaps, if configuration is injected as environment variables, updating the ConfigMap doesn't update the running Pod, so we need to restart the Pod. If it's mounted as a volume, Kubernetes can refresh the files automatically after a short delay. For immutable ConfigMaps or Secrets, we cannot modify the existing object; we create a new version and update the Deployment to use it.”

