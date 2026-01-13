# Railway Configuration for ML DevOps App

## Environment Variables

Add these to Railway dashboard for production:

```
FLASK_ENV=production
PORT=5000
```

## Deployment Instructions

1. Go to https://railway.app
2. Click "New Project" → "Deploy from GitHub repo"
3. Select `ml-devops-app` repository
4. Railway auto-detects Python and deploys
5. Get your backend URL from Railway dashboard

## Connection String

After deployment, your backend URL will be like:
```
https://ml-devops-app-production.up.railway.app
```

Use this URL in Vercel environment variables as `REACT_APP_API_BASE`

## Monitoring

View logs in Railway dashboard:
- Health check: `https://your-url.up.railway.app/health`
- Metrics: `https://your-url.up.railway.app/api/metrics`
