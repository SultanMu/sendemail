
from django.shortcuts import render
from django.http import HttpResponse
from django.conf import settings
from django.template.loader import get_template
import os

def frontend_dashboard(request):
    """Serve the React app's index.html file"""
    try:
        # Try to serve the built React app
        template = get_template('index.html')
        return HttpResponse(template.render(request=request))
    except:
        # Fallback if build doesn't exist
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
                <p>React app is being built...</p>
                <p>Please wait while the frontend is prepared.</p>
            </div>
        </body>
        </html>
        """
        return HttpResponse(html_content, content_type='text/html')
