# Python-Docker-WebApp-Deploy-AWS-Kubernetes ## First Deploy
# CI/CD Deployment Workflow

This project demonstrates a complete CI/CD pipeline for deploying a Python Flask application to an AWS-hosted Kubernetes (kubeadm) cluster using GitHub Actions, Docker, and Kubernetes.

## Architecture

```
Developer
    │
    │ Git Push
    ▼
GitHub Repository
    │
    ▼
GitHub Actions
    │
    ├── Checkout source code
    ├── Build Docker image
    ├── Push image to Docker Hub
    ├── Copy Kubernetes manifests to Kubernetes Master
    ├── SSH into Kubernetes Master
    ├── Apply Kubernetes manifests
    ├── Update Deployment with the latest Docker image
    └── Wait for successful rollout
    │
    ▼
AWS kubeadm Kubernetes Cluster
    │
    ▼
Python Flask Application
```

## Deployment Workflow

### 1. Source Code Commit

The deployment process starts when code is pushed to the `main` branch or when the workflow is manually triggered using **workflow_dispatch**.

```bash
git add .
git commit -m "Deploy new version"
git push origin main
```

---

### 2. Build Docker Image

GitHub Actions checks out the latest source code and builds a Docker image using the project's `Dockerfile`.

Example:

```bash
docker build \
-t dockerhub-user/python-app:<commit-sha> \
-t dockerhub-user/python-app:latest .
```

Two tags are created:

* **latest** – Latest application version
* **Commit SHA** – Immutable version for deployments and rollback

---

### 3. Push Image to Docker Hub

The newly built image is pushed to Docker Hub.

```bash
docker push dockerhub-user/python-app:<commit-sha>
docker push dockerhub-user/python-app:latest
```

This makes the application image available for the Kubernetes cluster.

---

### 4. Copy Kubernetes Manifests

The workflow securely copies the Kubernetes manifests (`deployment.yaml` and `service.yaml`) to the Kubernetes master node using SCP.

```
GitHub Actions
        │
        ▼
AWS EC2 Kubernetes Master
```

---

### 5. Connect to Kubernetes Master

GitHub Actions establishes an SSH connection to the Kubernetes master node.

This approach is useful for private kubeadm clusters because `kubectl` is already configured on the master node and the Kubernetes API server does not need to be exposed publicly.

---

### 6. Deploy to Kubernetes

The workflow applies the Kubernetes manifests.

```bash
kubectl apply -f k8s/deployment.yaml
kubectl apply -f k8s/service.yaml
```

If the resources already exist, Kubernetes updates them instead of recreating them.

---

### 7. Update Deployment Image

The deployment is updated to use the newly built Docker image.

```bash
kubectl set image deployment/python-app \
python-app=dockerhub-user/python-app:<commit-sha>
```

Using the commit SHA ensures every deployment references an immutable image version.

---

### 8. Rolling Update

Kubernetes performs a rolling update.

During the rollout:

* New Pods are created.
* Health checks are performed.
* Old Pods are terminated only after new Pods become healthy.
* The application remains available with minimal or no downtime.

The workflow waits until the rollout completes successfully.

```bash
kubectl rollout status deployment/python-app
```

---

### 9. Verify Deployment

After deployment, the workflow verifies the cluster state.

```bash
kubectl get deployment
kubectl get pods
kubectl get svc
```

This confirms that the Deployment, Pods, and Service are running successfully.

---

# Technologies Used

* Python (Flask)
* Docker
* GitHub Actions
* Docker Hub
* Kubernetes (kubeadm)
* AWS EC2
* SSH
* SCP

---

# Benefits of This Approach

* Fully automated CI/CD pipeline
* Versioned Docker images using Git commit SHA
* Rolling updates with minimal downtime
* Repeatable and consistent deployments
* Secure deployment using SSH instead of exposing the Kubernetes API
* Suitable for self-managed Kubernetes (kubeadm) clusters

---

# Deployment Flow Summary

```
Developer
    │
    ▼
Git Push
    │
    ▼
GitHub Actions
    │
    ├── Checkout Code
    ├── Build Docker Image
    ├── Push Image to Docker Hub
    ├── Copy Kubernetes YAML Files
    ├── SSH to Kubernetes Master
    ├── kubectl apply
    ├── kubectl set image
    ├── Rolling Update
    └── Verify Deployment
    │
    ▼
AWS kubeadm Kubernetes Cluster
    │
    ▼
Python Flask Application
```
