# 🚀 Quick Deployment Script
# Run this in PowerShell after installing Google Cloud SDK

# Configuration
$PROJECT_ID = "coconut-ai-project"
$SERVICE_NAME = "coconut-ai"
$REGION = "us-central1"
$GEMINI_API_KEY = "your_gemini_api_key_here"  # Replace with your actual key

Write-Host "🚀 Starting CocoNUT AI Deployment to Google Cloud Run" -ForegroundColor Cyan
Write-Host "=" * 60

# Step 1: Authenticate
Write-Host "`n📝 Step 1: Authenticating with Google Cloud..." -ForegroundColor Yellow
gcloud auth login

# Step 2: Create/Set Project
Write-Host "`n📝 Step 2: Setting up project..." -ForegroundColor Yellow
gcloud projects create $PROJECT_ID --name="CocoNUT AI" 2>$null
gcloud config set project $PROJECT_ID

# Step 3: Enable APIs
Write-Host "`n📝 Step 3: Enabling required APIs..." -ForegroundColor Yellow
gcloud services enable cloudbuild.googleapis.com
gcloud services enable run.googleapis.com

# Step 4: Build Container
Write-Host "`n📝 Step 4: Building container image..." -ForegroundColor Yellow
gcloud builds submit --tag gcr.io/$PROJECT_ID/$SERVICE_NAME

# Step 5: Deploy to Cloud Run
Write-Host "`n📝 Step 5: Deploying to Cloud Run..." -ForegroundColor Yellow
gcloud run deploy $SERVICE_NAME `
    --image gcr.io/$PROJECT_ID/$SERVICE_NAME `
    --platform managed `
    --region $REGION `
    --allow-unauthenticated `
    --memory 2Gi `
    --timeout 300 `
    --set-env-vars GEMINI_API_KEY=$GEMINI_API_KEY

# Step 6: Get URL
Write-Host "`n📝 Step 6: Getting service URL..." -ForegroundColor Yellow
$SERVICE_URL = gcloud run services describe $SERVICE_NAME --region $REGION --format 'value(status.url)'

Write-Host "`n" + "=" * 60
Write-Host "✅ Deployment Complete!" -ForegroundColor Green
Write-Host "=" * 60
Write-Host "`n🌐 Your CocoNUT AI is live at:" -ForegroundColor Cyan
Write-Host "   $SERVICE_URL" -ForegroundColor White
Write-Host "`n📊 View in Cloud Console:" -ForegroundColor Cyan
Write-Host "   https://console.cloud.google.com/run?project=$PROJECT_ID" -ForegroundColor White
Write-Host "`n💡 To update your deployment, run this script again!" -ForegroundColor Yellow
Write-Host ""
