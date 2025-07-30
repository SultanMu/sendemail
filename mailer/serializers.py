from rest_framework import serializers
from .models import Email, Campaign, EmailTemplate

class EmailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Email
        fields = ['email_id', 'email_address', 'campaign_id', 'name', 'added_at']


class CampaignSerializer(serializers.ModelSerializer):
    class Meta:
        model = Campaign
        fields = ['campaign_id', 'campaign_name', 'created_at', 'updated_at']

class EmailTemplateSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmailTemplate
        fields = ['template_id', 'template_name', 'subject', 'html_content', 'created_at', 'updated_at']