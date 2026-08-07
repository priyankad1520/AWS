# HPA (Horizontal Pod Autoscaler)

### Problem 1: Pods are not scaling up
> First, I'd check the HPA status using **kubectl get hpa** and **kubectl describe hpa**. Then I'd verify whether the Metrics Server is working by checking **kubectl top pods** and **kubectl top nodes**. Next, I'd confirm that the Deployment has CPU and Memory requests configured and that the current utilization has crossed the target threshold. I'd also verify that the HPA is pointing to the correct Deployment and hasn't reached its maximum replica limit. Based on the findings, I'd fix the issue and validate that the replicas scale automatically.

**Possible Causes:**

* Metrics Server is not running or installed.
* CPU or Memory requests are not defined in the Deployment.
* Current resource utilization has not reached the configured threshold.
* HPA target utilization is configured incorrectly.
* HPA is pointing to the wrong Deployment.
* HPA has already reached the maximum replica limit.

**Investigation:**

```bash
kubectl get hpa

kubectl describe hpa <hpa-name>

kubectl top pods

kubectl top nodes

kubectl describe deployment <deployment-name>
```

**Fixes:**

* Start or install the Metrics Server.
* Define CPU and Memory requests.
* Adjust the target utilization.
* Correct the HPA target Deployment.
* Increase the maximum replica limit if required.

### How to Fix
```yaml
# 1. Verify the Metrics Server**
kubectl top nodes
kubectl top pods

# If these commands fail, check the Metrics Server pod:
kubectl get pods -n kube-system
kubectl logs -n kube-system <metrics-server-pod>
------------------------------------------------------------
# 2. Verify CPU and Memory requests
kubectl describe deployment <deployment-name>

Ensure the Deployment defines resource requests:
resources:
  requests:
    cpu: 200m
    memory: 256Mi
------------------------------------------------------------
# 3. Verify HPA configuration**
kubectl describe hpa <hpa-name>
# Check: Current CPU utilization, Target utilization, Current replicas, Desired replicas, Events
------------------------------------------------------------
# 4. Generate load**
kubectl run load-test --rm -it --image=busybox -- sh

# Inside the pod:
while true; do
wget -q -O- http://my-service
done

# Monitor scaling:
kubectl get hpa -w
kubectl get pods -w
```

