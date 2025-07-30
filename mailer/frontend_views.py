from django.shortcuts import render
from django.http import HttpResponse
import os
from django.conf import settings

def frontend_dashboard(request):
    try:
        # Serve the React build
        template_path = os.path.join(settings.BASE_DIR, 'frontend', 'build', 'index.html')
        if os.path.exists(template_path):
            with open(template_path, 'r', encoding='utf-8') as f:
                return HttpResponse(f.read(), content_type='text/html')
        else:
            # Fallback to development index.html if build doesn't exist
            dev_template_path = os.path.join(settings.BASE_DIR, 'frontend', 'public', 'index.html')
            if os.path.exists(dev_template_path):
                with open(dev_template_path, 'r', encoding='utf-8') as f:
                    return HttpResponse(f.read(), content_type='text/html')
            else:
                return HttpResponse(
                    "<h1>Frontend not found</h1><p>Please ensure the React app is built or available</p>", 
                    content_type='text/html'
                )
    except Exception as e:
        return HttpResponse(
            f"<h1>Error loading frontend</h1><p>{str(e)}</p>", 
            content_type='text/html'
        )