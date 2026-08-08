## Volume vs Persistent Volume

**Volume:** A Kubernetes volume provides storage to containers inside a Pod. Some volume types, such as `emptyDir`, are tied to the **Pod's lifecycle**. When the Pod is deleted, the `emptyDir` data is deleted. It's mainly useful for **temporary or shared storage between containers in the same Pod**.

**Persistent Volume (PV):** A PV is storage that exists **independently of the Pod**. It can come from NFS, cloud storage, CSI drivers, or other storage systems. Even if the Pod is recreated, the persistent data can remain.

```text id="c8m4xp"
Pod → Volume → Temporary Data → Pod Deleted → Data Lost
Pod → PVC → PV → Persistent Storage → Pod Deleted → Data Remains
```

### `emptyDir` Volume YAML

```yaml id="v7n3kq"
volumes:
- name: nginx-data                         # Defines the volume.
  emptyDir: {}                             # Creates temporary storage for the Pod.
containers:
- name: nginx
  image: nginx
  volumeMounts:
  - name: nginx-data                        # Uses the emptyDir volume.
    mountPath: /usr/share/nginx/html        # Mounts the volume inside the container.
```

---

## Persistent Volume (PV)

A **PV is the actual storage resource** available in the Kubernetes cluster. The Pod doesn't directly use the PV. Instead, the application requests storage through a **PVC**.

```text id="m2q7vx"
Storage → PV → PVC → Pod → Container
```

### PV YAML

```yaml id="n5r8kc"
apiVersion: v1                              # Kubernetes API version.
kind: PersistentVolume                       # Creates a PersistentVolume.
metadata:
  name: my-pv                                # Name of the PV.
spec:
  capacity:
    storage: 5Gi                             # Provides 5Gi of storage.
  accessModes:
  - ReadWriteOnce                            # Volume can be mounted read-write by one node.
  persistentVolumeReclaimPolicy: Retain      # Keeps the data when the PVC is deleted.
  storageClassName: manual                   # Storage class used for binding.
  hostPath:
    path: /data/mysql                        # Storage location on the node.
```

**Note:** `hostPath` is mainly suitable for **single-node/testing scenarios**. In production, storage is commonly provided through cloud disks, NFS, or CSI-based storage.

---

## Persistent Volume Claim (PVC)

A **PVC is a request for storage**. The application asks for the required capacity and access mode, and Kubernetes finds a suitable PV.

### PVC YAML

```yaml id="k3v6mq"
apiVersion: v1                              # Kubernetes API version.
kind: PersistentVolumeClaim                   # Creates a PVC.
metadata:
  name: my-pvc                               # Name used by the Pod.
spec:
  accessModes:
  - ReadWriteOnce                            # Requests the same access mode as the PV.
  resources:
    requests:
      storage: 5Gi                            # Requests 5Gi of storage.
  storageClassName: manual                   # Matches the PV's storage class.
```

Kubernetes finds a compatible PV based on the **requested capacity, access mode, and storage class**, and binds the PVC to it.

```text id="q8n4wp"
PVC Request → Kubernetes Finds Matching PV → PVC Bound to PV
```

The relationship is:

```text id="x5m7kr"
PV = Actual Storage
PVC = Request for Storage
Pod = Consumer of PVC
```

---

## Pod Using PVC

The Pod references the **PVC**, not the PV directly.

```yaml id="r6p2zn"
volumes:
- name: app-storage                         # Defines the Pod volume.
  persistentVolumeClaim:
    claimName: my-pvc                        # Uses the PVC that is bound to the PV.
containers:
- name: nginx
  image: nginx
  volumeMounts:
  - name: app-storage                        # Uses the PVC-backed volume.
    mountPath: /usr/share/nginx/html         # Mounts persistent storage inside the container.
```

```text id="h4k8vx"
Pod → PVC → Bound PV → Underlying Storage
```

If the Pod is deleted and recreated:

