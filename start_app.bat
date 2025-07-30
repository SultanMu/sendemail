@echo off
echo 🚀 Email Campaign Management System - Windows Launcher
echo ======================================================

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python is not installed or not in PATH
    echo Please install Python 3.8 or higher and try again
    pause
    exit /b 1
)

REM Check if we're in the right directory
if not exist "manage.py" (
    echo ❌ Error: manage.py not found. Please run this script from the project root directory.
    pause
    exit /b 1
)

REM Install dependencies
echo 📦 Installing dependencies...
pip install -r requirements.txt

REM Handle migrations with automatic recovery
echo 🗄️ Setting up database...
python manage.py migrate
if errorlevel 1 (
    echo ⚠️ Migration failed, attempting to create missing migrations...
    python manage.py makemigrations mailer
    if not errorlevel 1 (
        python manage.py migrate
        if not errorlevel 1 (
            echo ✅ Migrations completed successfully after creation
        ) else (
            echo 🔄 Attempting database reset...
            python manage.py flush --no-input >nul 2>&1
            python manage.py migrate --run-syncdb
            if not errorlevel 1 (
                echo ✅ Database reset and sync completed
            ) else (
                echo ❌ Critical migration failure. Please check your database configuration.
                pause
                exit /b 1
            )
        )
    ) else (
        echo ❌ Failed to create migrations
        pause
        exit /b 1
    )
) else (
    echo ✅ Migrations completed successfully
)

REM Create sample templates
echo 📝 Creating sample templates...
python manage.py create_sample_templates
if errorlevel 1 (
    echo ⚠️ Sample template creation failed, but continuing...
)

REM Start the application
echo 🎯 Starting Email Campaign Management System...
python run_app.py 