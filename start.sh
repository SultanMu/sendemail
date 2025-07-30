
#!/bin/bash

# Kill any existing processes
pkill -f "python" 2>/dev/null
pkill -f "npm" 2>/dev/null
pkill -f "node" 2>/dev/null

echo "Starting Django backend..."
# Run Django migrations and start server in background
python manage.py migrate
python manage.py runserver 0.0.0.0:5000 &

echo "Installing frontend dependencies..."
cd frontend
npm install

echo "Starting React frontend..."
npm start &

# Wait for both processes
wait
