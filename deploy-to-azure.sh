#!/bin/bash

#############################################################
# Campus Pulse - Azure Deployment Script
#
# This script automates the deployment of Campus Pulse
# to Azure App Service using Container Registry
#
# Prerequisites:
# - Azure CLI installed and configured (az login)
# - Docker installed
#############################################################

set -e  # Exit on error

# Color codes for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Print colored output
print_info() {
    echo -e "${BLUE}ℹ ${NC}$1"
}

print_success() {
    echo -e "${GREEN}✓${NC} $1"
}

print_error() {
    echo -e "${RED}✗${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}⚠${NC} $1"
}

# Banner
echo ""
echo "╔════════════════════════════════════════════════════════╗"
echo "║                                                        ║"
echo "║         Campus Pulse - Azure Deployment               ║"
echo "║         University of Florida                          ║"
echo "║                                                        ║"
echo "╚════════════════════════════════════════════════════════╝"
echo ""

# Check if Azure CLI is installed
if ! command -v az &> /dev/null; then
    print_error "Azure CLI is not installed. Please install it first:"
    echo "  https://docs.microsoft.com/en-us/cli/azure/install-azure-cli"
    exit 1
fi

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    print_error "Docker is not installed. Please install it first:"
    echo "  https://docs.docker.com/get-docker/"
    exit 1
fi

# Check if logged in to Azure
print_info "Checking Azure login status..."
if ! az account show &> /dev/null; then
    print_error "Not logged in to Azure. Please run: az login"
    exit 1
fi

print_success "Azure CLI authenticated"

# Get current subscription
SUBSCRIPTION_NAME=$(az account show --query name -o tsv)
SUBSCRIPTION_ID=$(az account show --query id -o tsv)
print_info "Using subscription: ${BLUE}$SUBSCRIPTION_NAME${NC}"

# Configuration
print_info "Configuring deployment parameters..."
echo ""

# Prompt for configuration or use defaults
read -p "Resource Group name (default: campuspulse-rg): " RESOURCE_GROUP
RESOURCE_GROUP=${RESOURCE_GROUP:-campuspulse-rg}

read -p "Location (default: eastus): " LOCATION
LOCATION=${LOCATION:-eastus}

read -p "Container Registry name (default: campuspulseacr): " ACR_NAME
ACR_NAME=${ACR_NAME:-campuspulseacr}

read -p "App Service name (default: campuspulse-app): " APP_NAME
APP_NAME=${APP_NAME:-campuspulse-app}

read -p "App Service Plan name (default: campuspulse-plan): " APP_SERVICE_PLAN
APP_SERVICE_PLAN=${APP_SERVICE_PLAN:-campuspulse-plan}

read -p "Pricing tier B1/S1/P1V2 (default: B1): " PRICING_TIER
PRICING_TIER=${PRICING_TIER:-B1}

echo ""
print_info "Configuration Summary:"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "  Resource Group:      $RESOURCE_GROUP"
echo "  Location:            $LOCATION"
echo "  Container Registry:  $ACR_NAME"
echo "  App Name:            $APP_NAME"
echo "  App Service Plan:    $APP_SERVICE_PLAN"
echo "  Pricing Tier:        $PRICING_TIER"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

read -p "Continue with deployment? (y/n): " -n 1 -r
echo ""
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    print_warning "Deployment cancelled"
    exit 0
fi

echo ""
print_info "Starting deployment..."
echo ""

# Step 1: Create Resource Group
print_info "Step 1/7: Creating resource group..."
if az group show --name $RESOURCE_GROUP &> /dev/null; then
    print_warning "Resource group already exists"
else
    az group create \
      --name $RESOURCE_GROUP \
      --location $LOCATION \
      --output none
    print_success "Resource group created"
fi

# Step 2: Create Azure Container Registry
print_info "Step 2/7: Creating Azure Container Registry..."
if az acr show --name $ACR_NAME &> /dev/null; then
    print_warning "Container registry already exists"
else
    az acr create \
      --resource-group $RESOURCE_GROUP \
      --name $ACR_NAME \
      --sku Basic \
      --admin-enabled true \
      --output none
    print_success "Container registry created"
fi

# Step 3: Build and Push Docker Image
print_info "Step 3/7: Building and pushing Docker image..."

# Login to ACR
az acr login --name $ACR_NAME

# Get ACR login server
ACR_LOGIN_SERVER=$(az acr show --name $ACR_NAME --query loginServer --output tsv)
print_info "Registry: $ACR_LOGIN_SERVER"

# Build image
print_info "Building Docker image (this may take a few minutes)..."
docker build -t $ACR_LOGIN_SERVER/campuspulse:latest -f Dockerfile .

# Push image
print_info "Pushing image to Azure Container Registry..."
docker push $ACR_LOGIN_SERVER/campuspulse:latest

print_success "Docker image built and pushed"

