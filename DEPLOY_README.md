# CocoNUT AI - Deployment Files

This project includes everything you need to deploy to Google Cloud!

## 📁 Deployment Files Created:

1. **[Dockerfile](Dockerfile)** - Container configuration for Cloud Run
2. **[.dockerignore](.dockerignore)** - Files to exclude from container
3. **[app.yaml](app.yaml)** - App Engine configuration
4. **[deploy-to-cloud.ps1](deploy-to-cloud.ps1)** - One-click deployment script
5. **[DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md)** - Complete deployment guide
6. **[.github/workflows/deploy.yml](.github/workflows/deploy.yml)** - Auto-deployment with GitHub Actions

---

## 🚀 Quick Deploy (3 Steps)

### Step 1: Install Google Cloud SDK
Download from: https://cloud.google.com/sdk/docs/install

### Step 2: Get Gemini API Key (Free)
Get from: https://makersuite.google.com/app/apikey

### Step 3: Run Deployment Script

#### Option A: Automated (PowerShell):
```powershell
# Edit deploy-to-cloud.ps1 and add your Gemini API key
# Then run:
.\deploy-to-cloud.ps1
```

#### Option B: Manual Commands:
```bash
# Authenticate
gcloud auth login

# Create project
gcloud projects create coconut-ai-project

# Set project
gcloud config set project coconut-ai-project

# Enable APIs
gcloud services enable cloudbuild.googleapis.com run.googleapis.com

# Deploy
gcloud run deploy coconut-ai --source . --region us-central1 --allow-unauthenticated
```

---

## 🌐 Where to Deploy

### ✅ Recommended: Google Cloud Run
- **Free tier**: 2M requests/month
- **Auto-scaling**: 0 to 1000 instances
- **Pay per use**: $0.40 per million requests
- **Best for**: Web apps with variable traffic

### App Engine
- **Free tier**: 28 hours/day
- **Fully managed**
- **Best for**: Always-on apps

### Compute Engine
- **Full VM control**
- **Best for**: Custom requirements

---

## 💰 Cost Estimate

**Free Tier (Cloud Run)**:
- 2 million requests/month: FREE
- 360,000 GB-seconds: FREE
- 180,000 vCPU-seconds: FREE

**After Free Tier**:
- Light usage (1000 users/month): $5-10
- Medium usage (10000 users/month): $20-50
- Heavy usage (100000 users/month): $100-300

---

## 🔐 Security Setup

### 1. Set API Keys Securely

Don't hardcode keys! Use Google Secret Manager:

```bash
# Create secret
echo -n "your_gemini_key" | gcloud secrets create gemini-api-key --data-file=-

# Use in Cloud Run
gcloud run deploy coconut-ai \
  --set-secrets GEMINI_API_KEY=gemini-api-key:latest
```

### 2. Database Options

**Option A: Cloud SQL (Production)**
```bash
gcloud sql instances create coconut-db \
  --database-version=MYSQL_8_0 \
  --region=us-central1
```

**Option B: SQLite (Simple)**
Already configured, works out of the box!

---

## 🧪 Test Before Deploy

```bash
# Test locally with Docker
docker build -t coconut-ai .
docker run -p 8080:8080 -e GEMINI_API_KEY=your_key coconut-ai
```

Open: http://localhost:8080

---

## 📊 Monitoring

After deployment:

```bash
# View logs
gcloud run services logs read coconut-ai

# Monitor in console
https://console.cloud.google.com/run
```

---

## 🔄 Update Deployment

To push updates:

```bash
# Simple update
gcloud run deploy coconut-ai --source . --region us-central1

# Or use the script
.\deploy-to-cloud.ps1
```

---

## 🎯 Custom Domain

Connect your own domain:

1. Go to Cloud Run console
2. Select your service
3. Click "Manage Custom Domains"
4. Follow the wizard

Example: `chat.yoursite.com`

---

## 📱 Share Your Chatbot

After deployment, you'll get a URL like:
```
https://coconut-ai-xxxxx-uc.a.run.app
```

Share this link with anyone! Your AI chatbot is now:
- ✅ Publicly accessible
- ✅ Auto-scaling
- ✅ Secure (HTTPS)
- ✅ Fast (Google's network)

---

## 🆘 Need Help?

See [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md) for:
- Detailed step-by-step instructions
- Troubleshooting guide
- Advanced configurations
- Cost optimization tips

---

## ✅ Deployment Checklist

- [ ] Google Cloud account created
- [ ] Billing enabled (required even for free tier)
- [ ] Cloud SDK installed
- [ ] Gemini API key obtained
- [ ] Edited `deploy-to-cloud.ps1` with your API key
- [ ] Ran deployment script
- [ ] Tested the live URL
- [ ] Shared with friends! 🎉

**Your AI is ready to go global! 🚀🌍**
