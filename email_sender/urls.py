from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import static
from mailer.frontend_views import frontend_dashboard

urlpatterns = [
    path('admin/', admin.site.urls),
    path('email/', include('mailer.urls')),  # API endpoints
    path('', frontend_dashboard, name='frontend'),  # Frontend at root
]

# Serve static files in development
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)