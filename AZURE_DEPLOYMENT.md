# ☁️ Campus Pulse - Azure Deployment Guide

This guide provides step-by-step instructions for deploying Campus Pulse to Microsoft Azure using containerization.

## 📋 Prerequisites

- **Azure Account** - [Create free account](https://azure.microsoft.com/free/) (includes $200 credit)
- **Azure CLI** - [Install Azure CLI](https://docs.microsoft.com/en-us/cli/azure/install-azure-cli)
- **Docker** - Already installed (used for building the image)
- **Git** - For repository management

## 🎯 Deployment Options

Campus Pulse can be deployed to Azure in several ways:

| Option | Best For | Complexity | Cost (Estimate) |
|--------|----------|------------|-----------------|
| **Azure App Service** | Quick deployment, managed platform | ⭐ Easy | $13-50/month |
| **Azure Container Instances** | Simple containerized apps | ⭐⭐ Moderate | $10-30/month |
| **Azure Kubernetes Service** | Enterprise scale, high availability | ⭐⭐⭐ Advanced | $70+/month |
| **Azure Container Apps** | Modern serverless containers | ⭐⭐ Moderate | $15-40/month |

**Recommended: Azure App Service (Web App for Containers)** - Best balance of simplicity and features.

---

## 🚀 Method 1: Azure App Service (Recommended)

Azure App Service is a fully managed platform for building and hosting web applications.

### Step 1: Install Azure CLI and Login

```bash
# Install Azure CLI (if not already installed)
# macOS: brew install azure-cli
# Windows: Download from https://aka.ms/installazurecliwindows
# Linux: curl -sL https://aka.ms/InstallAzureCLIDeb | sudo bash

# Login to Azure
az login

# Set your subscription (if you have multiple)
az account list --output table
az account set --subscription "Your Subscription Name"
```

### Step 2: Create Azure Resources

```bash
# Set variables (customize these)
RESOURCE_GROUP="campuspulse-rg"
LOCATION="eastus"  # or: westus2, centralus, westeurope, etc.
ACR_NAME="campuspulseacr"  # Must be globally unique, lowercase, no hyphens
APP_NAME="campuspulse-app"  # Must be globally unique
APP_SERVICE_PLAN="campuspulse-plan"

# Create resource group
az group create \
  --name $RESOURCE_GROUP \
  --location $LOCATION

# Create Azure Container Registry (ACR)
az acr create \
  --resource-group $RESOURCE_GROUP \
  --name $ACR_NAME \
  --sku Basic \
  --admin-enabled true

# Create App Service Plan (Linux, B1 tier)
az appservice plan create \
  --name $APP_SERVICE_PLAN \
  --resource-group $RESOURCE_GROUP \
  --is-linux \
  --sku B1  # Basic tier; upgrade to S1 for production
```

### Step 3: Build and Push Docker Image to ACR

```bash
# Navigate to your project directory
cd /path/to/campuspulse

# Login to Azure Container Registry
az acr login --name $ACR_NAME

# Get ACR login server
ACR_LOGIN_SERVER=$(az acr show --name $ACR_NAME --query loginServer --output tsv)
echo "ACR Login Server: $ACR_LOGIN_SERVER"

# Build and tag the Docker image
docker build -t $ACR_LOGIN_SERVER/campuspulse:latest .

# Push the image to ACR
docker push $ACR_LOGIN_SERVER/campuspulse:latest

# Verify the image was pushed
az acr repository list --name $ACR_NAME --output table
```

### Step 4: Create and Deploy Web App

```bash
# Get ACR credentials
ACR_USERNAME=$(az acr credential show --name $ACR_NAME --query username --output tsv)
ACR_PASSWORD=$(az acr credential show --name $ACR_NAME --query passwords[0].value --output tsv)

# Create Web App from container
az webapp create \
  --resource-group $RESOURCE_GROUP \
  --plan $APP_SERVICE_PLAN \
  --name $APP_NAME \
  --deployment-container-image-name $ACR_LOGIN_SERVER/campuspulse:latest

# Configure ACR credentials
az webapp config container set \
  --name $APP_NAME \
  --resource-group $RESOURCE_GROUP \
  --docker-custom-image-name $ACR_LOGIN_SERVER/campuspulse:latest \
  --docker-registry-server-url https://$ACR_LOGIN_SERVER \
  --docker-registry-server-user $ACR_USERNAME \
  --docker-registry-server-password $ACR_PASSWORD

# Configure container port
az webapp config appsettings set \
  --resource-group $RESOURCE_GROUP \
  --name $APP_NAME \
  --settings WEBSITES_PORT=8501

# Enable continuous deployment (auto-update on new image push)
az webapp deployment container config \
  --name $APP_NAME \
  --resource-group $RESOURCE_GROUP \
  --enable-cd true

# Configure Streamlit environment variables
az webapp config appsettings set \
  --resource-group $RESOURCE_GROUP \
  --name $APP_NAME \
  --settings \
    STREAMLIT_SERVER_PORT=8501 \
    STREAMLIT_SERVER_ADDRESS=0.0.0.0 \
    STREAMLIT_SERVER_HEADLESS=true \
    STREAMLIT_BROWSER_GATHER_USAGE_STATS=false \
    STREAMLIT_SERVER_ENABLE_CORS=false \
    STREAMLIT_SERVER_ENABLE_XSRF_PROTECTION=true
```

### Step 5: Access Your Application

```bash
# Get the URL
APP_URL="https://${APP_NAME}.azurewebsites.net"
echo "Your app is available at: $APP_URL"

# Open in browser
open $APP_URL  # macOS
# xdg-open $APP_URL  # Linux
# start $APP_URL  # Windows

# View logs
az webapp log tail --name $APP_NAME --resource-group $RESOURCE_GROUP
```

### Step 6: Configure Custom Domain (Optional)

```bash
# Add custom domain
az webapp config hostname add \
  --webapp-name $APP_NAME \
  --resource-group $RESOURCE_GROUP \
  --hostname "campuspulse.yourdomain.com"

# Enable HTTPS (managed certificate)
az webapp config ssl create \
  --resource-group $RESOURCE_GROUP \
  --name $APP_NAME \
  --hostname "campuspulse.yourdomain.com"

# Enforce HTTPS only
az webapp update \
  --resource-group $RESOURCE_GROUP \
  --name $APP_NAME \
  --https-only true
```

---

## 🔄 Updating Your Deployment

### Option A: Manual Update

```bash
# Rebuild and push new image
docker build -t $ACR_LOGIN_SERVER/campuspulse:latest .
docker push $ACR_LOGIN_SERVER/campuspulse:latest

# Restart the web app (will pull latest image if CD is enabled)
az webapp restart --name $APP_NAME --resource-group $RESOURCE_GROUP
```

### Option B: Automated CI/CD with GitHub Actions

Create `.github/workflows/azure-deploy.yml`:

```yaml
name: Deploy to Azure App Service

on:
  push:
    branches: [ main ]
  workflow_dispatch:

env:
  ACR_NAME: campuspulseacr
  APP_NAME: campuspulse-app
  RESOURCE_GROUP: campuspulse-rg

jobs:
  build-and-deploy:
    runs-on: ubuntu-latest

    steps:
    - name: Checkout code
      uses: actions/checkout@v3

    - name: Login to Azure
      uses: azure/login@v1
      with:
        creds: ${{ secrets.AZURE_CREDENTIALS }}

    - name: Login to ACR
      run: az acr login --name ${{ env.ACR_NAME }}

    - name: Get ACR login server
      id: acr
      run: echo "login_server=$(az acr show --name ${{ env.ACR_NAME }} --query loginServer -o tsv)" >> $GITHUB_OUTPUT

    - name: Build and push Docker image
      run: |
        docker build -t ${{ steps.acr.outputs.login_server }}/campuspulse:${{ github.sha }} .
        docker build -t ${{ steps.acr.outputs.login_server }}/campuspulse:latest .
        docker push ${{ steps.acr.outputs.login_server }}/campuspulse:${{ github.sha }}
        docker push ${{ steps.acr.outputs.login_server }}/campuspulse:latest

    - name: Deploy to Azure Web App
      uses: azure/webapps-deploy@v2
      with:
        app-name: ${{ env.APP_NAME }}
        images: ${{ steps.acr.outputs.login_server }}/campuspulse:${{ github.sha }}
```

**Setup GitHub Secrets:**

```bash
# Create service principal
az ad sp create-for-rbac \
  --name "campuspulse-github-actions" \
  --role contributor \
  --scopes /subscriptions/{subscription-id}/resourceGroups/$RESOURCE_GROUP \
  --sdk-auth

# Copy the JSON output and add it as GitHub secret: AZURE_CREDENTIALS
# Go to: GitHub repo > Settings > Secrets and variables > Actions > New repository secret
```

---

## 🗄️ Method 2: Azure Container Instances (Simple Alternative)

For simpler deployments without App Service features:

```bash
# Set variables
RESOURCE_GROUP="campuspulse-rg"
LOCATION="eastus"
ACI_NAME="campuspulse-aci"
ACR_NAME="campuspulseacr"

# Create resource group
az group create --name $RESOURCE_GROUP --location $LOCATION

# Create Azure Container Registry
az acr create \
  --resource-group $RESOURCE_GROUP \
  --name $ACR_NAME \
  --sku Basic

# Build image in ACR (no local Docker needed!)
az acr build \
  --registry $ACR_NAME \
  --image campuspulse:latest \
  --file Dockerfile \
  .

# Get ACR credentials
ACR_LOGIN_SERVER=$(az acr show --name $ACR_NAME --query loginServer -o tsv)
ACR_USERNAME=$(az acr credential show --name $ACR_NAME --query username -o tsv)
ACR_PASSWORD=$(az acr credential show --name $ACR_NAME --query passwords[0].value -o tsv)

# Create container instance
az container create \
  --resource-group $RESOURCE_GROUP \
  --name $ACI_NAME \
  --image $ACR_LOGIN_SERVER/campuspulse:latest \
  --registry-login-server $ACR_LOGIN_SERVER \
  --registry-username $ACR_USERNAME \
  --registry-password $ACR_PASSWORD \
  --dns-name-label campuspulse-demo \
  --ports 8501 \
  --cpu 2 \
  --memory 4 \
  --environment-variables \
    STREAMLIT_SERVER_PORT=8501 \
    STREAMLIT_SERVER_ADDRESS=0.0.0.0 \
    STREAMLIT_SERVER_HEADLESS=true

# Get the public URL
az container show \
  --resource-group $RESOURCE_GROUP \
  --name $ACI_NAME \
  --query ipAddress.fqdn \
  --output tsv

# Access at: http://<fqdn>:8501
```

**Note:** ACI doesn't support HTTPS by default. Use Azure Application Gateway or Front Door for SSL.

---

## 💾 Database Persistence

Campus Pulse uses SQLite databases that need to persist across container restarts.

### For App Service:

```bash
# Enable Azure Storage mounting (for persistent SQLite files)
# Create storage account
STORAGE_ACCOUNT="campuspulsestorage"

az storage account create \
  --name $STORAGE_ACCOUNT \
  --resource-group $RESOURCE_GROUP \
  --location $LOCATION \
  --sku Standard_LRS

# Create file share
az storage share create \
  --name campuspulse-data \
  --account-name $STORAGE_ACCOUNT

# Get storage key
STORAGE_KEY=$(az storage account keys list \
  --resource-group $RESOURCE_GROUP \
  --account-name $STORAGE_ACCOUNT \
  --query '[0].value' -o tsv)

# Mount storage to web app
az webapp config storage-account add \
  --resource-group $RESOURCE_GROUP \
  --name $APP_NAME \
  --custom-id CampusPulseData \
  --storage-type AzureFiles \
  --share-name campuspulse-data \
  --account-name $STORAGE_ACCOUNT \
  --access-key $STORAGE_KEY \
  --mount-path /app/streamlit_app
```

### For Container Instances:

```bash
# Add Azure Files mount to container
az container create \
  --resource-group $RESOURCE_GROUP \
  --name $ACI_NAME \
  --image $ACR_LOGIN_SERVER/campuspulse:latest \
  --azure-file-volume-account-name $STORAGE_ACCOUNT \
  --azure-file-volume-account-key $STORAGE_KEY \
  --azure-file-volume-share-name campuspulse-data \
  --azure-file-volume-mount-path /app/streamlit_app \
  # ... other parameters
```

---

## 📊 Monitoring and Diagnostics

### Enable Application Insights

```bash
# Create Application Insights
az monitor app-insights component create \
  --app campuspulse-insights \
  --location $LOCATION \
  --resource-group $RESOURCE_GROUP

# Get instrumentation key
INSTRUMENTATION_KEY=$(az monitor app-insights component show \
  --app campuspulse-insights \
  --resource-group $RESOURCE_GROUP \
  --query instrumentationKey -o tsv)

# Add to web app settings
az webapp config appsettings set \
  --resource-group $RESOURCE_GROUP \
  --name $APP_NAME \
  --settings APPINSIGHTS_INSTRUMENTATIONKEY=$INSTRUMENTATION_KEY
```

### View Logs

```bash
# Enable logging
az webapp log config \
  --name $APP_NAME \
  --resource-group $RESOURCE_GROUP \
  --docker-container-logging filesystem

# Stream logs
az webapp log tail \
  --name $APP_NAME \
  --resource-group $RESOURCE_GROUP

# Download logs
az webapp log download \
  --name $APP_NAME \
  --resource-group $RESOURCE_GROUP \
  --log-file logs.zip
```

### Monitor Performance

```bash
# View metrics
az monitor metrics list \
  --resource /subscriptions/{subscription-id}/resourceGroups/$RESOURCE_GROUP/providers/Microsoft.Web/sites/$APP_NAME \
  --metric "CpuPercentage" "MemoryPercentage" "HttpResponseTime"

# View in Azure Portal:
# https://portal.azure.com > Resource Groups > campuspulse-rg > campuspulse-app > Monitoring
```

---

## 💰 Cost Optimization

### App Service Pricing Tiers

| Tier | vCPU | RAM | Price/Month | Best For |
|------|------|-----|-------------|----------|
| **B1** (Basic) | 1 | 1.75GB | ~$13 | Development/Testing |
| **S1** (Standard) | 1 | 1.75GB | ~$70 | Production (recommended) |
| **P1V2** (Premium) | 1 | 3.5GB | ~$96 | High performance |

```bash
# Scale up to Standard tier (production)
az appservice plan update \
  --name $APP_SERVICE_PLAN \
  --resource-group $RESOURCE_GROUP \
  --sku S1

# Scale down to Free tier (testing only)
az appservice plan update \
  --name $APP_SERVICE_PLAN \
  --resource-group $RESOURCE_GROUP \
  --sku F1
```

### Auto-Scaling (S1+ tier)

```bash
# Enable autoscale
az monitor autoscale create \
  --resource-group $RESOURCE_GROUP \
  --resource $APP_SERVICE_PLAN \
  --resource-type Microsoft.Web/serverfarms \
  --name autoscale-campuspulse \
  --min-count 1 \
  --max-count 3 \
  --count 1

# Scale on CPU > 70%
az monitor autoscale rule create \
  --resource-group $RESOURCE_GROUP \
  --autoscale-name autoscale-campuspulse \
  --condition "Percentage CPU > 70 avg 5m" \
  --scale out 1
```

---

## 🔒 Security Best Practices

### 1. Use Managed Identities

```bash
# Enable system-assigned managed identity
az webapp identity assign \
  --name $APP_NAME \
  --resource-group $RESOURCE_GROUP

# Grant ACR pull permissions
PRINCIPAL_ID=$(az webapp identity show \
  --name $APP_NAME \
  --resource-group $RESOURCE_GROUP \
  --query principalId -o tsv)

az role assignment create \
  --assignee $PRINCIPAL_ID \
  --role AcrPull \
  --scope $(az acr show --name $ACR_NAME --query id -o tsv)
```

### 2. Disable Admin Credentials

```bash
# Use managed identity instead of admin credentials
az acr update --name $ACR_NAME --admin-enabled false
```

### 3. Enable HTTPS and Security Headers

```bash
# Enforce HTTPS only
az webapp update \
  --resource-group $RESOURCE_GROUP \
  --name $APP_NAME \
  --https-only true

# Set minimum TLS version
az webapp config set \
  --resource-group $RESOURCE_GROUP \
  --name $APP_NAME \
  --min-tls-version 1.2
```

### 4. Network Security

```bash
# Restrict access to specific IPs (optional)
az webapp config access-restriction add \
  --resource-group $RESOURCE_GROUP \
  --name $APP_NAME \
  --rule-name "Allow-UF-Campus" \
  --action Allow \
  --ip-address 128.227.0.0/16 \
  --priority 100

# Enable VNet integration for private resources
# (Requires Standard tier or higher)
```

---

## 🐛 Troubleshooting

### Container Won't Start

```bash
# Check container logs
az webapp log tail --name $APP_NAME --resource-group $RESOURCE_GROUP

# Check deployment status
az webapp deployment list --name $APP_NAME --resource-group $RESOURCE_GROUP

# Restart the app
az webapp restart --name $APP_NAME --resource-group $RESOURCE_GROUP
```

### Application Not Responding

```bash
# Check if container is running
az webapp show --name $APP_NAME --resource-group $RESOURCE_GROUP --query state

# Test health endpoint
curl https://$APP_NAME.azurewebsites.net/_stcore/health

# Verify port configuration
az webapp config appsettings list \
  --name $APP_NAME \
  --resource-group $RESOURCE_GROUP \
  --query "[?name=='WEBSITES_PORT'].value"
```

### Image Pull Errors

```bash
# Verify ACR credentials
az acr credential show --name $ACR_NAME

# Test login manually
docker login $ACR_LOGIN_SERVER -u $ACR_USERNAME -p $ACR_PASSWORD

# Check if image exists
az acr repository show --name $ACR_NAME --image campuspulse:latest
```

### Performance Issues

```bash
# Increase instance size
az appservice plan update \
  --name $APP_SERVICE_PLAN \
  --resource-group $RESOURCE_GROUP \
  --sku S2  # 2 vCPU, 3.5GB RAM

# Check resource usage
az webapp show \
  --name $APP_NAME \
  --resource-group $RESOURCE_GROUP \
  --query "siteConfig.numberOfWorkers"
```

---

## 🧹 Cleanup Resources

When you're done testing:

```bash
# Delete entire resource group (deletes all resources)
az group delete --name $RESOURCE_GROUP --yes --no-wait

# Or delete individual resources
az webapp delete --name $APP_NAME --resource-group $RESOURCE_GROUP
az acr delete --name $ACR_NAME --resource-group $RESOURCE_GROUP
az appservice plan delete --name $APP_SERVICE_PLAN --resource-group $RESOURCE_GROUP
```

---

## 📚 Additional Resources

- [Azure App Service Documentation](https://docs.microsoft.com/en-us/azure/app-service/)
- [Azure Container Registry Documentation](https://docs.microsoft.com/en-us/azure/container-registry/)
- [Deploy a custom container to App Service](https://docs.microsoft.com/en-us/azure/app-service/quickstart-custom-container)
- [Streamlit deployment guide](https://docs.streamlit.io/knowledge-base/tutorials/deploy)
- [Azure Pricing Calculator](https://azure.microsoft.com/en-us/pricing/calculator/)

---

## 🎓 For Your Professor

This Azure deployment demonstrates:

1. **Cloud Infrastructure**: Containerized deployment on Azure PaaS
2. **DevOps Practices**: CI/CD with GitHub Actions
3. **Scalability**: Auto-scaling based on demand
4. **Security**: Managed identities, HTTPS, network restrictions
5. **Monitoring**: Application Insights, logging, metrics
6. **Cost Optimization**: Right-sized resources for academic project

**Estimated Monthly Cost for Academic Use:**
- Resource Group: Free
- Container Registry (Basic): ~$5/month
- App Service (B1 tier): ~$13/month
- Storage Account: ~$2/month
- **Total: ~$20/month** (or use free Azure credits)

---

**Built with ❤️ for University of Florida • Campus Pulse**
