from django.db import models

# Create your models here.
class Email(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField(null=True, blank=True)