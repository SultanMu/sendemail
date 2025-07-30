
from django.db import models

class Campaign(models.Model):
    campaign_id = models.AutoField(primary_key=True)
    campaign_name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'mailer_campaign'

    def __str__(self):
        return self.campaign_name

class Email(models.Model):
    email_id = models.AutoField(primary_key=True)
    email_address = models.EmailField()
    campaign_id = models.ForeignKey(Campaign, on_delete=models.CASCADE, related_name='emails')
    name = models.CharField(max_length=255, blank=True, null=True)
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'mailer_email'
        unique_together = ('email_address', 'campaign_id')

    def __str__(self):
        return f"{self.email_address} - {self.campaign_id.campaign_name}"
