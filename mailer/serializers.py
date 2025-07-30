from rest_framework import serializers
from .models import Email, Campaign, EmailTemplate, TemplateVariable, TemplateCategory

class EmailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Email
        fields = ['email_id', 'email_address', 'campaign_id', 'name', 'added_at']


class CampaignSerializer(serializers.ModelSerializer):
    class Meta:
        model = Campaign
        fields = ['campaign_id', 'campaign_name', 'created_at', 'updated_at']


class TemplateVariableSerializer(serializers.ModelSerializer):
    class Meta:
        model = TemplateVariable
        fields = ['variable_name', 'display_name', 'variable_type', 'default_value', 'is_required', 'description']


class EmailTemplateSerializer(serializers.ModelSerializer):
    template_variables = TemplateVariableSerializer(many=True, read_only=True)
    variables_count = serializers.SerializerMethodField()
    
    class Meta:
        model = EmailTemplate
        fields = [
            'template_id', 'name', 'description', 'subject', 'html_content', 
            'css_styles', 'is_active', 'is_default', 'created_at', 'updated_at',
            'template_variables', 'variables_count'
        ]
    
    def get_variables_count(self, obj):
        return obj.template_variables.count()


class EmailTemplateCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating templates with variables"""
    variables = TemplateVariableSerializer(many=True, required=False)
    
    class Meta:
        model = EmailTemplate
        fields = [
            'name', 'description', 'subject', 'html_content', 
            'css_styles', 'is_active', 'variables'
        ]
    
    def create(self, validated_data):
        variables_data = validated_data.pop('variables', [])
        template = EmailTemplate.objects.create(**validated_data)
        
        for variable_data in variables_data:
            TemplateVariable.objects.create(template=template, **variable_data)
        
        return template


class EmailTemplateUpdateSerializer(serializers.ModelSerializer):
    """Serializer for updating templates"""
    variables = TemplateVariableSerializer(many=True, required=False)
    
    class Meta:
        model = EmailTemplate
        fields = [
            'name', 'description', 'subject', 'html_content', 
            'css_styles', 'is_active', 'variables'
        ]
    
    def update(self, instance, validated_data):
        variables_data = validated_data.pop('variables', None)
        
        # Update template fields
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        
        # Update variables if provided
        if variables_data is not None:
            # Delete existing variables
            instance.template_variables.all().delete()
            # Create new variables
            for variable_data in variables_data:
                TemplateVariable.objects.create(template=instance, **variable_data)
        
        return instance


class TemplateCategorySerializer(serializers.ModelSerializer):
    templates_count = serializers.SerializerMethodField()
    
    class Meta:
        model = TemplateCategory
        fields = ['category_id', 'name', 'description', 'created_at', 'templates_count']
    
    def get_templates_count(self, obj):
        return obj.emailtemplate_set.count()


class CampaignDetailSerializer(serializers.ModelSerializer):
    """Enhanced serializer for campaigns with template information"""
    custom_template = EmailTemplateSerializer(read_only=True)
    custom_template_id = serializers.SerializerMethodField()
    template_id = serializers.IntegerField(write_only=True, required=False, allow_null=True)
    
    class Meta:
        model = Campaign
        fields = [
            'campaign_id', 'campaign_name', 'created_at', 'updated_at',
            'custom_template', 'custom_template_id', 'custom_subject', 'custom_message', 
            'use_custom_template', 'template_id'
        ]
    
    def get_custom_template_id(self, obj):
        return obj.custom_template.template_id if obj.custom_template else None
    
    def update(self, instance, validated_data):
        template_id = validated_data.pop('template_id', None)
        
        if template_id is not None:
            try:
                template = EmailTemplate.objects.get(template_id=template_id, is_active=True)
                instance.custom_template = template
            except EmailTemplate.DoesNotExist:
                instance.custom_template = None
        
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        
        return instance


class TemplatePreviewSerializer(serializers.Serializer):
    """Serializer for template preview with sample data"""
    template_id = serializers.IntegerField()
    sample_data = serializers.JSONField(required=False, default=dict)
    
    def validate_template_id(self, value):
        try:
            EmailTemplate.objects.get(template_id=value, is_active=True)
        except EmailTemplate.DoesNotExist:
            raise serializers.ValidationError("Template not found or inactive")
        return value