# Step 4: Create App Service Plan
print_info "Step 4/7: Creating App Service Plan..."
if az appservice plan show --name $APP_SERVICE_PLAN --resource-group $RESOURCE_GROUP &> /dev/null; then
    print_warning "App Service Plan already exists"
else
    az appservice plan create \
      --name $APP_SERVICE_PLAN \
      --resource-group $RESOURCE_GROUP \
      --is-linux \
      --sku $PRICING_TIER \
      --output none
    print_success "App Service Plan created"
fi

# Step 5: Create Web App
print_info "Step 5/7: Creating Web App..."
if az webapp show --name $APP_NAME --resource-group $RESOURCE_GROUP &> /dev/null; then
    print_warning "Web App already exists, updating configuration..."
else
    az webapp create \
      --resource-group $RESOURCE_GROUP \
      --plan $APP_SERVICE_PLAN \
      --name $APP_NAME \
      --deployment-container-image-name $ACR_LOGIN_SERVER/campuspulse:latest \
      --output none
    print_success "Web App created"
fi

# Step 6: Configure Web App
print_info "Step 6/7: Configuring Web App..."

# Get ACR credentials
ACR_USERNAME=$(az acr credential show --name $ACR_NAME --query username --output tsv)
ACR_PASSWORD=$(az acr credential show --name $ACR_NAME --query passwords[0].value --output tsv)

# Configure container settings
az webapp config container set \
  --name $APP_NAME \
  --resource-group $RESOURCE_GROUP \
  --docker-custom-image-name $ACR_LOGIN_SERVER/campuspulse:latest \
  --docker-registry-server-url https://$ACR_LOGIN_SERVER \
  --docker-registry-server-user $ACR_USERNAME \
  --docker-registry-server-password $ACR_PASSWORD \
  --output none

# Configure port
az webapp config appsettings set \
  --resource-group $RESOURCE_GROUP \
  --name $APP_NAME \
  --settings WEBSITES_PORT=8501 \
  --output none

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
    STREAMLIT_SERVER_ENABLE_XSRF_PROTECTION=true \
  --output none

# Enable continuous deployment
az webapp deployment container config \
  --name $APP_NAME \
  --resource-group $RESOURCE_GROUP \
  --enable-cd true \
  --output none

# Enable logging
az webapp log config \
  --name $APP_NAME \
  --resource-group $RESOURCE_GROUP \
  --docker-container-logging filesystem \
  --output none

print_success "Web App configured"

# Step 7: Restart and verify
print_info "Step 7/7: Restarting Web App..."
az webapp restart \
  --name $APP_NAME \
  --resource-group $RESOURCE_GROUP \
  --output none

print_success "Web App restarted"

# Get the URL
APP_URL="https://${APP_NAME}.azurewebsites.net"

echo ""
echo "╔════════════════════════════════════════════════════════╗"
echo "║                                                        ║"
echo "║         🎉 Deployment Successful! 🎉                   ║"
echo "║                                                        ║"
echo "╚════════════════════════════════════════════════════════╝"
echo ""
print_success "Campus Pulse is deployed!"
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "  🌐 Application URL:"
echo "     ${GREEN}$APP_URL${NC}"
echo ""
echo "  📊 Azure Portal:"
echo "     https://portal.azure.com/#@/resource/subscriptions/$SUBSCRIPTION_ID/resourceGroups/$RESOURCE_GROUP/providers/Microsoft.Web/sites/$APP_NAME"
echo ""
echo "  📝 View Logs:"
echo "     ${BLUE}az webapp log tail --name $APP_NAME --resource-group $RESOURCE_GROUP${NC}"
echo ""
echo "  🔄 Update Deployment:"
echo "     ${BLUE}docker build -t $ACR_LOGIN_SERVER/campuspulse:latest .${NC}"
echo "     ${BLUE}docker push $ACR_LOGIN_SERVER/campuspulse:latest${NC}"
echo "     ${BLUE}az webapp restart --name $APP_NAME --resource-group $RESOURCE_GROUP${NC}"
echo ""
echo "  🗑️  Delete Resources:"
echo "     ${BLUE}az group delete --name $RESOURCE_GROUP --yes${NC}"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

print_info "The application may take 2-3 minutes to start up..."
print_info "You can monitor the startup with: ${BLUE}az webapp log tail --name $APP_NAME --resource-group $RESOURCE_GROUP${NC}"
echo ""

# Optionally open browser
read -p "Open application in browser? (y/n): " -n 1 -r
echo ""
if [[ $REPLY =~ ^[Yy]$ ]]; then
    if [[ "$OSTYPE" == "darwin"* ]]; then
        open $APP_URL
    elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
        xdg-open $APP_URL 2>/dev/null || echo "Please open: $APP_URL"
    elif [[ "$OSTYPE" == "msys" ]] || [[ "$OSTYPE" == "win32" ]]; then
        start $APP_URL
    else
        echo "Please open: $APP_URL"
    fi
fi

echo ""
print_success "Deployment complete!"
echo ""
