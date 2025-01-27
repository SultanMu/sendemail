from django.urls import path
from .views import *

urlpatterns = [
    # path('home/', home, name='home'),
    # path('', intro, name='intro'),
    path('campaigns/', CampaignListView.as_view(), name='campaign_list'),
    path('campaigns/create', CampaignCreateView.as_view(), name='campaign_create'),
    # path('campaigns/<int:pk>/', CampaignUpdateView.as_view(), name='campaign_update'),
    # path('campaigns/<int:pk>/', CampaignDeleteView.as_view(), name='campaign_delete'),
    path('list-emails/', ListEmailView.as_view(), name='email_list'),
    path('upload-xls/', XLSReaderView.as_view(), name='upload_xls'),
    path('send-emails/', SendEmailsView.as_view(), name='send_emails'),
    # path('sendemails', send_emails, name='send_emails'),
]
