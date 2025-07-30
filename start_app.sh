#!/bin/bash

echo "🚀 Email Campaign Management System - Unix/Linux/Mac Launcher"
echo "=============================================================="

# Check if Python3 is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 is not installed. Please install Python 3.8 or higher."
    exit 1
fi

# Check if we're in the right directory
if [ ! -f "manage.py" ]; then
    echo "❌ Error: manage.py not found. Please run this script from the project root directory."
    exit 1
fi

# Install dependencies
echo "📦 Installing dependencies..."
pip3 install -r requirements.txt

# Function to check if EmailTemplate table exists
check_emailtemplate_table() {
    python3 manage.py shell -c "
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

# Handle migrations with smart recovery
echo "🗄️ Setting up database..."
if python3 manage.py migrate; then
    echo "✅ Migrations completed successfully"
    
    # Check if EmailTemplate table exists
    if check_emailtemplate_table; then
        echo "✅ All required tables exist"
    else
        echo "⚠️ EmailTemplate table missing, creating missing migrations..."
        if python3 manage.py makemigrations mailer && python3 manage.py migrate; then
            echo "✅ Migrations completed successfully after creation"
        else
            echo "🔄 Attempting database reset..."
            python3 manage.py flush --no-input 2>/dev/null || true
            if python3 manage.py migrate --run-syncdb; then
                echo "✅ Database reset and sync completed"
            else
                echo "❌ Critical migration failure. Please check your database configuration."
                exit 1
            fi
        fi
    fi
else
    echo "⚠️ Migration failed, attempting to create missing migrations..."
    if python3 manage.py makemigrations mailer && python3 manage.py migrate; then
        echo "✅ Migrations completed successfully after creation"
    else
        echo "🔄 Attempting database reset..."
        python3 manage.py flush --no-input 2>/dev/null || true
        if python3 manage.py migrate --run-syncdb; then
            echo "✅ Database reset and sync completed"
        else
            echo "❌ Critical migration failure. Please check your database configuration."
            exit 1
        fi
    fi
fi

# Create sample templates
echo "📝 Creating sample templates..."
python3 manage.py create_sample_templates || {
    echo "⚠️ Sample template creation failed, but continuing..."
}

# Start the application
echo "🎯 Starting Email Campaign Management System..."
python3 run_app.py 