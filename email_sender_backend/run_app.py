
#!/usr/bin/env python3

import subprocess
import sys
import os
import signal
import time
from threading import Thread

def run_django():
    """Run Django development server"""
    print("Starting Django server...")
    subprocess.run([sys.executable, "manage.py", "migrate"], check=True)
    subprocess.run([sys.executable, "manage.py", "runserver", "0.0.0.0:5000"])

def run_react():
    """Run React development server"""
    print("Starting React email_sender_frontend...")
    os.chdir("email_sender_frontend")
    subprocess.run(["npm", "install"], check=True)
    env = os.environ.copy()
    env.update({
        "HOST": "0.0.0.0",
        "PORT": "3000",
        "BROWSER": "none",
        "DANGEROUSLY_DISABLE_HOST_CHECK": "true"
    })
    subprocess.run(["npm", "start"], env=env)

def signal_handler(sig, frame):
    print("\nShutting down servers...")
    sys.exit(0)

if __name__ == "__main__":
    signal.signal(signal.SIGINT, signal_handler)
    
    # Start Django in a separate thread
    django_thread = Thread(target=run_django, daemon=True)
    django_thread.start()
    
    # Give Django a moment to start
    time.sleep(3)
    
    # Start React in main thread
    try:
        run_react()
    except KeyboardInterrupt:
        print("\nShutting down...")
