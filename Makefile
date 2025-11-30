# Campus Pulse - Docker Management Makefile

.PHONY: help build up down restart logs clean prune test shell health

# Default target
help:
	@echo "Campus Pulse - Docker Commands"
	@echo "==============================="
	@echo "make build     - Build the Docker image"
	@echo "make up        - Start the application"
	@echo "make down      - Stop the application"
	@echo "make restart   - Restart the application"
	@echo "make logs      - View application logs"
	@echo "make shell     - Open a shell in the container"
	@echo "make health    - Check container health"
	@echo "make clean     - Stop and remove containers"
	@echo "make prune     - Remove all unused Docker resources"
	@echo "make test      - Run tests in container"

# Build the Docker image
build:
	@echo "🏗️  Building Campus Pulse Docker image..."
	docker-compose build

# Start the application
up:
	@echo "🚀 Starting Campus Pulse..."
	docker-compose up -d
	@echo "✅ Campus Pulse is running at http://localhost:8501"

# Stop the application
down:
	@echo "🛑 Stopping Campus Pulse..."
	docker-compose down

# Restart the application
restart:
	@echo "🔄 Restarting Campus Pulse..."
	docker-compose restart
	@echo "✅ Campus Pulse restarted"

# View logs
logs:
	@echo "📋 Viewing Campus Pulse logs (Ctrl+C to exit)..."
	docker-compose logs -f

# Open shell in container
shell:
	@echo "🐚 Opening shell in Campus Pulse container..."
	docker exec -it campuspulse-app /bin/bash

# Check health status
health:
	@echo "🏥 Checking Campus Pulse health..."
	@docker inspect --format='{{.State.Health.Status}}' campuspulse-app 2>/dev/null || echo "Container not running"

# Clean up containers
clean:
	@echo "🧹 Cleaning up Campus Pulse containers..."
	docker-compose down -v
	@echo "✅ Cleanup complete"

# Prune all unused Docker resources
prune:
	@echo "🗑️  Removing unused Docker resources..."
	docker system prune -af
	@echo "✅ Prune complete"

# Run tests (if you add tests later)
test:
	@echo "🧪 Running tests..."
	docker-compose run --rm campuspulse pytest

# Quick rebuild and restart
rebuild: down build up
	@echo "✅ Rebuild complete - Campus Pulse is running at http://localhost:8501"

# Development mode with live reload
dev:
	@echo "👨‍💻 Starting Campus Pulse in development mode..."
	docker-compose up
