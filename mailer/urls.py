from django.urls import path
from .views import *

urlpatterns = [
    # path('home/', home, name='home'),
    # path('', intro, name='intro'),
    path('upload-xls/', XLSReaderView.as_view(), name='upload_xls'),
    path('send-emails/', SendEmailsView.as_view(), name='send_emails'),
    # path('sendemails', send_emails, name='send_emails'),
]
