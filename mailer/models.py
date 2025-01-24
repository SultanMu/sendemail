from django.db import models

# Create your models here.
# class Email(models.Model):
#     name = models.CharField(max_length=255)
#     email = models.EmailField(null=True, blank=True)

# class Compaign(models,Model):
#     # compaign_name = models.CharField(prmarykey = 'yes') 
#     pass

class Campaign(models.Model):
    campaign_id = models.AutoField(primary_key=True)
    campaign_name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Email(models.Model):
    email_address = models.EmailField(primary_key=True) # prmarykey 
    campaign = models.ForeignKey(Campaign, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    added_at = models.DateTimeField(auto_now_add=True)
    # subject = models.CharField(max_length=255)
    # message = models.TextField()