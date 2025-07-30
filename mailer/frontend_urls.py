
from django.urls import path
from .frontend_views import frontend_dashboard

urlpatterns = [
    path('', frontend_dashboard, name='dashboard'),  # Frontend at root only
]
from django.urls import path
from .frontend_views import frontend_dashboard

urlpatterns = [
    path('', frontend_dashboard, name='frontend_dashboard'),
]
