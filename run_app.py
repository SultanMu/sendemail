#!/usr/bin/env python3
"""
Launcher script for the Email Campaign Management System
This script can start both the Django backend and Streamlit frontend
"""

import subprocess
import sys
import time
import os
import signal
import threading
from pathlib import Path

def check_dependencies():
    """Check if required packages are installed"""
    required_packages = ['django', 'streamlit', 'requests', 'pandas', 'plotly']
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package)
        except ImportError:
            missing_packages.append(package)
    
    if missing_packages:
        print(f"❌ Missing required packages: {', '.join(missing_packages)}")
        print("Please install them using: pip install -r requirements.txt")
        return False
    
    return True

def check_emailtemplate_table():
    """Check if EmailTemplate table exists"""
    try:
        result = subprocess.run([sys.executable, "manage.py", "shell", "-c", 
                               "from django.db import connection; cursor = connection.cursor(); cursor.execute('SELECT 1 FROM mailer_emailtemplate LIMIT 1'); print('✅ EmailTemplate table exists')"], 
                              cwd=Path(__file__).parent, capture_output=True, text=True)
        return result.returncode == 0
    except:
        return False

def run_migrations():
    """Run database migrations with smart error recovery"""
    print("🗄️ Checking and running database migrations...")
    
    try:
        # First, try to run migrations normally
        result = subprocess.run([sys.executable, "manage.py", "migrate"], 
                              check=True, cwd=Path(__file__).parent, 
                              capture_output=True, text=True)
        print("✅ Migrations completed successfully")
        
        # Check if EmailTemplate table exists
        if check_emailtemplate_table():
            print("✅ All required tables exist")
            return True
        else:
            print("⚠️ EmailTemplate table missing, creating missing migrations...")
            return False
        
    except subprocess.CalledProcessError as e:
        print("⚠️ Migration failed, attempting to create missing migrations...")
        return False

def create_missing_migrations():
    """Create missing migrations when needed"""
    try:
        # Try to create migrations for the mailer app
        result = subprocess.run([sys.executable, "manage.py", "makemigrations", "mailer"], 
                              check=True, cwd=Path(__file__).parent,
                              capture_output=True, text=True)
        print("📝 Created new migrations, running them...")
        
        # Run migrations again
        result = subprocess.run([sys.executable, "manage.py", "migrate"], 
                              check=True, cwd=Path(__file__).parent,
                              capture_output=True, text=True)
        print("✅ Migrations completed successfully after creation")
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to create or run migrations: {e}")
        return False

def force_migration_reset():
    """Force complete migration reset (only when needed)"""
    print("🔄 Force resetting migrations (this will clear existing data)...")
    
    try:
        # Remove old migration files
        import glob
        import os
        migration_files = glob.glob("mailer/migrations/0*.py")
        for file in migration_files:
            os.remove(file)
        print("🗑️ Removed old migration files")
        
        # Create fresh migrations
        result = subprocess.run([sys.executable, "manage.py", "makemigrations", "mailer"], 
                              check=True, cwd=Path(__file__).parent,
                              capture_output=True, text=True)
        print("📝 Created fresh migrations")
        
        # Reset database and run migrations
        subprocess.run([sys.executable, "manage.py", "flush", "--no-input"], 
                     cwd=Path(__file__).parent, check=False)
        result = subprocess.run([sys.executable, "manage.py", "migrate", "--run-syncdb"], 
                              cwd=Path(__file__).parent, check=True)
        print("✅ Database reset and sync completed")
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Critical migration failure: {e}")
        print("💡 Try running: python manage.py migrate --run-syncdb")
        return False

def create_sample_templates():
    """Create sample templates"""
    print("📝 Creating sample templates...")
    try:
        subprocess.run([sys.executable, "manage.py", "create_sample_templates"], 
                      check=True, cwd=Path(__file__).parent)
        print("✅ Sample templates created successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to create sample templates: {e}")
        return False

def run_django_server():
    """Run Django development server"""
    print("🚀 Starting Django backend server...")
    try:
        subprocess.run([sys.executable, "manage.py", "runserver", "localhost:8000"], 
                      check=True, cwd=Path(__file__).parent)
    except KeyboardInterrupt:
        print("\n🛑 Django server stopped")
    except subprocess.CalledProcessError as e:
        print(f"❌ Django server failed to start: {e}")

def run_streamlit_app():
    """Run Streamlit frontend"""
    print("🎨 Starting Streamlit frontend...")
    try:
        subprocess.run([sys.executable, "-m", "streamlit", "run", "streamlit_app.py", 
                       "--server.port", "8501", "--server.address", "localhost"], 
                      check=True, cwd=Path(__file__).parent)
    except KeyboardInterrupt:
        print("\n🛑 Streamlit app stopped")
    except subprocess.CalledProcessError as e:
        print(f"❌ Streamlit app failed to start: {e}")

def main():
    print("📧 Email Campaign Management System")
    print("=" * 50)
    
    # Check dependencies
    if not check_dependencies():
        sys.exit(1)
    
    # Check if we're in the right directory
    if not Path("manage.py").exists():
        print("❌ Error: manage.py not found. Please run this script from the project root directory.")
        sys.exit(1)
    
    # Show menu
    print("\nChoose an option:")
    print("1. 🚀 Start both backend and frontend")
    print("2. 🗄️ Run database migrations only")
    print("3. 📝 Create sample templates only")
    print("4. 🎨 Start Streamlit frontend only")
    print("5. ⚙️ Start Django backend only")
    print("6. ❌ Exit")
    
    choice = input("\nEnter your choice (1-6): ").strip()
    
    if choice == "1":
        # Run migrations with smart recovery
        if not run_migrations():
            print("⚠️ Normal migration failed, attempting to create missing migrations...")
            if not create_missing_migrations():
                print("❌ Failed to create missing migrations, forcing complete reset...")
                if not force_migration_reset():
                    sys.exit(1)
        
        # Create sample templates
        create_sample_templates()
        
        # Start both servers
        print("\n🎯 Starting both servers...")
        print("📧 Django backend will be available at: http://localhost:8000")
        print("🎨 Streamlit frontend will be available at: http://localhost:8501")
        print("\nPress Ctrl+C to stop both servers")
        
        # Start Django in a separate thread
        django_thread = threading.Thread(target=run_django_server, daemon=True)
        django_thread.start()
        
        # Wait a bit for Django to start
        time.sleep(3)
        
        # Start Streamlit in main thread
        run_streamlit_app()
        
    elif choice == "2":
        if not run_migrations():
            print("⚠️ Normal migration failed, attempting to create missing migrations...")
            if not create_missing_migrations():
                print("❌ Failed to create missing migrations, forcing complete reset...")
                force_migration_reset()
        
    elif choice == "3":
        create_sample_templates()
        
    elif choice == "4":
        print("🎨 Starting Streamlit frontend only...")
        print("Note: Make sure Django backend is running on localhost:8000")
        run_streamlit_app()
        
    elif choice == "5":
        print("🚀 Starting Django backend only...")
        run_django_server()
        
    elif choice == "6":
        print("👋 Goodbye!")
        sys.exit(0)
        
    else:
        print("❌ Invalid choice. Please enter a number between 1-6.")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n🛑 Application stopped by user")
        sys.exit(0) 