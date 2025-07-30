from django.urls import path
from .views import *

urlpatterns = [
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
    # path('sendemails', send_emails, name='send_emails'),
    
    # ==================== TEMPLATE MANAGEMENT URLS ====================
    path('templates/', TemplateListView.as_view(), name='template_list'),
    path('templates/create/', TemplateCreateView.as_view(), name='template_create'),
    path('templates/<int:template_id>/', TemplateDetailView.as_view(), name='template_detail'),
    path('templates/<int:template_id>/update/', TemplateUpdateView.as_view(), name='template_update'),
    path('templates/<int:template_id>/delete/', TemplateDeleteView.as_view(), name='template_delete'),
    path('templates/preview/', TemplatePreviewView.as_view(), name='template_preview'),
    
    # ==================== ENHANCED CAMPAIGN URLS ====================
    path('campaigns/template-update/', CampaignTemplateUpdateView.as_view(), name='campaign_template_update'),
    path('campaigns/send-enhanced/', EnhancedSendEmailsView.as_view(), name='enhanced_send_emails'),
]
