
from django.shortcuts import render
from django.http import HttpResponse
from django.conf import settings
import os

def frontend_dashboard(request):
    """Serve a simple HTML page that redirects to the React dev server"""
    html_content = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Email Campaign Manager</title>
        <style>
            body { font-family: Arial, sans-serif; text-align: center; padding: 50px; }
            .container { max-width: 600px; margin: 0 auto; }
            .btn { display: inline-block; padding: 12px 24px; background: #007bff; color: white; text-decoration: none; border-radius: 4px; margin: 10px; }
            .btn:hover { background: #0056b3; }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>Email Campaign Manager</h1>
            <p>Your Django backend is running on port 5000</p>
            <p>Your React frontend is running on port 3000</p>
            <p>Click below to access the React frontend:</p>
            <a href="http://localhost:3000" class="btn" target="_blank">Open React Frontend</a>
            <br><br>
            <p><small>If you're seeing this page, your Django server is working correctly. 
            The React app should be accessible on port 3000.</small></p>
        </div>
    </body>
    </html>
    """
    return HttpResponse(html_content, content_type='text/html')
