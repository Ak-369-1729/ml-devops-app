# ML DevOps App - Production Deployment Guide

## Pre-Deployment Checklist

- [ ] All tests passing locally
- [ ] Security scan completed with no critical issues
- [ ] Docker image built successfully
- [ ] Environment variables configured
- [ ] Database backups created
- [ ] Monitoring and logging configured
- [ ] Load testing completed
- [ ] Documentation updated
- [ ] Team approval received

## Cloud Deployment Strategies

### 1. AWS Deployment

#### Using ECR + ECS

```bash
# Build and push to ECR
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin 123456789.dkr.ecr.us-east-1.amazonaws.com

docker build -t ml-devops-app .
docker tag ml-devops-app:latest 123456789.dkr.ecr.us-east-1.amazonaws.com/ml-devops-app:latest
docker push 123456789.dkr.ecr.us-east-1.amazonaws.com/ml-devops-app:latest
```

#### Infrastructure as Code (Terraform)

```hcl
# main.tf
resource "aws_ecs_cluster" "main" {
  name = "ml-devops-cluster"
}

resource "aws_ecs_service" "main" {
  name            = "ml-devops-service"
  cluster         = aws_ecs_cluster.main.id
  task_definition = aws_ecs_task_definition.main.arn
  desired_count   = 2
  launch_type     = "FARGATE"
}
```

### 2. Google Cloud Deployment

#### Using Cloud Run

```bash
# Deploy directly
gcloud run deploy ml-devops-app \
  --source . \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated
```

### 3. Azure Deployment

#### Using Container Instances

```bash
# Build and push to ACR
az acr build --registry myregistry --image ml-devops-app:latest .

# Deploy
az container create \
  --resource-group mygroup \
  --name ml-devops-app \
  --image myregistry.azurecr.io/ml-devops-app:latest \
  --ports 5000 \
  --environment-variables FLASK_ENV=production
```

### 4. Kubernetes Deployment

```yaml
# deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: ml-devops-app
spec:
  replicas: 3
  selector:
    matchLabels:
      app: ml-devops-app
  template:
    metadata:
      labels:
        app: ml-devops-app
    spec:
      containers:
      - name: backend
        image: ml-devops-app:latest
        ports:
        - containerPort: 5000
        livenessProbe:
          httpGet:
            path: /health
            port: 5000
          initialDelaySeconds: 30
          periodSeconds: 10
        readinessProbe:
          httpGet:
            path: /health
            port: 5000
          initialDelaySeconds: 5
          periodSeconds: 5
        resources:
          requests:
            memory: "128Mi"
            cpu: "100m"
          limits:
            memory: "256Mi"
            cpu: "500m"
```

## Monitoring & Logging Setup

### CloudWatch Integration

```python
# Add to app.py
import watchtower
import logging

handler = watchtower.CloudWatchLogHandler()
logging.getLogger().addHandler(handler)
```

### ELK Stack (Elasticsearch, Logstash, Kibana)

```yaml
# docker-compose.yml additions
elk:
  image: docker.elastic.co/elasticsearch/elasticsearch:7.17.0
  environment:
    - discovery.type=single-node
  ports:
    - "9200:9200"
```

### Prometheus Metrics

```python
# Add to app.py
from prometheus_client import Counter, Histogram, generate_latest

predictions = Counter('predictions_total', 'Total predictions')
latency = Histogram('prediction_latency_seconds', 'Prediction latency')
```

## Auto-Scaling Configuration

### AWS Auto Scaling

```bash
# Set up target tracking
aws autoscaling put-scaling-policy \
  --auto-scaling-group-name ml-devops-asg \
  --policy-name scale-on-cpu \
  --policy-type TargetTrackingScaling \
  --target-tracking-configuration file://config.json
```

### Kubernetes HPA

```yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: ml-devops-app-hpa
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: ml-devops-app
  minReplicas: 2
  maxReplicas: 10
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 70
```

## Continuous Deployment

### GitHub Actions to Cloud

```yaml
name: Deploy to Production

on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Deploy to AWS
        run: |
          aws ecs update-service \
            --cluster ml-devops-cluster \
            --service ml-devops-service \
            --force-new-deployment
        env:
          AWS_ACCESS_KEY_ID: ${{ secrets.AWS_ACCESS_KEY_ID }}
          AWS_SECRET_ACCESS_KEY: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
```

## Rollback Procedures

### Docker Rollback
```bash
# Revert to previous image
docker-compose down
docker pull ml-devops-app:previous
docker-compose up -d
```

### Kubernetes Rollback
```bash
kubectl rollout undo deployment/ml-devops-app
kubectl rollout history deployment/ml-devops-app
```

## Health Checks & Alerts

### Define SLOs
- API Response Time: < 500ms (99th percentile)
- Availability: 99.9%
- Model Accuracy: > 90%

### Alert Rules
```yaml
groups:
- name: ml-devops-alerts
  rules:
  - alert: HighErrorRate
    expr: rate(http_requests_total{status=~"5.."}[5m]) > 0.01
  - alert: HighLatency
    expr: histogram_quantile(0.99, http_request_duration_seconds) > 0.5
```

## Disaster Recovery

### Backup Strategy
```bash
# Daily backup
0 2 * * * docker exec ml-devops-app tar -czf /backup/models-$(date +%Y%m%d).tar.gz /app/models
```

### Restore from Backup
```bash
tar -xzf models-20260113.tar.gz -C /app/models
docker restart ml-devops-app
```

## Cost Optimization

1. **Container Size**: Use slim images (100MB vs 300MB+)
2. **Scaling**: Set appropriate min/max replicas
3. **Resource Limits**: Define CPU/memory requests and limits
4. **Scheduled Scaling**: Scale down during off-peak hours
5. **Image Registry**: Use ECR lifecycle policies to delete old images

## Deployment Validation

```bash
#!/bin/bash
# validate-deployment.sh

API_URL="http://api.example.com"

# Test health
curl -f $API_URL/health || exit 1

# Test prediction
curl -f -X POST $API_URL/api/predict \
  -H "Content-Type: application/json" \
  -d '{"features": [5.1, 3.5, 1.4, 0.2]}' || exit 1

# Test metrics
curl -f $API_URL/api/metrics || exit 1

echo "Deployment validation passed!"
```

## Post-Deployment

1. **Verify**: Check all endpoints responding
2. **Monitor**: Watch error rates and latency for 1 hour
3. **Load Test**: Run synthetic traffic tests
4. **Document**: Update runbooks with actual URLs
5. **Notify**: Inform team of successful deployment

---

For more information, see main README.md
