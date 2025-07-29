
from django.shortcuts import render
from django.http import HttpResponse
import os

def frontend_dashboard(request):
    """Serve the frontend dashboard"""
    try:
        with open('frontend/index.html', 'r') as file:
            content = file.read()
        return HttpResponse(content, content_type='text/html')
    except FileNotFoundError:
        return HttpResponse("Frontend file not found", status=404)
