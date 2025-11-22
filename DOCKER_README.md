# 🐳 Campus Pulse - Docker Deployment Guide

This guide explains how to run Campus Pulse using Docker and Docker Compose for easy, consistent deployment across any environment.

## 📋 Prerequisites

- **Docker** (version 20.10 or higher) - [Install Docker](https://docs.docker.com/get-docker/)
- **Docker Compose** (version 2.0 or higher) - Usually included with Docker Desktop
- At least **4GB RAM** available for the container
- At least **2GB disk space** for the image

## 🚀 Quick Start

### Option 1: Using Docker Compose (Recommended)

The easiest way to run Campus Pulse:

```bash
# Build and start the application
docker-compose up -d

# View logs
docker-compose logs -f

# Stop the application
docker-compose down
```

Access the application at: **http://localhost:8501**

### Option 2: Using Docker CLI

Build and run manually with Docker commands:

```bash
# Build the Docker image
docker build -t campuspulse:latest .

# Run the container
docker run -d \
  --name campuspulse-app \
  -p 8501:8501 \
  --restart unless-stopped \
  campuspulse:latest

# View logs
docker logs -f campuspulse-app

# Stop the container
docker stop campuspulse-app
docker rm campuspulse-app
```

## 🔧 Configuration Options

### Environment Variables

You can customize the application behavior with environment variables:

```bash
# In docker-compose.yml, add to 'environment:' section:
environment:
  - STREAMLIT_SERVER_PORT=8501
  - STREAMLIT_SERVER_ADDRESS=0.0.0.0
  - STREAMLIT_THEME_BASE=light          # light or dark
  - STREAMLIT_BROWSER_GATHER_USAGE_STATS=false
```

### Port Mapping

To run on a different port (e.g., port 80):

```bash
# In docker-compose.yml:
ports:
  - "80:8501"

# Or with Docker CLI:
docker run -p 80:8501 campuspulse:latest
```

## 🏗️ Development Mode

For active development with live code reloading:

```bash
# Uncomment the volumes section in docker-compose.yml
volumes:
  - ./streamlit_app:/app/streamlit_app:ro

# Run with docker-compose
docker-compose up

# Code changes will automatically reload the app
```

## 🎯 GPU Support (Optional)

If you have an NVIDIA GPU and want to accelerate PyTorch models:

### Prerequisites
- Install [NVIDIA Docker runtime](https://github.com/NVIDIA/nvidia-docker)
- NVIDIA GPU with CUDA support

### Enable GPU

In `docker-compose.yml`, uncomment the GPU sections:

```yaml
environment:
  - NVIDIA_VISIBLE_DEVICES=all

deploy:
  resources:
    reservations:
      devices:
        - driver: nvidia
          count: 1
          capabilities: [gpu]
```

## 📊 Container Management

### Useful Commands

```bash
# View running containers
docker ps

# View all containers (including stopped)
docker ps -a

# View container resource usage
docker stats campuspulse-app

# Execute commands inside container
docker exec -it campuspulse-app /bin/bash

# View application logs
docker logs -f campuspulse-app

# Restart the application
docker-compose restart

# Rebuild after code changes
docker-compose up --build -d
```

### Health Checks

The container includes automatic health checks:

```bash
# Check health status
docker inspect --format='{{.State.Health.Status}}' campuspulse-app

# View health check logs
docker inspect --format='{{range .State.Health.Log}}{{.Output}}{{end}}' campuspulse-app
```

## 🔒 Security Best Practices

The Docker setup includes several security features:

- ✅ **Non-root user**: Container runs as user `streamlit` (UID 1000)
- ✅ **Multi-stage build**: Smaller attack surface, reduced image size
- ✅ **No unnecessary packages**: Minimal runtime dependencies
- ✅ **Health checks**: Automatic container restart on failure
- ✅ **Read-only volumes**: Development mounts are read-only

## 🚢 Production Deployment

### Basic Production Setup

```bash
# Remove development volumes from docker-compose.yml
# Comment out or remove the 'volumes:' section

# Build for production
docker-compose up -d --build

# Verify it's running
curl http://localhost:8501/_stcore/health
```

### Behind a Reverse Proxy (Nginx/Traefik)

Example Nginx configuration:

```nginx
server {
    listen 80;
    server_name campuspulse.yourdomain.com;

    location / {
        proxy_pass http://localhost:8501;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

### Using Docker Hub

```bash
# Tag the image
docker tag campuspulse:latest yourusername/campuspulse:latest

# Push to Docker Hub
docker push yourusername/campuspulse:latest

# Pull and run on any machine
docker pull yourusername/campuspulse:latest
docker run -d -p 8501:8501 yourusername/campuspulse:latest
```

## 🐛 Troubleshooting

### Container won't start

```bash
# Check logs for errors
docker-compose logs campuspulse

# Check if port is already in use
lsof -i :8501
# Or on Windows: netstat -ano | findstr :8501

# Remove and rebuild
docker-compose down
docker-compose up --build
```

### Out of memory errors

```bash
# Increase Docker memory limit (Docker Desktop settings)
# Or limit container memory in docker-compose.yml:

services:
  campuspulse:
    deploy:
      resources:
        limits:
          memory: 4G
```

### Slow PyTorch model loading

```bash
# Add a volume for model caching
volumes:
  - model-cache:/root/.cache/huggingface

volumes:
  model-cache:
    driver: local
```

### Permission denied errors

```bash
# Fix file permissions
sudo chown -R $USER:$USER streamlit_app/

# Rebuild the container
docker-compose up --build -d
```

## 📏 Image Size Optimization

Current image size: ~2-3GB (includes PyTorch and Transformers)

To further optimize:

```bash
# View image size
docker images campuspulse

# Remove unused images
docker image prune -a

# Build with specific platform (for M1/M2 Macs)
docker build --platform linux/amd64 -t campuspulse:latest .
```

## 🔄 Updates and Maintenance

### Updating the Application

```bash
# Pull latest code
git pull origin main

# Rebuild and restart
docker-compose up --build -d

# Clean up old images
docker image prune
```

### Backup and Restore

```bash
# Save container state (if needed)
docker commit campuspulse-app campuspulse-backup:$(date +%Y%m%d)

# Export image
docker save campuspulse:latest | gzip > campuspulse-backup.tar.gz

# Import image
docker load < campuspulse-backup.tar.gz
```

## 📚 Additional Resources

- [Streamlit Docker Documentation](https://docs.streamlit.io/knowledge-base/tutorials/deploy/docker)
- [Docker Compose Documentation](https://docs.docker.com/compose/)
- [Docker Best Practices](https://docs.docker.com/develop/dev-best-practices/)

## 🆘 Getting Help

If you encounter issues:

1. Check the logs: `docker-compose logs -f`
2. Verify health status: `docker ps`
3. Review environment variables in `docker-compose.yml`
4. Ensure all required ports are available
5. Check Docker daemon is running: `docker info`

---

**Built with ❤️ for University of Florida • Campus Pulse**
