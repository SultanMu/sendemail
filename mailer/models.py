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
    campaign_name = models.CharField(max_length=255, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.campaign_name


class Email(models.Model):
    email_id = models.AutoField(primary_key=True)
    email_address = models.EmailField()
    campaign_id = models.ForeignKey(Campaign, on_delete=models.CASCADE, related_name='emails')
    name = models.CharField(max_length=255)
    added_at = models.DateTimeField(auto_now_add=True)
    # subject = models.CharField(max_length=255)
    # message = models.TextField()

    def __str__(self):
        return f"{self.name} <{self.email_address}>"