```text id="w7m3qp"
Pod Deleted → PVC Remains → PV Remains → New Pod → Same PVC → Same Data
```

### Reclaim Policy

`Retain` means Kubernetes **keeps the PV and its data** after the PVC is deleted.

```text id="j9k4mz"
PVC Deleted → Retain → PV/Data Kept
```

### Quick Revision

```text id="z3n7qx"
Volume/emptyDir → Temporary Pod Storage
PV → Actual Persistent Storage
PVC → Request for Storage
Pod → Uses PVC
PV + PVC → Bound One-to-One
Retain → Keep Data After PVC Deletion
```

### Interview-Ready Answer

> **“Basically, the main difference is that a normal Pod volume such as `emptyDir` is generally used for temporary storage and follows the Pod lifecycle, whereas a Persistent Volume provides storage independently of the Pod.** For persistent storage, Kubernetes uses three components: PV, PVC, and Pod. The **PV is the actual storage**, the **PVC is the application's request for storage**, and the Pod consumes the PVC. Kubernetes matches the PVC with a suitable PV based on capacity, access mode, and storage class, and then binds them. The Pod never directly talks to the PV; it mounts the PVC. So even if the Pod is deleted or recreated, the PVC-PV relationship can remain and the application can access the same persistent data. This is commonly used for databases and other workloads that need data to survive Pod recreation.”

---
## Static Provisioning

**Static provisioning** means the administrator **creates the Persistent Volume manually before the application requests storage**. When a PVC is created, Kubernetes looks for an existing PV that matches the PVC requirements and binds them together.

```text id="p7m4xq"
Admin Creates PV → PV Available → Application Creates PVC → Kubernetes Finds Matching PV → PVC Bound → Pod Uses PVC
```

### Static PV YAML

```yaml id="c8n5rz"
apiVersion: v1                              # Kubernetes API version.
kind: PersistentVolume                      # Creates a Persistent Volume.
metadata:
  name: static-pv                           # Name of the PV.
spec:
  capacity:
    storage: 10Gi                           # PV provides 10Gi storage.
  accessModes:
  - ReadWriteOnce                           # Volume can be mounted read-write by one node.
  storageClassName: manual                  # Storage class used for matching.
  persistentVolumeReclaimPolicy: Retain     # Keeps the data when the PVC is deleted.
  hostPath:
    path: /data/static                      # Storage location for this example.
```

The PV exists **before any application requests it**.

### Static PVC YAML

```yaml id="m6q3wp"
apiVersion: v1                              # Kubernetes API version.
kind: PersistentVolumeClaim                 # Creates a storage request.
metadata:
  name: static-pvc                          # Name used by the Pod.
spec:
  accessModes:
  - ReadWriteOnce                           # Must be compatible with the PV.
  resources:
    requests:
      storage: 10Gi                         # Requests 10Gi storage.
  storageClassName: manual                  # Matches the PV's storage class.
```

```text id="r4k8zn"
PVC Request → Find Existing Matching PV → Bind → PVC Uses That PV
```

### Pod YAML

```yaml id="q7v2mx"
volumes:
- name: app-storage                         # Defines the Pod volume.
  persistentVolumeClaim:
    claimName: static-pvc                    # Uses the already-bound PVC.
containers:
- name: app
  image: nginx
  volumeMounts:
  - name: app-storage                        # Uses the PVC-backed storage.
    mountPath: /data                          # Storage appears here inside the container.
```

**Key idea:**

```text id="k9m3vx"
Static Provisioning → PV Created First → PVC Claims Existing PV
```

---

## Dynamic Provisioning

**Dynamic provisioning** means you don't manually create PVs beforehand. Kubernetes automatically creates the required storage when a PVC requests it through a **StorageClass**.

```text id="z5q7nw"
StorageClass → PVC Created → Kubernetes Creates PV → PVC Bound → Pod Uses PVC
```

### StorageClass YAML

