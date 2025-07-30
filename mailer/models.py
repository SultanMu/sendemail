from django.db import models

# Create your models here.
# class Email(models.Model):
#     name = models.CharField(max_length=255)
#     email = models.EmailField(null=True, blank=True)

# class Compaign(models,Model):
#     # compaign_name = models.CharField(prmarykey = 'yes') 
#     pass

class TemplateCategory(models.Model):
    """Model for organizing templates into categories"""
    category_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name_plural = "Template categories"


class EmailTemplate(models.Model):
    """Model for managing custom email templates"""
    template_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, unique=True, help_text="Template name for identification")
    description = models.TextField(blank=True, help_text="Brief description of the template")
    subject = models.CharField(max_length=255, help_text="Default subject line for emails using this template")
    html_content = models.TextField(help_text="HTML content of the email template")
    css_styles = models.TextField(blank=True, help_text="CSS styles for the template")
    is_active = models.BooleanField(default=True, help_text="Whether this template is available for use")
    is_default = models.BooleanField(default=False, help_text="Whether this is a system default template")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    category = models.ForeignKey(TemplateCategory, on_delete=models.SET_NULL, null=True, blank=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return self.name
    
    def get_available_variables(self):
        """Get list of available template variables"""
        return self.template_variables.all()


class TemplateVariable(models.Model):
    """Model for defining template variables that can be used in templates"""
    VARIABLE_TYPES = [
        ('text', 'Text'),
        ('email', 'Email'),
        ('url', 'URL'),
        ('date', 'Date'),
        ('number', 'Number'),
    ]
    
    template = models.ForeignKey(EmailTemplate, on_delete=models.CASCADE, related_name='template_variables')
    variable_name = models.CharField(max_length=100, help_text="Variable name used in template (e.g., 'name', 'company')")
    display_name = models.CharField(max_length=100, help_text="Human-readable name (e.g., 'Recipient Name', 'Company Name')")
    variable_type = models.CharField(max_length=20, choices=VARIABLE_TYPES, default='text')
    default_value = models.CharField(max_length=255, blank=True, help_text="Default value if not provided")
    is_required = models.BooleanField(default=True, help_text="Whether this variable is required")
    description = models.TextField(blank=True, help_text="Description of what this variable is used for")
    
    class Meta:
        unique_together = ['template', 'variable_name']
    
    def __str__(self):
        return f"{self.template.name} - {self.display_name}"


class Campaign(models.Model):
    campaign_id = models.AutoField(primary_key=True)
    campaign_name = models.CharField(max_length=255, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    # New fields for template and message control
    custom_template = models.ForeignKey(EmailTemplate, on_delete=models.SET_NULL, null=True, blank=True, related_name='campaigns')
    custom_subject = models.CharField(max_length=255, blank=True, help_text="Custom subject line for this campaign")
    custom_message = models.TextField(blank=True, help_text="Custom message content for this campaign")
    use_custom_template = models.BooleanField(default=False, help_text="Use custom template instead of default templates")

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