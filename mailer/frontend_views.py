
from django.shortcuts import render
from django.http import HttpResponse
from django.conf import settings
import os

def frontend_dashboard(request):
    """Serve the React frontend build"""
    try:
        # Try to serve the built React app first
        build_index_path = os.path.join(settings.BASE_DIR, 'frontend', 'build', 'index.html')
        if os.path.exists(build_index_path):
            with open(build_index_path, 'r') as file:
                content = file.read()
            return HttpResponse(content, content_type='text/html')
        
        # Fallback to development index.html
        dev_index_path = os.path.join(settings.BASE_DIR, 'frontend', 'public', 'index.html')
        if os.path.exists(dev_index_path):
            with open(dev_index_path, 'r') as file:
                content = file.read()
            return HttpResponse(content, content_type='text/html')
            
        return HttpResponse("Frontend files not found. Please build your React app first.", status=404)
    except Exception as e:
        return HttpResponse(f"Error loading frontend: {str(e)}", status=500)
