#!/bin/bash

echo "🔄 Resetting database and starting fresh..."

# Stop all containers
echo "🛑 Stopping all containers..."
docker-compose down -v

# Remove all volumes
echo "🗑️ Removing all volumes..."
docker volume prune -f

# Rebuild and start
echo "🚀 Rebuilding and starting services..."
docker-compose up --build

echo "✅ Database reset complete!" 