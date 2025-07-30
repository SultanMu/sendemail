#!/bin/bash

echo "🔄 Complete System Reset - Email Campaign Management System"
echo "============================================================"

# Stop all containers
echo "🛑 Stopping all containers..."
docker-compose down -v

# Remove all volumes
echo "🗑️ Removing all volumes..."
docker volume prune -f

# Remove all migration files except __init__.py
echo "🗑️ Removing old migration files..."
find mailer/migrations/ -name "*.py" ! -name "__init__.py" -delete

# Clean Docker cache
echo "🧹 Cleaning Docker cache..."
docker system prune -f

# Rebuild and start
echo "🚀 Rebuilding and starting services..."
docker-compose up --build

echo "✅ Complete reset finished!" 