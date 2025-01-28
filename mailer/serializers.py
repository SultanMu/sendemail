from rest_framework import serializers
from .models import Email, Campaign

class EmailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Email
        fields = ['email_address', 'campaign_id', 'name', 'added_at']


class CampaignSerializer(serializers.ModelSerializer):
    class Meta:
        model = Campaign
        fields = ['campaign_id', 'campaign_name', 'created_at', 'updated_at']