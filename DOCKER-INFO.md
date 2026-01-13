2# ML DevOps App - Docker Build & Deploy Configuration

## Build Information
- **Base Image**: python:3.11-slim (50MB)
- **Total Image Size**: ~200MB
- **Build Time**: ~2-3 minutes

## Volumes
- `models/` - Trained ML models (persistent)
- `logs/` - Application logs (persistent)

## Environment Variables
- `FLASK_ENV=production` - Production mode
- `FLASK_APP=app.py` - Application entry point

## Ports
- `5000` - Backend API
- `8080` - Frontend (Nginx)

## Health Check
- **Endpoint**: `/health`
- **Interval**: 30 seconds
- **Timeout**: 10 seconds
- **Retries**: 3

## Logging
- **Driver**: json-file
- **Max Size**: 10m
- **Max Files**: 3

## Network
- Services communicate via Docker network
- Nginx reverse proxy routes requests to backend
- CORS enabled for frontend-backend communication

## Storage
- Models: `./backend/models`
- Logs: `./backend/logs`
- Auto-created on first run

## Resource Limits (Recommended)
```yaml
resources:
  limits:
    cpus: '1'
    memory: 512M
  reservations:
    cpus: '0.5'
    memory: 256M
```

## Restart Policy
```yaml
restart_policy:
  condition: on-failure
  delay: 5s
  max_attempts: 3
  window: 120s
```
