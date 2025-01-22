from django.db import models

# Create your models here.
# class Email(models.Model):
#     name = models.CharField(max_length=255)
#     email = models.EmailField(null=True, blank=True)

# class Compaign(models,Model):
#     # compaign_name = models.CharField(prmarykey = 'yes') 
#     pass


class Email(models.Model):
    email_address = models.EmailField() # prmarykey 
    name = models.CharField(max_length=255)
    added_at = models.DateTimeField(auto_now_add=True)
    # subject = models.CharField(max_length=255)
    # message = models.TextField()