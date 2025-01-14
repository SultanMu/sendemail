from rest_framework import serializers
from .models import Email

class EmailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Email
        fields = ['email_address', 'subject', 'message', 'added_at']