from rest_framework import serializers
from .models import Email, Campaign

class EmailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Email
        fields = ['id', 'email_address', 'name', 'campaign_name', 'added_at']


class CampaignSerializer(serializers.ModelSerializer):
    class Meta:
        model = Campaign
        fields = ['id', 'name', 'created_at', 'updated_at', 'emails']