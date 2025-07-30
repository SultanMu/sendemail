#!/bin/bash

echo "🚀 Starting Email Campaign Management System in Docker..."

# Function to handle graceful shutdown
cleanup() {
    echo "🛑 Shutting down services..."
    kill $DJANGO_PID $STREAMLIT_PID 2>/dev/null
    exit 0
}

# Set up signal handlers
trap cleanup SIGTERM SIGINT

# Wait for database to be ready
echo "🗄️ Waiting for database to be ready..."
sleep 10  # Give database time to start

# Function to check if EmailTemplate table exists
check_emailtemplate_table() {
    python manage.py shell -c "
from django.db import connection
cursor = connection.cursor()
try:
    cursor.execute('SELECT 1 FROM mailer_emailtemplate LIMIT 1')
    print('✅ EmailTemplate table exists')
    exit(0)
except Exception as e:
    print('❌ EmailTemplate table does not exist')
    exit(1)
" >/dev/null 2>&1
    return $?
}

# Function to handle migrations with automatic recovery
handle_migrations() {
    echo "🗄️ Checking and running database migrations..."
    
    # First, try to run migrations normally
    if python manage.py migrate; then
        echo "✅ Migrations completed successfully"
        
        # Check if EmailTemplate table exists
        if check_emailtemplate_table; then
            echo "✅ All required tables exist"
            return 0
        else
            echo "⚠️ EmailTemplate table missing, creating missing migrations..."
            return 1
        fi
    else
        echo "⚠️ Migration failed, attempting to create missing migrations..."
        return 1
    fi
}

# Function to force migration reset (only when needed)
force_migration_reset() {
    echo "🔄 Force resetting migrations (this will clear existing data)..."
    
    # Remove all migration files except __init__.py
    echo "🗑️ Removing old migration files..."
    find mailer/migrations/ -name "*.py" ! -name "__init__.py" -delete
    
    # Create fresh initial migration
    echo "📝 Creating fresh migrations..."
    python manage.py makemigrations mailer
    
    # Reset database and run migrations
    echo "🗄️ Resetting database and running migrations..."
    python manage.py flush --no-input || true
    python manage.py migrate --run-syncdb || {
        echo "❌ Critical migration failure. Please check the database connection."
        exit 1
    }
    
    echo "✅ Migration reset completed successfully"
}

# Try normal migrations first
if ! handle_migrations; then
    echo "⚠️ Normal migration failed, attempting to create missing migrations..."
    
    # Try to create migrations for the mailer app
    if python manage.py makemigrations mailer; then
        echo "📝 Created new migrations, running them..."
        if python manage.py migrate; then
            echo "✅ Migrations completed successfully after creation"
        else
            echo "❌ Migration still failed, forcing complete reset..."
            force_migration_reset
        fi
    else
        echo "❌ Failed to create migrations, forcing complete reset..."
        force_migration_reset
    fi
fi

# Create sample templates with error handling
echo "📝 Creating sample templates..."
python manage.py create_sample_templates || {
    echo "⚠️ Sample template creation failed, but continuing..."
    echo "You can create templates manually through the admin interface or API"
}

# Start Django server in background
echo "📧 Starting Django server on port 8000..."
python manage.py runserver 0.0.0.0:8000 &
DJANGO_PID=$!

# Wait a moment for Django to start
sleep 3

# Start Streamlit server
echo "🎨 Starting Streamlit frontend on port 8501..."
streamlit run streamlit_app.py \
    --server.port 8501 \
    --server.address 0.0.0.0 \
    --server.headless true \
    --browser.gatherUsageStats false &
STREAMLIT_PID=$!

echo "✅ All services started successfully!"
echo "📧 Django API: http://localhost:8000"
echo "🎨 Streamlit Frontend: http://localhost:8501"
echo ""
echo "Press Ctrl+C to stop all services"

# Wait for both processes
wait $DJANGO_PID $STREAMLIT_PID 