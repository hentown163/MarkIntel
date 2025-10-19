# NexusPlanner - AWS EKS Deployment Guide

Complete guide for deploying NexusPlanner with AWS Bedrock integration on Amazon EKS.

## Table of Contents

- [Prerequisites](#prerequisites)
- [Architecture Overview](#architecture-overview)
- [AWS Infrastructure Setup](#aws-infrastructure-setup)
- [Amazon Bedrock Setup](#amazon-bedrock-setup)
- [EKS Cluster Setup](#eks-cluster-setup)
- [Application Deployment](#application-deployment)
- [Post-Deployment Verification](#post-deployment-verification)
- [Operational Tasks](#operational-tasks)
- [Troubleshooting](#troubleshooting)

---

## Prerequisites

### Required Tools

```bash
# AWS CLI
aws --version  # >= 2.x

# kubectl
kubectl version --client  # >= 1.28

# eksctl
eksctl version  # >= 0.150.0

# Helm
helm version  # >= 3.12

# Docker
docker --version  # >= 24.0
```

### AWS Account Requirements

- AWS Account with appropriate permissions
- AWS CLI configured with credentials
- Access to Amazon Bedrock (request access if needed)
- VPC with public and private subnets across 3 AZs

---

## Architecture Overview

```
┌─────────────────────────────────────────────────────────────┐
│                     AWS Cloud (us-east-1)                    │
│                                                               │
│  ┌──────────────────────────────────────────────────────┐   │
│  │                    Amazon EKS Cluster                 │   │
│  │                                                        │   │
│  │  ┌──────────────┐        ┌─────────────┐            │   │
│  │  │   Frontend   │        │   Backend   │            │   │
│  │  │   (React +   │◄───────┤  (FastAPI)  │            │   │
│  │  │    Nginx)    │        │             │            │   │
│  │  └──────┬───────┘        └──────┬──────┘            │   │
│  │         │                       │                    │   │
│  └─────────┼───────────────────────┼────────────────────┘   │
│            │                       │                         │
│            │                       │  ┌───────────────────┐ │
│            │                       └──┤ Amazon Bedrock    │ │
│            │                          │ (Claude 3.5      │ │
│            │                          │  Sonnet)         │ │
│            │                          └───────────────────┘ │
│            │                                                 │
│       ┌────▼──────┐              ┌──────────────────────┐  │
│       │    ALB    │              │   AWS RDS Aurora     │  │
│       │ (Ingress) │              │   (PostgreSQL)       │  │
│       └───────────┘              └──────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
```

**Key Features:**
- **Multi-AZ Deployment**: High availability across 3 availability zones
- **Bedrock Integration**: Secure, VPC-native AI model access
- **IRSA**: IAM Roles for Service Accounts (no hardcoded credentials)
- **RDS Aurora**: Managed PostgreSQL with automated backups
- **Auto-scaling**: HPA for dynamic workload management
- **Security**: Private subnets, security groups, encryption at rest/transit

---

## AWS Infrastructure Setup

### 1. Create VPC (if needed)

```bash
# Create VPC with public and private subnets
eksctl create cluster --name nexusplanner-cluster \
  --version 1.28 \
  --region us-east-1 \
  --zones us-east-1a,us-east-1b,us-east-1c \
  --nodegroup-name standard-workers \
  --node-type t3.large \
  --nodes 3 \
  --nodes-min 3 \
  --nodes-max 10 \
  --managed \
  --with-oidc \
  --full-ecr-access \
  --dry-run  # Remove --dry-run when ready
```

### 2. Create RDS Aurora PostgreSQL

```bash
# Create DB subnet group
aws rds create-db-subnet-group \
  --db-subnet-group-name nexusplanner-db-subnet \
  --db-subnet-group-description "NexusPlanner DB Subnet Group" \
  --subnet-ids subnet-xxx subnet-yyy subnet-zzz

# Create Aurora PostgreSQL cluster
aws rds create-db-cluster \
  --db-cluster-identifier nexusplanner-db \
  --engine aurora-postgresql \
  --engine-version 15.4 \
  --master-username nexusplanner \
  --master-user-password $(openssl rand -base64 32) \
  --db-subnet-group-name nexusplanner-db-subnet \
  --vpc-security-group-ids sg-xxxxx \
  --backup-retention-period 7 \
  --preferred-backup-window "03:00-04:00" \
  --preferred-maintenance-window "mon:04:00-mon:05:00" \
  --enable-cloudwatch-logs-exports '["postgresql"]' \
  --storage-encrypted

# Create DB instance
aws rds create-db-instance \
  --db-instance-identifier nexusplanner-db-instance-1 \
  --db-cluster-identifier nexusplanner-db \
  --db-instance-class db.r6g.large \
  --engine aurora-postgresql
```

### 3. Store Secrets in AWS Secrets Manager

```bash
# Database URL
aws secretsmanager create-secret \
  --name nexusplanner/database-url \
  --description "NexusPlanner Database URL" \
  --secret-string "postgresql://nexusplanner:PASSWORD@<RDS_ENDPOINT>:5432/nexusplanner"

# JWT Secret
aws secretsmanager create-secret \
  --name nexusplanner/jwt-secret \
  --description "NexusPlanner JWT Secret" \
  --secret-string "$(openssl rand -hex 32)"

# OpenAI API Key (if using OpenAI)
aws secretsmanager create-secret \
  --name nexusplanner/openai-api-key \
  --description "OpenAI API Key" \
  --secret-string "sk-..."
```

---

## Amazon Bedrock Setup

### 1. Enable Bedrock Access

1. **Request Model Access**:
   - Go to AWS Console → Bedrock → Model Access
   - Request access to: **Claude 3.5 Sonnet**, **Claude 3 Sonnet**, **Claude 3 Haiku**
   - Wait for approval (usually instant for most models)

2. **Verify Access**:
```bash
aws bedrock list-foundation-models --region us-east-1 | grep -A5 "claude-3-5"
```

### 2. Create IAM Policy for Bedrock Access

Create `bedrock-policy.json`:

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "bedrock:InvokeModel",
        "bedrock:InvokeModelWithResponseStream"
      ],
      "Resource": [
        "arn:aws:bedrock:us-east-1::foundation-model/anthropic.claude-3-5-sonnet-20241022-v2:0",
        "arn:aws:bedrock:us-east-1::foundation-model/anthropic.claude-3-sonnet-20240229-v1:0",
        "arn:aws:bedrock:us-east-1::foundation-model/anthropic.claude-3-haiku-20240307-v1:0",
        "arn:aws:bedrock:us-east-1::foundation-model/meta.llama3-2-90b-instruct-v1:0"
      ]
    }
  ]
}
```

```bash
aws iam create-policy \
  --policy-name NexusPlannerBedrockPolicy \
  --policy-document file://bedrock-policy.json
```

### 3. Create IRSA (IAM Role for Service Account)

```bash
# Create IAM role for service account
eksctl create iamserviceaccount \
  --name nexusplanner-backend \
  --namespace nexusplanner \
  --cluster nexusplanner-cluster \
  --region us-east-1 \
  --attach-policy-arn arn:aws:iam::$(aws sts get-caller-identity --query Account --output text):policy/NexusPlannerBedrockPolicy \
  --approve \
  --override-existing-serviceaccounts
```

---

## EKS Cluster Setup

### 1. Install Required Add-ons

```bash
# AWS Load Balancer Controller
helm repo add eks https://aws.github.io/eks-charts
helm repo update

helm install aws-load-balancer-controller eks/aws-load-balancer-controller \
  -n kube-system \
  --set clusterName=nexusplanner-cluster \
  --set serviceAccount.create=false \
  --set serviceAccount.name=aws-load-balancer-controller

# External Secrets Operator (for AWS Secrets Manager integration)
helm repo add external-secrets https://charts.external-secrets.io
helm install external-secrets \
  external-secrets/external-secrets \
  -n external-secrets-system \
  --create-namespace

# Metrics Server (for HPA)
kubectl apply -f https://github.com/kubernetes-sigs/metrics-server/releases/latest/download/components.yaml
```

### 2. Configure ExternalSecrets

Create `secret-store.yaml`:

```yaml
apiVersion: external-secrets.io/v1beta1
kind: SecretStore
metadata:
  name: aws-secrets-manager
  namespace: nexusplanner
spec:
  provider:
    aws:
      service: SecretsManager
      region: us-east-1
      auth:
        jwt:
          serviceAccountRef:
            name: nexusplanner-backend
```

```bash
kubectl apply -f secret-store.yaml
```

---

## Application Deployment

### Option 1: Deploy with Helm (Recommended)

```bash
# 1. Build and push Docker images to ECR
AWS_ACCOUNT_ID=$(aws sts get-caller-identity --query Account --output text)
AWS_REGION=us-east-1

# Create ECR repositories
aws ecr create-repository --repository-name nexusplanner-backend --region $AWS_REGION
aws ecr create-repository --repository-name nexusplanner-frontend --region $AWS_REGION

# Login to ECR
aws ecr get-login-password --region $AWS_REGION | docker login --username AWS --password-stdin $AWS_ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com

# Build and push backend
docker build -f Dockerfile.backend -t nexusplanner-backend .
docker tag nexusplanner-backend:latest $AWS_ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com/nexusplanner-backend:latest
docker push $AWS_ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com/nexusplanner-backend:latest

# Build and push frontend
docker build -f Dockerfile.frontend -t nexusplanner-frontend .
docker tag nexusplanner-frontend:latest $AWS_ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com/nexusplanner-frontend:latest
docker push $AWS_ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com/nexusplanner-frontend:latest

# 2. Create values override file
cat > values-production.yaml <<EOF
image:
  backend:
    repository: $AWS_ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com/nexusplanner-backend
    tag: latest
  frontend:
    repository: $AWS_ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com/nexusplanner-frontend
    tag: latest

app:
  llmProvider: bedrock
  aws:
    region: us-east-1
    bedrockModelName: claude-3-5-sonnet
    iamRoleArn: arn:aws:iam::$AWS_ACCOUNT_ID:role/<IRSA_ROLE_NAME>

database:
  external:
    enabled: true
    host: <RDS_ENDPOINT>
    port: 5432
    name: nexusplanner
    username: nexusplanner

ingress:
  enabled: true
  hosts:
    - host: nexusplanner.yourdomain.com
      paths:
        - path: /api
          pathType: Prefix
          backend: backend
        - path: /
          pathType: Prefix
          backend: frontend
EOF

# 3. Deploy with Helm
helm install nexusplanner ./helm/nexusplanner \
  --namespace nexusplanner \
  --create-namespace \
  --values values-production.yaml

# 4. Verify deployment
kubectl get pods -n nexusplanner
kubectl get svc -n nexusplanner
kubectl get ingress -n nexusplanner
```

### Option 2: Deploy with Kubectl + Kustomize

```bash
# 1. Update image references in deployment files
# Edit kubernetes/base/*-deployment.yaml to replace <AWS_ACCOUNT_ID> and <AWS_REGION>

# 2. Apply manifests
kubectl apply -k kubernetes/base/

# 3. Verify deployment
kubectl get all -n nexusplanner
```

---

## Post-Deployment Verification

### 1. Check Pod Status

```bash
kubectl get pods -n nexusplanner

# Expected output:
# NAME                                     READY   STATUS    RESTARTS   AGE
# nexusplanner-backend-xxx                 1/1     Running   0          2m
# nexusplanner-backend-yyy                 1/1     Running   0          2m
# nexusplanner-frontend-zzz                1/1     Running   0          2m
```

### 2. Test Health Endpoints

```bash
# Port-forward backend
kubectl port-forward -n nexusplanner svc/nexusplanner-backend 8000:8000

# In another terminal
curl http://localhost:8000/health
curl http://localhost:8000/ready

# Expected: {"status":"healthy"} and {"status":"ready","database":"connected",...}
```

### 3. Verify Bedrock Integration

```bash
kubectl exec -n nexusplanner -it deploy/nexusplanner-backend -- python3 <<EOF
from app.infrastructure.llm.adapter_factory import AdapterFactory
adapter = AdapterFactory.create_adapter(provider="bedrock")
print(adapter.get_model_info())
EOF

# Expected: Model info with claude-3-5-sonnet
```

### 4. Check Ingress

```bash
kubectl get ingress -n nexusplanner
# Note the ADDRESS (ALB DNS name)

# Wait for DNS propagation, then test
curl https://nexusplanner.yourdomain.com/api/
```

---

## Operational Tasks

### Scaling

```bash
# Manual scaling
kubectl scale deployment nexusplanner-backend -n nexusplanner --replicas=5

# Check HPA status
kubectl get hpa -n nexusplanner
```

### Updates/Rollouts

```bash
# Update image
kubectl set image deployment/nexusplanner-backend \
  backend=$AWS_ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com/nexusplanner-backend:v2.1.0 \
  -n nexusplanner

# Monitor rollout
kubectl rollout status deployment/nexusplanner-backend -n nexusplanner

# Rollback if needed
kubectl rollout undo deployment/nexusplanner-backend -n nexusplanner
```

### Monitoring

```bash
# View logs
kubectl logs -n nexusplanner -l app=nexusplanner,component=backend --tail=100 -f

# Exec into pod
kubectl exec -n nexusplanner -it deploy/nexusplanner-backend -- /bin/bash

# View resource usage
kubectl top pods -n nexusplanner
```

---

## Troubleshooting

### Pods not starting

```bash
# Check pod events
kubectl describe pod <pod-name> -n nexusplanner

# Common issues:
# - ImagePullBackOff: Check ECR permissions
# - CrashLoopBackOff: Check logs with kubectl logs
# - Pending: Check node resources and HPA
```

### Database connection issues

```bash
# Test database connectivity
kubectl run -it --rm debug --image=postgres:15 --restart=Never -- \
  psql postgresql://nexusplanner:PASSWORD@<RDS_ENDPOINT>:5432/nexusplanner

# Check security groups allow traffic from EKS worker nodes
```

### Bedrock access denied

```bash
# Verify IRSA is configured
kubectl describe sa nexusplanner-backend -n nexusplanner
# Should show: eks.amazonaws.com/role-arn annotation

# Test Bedrock API directly
aws bedrock invoke-model \
  --model-id anthropic.claude-3-5-sonnet-20241022-v2:0 \
  --body '{"anthropic_version":"bedrock-2023-05-31","max_tokens":100,"messages":[{"role":"user","content":[{"type":"text","text":"Hello"}]}]}' \
  --cli-binary-format raw-in-base64-out \
  --region us-east-1 \
  /tmp/response.json
```

---

## Security Best Practices

1. **Use IRSA**: Never hardcode AWS credentials
2. **Secrets Management**: Use AWS Secrets Manager + External Secrets
3. **Network Policies**: Implement Kubernetes Network Policies
4. **Pod Security**: Use Pod Security Standards (PSS)
5. **Image Scanning**: Enable ECR image scanning
6. **Least Privilege**: Minimize IAM permissions
7. **Encryption**: Enable encryption at rest for RDS and EBS
8. **VPC Endpoints**: Use VPC endpoints for Bedrock (no internet required)

---

## Cost Optimization

- **Right-size instances**: Start with t3.medium, monitor and adjust
- **Use Savings Plans**: For predictable workloads
- **HPA**: Scale down during off-hours
- **Bedrock vs OpenAI**: Claude 3 Haiku for cost-sensitive tasks
- **RDS Aurora Serverless**: Consider for variable workloads
- **EBS GP3**: More cost-effective than GP2

---

## Support

- GitHub Issues: https://github.com/yourorg/nexusplanner/issues
- Documentation: https://docs.nexusplanner.example.com
- Email: support@nexusplanner.example.com

---

**Last Updated**: 2025-10-19  
**Version**: 2.0.0
