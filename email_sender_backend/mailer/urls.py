from django.urls import path
from .views import (
    CampaignCreateView,
    CampaignListView,
    XLSReaderView,
    SendEmailsView,
    ListEmailView,
    UpdateCampaignView,
    DeleteCampaignView,
    DeleteEmailView,
    UpdateEmailView,
    EmailTemplatePreviewView,
    EmailTemplateListView,
    EmailTemplateCreateView
)
from .frontend_views import frontend_dashboard

urlpatterns = [
    # API endpoints
    # path('home/', home, name='home'),
    # path('', intro, name='intro'),
    path('campaigns/', CampaignListView.as_view(), name='campaign_list'),
    path('campaigns/create', CampaignCreateView.as_view(), name='campaign_create'),
    path('update-campaign', UpdateCampaignView.as_view(), name='update_campaign'),
    path('delete-campaign', DeleteCampaignView.as_view(), name="delete_campaign"),
    # path('campaigns/<int:pk>/', CampaignUpdateView.as_view(), name='campaign_update'),
    # path('campaigns/<int:pk>/', CampaignDeleteView.as_view(), name='campaign_delete'),
    path('list-emails/', ListEmailView.as_view(), name='email_list'),
    path('upload-xls/', XLSReaderView.as_view(), name='upload_xls'),
    path('send-emails/', SendEmailsView.as_view(), name='send_emails'),
    path('delete-email', DeleteEmailView.as_view(), name='delete_email'),
    path('update-email', UpdateEmailView.as_view(), name='update_email'),
    path('template-preview/', EmailTemplatePreviewView.as_view(), name='email-template-preview'),
    path('templates/', EmailTemplateListView.as_view(), name='email-templates-list'),
    path('templates/create/', EmailTemplateCreateView.as_view(), name='email-template-create'),
]