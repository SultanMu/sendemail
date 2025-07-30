from django.core.management.base import BaseCommand
from mailer.models import EmailTemplate, TemplateVariable


class Command(BaseCommand):
    help = 'Create sample email templates for demonstration'

    def handle(self, *args, **options):
        self.stdout.write('Creating sample email templates...')
        
        # Sample Template 1: Welcome Email
        welcome_template, created = EmailTemplate.objects.get_or_create(
            name="Welcome Email Template",
            defaults={
                'description': 'A professional welcome email template with customizable content',
                'subject': 'Welcome to Our Platform',
                'html_content': '''
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Welcome</title>
    <style>
        body { font-family: Arial, sans-serif; line-height: 1.6; color: #333; }
        .container { max-width: 600px; margin: 0 auto; padding: 20px; }
        .header { background-color: #007bff; color: white; padding: 20px; text-align: center; }
        .content { padding: 20px; background-color: #f8f9fa; }
        .footer { background-color: #6c757d; color: white; padding: 15px; text-align: center; font-size: 12px; }
        .button { display: inline-block; padding: 10px 20px; background-color: #28a745; color: white; text-decoration: none; border-radius: 5px; }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>Welcome to Our Platform</h1>
        </div>
        <div class="content">
            <h2>Hello {{ name }}!</h2>
            <p>{{ message }}</p>
            {% if company %}
            <p>We're excited to have <strong>{{ company }}</strong> on board!</p>
            {% endif %}
            <p>Here are some next steps to get you started:</p>
            <ul>
                <li>Complete your profile</li>
                <li>Explore our features</li>
                <li>Connect with our team</li>
            </ul>
            <p style="text-align: center;">
                <a href="{{ cta_url|default:'#' }}" class="button">Get Started</a>
            </p>
        </div>
        <div class="footer">
            <p>© 2024 Our Platform. All rights reserved.</p>
            <p>If you have any questions, contact us at {{ support_email|default:'support@example.com' }}</p>
        </div>
    </div>
</body>
</html>
                ''',
                'css_styles': '''
body { font-family: Arial, sans-serif; line-height: 1.6; color: #333; }
.container { max-width: 600px; margin: 0 auto; padding: 20px; }
.header { background-color: #007bff; color: white; padding: 20px; text-align: center; }
.content { padding: 20px; background-color: #f8f9fa; }
.footer { background-color: #6c757d; color: white; padding: 15px; text-align: center; font-size: 12px; }
.button { display: inline-block; padding: 10px 20px; background-color: #28a745; color: white; text-decoration: none; border-radius: 5px; }
                ''',
                'is_active': True,
                'is_default': False
            }
        )
        
        if created:
            # Create variables for welcome template
            TemplateVariable.objects.bulk_create([
                TemplateVariable(
                    template=welcome_template,
                    variable_name='name',
                    display_name='Recipient Name',
                    variable_type='text',
                    is_required=True,
                    description='The name of the recipient'
                ),
                TemplateVariable(
                    template=welcome_template,
                    variable_name='message',
                    display_name='Welcome Message',
                    variable_type='text',
                    default_value='Welcome to our platform! We\'re thrilled to have you join us.',
                    is_required=False,
                    description='Custom welcome message'
                ),
                TemplateVariable(
                    template=welcome_template,
                    variable_name='company',
                    display_name='Company Name',
                    variable_type='text',
                    is_required=False,
                    description='Company name (optional)'
                ),
                TemplateVariable(
                    template=welcome_template,
                    variable_name='cta_url',
                    display_name='Call-to-Action URL',
                    variable_type='url',
                    default_value='https://example.com/get-started',
                    is_required=False,
                    description='URL for the call-to-action button'
                ),
                TemplateVariable(
                    template=welcome_template,
                    variable_name='support_email',
                    display_name='Support Email',
                    variable_type='email',
                    default_value='support@example.com',
                    is_required=False,
                    description='Support email address'
                )
            ])
            self.stdout.write(self.style.SUCCESS('Created Welcome Email Template'))
        else:
            self.stdout.write('Welcome Email Template already exists')

        # Sample Template 2: Newsletter Template
        newsletter_template, created = EmailTemplate.objects.get_or_create(
            name="Newsletter Template",
            defaults={
                'description': 'A modern newsletter template with featured content sections',
                'subject': '{{ newsletter_title|default:"Our Monthly Newsletter" }}',
                'html_content': '''
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Newsletter</title>
    <style>
        body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; line-height: 1.6; color: #333; }
        .container { max-width: 600px; margin: 0 auto; padding: 20px; }
        .header { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 30px; text-align: center; }
        .content { padding: 20px; background-color: #ffffff; }
        .featured-article { background-color: #f8f9fa; padding: 20px; margin: 20px 0; border-left: 4px solid #007bff; }
        .footer { background-color: #343a40; color: white; padding: 20px; text-align: center; font-size: 12px; }
        .button { display: inline-block; padding: 12px 24px; background-color: #007bff; color: white; text-decoration: none; border-radius: 5px; margin: 10px 0; }
        .social-links { margin: 20px 0; }
        .social-links a { margin: 0 10px; color: #007bff; text-decoration: none; }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>{{ newsletter_title|default:"Monthly Newsletter" }}</h1>
            <p>{{ newsletter_subtitle|default:"Stay updated with our latest news and insights" }}</p>
        </div>
        <div class="content">
            <h2>Hello {{ name }}!</h2>
            <p>{{ intro_message|default:"Here's what's new this month:" }}</p>
            
            <div class="featured-article">
                <h3>{{ featured_title|default:"Featured Article" }}</h3>
                <p>{{ featured_content|default:"This is our featured content for this month." }}</p>
                <a href="{{ featured_url|default:'#' }}" class="button">Read More</a>
            </div>
            
            <h3>Latest Updates</h3>
            <ul>
                {% for update in updates %}
                <li>{{ update }}</li>
                {% endfor %}
            </ul>
            
            <div class="social-links">
                <p>Follow us on social media:</p>
                <a href="{{ facebook_url|default:'#' }}">Facebook</a>
                <a href="{{ twitter_url|default:'#' }}">Twitter</a>
                <a href="{{ linkedin_url|default:'#' }}">LinkedIn</a>
            </div>
        </div>
        <div class="footer">
            <p>© 2024 {{ company_name|default:"Our Company" }}. All rights reserved.</p>
            <p><a href="{{ unsubscribe_url|default:'#' }}" style="color: #fff;">Unsubscribe</a> | 
               <a href="{{ preferences_url|default:'#' }}" style="color: #fff;">Email Preferences</a></p>
        </div>
    </div>
</body>
</html>
                ''',
                'css_styles': '''
body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; line-height: 1.6; color: #333; }
.container { max-width: 600px; margin: 0 auto; padding: 20px; }
.header { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 30px; text-align: center; }
.content { padding: 20px; background-color: #ffffff; }
.featured-article { background-color: #f8f9fa; padding: 20px; margin: 20px 0; border-left: 4px solid #007bff; }
.footer { background-color: #343a40; color: white; padding: 20px; text-align: center; font-size: 12px; }
.button { display: inline-block; padding: 12px 24px; background-color: #007bff; color: white; text-decoration: none; border-radius: 5px; margin: 10px 0; }
.social-links { margin: 20px 0; }
.social-links a { margin: 0 10px; color: #007bff; text-decoration: none; }
                ''',
                'is_active': True,
                'is_default': False
            }
        )
        
        if created:
            # Create variables for newsletter template
            TemplateVariable.objects.bulk_create([
                TemplateVariable(
                    template=newsletter_template,
                    variable_name='name',
                    display_name='Recipient Name',
                    variable_type='text',
                    is_required=True,
                    description='The name of the recipient'
                ),
                TemplateVariable(
                    template=newsletter_template,
                    variable_name='newsletter_title',
                    display_name='Newsletter Title',
                    variable_type='text',
                    default_value='Monthly Newsletter',
                    is_required=False,
                    description='Title of the newsletter'
                ),
                TemplateVariable(
                    template=newsletter_template,
                    variable_name='newsletter_subtitle',
                    display_name='Newsletter Subtitle',
                    variable_type='text',
                    default_value='Stay updated with our latest news and insights',
                    is_required=False,
                    description='Subtitle for the newsletter'
                ),
                TemplateVariable(
                    template=newsletter_template,
                    variable_name='intro_message',
                    display_name='Introduction Message',
                    variable_type='text',
                    default_value="Here's what's new this month:",
                    is_required=False,
                    description='Introduction message'
                ),
                TemplateVariable(
                    template=newsletter_template,
                    variable_name='featured_title',
                    display_name='Featured Article Title',
                    variable_type='text',
                    default_value='Featured Article',
                    is_required=False,
                    description='Title of the featured article'
                ),
                TemplateVariable(
                    template=newsletter_template,
                    variable_name='featured_content',
                    display_name='Featured Article Content',
                    variable_type='text',
                    default_value='This is our featured content for this month.',
                    is_required=False,
                    description='Content of the featured article'
                ),
                TemplateVariable(
                    template=newsletter_template,
                    variable_name='featured_url',
                    display_name='Featured Article URL',
                    variable_type='url',
                    default_value='https://example.com/featured-article',
                    is_required=False,
                    description='URL for the featured article'
                ),
                TemplateVariable(
                    template=newsletter_template,
                    variable_name='company_name',
                    display_name='Company Name',
                    variable_type='text',
                    default_value='Our Company',
                    is_required=False,
                    description='Company name for footer'
                )
            ])
            self.stdout.write(self.style.SUCCESS('Created Newsletter Template'))
        else:
            self.stdout.write('Newsletter Template already exists')

        # Sample Template 3: Promotional Email
        promo_template, created = EmailTemplate.objects.get_or_create(
            name="Promotional Email Template",
            defaults={
                'description': 'An attractive promotional email template for sales and offers',
                'subject': '{{ offer_title|default:"Special Offer Just for You!" }}',
                'html_content': '''
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Special Offer</title>
    <style>
        body { font-family: 'Arial', sans-serif; line-height: 1.6; color: #333; }
        .container { max-width: 600px; margin: 0 auto; padding: 20px; }
        .header { background: linear-gradient(45deg, #ff6b6b, #ee5a24); color: white; padding: 30px; text-align: center; }
        .offer-badge { background-color: #ff4757; color: white; padding: 10px 20px; border-radius: 25px; display: inline-block; margin: 10px 0; }
        .content { padding: 20px; background-color: #ffffff; }
        .cta-section { text-align: center; padding: 30px; background-color: #f1f2f6; }
        .cta-button { display: inline-block; padding: 15px 30px; background: linear-gradient(45deg, #ff6b6b, #ee5a24); color: white; text-decoration: none; border-radius: 25px; font-size: 18px; font-weight: bold; }
        .footer { background-color: #2f3542; color: white; padding: 20px; text-align: center; font-size: 12px; }
        .price { font-size: 24px; color: #ff4757; font-weight: bold; }
        .original-price { text-decoration: line-through; color: #747d8c; }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>{{ offer_title|default:"Special Offer Just for You!" }}</h1>
            <div class="offer-badge">{{ discount_percentage|default:"50% OFF" }}</div>
        </div>
        <div class="content">
            <h2>Hello {{ name }}!</h2>
            <p>{{ personalized_message|default:"We have an exclusive offer that we think you'll love!" }}</p>
            
            <h3>{{ product_name|default:"Premium Product" }}</h3>
            <p>{{ product_description|default:"Get access to our premium features and take your experience to the next level." }}</p>
            
            <div style="text-align: center; margin: 20px 0;">
                <p class="original-price">${{ original_price|default:"99" }}</p>
                <p class="price">${{ discounted_price|default:"49" }}</p>
                <p><strong>Save {{ discount_amount|default:"$50" }}!</strong></p>
            </div>
            
            <p>{{ urgency_message|default:"This offer expires soon, so don't miss out!" }}</p>
        </div>
        <div class="cta-section">
            <a href="{{ cta_url|default:'#' }}" class="cta-button">{{ cta_text|default:"Claim Your Offer Now" }}</a>
        </div>
        <div class="footer">
            <p>© 2024 {{ company_name|default:"Our Company" }}. All rights reserved.</p>
            <p>Offer expires: {{ expiry_date|default:"December 31, 2024" }}</p>
            <p><a href="{{ unsubscribe_url|default:'#' }}" style="color: #fff;">Unsubscribe</a></p>
        </div>
    </div>
</body>
</html>
                ''',
                'css_styles': '''
body { font-family: 'Arial', sans-serif; line-height: 1.6; color: #333; }
.container { max-width: 600px; margin: 0 auto; padding: 20px; }
.header { background: linear-gradient(45deg, #ff6b6b, #ee5a24); color: white; padding: 30px; text-align: center; }
.offer-badge { background-color: #ff4757; color: white; padding: 10px 20px; border-radius: 25px; display: inline-block; margin: 10px 0; }
.content { padding: 20px; background-color: #ffffff; }
.cta-section { text-align: center; padding: 30px; background-color: #f1f2f6; }
.cta-button { display: inline-block; padding: 15px 30px; background: linear-gradient(45deg, #ff6b6b, #ee5a24); color: white; text-decoration: none; border-radius: 25px; font-size: 18px; font-weight: bold; }
.footer { background-color: #2f3542; color: white; padding: 20px; text-align: center; font-size: 12px; }
.price { font-size: 24px; color: #ff4757; font-weight: bold; }
.original-price { text-decoration: line-through; color: #747d8c; }
                ''',
                'is_active': True,
                'is_default': False
            }
        )
        
        if created:
            # Create variables for promotional template
            TemplateVariable.objects.bulk_create([
                TemplateVariable(
                    template=promo_template,
                    variable_name='name',
                    display_name='Recipient Name',
                    variable_type='text',
                    is_required=True,
                    description='The name of the recipient'
                ),
                TemplateVariable(
                    template=promo_template,
                    variable_name='offer_title',
                    display_name='Offer Title',
                    variable_type='text',
                    default_value='Special Offer Just for You!',
                    is_required=False,
                    description='Title of the promotional offer'
                ),
                TemplateVariable(
                    template=promo_template,
                    variable_name='discount_percentage',
                    display_name='Discount Percentage',
                    variable_type='text',
                    default_value='50% OFF',
                    is_required=False,
                    description='Discount percentage to display'
                ),
                TemplateVariable(
                    template=promo_template,
                    variable_name='personalized_message',
                    display_name='Personalized Message',
                    variable_type='text',
                    default_value="We have an exclusive offer that we think you'll love!",
                    is_required=False,
                    description='Personalized message for the recipient'
                ),
                TemplateVariable(
                    template=promo_template,
                    variable_name='product_name',
                    display_name='Product Name',
                    variable_type='text',
                    default_value='Premium Product',
                    is_required=False,
                    description='Name of the product being promoted'
                ),
                TemplateVariable(
                    template=promo_template,
                    variable_name='product_description',
                    display_name='Product Description',
                    variable_type='text',
                    default_value='Get access to our premium features and take your experience to the next level.',
                    is_required=False,
                    description='Description of the product'
                ),
                TemplateVariable(
                    template=promo_template,
                    variable_name='original_price',
                    display_name='Original Price',
                    variable_type='text',
                    default_value='99',
                    is_required=False,
                    description='Original price before discount'
                ),
                TemplateVariable(
                    template=promo_template,
                    variable_name='discounted_price',
                    display_name='Discounted Price',
                    variable_type='text',
                    default_value='49',
                    is_required=False,
                    description='Price after discount'
                ),
                TemplateVariable(
                    template=promo_template,
                    variable_name='cta_text',
                    display_name='Call-to-Action Text',
                    variable_type='text',
                    default_value='Claim Your Offer Now',
                    is_required=False,
                    description='Text for the call-to-action button'
                ),
                TemplateVariable(
                    template=promo_template,
                    variable_name='cta_url',
                    display_name='Call-to-Action URL',
                    variable_type='url',
                    default_value='https://example.com/claim-offer',
                    is_required=False,
                    description='URL for the call-to-action button'
                )
            ])
            self.stdout.write(self.style.SUCCESS('Created Promotional Email Template'))
        else:
            self.stdout.write('Promotional Email Template already exists')

        self.stdout.write(self.style.SUCCESS('Sample templates created successfully!'))
        self.stdout.write('You can now use these templates in your campaigns.') 