```yaml id="v4n8kp"
apiVersion: storage.k8s.io/v1                # StorageClass API version.
kind: StorageClass                           # Creates a StorageClass.
metadata:
  name: dynamic-storage                      # Name referenced by the PVC.
provisioner: <storage-provisioner>           # Defines which storage backend creates the volume.
volumeBindingMode: WaitForFirstConsumer      # Delays provisioning until a Pod uses the PVC.
```

The `provisioner` depends on the environment, such as a **cloud CSI driver**.

### Dynamic PVC YAML

```yaml id="m8r2qx"
apiVersion: v1                              # Kubernetes API version.
kind: PersistentVolumeClaim                 # Creates a storage request.
metadata:
  name: dynamic-pvc                         # Name used by the Pod.
spec:
  accessModes:
  - ReadWriteOnce                           # Requested access mode.
  resources:
    requests:
      storage: 10Gi                         # Requests 10Gi storage.
  storageClassName: dynamic-storage         # Requests dynamic provisioning through this StorageClass.
```

Unlike static provisioning, there doesn't need to be a pre-created matching PV.

```text id="x6k3qp"
PVC → StorageClass → Storage Backend → New PV Created → PVC Bound
```

### Pod YAML

```yaml id="n5v7kc"
volumes:
- name: app-storage                         # Defines the Pod volume.
  persistentVolumeClaim:
    claimName: dynamic-pvc                   # Uses the dynamically provisioned PVC.
containers:
- name: app
  image: nginx
  volumeMounts:
  - name: app-storage                        # Uses the PVC-backed storage.
    mountPath: /data                          # Storage appears here inside the container.
```

```text id="q3m8wx"
Pod → PVC → Dynamically Created PV → Storage Backend
```

### Static vs Dynamic

```text id="p8k4zn"
Static → Admin Creates PV → PVC Finds PV → Pod Uses PVC
Dynamic → StorageClass → PVC → Kubernetes Creates PV → Pod Uses PVC
```

|                  | Static                   | Dynamic              |
| ---------------- | ------------------------ | -------------------- |
| **PV creation**  | Manual                   | Automatic            |
| **StorageClass** | Not necessarily required | Required             |
| **Admin work**   | Higher                   | Lower                |
| **Best for**     | Predefined storage       | Cloud/large clusters |
| **Scaling**      | Manual                   | Automatic            |

### Interview-Ready Answer

> **“Basically, static provisioning means the administrator manually creates Persistent Volumes in advance.** When an application creates a PVC, Kubernetes looks for an existing PV that matches the requested capacity, access mode, and storage class, and then binds the PVC to that PV. In dynamic provisioning, we don't create the PV manually. Instead, we create a **StorageClass**, and when a PVC requests storage through that StorageClass, Kubernetes automatically provisions the underlying storage and creates a PV. The PVC is then bound to that PV, and the Pod consumes the PVC. So, the main difference is **static provisioning creates storage first and applications claim it later, while dynamic provisioning creates storage on demand**. Dynamic provisioning is commonly used in cloud and large Kubernetes environments because it reduces manual storage management.”

---
## Access Modes

**Access mode** defines how a Persistent Volume can be mounted and shared. The two important modes here are **ReadWriteOnce (RWO)** and **ReadWriteMany (RWX)**.

### ReadWriteOnce — RWO

RWO means the volume can be mounted as **read-write by one node at a time**. Multiple Pods can use it only when they are on the same node.

```yaml
accessModes:
- ReadWriteOnce                              # Allows read-write access from one node at a time.
```

```text id="a7m3kx"
PVC → RWO PV → Node 1 → Pod 1 + Pod 2
                   ↓
              Node 2 → ❌ Cannot mount as read-write
```

Common for **databases and single-node workloads**.

### ReadWriteMany — RWX

RWX allows the same volume to be mounted as **read-write by multiple nodes simultaneously**.

```yaml
accessModes:
- ReadWriteMany                              # Allows read-write access from multiple nodes.
```

