import os
from django.core.management.base import BaseCommand
from django.conf import settings
from mailer.models import EmailTemplate

class Command(BaseCommand):
    help = 'Populates the EmailTemplate table with HTML files from the templates directory'

    def handle(self, *args, **kwargs):
        templates_dir = os.path.join(settings.BASE_DIR, 'mailer', 'templates')
        self.stdout.write(f'Scanning for HTML templates in {templates_dir}...')

        for filename in os.listdir(templates_dir):
            if filename.endswith('.html'):
                template_path = os.path.join(templates_dir, filename)
                template_name = os.path.splitext(filename)[0]
                
                with open(template_path, 'r', encoding='utf-8') as f:
                    html_content = f.read()

                # Check if a template with the same name already exists
                if EmailTemplate.objects.filter(template_name=template_name).exists():
                    self.stdout.write(self.style.WARNING(f'Template "{template_name}" already exists. Skipping...'))
                    continue

                # Create and save the new template
                EmailTemplate.objects.create(
                    template_name=template_name,
                    subject='Default Subject',
                    html_content=html_content
                )
                self.stdout.write(self.style.SUCCESS(f'Successfully added template: {template_name}'))

        self.stdout.write(self.style.SUCCESS('Finished populating email templates.'))
