# 🚀 Deploy CocoNUT AI to Google Cloud

This guide will help you deploy your CocoNUT AI chatbot to Google Cloud Platform.

## 🎯 Deployment Options

### Option 1: Google Cloud Run (Recommended) ⭐
- **Easiest & Fastest**
- **Pay only for usage**
- **Auto-scaling**
- **Free tier available**

### Option 2: Google App Engine
- Fully managed platform
- Good for long-running apps

### Option 3: Google Compute Engine
- Full VM control
- More complex setup

---

## 🚀 Option 1: Deploy to Cloud Run (Recommended)

### Prerequisites
1. Google Cloud account ([Sign up free](https://cloud.google.com/free))
2. Google Cloud SDK installed

### Step 1: Install Google Cloud SDK

#### Windows:
Download and install from: https://cloud.google.com/sdk/docs/install

#### Verify Installation:
```bash
gcloud --version
```

### Step 2: Initialize Google Cloud

```bash
# Login to your Google account
gcloud auth login

# Create a new project (or use existing)
gcloud projects create coconut-ai-project --name="CocoNUT AI"

# Set the project
gcloud config set project coconut-ai-project

# Enable required APIs
gcloud services enable cloudbuild.googleapis.com
gcloud services enable run.googleapis.com
```

### Step 3: Update app.py for Production

The app needs to use Cloud SQL or remove local database for Cloud deployment.

**Option A: Use Cloud SQL (MySQL)**
```bash
# Create Cloud SQL instance
gcloud sql instances create coconut-db \
    --database-version=MYSQL_8_0 \
    --tier=db-f1-micro \
    --region=us-central1

# Create database
gcloud sql databases create coconut_ai --instance=coconut-db
```

**Option B: Use SQLite (Simpler, but limited)**
Update `config.py` to use SQLite for cloud deployment.

### Step 4: Build and Deploy

```bash
# Navigate to project directory
cd D:\CoconuT-Ai

# Build the container image
gcloud builds submit --tag gcr.io/coconut-ai-project/coconut-ai

# Deploy to Cloud Run
gcloud run deploy coconut-ai \
    --image gcr.io/coconut-ai-project/coconut-ai \
    --platform managed \
    --region us-central1 \
    --allow-unauthenticated \
    --set-env-vars GEMINI_API_KEY=your_api_key_here \
    --memory 2Gi \
    --timeout 300
```

### Step 5: Get Your URL

After deployment, you'll get a URL like:
```
https://coconut-ai-xxxxxx-uc.a.run.app
```

Your chatbot is now live! 🎉

---

## 🚀 Option 2: Deploy to App Engine

### Step 1: Update app.yaml

Edit `app.yaml` and add your Gemini API key:
```yaml
env_variables:
  GEMINI_API_KEY: "your_actual_api_key"
```

### Step 2: Deploy

```bash
# Navigate to project directory
cd D:\CoconuT-Ai

# Deploy to App Engine
gcloud app deploy app.yaml

# View your app
gcloud app browse
```

---

## 🔧 Production Configuration

### 1. Update Database Configuration

For production, modify `config.py`:

```python
import os

# Use environment variables for production
if os.getenv('GAE_ENV', '').startswith('standard'):
    # Production on App Engine
    DB_CONFIG = {
        'unix_socket': '/cloudsql/your-project:region:instance',
        'user': 'root',
        'password': os.getenv('DB_PASSWORD'),
        'database': 'coconut_ai',
    }
else:
    # Local development
    DB_CONFIG = {
        'host': 'localhost',
        'port': 3306,
        'user': 'root',
        'password': '',
        'database': 'coconut_ai',
    }
```

### 2. Set Environment Variables

```bash
# Set Gemini API key
gcloud run services update coconut-ai \
    --set-env-vars GEMINI_API_KEY=your_key_here

# Set database password
gcloud run services update coconut-ai \
    --set-env-vars DB_PASSWORD=your_db_password
```

### 3. Update Port Configuration

In `app.py`, ensure port comes from environment:

```python
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=False, host='0.0.0.0', port=port)
```

---

## 📊 Cost Estimation

### Cloud Run (Recommended)
- **Free Tier**: 2 million requests/month
- **After free tier**: $0.40 per million requests
- **Typical monthly cost**: $5-20 for moderate usage

### App Engine
- **Free Tier**: 28 instance hours/day
- **After free tier**: ~$0.05/hour per instance
- **Typical monthly cost**: $10-50

---

## 🔐 Security Best Practices

### 1. Use Secret Manager

```bash
# Create secret for Gemini API key
echo -n "your_api_key" | gcloud secrets create gemini-api-key --data-file=-

# Grant access to Cloud Run
gcloud secrets add-iam-policy-binding gemini-api-key \
    --member=serviceAccount:your-project@appspot.gserviceaccount.com \
    --role=roles/secretmanager.secretAccessor
```

### 2. Update app.py to use secrets

```python
from google.cloud import secretmanager

def get_secret(secret_id):
    client = secretmanager.SecretManagerServiceClient()
    name = f"projects/your-project/secrets/{secret_id}/versions/latest"
    response = client.access_secret_version(request={"name": name})
    return response.payload.data.decode("UTF-8")

# In your AI initialization
self.gemini_api_key = get_secret('gemini-api-key')
```

### 3. Enable HTTPS Only

```bash
gcloud run services update coconut-ai --no-allow-unauthenticated
```

---

## 🧪 Test Your Deployment

### 1. Health Check

```bash
# Test the endpoint
curl https://your-app-url.run.app/test_db
```

### 2. Load Testing

```bash
# Install Apache Bench
# Test with 100 requests, 10 concurrent
ab -n 100 -c 10 https://your-app-url.run.app/
```

---

## 📝 Quick Deployment Commands

### Complete Deployment Script:

```bash
# 1. Set project
gcloud config set project coconut-ai-project

# 2. Build container
gcloud builds submit --tag gcr.io/coconut-ai-project/coconut-ai

# 3. Deploy
gcloud run deploy coconut-ai \
    --image gcr.io/coconut-ai-project/coconut-ai \
    --platform managed \
    --region us-central1 \
    --allow-unauthenticated \
    --memory 2Gi \
    --set-env-vars GEMINI_API_KEY=your_key \
    --max-instances 5

# 4. Get URL
gcloud run services describe coconut-ai --region us-central1 --format 'value(status.url)'
```

---

## 🔄 Update Deployment

To update your deployed app:

```bash
# Rebuild and deploy
gcloud builds submit --tag gcr.io/coconut-ai-project/coconut-ai
gcloud run deploy coconut-ai --image gcr.io/coconut-ai-project/coconut-ai --region us-central1
```

Or use one command:

```bash
gcloud run deploy coconut-ai --source . --region us-central1
```

---

## 📱 Alternative: Deploy to Heroku (Simpler)

If Google Cloud is too complex:

```bash
# Install Heroku CLI
# Then:
heroku login
heroku create coconut-ai-chatbot
git init
git add .
git commit -m "Initial commit"
git push heroku main
heroku config:set GEMINI_API_KEY=your_key
heroku open
```

---

## 🐛 Troubleshooting

### Build Fails
```bash
# Check build logs
gcloud builds list
gcloud builds log [BUILD_ID]
```

### Deployment Issues
```bash
# View logs
gcloud run services logs read coconut-ai --region us-central1

# Check service status
gcloud run services describe coconut-ai --region us-central1
```

### Memory Issues
```bash
# Increase memory
gcloud run services update coconut-ai --memory 4Gi
```

### Timeout Issues
```bash
# Increase timeout (max 3600 seconds)
gcloud run services update coconut-ai --timeout 600
```

---

## 📚 Resources

- [Google Cloud Free Tier](https://cloud.google.com/free)
- [Cloud Run Documentation](https://cloud.google.com/run/docs)
- [Cloud SDK Install](https://cloud.google.com/sdk/docs/install)
- [Pricing Calculator](https://cloud.google.com/products/calculator)

---

## ✅ Pre-Deployment Checklist

- [ ] Google Cloud account created
- [ ] Billing enabled (even for free tier)
- [ ] Cloud SDK installed and authenticated
- [ ] Gemini API key obtained
- [ ] Database strategy decided (Cloud SQL or SQLite)
- [ ] `requirements.txt` updated
- [ ] `Dockerfile` created
- [ ] Environment variables configured
- [ ] Security settings reviewed

---

## 🎉 Next Steps

After deployment:
1. Test all features on the live URL
2. Set up monitoring in Google Cloud Console
3. Configure custom domain (optional)
4. Set up CI/CD with GitHub Actions (optional)
5. Enable Cloud Monitoring and Logging

Your CocoNUT AI is now accessible to the world! 🌍🤖
