# ML DevOps App - Operating Guide

## Daily Operations

### 1. Monitoring

#### Check Application Health
```bash
curl http://localhost:5000/health
```

#### View Logs
```bash
# Docker logs
docker-compose logs -f backend

# Local logs
tail -f backend/logs/app.log
```

#### Check Resource Usage
```bash
docker stats ml-devops-app_backend_1
```

### 2. Common Operations

#### Restart Application
```bash
docker-compose restart backend
```

#### View Active Predictions
```bash
tail -50 backend/logs/app.log | grep "Prediction made"
```

#### Check API Response Time
```bash
time curl http://localhost:5000/health
```

## Troubleshooting

### Issue: API Returns 500 Error

```bash
# 1. Check logs
docker-compose logs backend | tail -50

# 2. Verify model file exists
docker-compose exec backend ls -la models/

# 3. Retrain model if needed
docker-compose exec backend python -c "from app import load_or_train_model; load_or_train_model()"

# 4. Restart service
docker-compose restart backend
```

### Issue: High Memory Usage

```bash
# 1. Check current memory
docker stats

# 2. Clear old logs
docker-compose exec backend bash -c "rm -f logs/*.log"

# 3. Restart container
docker-compose restart backend
```

### Issue: Slow Response Times

```bash
# 1. Check if model is loaded
curl http://localhost:5000/api/model/info

# 2. Test with simpler request
curl http://localhost:5000/health

# 3. Check server resources
docker stats
```

## Maintenance Tasks

### Weekly

- [ ] Review error logs: `docker-compose logs backend | grep ERROR`
- [ ] Check disk space: `du -sh *`
- [ ] Verify backups: `ls -la models/`

### Monthly

- [ ] Update dependencies: `pip list --outdated`
- [ ] Run security scan: `trivy fs .`
- [ ] Performance review: `docker stats`
- [ ] Update documentation

### Quarterly

- [ ] Retrain model with new data
- [ ] Security audit
- [ ] Load testing
- [ ] Disaster recovery drill

## Backup & Recovery

### Backup Model Files
```bash
docker-compose exec backend tar -czf /tmp/models-backup.tar.gz models/
docker cp ml-devops-app_backend_1:/tmp/models-backup.tar.gz ./backups/
```

### Restore Model Files
```bash
docker cp ./backups/models-backup.tar.gz ml-devops-app_backend_1:/tmp/
docker-compose exec backend tar -xzf /tmp/models-backup.tar.gz
docker-compose restart backend
```

## Performance Optimization

### 1. Enable Caching
```python
from flask_caching import Cache

cache = Cache(app, config={'CACHE_TYPE': 'simple'})

@app.route('/api/model/info')
@cache.cached(timeout=3600)
def model_info():
    ...
```

### 2. Increase Worker Processes
```bash
# Update docker-compose.yml
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

### 3. Database Connection Pooling
```python
from sqlalchemy.pool import QueuePool
engine = create_engine('...', poolclass=QueuePool, pool_size=10)
```

## Security Checklist

- [ ] Change default credentials
- [ ] Enable HTTPS/SSL
- [ ] Configure firewall rules
- [ ] Set up VPN access if needed
- [ ] Enable audit logging
- [ ] Run vulnerability scanner monthly
- [ ] Keep dependencies updated

## Useful Commands

```bash
# View all containers
docker-compose ps

# Execute command in container
docker-compose exec backend bash

# View real-time logs
docker-compose logs -f --tail=100 backend

# Rebuild images
docker-compose up --build

# Stop all services
docker-compose down

# Remove all data
docker-compose down -v

# View resource limits
docker stats --no-stream

# Check logs since specific time
docker-compose logs --since 2h backend

# Export logs
docker-compose logs backend > debug.log
```

## Escalation Procedures

### Critical Issues (Service Down)

1. Check health endpoint: `curl http://localhost:5000/health`
2. View recent logs: `docker-compose logs backend | tail -100`
3. Restart service: `docker-compose restart backend`
4. If still down, rebuild: `docker-compose up --build`
5. Notify on-call team if issue persists

### Performance Issues (High Latency)

1. Check resource usage: `docker stats`
2. View slow request logs
3. Scale horizontally: `docker-compose up -d --scale backend=2`
4. Review model size and optimization

### Data Issues

1. Verify model files: `docker-compose exec backend ls -la models/`
2. Check logs for training errors
3. Retrain model: `docker-compose exec backend python train_model.py`
4. Restore from backup if corrupted

## On-Call Runbook

### Morning Check (Start of Day)
```bash
# 1. Verify services running
docker-compose ps

# 2. Check health
curl http://localhost:5000/health

# 3. Review overnight logs
docker-compose logs backend --since 8h | grep ERROR
```

### Evening Check (End of Day)
```bash
# 1. Confirm no active issues
curl http://localhost:5000/metrics

# 2. Backup model files
tar -czf models-backup-$(date +%Y%m%d).tar.gz models/

# 3. Archive logs
gzip backend/logs/app.log
```

## Contact & Escalation

- **Tier 1 Support**: Check logs and restart service
- **Tier 2 Support**: Rebuild container, restore from backup
- **Tier 3 Support**: Architecture review, capacity planning

---

**Last Updated**: January 2026
**Version**: 1.0.0
