from django.urls import path
from .views import home, intro, send_emails

urlpatterns = [
    path('home/', home, name='home'),
    path('', intro, name='intro'),
    path('sendemails', send_emails, name='send_emails'),
]