```text id="k4n8wp"
PVC → RWX PV → Node 1 → Pod 1
            → Node 2 → Pod 2
            → Node 3 → Pod 3
```

Common for **shared file storage**. The underlying storage must support RWX, such as NFS or a compatible CSI-backed storage system.

```text id="q6m2vz"
RWO → One Node → Read/Write
RWX → Multiple Nodes → Read/Write
```

---

## Reclaim Policy

**Reclaim policy** defines what happens to the **Persistent Volume and underlying storage when the PVC is deleted**.

It does **not** apply when the Pod is deleted.

### Retain

`Retain` keeps the PV and its data after the PVC is deleted. The PV enters the **Released** state and requires administrator action for cleanup/reuse.

```yaml
persistentVolumeReclaimPolicy: Retain         # Keeps the PV and underlying data after PVC deletion.
```

```text id="w5k9rx"
PVC Deleted → Retain → PV Released → Data Kept → Manual Cleanup
```

Useful for **important database data**.

### Delete

`Delete` automatically deletes the PV and the underlying dynamically provisioned storage when the PVC is deleted.

```yaml
persistentVolumeReclaimPolicy: Delete         # Deletes the PV and underlying storage when the claim is deleted.
```

```text id="n3q7kp"
PVC Deleted → Delete → PV Deleted → Underlying Storage Deleted
```

Common with **dynamic provisioning in cloud environments**.

```text id="z8m4qx"
Retain → Keep Data
Delete → Remove Data
```

---

## Volume Lifecycle

The basic lifecycle is:

```text id="p6k2vw"
Create PV → Create PVC → PVC Bound to PV → Pod Mounts PVC → Pod Deleted → PVC Remains → PVC Deleted → Reclaim Policy
```

### 1. Volume Creation

The PV can be created manually through **static provisioning** or automatically through **dynamic provisioning**.

```text id="r4n8mx"
Static → Admin Creates PV
Dynamic → StorageClass → Kubernetes Creates PV
```

### 2. PVC Claims the PV

Kubernetes looks for a suitable PV based on requirements such as **capacity, access mode, and StorageClass**.

```text id="c7q3zp"
PVC → Matching PV Found → PVC Bound to PV
```

### 3. Pod Uses the Volume

The Pod references the PVC, and Kubernetes mounts the underlying storage into the container.

```text id="m8v4kx"
Pod → PVC → PV → Storage → /data
```

### 4. Pod Deleted

Deleting the Pod **does not delete the storage**. The PVC remains bound to the PV.

```text id="h5q9wn"
Pod Deleted → Volume Detached → PVC Remains → Data Remains
```

### 5. PVC Deleted

Now the reclaim policy determines what happens.

```text id="x3m7qk"
PVC Deleted → Retain → Data Kept
            → Delete → Storage Deleted
```

### Quick Revision

```text id="v9k4mx"
RWO → Read/Write from One Node
RWX → Read/Write from Multiple Nodes
Retain → Keep Storage/Data
Delete → Delete Storage/Data
Pod Deleted → Data Normally Remains
PVC Deleted → Reclaim Policy Decides
```

### Interview-Ready Answer

> **“Basically, access modes define how a Persistent Volume can be mounted and shared.** The common modes are RWO and RWX. **ReadWriteOnce** allows read-write access from one node at a time, so it's commonly used for workloads like databases. **ReadWriteMany** allows multiple nodes to mount the same volume for read-write access, which is useful for shared storage, provided the backend supports RWX. Reclaim policy defines what happens when the **PVC is deleted**. With `Retain`, Kubernetes keeps the data and the administrator handles cleanup. With `Delete`, Kubernetes deletes the underlying storage, which is commonly used with dynamic provisioning. The overall lifecycle is **PV creation, PVC binding, Pod usage, Pod deletion, and finally PVC deletion**, where the reclaim policy determines the final storage behavior.”
