# 🐳 Docker Setup Guide - Email Campaign Management System

This guide covers running the enhanced email campaign system with Docker, including both Django backend and Streamlit frontend.

## 🚀 Quick Start with Docker

### Prerequisites
- **Docker** installed on your system
- **Docker Compose** installed
- **Git** (optional)

### Step 1: Clone/Download the Project
```bash
git clone <your-repo-url>
cd sendemail
```

### Step 2: Build and Start with Docker Compose
```bash
# Build and start all services
docker-compose up --build

# Or run in background
docker-compose up -d --build
```

### Step 3: Access the Application
- **🎨 Streamlit Frontend**: http://localhost:8501
- **📧 Django Backend API**: http://localhost:8000
- **🗄️ Database**: localhost:5432

## 📋 Docker Services

### **Main Application (`app`)**
- **Django Backend**: Port 8000
- **Streamlit Frontend**: Port 8501
- **Features**: 
  - Template management
  - Campaign management
  - Email sending
  - API endpoints

### **Database (`db`)**
- **PostgreSQL**: Port 5432
- **Database**: `email_campaign_db`
- **Credentials**: 
  - Username: `postgres`
  - Password: `postgres`

### **Cache (`redis`)**
- **Redis**: Port 6379
- **Purpose**: Caching and session storage

## 🔧 Docker Commands

### **Basic Operations**
```bash
# Start all services
docker-compose up

# Start in background
docker-compose up -d

# Stop all services
docker-compose down

# View logs
docker-compose logs

# View logs for specific service
docker-compose logs app
docker-compose logs db

# Rebuild and start
docker-compose up --build
```

### **Database Operations**
```bash
# Access database
docker-compose exec db psql -U postgres -d email_campaign_db

# Run migrations
docker-compose exec app python manage.py migrate

# Create superuser
docker-compose exec app python manage.py createsuperuser

# Create sample templates
docker-compose exec app python manage.py create_sample_templates
```

### **Development Operations**
```bash
# Access app container
docker-compose exec app bash

# Run tests
docker-compose exec app python manage.py test

# Collect static files
docker-compose exec app python manage.py collectstatic
```

## 🌐 Environment Configuration

### **Environment Variables**
Create a `.env` file in the project root:

```env
# Django Settings
DEBUG=True
SECRET_KEY=your-secret-key-here
ALLOWED_HOSTS=localhost,127.0.0.1

# Database Settings
DATABASE_URL=postgres://postgres:postgres@db:5432/email_campaign_db

# Email Settings
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
DEFAULT_FROM_EMAIL=your-email@gmail.com

# Streamlit Settings
STREAMLIT_SERVER_PORT=8501
STREAMLIT_SERVER_ADDRESS=0.0.0.0
```

### **Update docker-compose.yml for Environment Variables**
```yaml
services:
  app:
    build: .
    ports:
      - "8000:8000"
      - "8501:8501"
    volumes:
      - .:/app
    env_file:
      - .env
    environment:
      - DATABASE_URL=postgres://postgres:postgres@db:5432/email_campaign_db
```

## 📊 Monitoring and Logs

### **View Real-time Logs**
```bash
# All services
docker-compose logs -f

# Specific service
docker-compose logs -f app
docker-compose logs -f db
```

### **Check Service Status**
```bash
# List running containers
docker-compose ps

# Check resource usage
docker stats
```

## 🔍 Troubleshooting

### **Common Issues**

#### **1. Port Already in Use**
```bash
# Check what's using the ports
lsof -i :8000
lsof -i :8501

# Kill processes if needed
sudo kill -9 <PID>
```

#### **2. Database Connection Issues**
```bash
# Check database logs
docker-compose logs db

# Restart database
docker-compose restart db

# Reset database (WARNING: This will delete all data)
docker-compose down -v
docker-compose up --build
```

#### **3. Build Failures**
```bash
# Clean build
docker-compose down
docker system prune -f
docker-compose up --build
```

#### **4. Permission Issues**
```bash
# Fix file permissions
sudo chown -R $USER:$USER .

# Or run with sudo (not recommended for production)
sudo docker-compose up
```

### **Debug Mode**
```bash
# Access container for debugging
docker-compose exec app bash

# Check Django logs
docker-compose exec app python manage.py check

# Test database connection
docker-compose exec app python manage.py dbshell
```

## 🚀 Production Deployment

### **Production Docker Compose**
```yaml
version: '3.8'

services:
  app:
    build: .
    ports:
      - "8000:8000"
      - "8501:8501"
    volumes:
      - static_volume:/app/staticfiles
      - media_volume:/app/media
    environment:
      - DEBUG=False
      - DJANGO_SETTINGS_MODULE=email_sender.settings
    depends_on:
      - db
    restart: always

  db:
    image: postgres:13
    volumes:
      - postgres_data:/var/lib/postgresql/data
    environment:
      - POSTGRES_DB=email_campaign_db
      - POSTGRES_USER=postgres
      - POSTGRES_PASSWORD=${DB_PASSWORD}
    restart: always

  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf
      - static_volume:/app/staticfiles
    depends_on:
      - app
    restart: always

volumes:
  postgres_data:
  static_volume:
  media_volume:
```

## 📝 Development Workflow

### **Local Development with Docker**
```bash
# Start services
docker-compose up -d

# Make changes to code
# (Files are mounted as volumes, so changes are reflected immediately)

# View logs
docker-compose logs -f app

# Stop services
docker-compose down
```

### **Testing with Docker**
```bash
# Run tests
docker-compose exec app python manage.py test

# Run demo script
docker-compose exec app python demo_features.py

# Run API tests
docker-compose exec app python test_template_features.py
```

## 🔄 Migration from Local to Docker

If you were running the application locally:

1. **Stop local services**:
   ```bash
   # Stop Django and Streamlit if running
   pkill -f "python manage.py runserver"
   pkill -f "streamlit"
   ```

2. **Start with Docker**:
   ```bash
   docker-compose up --build
   ```

3. **Access the same URLs**:
   - Frontend: http://localhost:8501
   - Backend: http://localhost:8000

## 🎯 Benefits of Docker Setup

✅ **Consistent Environment**: Same setup across all machines
✅ **Easy Deployment**: One command to start everything
✅ **Isolated Services**: Each service runs in its own container
✅ **Scalable**: Easy to add more services
✅ **Production Ready**: Can be deployed to any Docker host
✅ **Version Control**: All dependencies are versioned

## 🆘 Need Help?

- **Docker Issues**: Check `docker-compose logs`
- **Application Issues**: Check the main README.md
- **Database Issues**: Check `docker-compose logs db`
- **Network Issues**: Check if ports are available

The Docker setup provides a complete, isolated environment for running your email campaign system with both Django and Streamlit services! 🐳 