from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from mailer.frontend_views import frontend_dashboard

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('mailer.urls')),
    path('', frontend_dashboard, name='frontend'),
]

# Serve static files
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)