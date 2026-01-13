# ML DevOps App - Quick Start Guide

## ⚡ 5-Minute Setup

### Option A: Docker (Easiest)

```bash
# 1. Build and start
cd ml-devops-app
docker-compose up --build

# 2. Wait for startup (30 seconds)
# 3. Open browser: http://localhost:8080

# Done! 🎉
```

### Option B: Local Python

```bash
# 1. Setup
cd ml-devops-app/backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt

# 2. Run
python app.py

# 3. In another terminal, open frontend
# Just open ml-devops-app/frontend/index.html in browser
# Update API_BASE to: http://localhost:5000

# Done! 🎉
```

## 📝 First Test

### Using Web UI
1. Open http://localhost:8080 (Docker) or frontend/index.html
2. Enter example values: 5.1, 3.5, 1.4, 0.2
3. Click "Classify Flower"
4. See prediction: Setosa with ~95% confidence

### Using API
```bash
curl -X POST http://localhost:5000/api/predict \
  -H "Content-Type: application/json" \
  -d '{"features": [5.1, 3.5, 1.4, 0.2]}'
```

Expected response:
```json
{
  "prediction": 0,
  "class": "Setosa",
  "confidence": 0.95,
  "probabilities": {
    "Setosa": 0.95,
    "Versicolor": 0.04,
    "Virginica": 0.01
  }
}
```

## 🔗 Important URLs

| Service | URL | Purpose |
|---------|-----|---------|
| Frontend | http://localhost:8080 | Web interface |
| Backend API | http://localhost:5000 | ML API |
| Health Check | http://localhost:5000/health | Server status |
| Model Info | http://localhost:5000/api/model/info | Model details |
| Metrics | http://localhost:5000/api/metrics | App metrics |

## 🎯 Key Features

✅ **Machine Learning**: Random Forest iris classifier
✅ **REST API**: Production-ready Flask backend
✅ **Web UI**: Modern responsive interface
✅ **Docker**: Multi-container setup
✅ **CI/CD**: GitHub Actions pipeline
✅ **Monitoring**: Health checks & logging
✅ **Error Handling**: Proper validation & error responses

## 📊 Example Data

Try these inputs:

**Setosa** (small petals)
```
Sepal Length: 5.1, Sepal Width: 3.5
Petal Length: 1.4, Petal Width: 0.2
```

**Versicolor** (medium petals)
```
Sepal Length: 7.0, Sepal Width: 3.2
Petal Length: 4.7, Petal Width: 1.4
```

**Virginica** (large petals)
```
Sepal Length: 6.3, Sepal Width: 3.3
Petal Length: 6.0, Petal Width: 2.5
```

## 🐛 Troubleshooting

### "Connection refused" error
**Solution**: Make sure Docker or Python backend is running
```bash
docker-compose up  # or: python backend/app.py
```

### "Port already in use"
**Solution**: Use different ports
```bash
# Edit docker-compose.yml or use different ports
docker-compose down
```

### "API offline" in web UI
**Solution**: Check if backend is running and accessible
```bash
curl http://localhost:5000/health
# Should return: {"status": "healthy", ...}
```

## 📚 Next Steps

- [ ] Read [README.md](README.md) for full documentation
- [ ] Review [DEPLOYMENT.md](DEPLOYMENT.md) for production deployment
- [ ] Check [OPERATIONS.md](OPERATIONS.md) for maintenance
- [ ] Run tests: `pytest backend/tests/ -v`
- [ ] Explore API endpoints with Postman/cURL

## 🚀 Deploy to Cloud

See [DEPLOYMENT.md](DEPLOYMENT.md) for:
- AWS deployment (ECR + ECS)
- Google Cloud Run
- Azure Container Instances
- Kubernetes setup

## 📞 Support

**Check health**: `curl http://localhost:5000/health`

**View logs**: `docker-compose logs -f backend`

**Restart**: `docker-compose restart`

---

**Ready?** Start with `docker-compose up --build` 🚀
