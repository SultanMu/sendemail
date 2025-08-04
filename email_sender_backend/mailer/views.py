import openpyxl
from openpyxl.utils.exceptions import InvalidFileException
from django.core.mail import send_mail
from django.shortcuts import render
from django.db import transaction
from django.core.mail import send_mail, send_mass_mail
from django.template.loader import render_to_string
from django.template import Template, Context
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser
from drf_spectacular.utils import (
    extend_schema,
    OpenApiParameter,
    OpenApiResponse,
    OpenApiExample,
    OpenApiRequest,
)
from drf_spectacular.types import OpenApiTypes
from .models import Email, Campaign, EmailTemplate
from .serializers import EmailSerializer, CampaignSerializer, EmailTemplateSerializer
from django.conf import settings


class CampaignCreateView(APIView):
    @extend_schema(
        request=CampaignSerializer,
        responses={201: CampaignSerializer, 400: OpenApiResponse(description="Bad Request")},
        description="Create a new campaign",
    )
    def post(self, request):
        try:
            serializer = CampaignSerializer(data=request.data)
            if serializer.is_valid():
                campaign = serializer.save()
                return Response(serializer.data, status=201)
            return Response(serializer.errors, status=400)
        except Exception as e:
            return Response({"error": str(e)}, status=500)


class UpdateCampaignView(APIView):
    def post(self, request):
        try:
            campaign_id = request.GET.get('campaign_id')
            campaign_name = request.GET.get('campaign_name')

            if not campaign_id or not campaign_name:
                return Response({"error": "campaign_id and campaign_name are required"}, status=400)

            campaign = Campaign.objects.get(id=campaign_id)
            campaign.name = campaign_name
            campaign.save()

            serializer = CampaignSerializer(campaign)
            return Response(serializer.data, status=200)
        except Campaign.DoesNotExist:
            return Response({"error": "Campaign not found"}, status=404)
        except Exception as e:
            return Response({"error": str(e)}, status=500)


class DeleteCampaignView(APIView):
    def post(self, request):
        try:
            campaign_id = request.GET.get('campaign_id')

            if not campaign_id:
                return Response({"error": "campaign_id is required"}, status=400)

            campaign = Campaign.objects.get(id=campaign_id)
            campaign.delete()

            return Response({"message": "Campaign deleted successfully"}, status=200)
        except Campaign.DoesNotExist:
            return Response({"error": "Campaign not found"}, status=404)
        except Exception as e:
            return Response({"error": str(e)}, status=500)


class ListEmailView(APIView):
    def get(self, request):
        try:
            campaign_id = request.GET.get('campaign_id')

            if not campaign_id:
                return Response({"error": "campaign_id is required"}, status=400)

            emails = Email.objects.filter(campaign_id=campaign_id)
            serializer = EmailSerializer(emails, many=True)
            return Response(serializer.data, status=200)
        except Exception as e:
            return Response({"error": str(e)}, status=500)


class XLSReaderView(APIView):
    parser_classes = [MultiPartParser]

    def post(self, request):
        try:
            campaign_id = request.GET.get('campaign_id')
            file = request.FILES.get('file')

            if not campaign_id or not file:
                return Response({"error": "campaign_id and file are required"}, status=400)

            campaign = Campaign.objects.get(id=campaign_id)

            # Process Excel file
            workbook = openpyxl.load_workbook(file)
            sheet = workbook.active

            emails_created = 0
            for row in sheet.iter_rows(min_row=2, values_only=True):
                if row[0]:  # Assuming email is in first column
                    email_address = str(row[0]).strip()
                    name = str(row[1]).strip() if len(row) > 1 and row[1] else ""

                    Email.objects.get_or_create(
                        email_address=email_address,
                        campaign=campaign,
                        defaults={'name': name}
                    )
                    emails_created += 1

            return Response({"message": f"{emails_created} emails processed"}, status=200)
        except Campaign.DoesNotExist:
            return Response({"error": "Campaign not found"}, status=404)
        except Exception as e:
            return Response({"error": str(e)}, status=500)


class SendEmailsView(APIView):
    @extend_schema(
        parameters=[
            OpenApiParameter(
                "campaign_id",
                type=int,
                location="query",
                required=True,
                description="ID of the campaign to send emails for.",
            ),
            OpenApiParameter(
                "template_id",
                type=int,
                location="query",
                required=True,
                description="ID of the email template to use.",
            ),
        ],
        request={
            "application/json": {
                "type": "object",
                "properties": {
                    "message": {
                        "type": "string",
                        "description": "Custom message to send in the email (optional).",
                    }
                },
            }
        },
        responses={200: OpenApiResponse(description="Emails sent successfully.")},
    )
    def post(self, request):
        campaign_id = request.query_params.get("campaign_id")
        template_id = request.query_params.get("template_id")

        if not campaign_id:
            return Response({"error": "Campaign ID is required."}, status=400)
        if not template_id:
            return Response({"error": "Template ID is required."}, status=400)

        try:
            campaign = Campaign.objects.get(campaign_id=campaign_id)
            template = EmailTemplate.objects.get(template_id=template_id)
        except Campaign.DoesNotExist:
            return Response({"error": "Campaign not found."}, status=404)
        except EmailTemplate.DoesNotExist:
            return Response({"error": "Template not found."}, status=404)

        emails = Email.objects.filter(campaign_id=campaign)
        if not emails.exists():
            return Response({"error": "No emails found for the given campaign."}, status=404)

        custom_message = request.data.get("message", "")
        success_count = 0
        failure_count = 0

        for email in emails:
            try:
                context = {"name": email.name or "Valued Customer", "message": custom_message}
                
                # Render the HTML content from the database
                template_string = Template(template.html_content)
                html_content = template_string.render(Context(context))

                send_mail(
                    subject=template.subject,
                    message="",
                    from_email=settings.EMAIL_HOST_USER,
                    recipient_list=[email.email_address],
                    html_message=html_content,
                )
                success_count += 1
            except Exception as e:
                failure_count += 1
                print(f"Failed to send email to {email.email_address}: {str(e)}")

        return Response(
            {
                "message": "Emails processed.",
                "details": {"sent": success_count, "failed": failure_count},
            },
            status=200 if failure_count == 0 else 207,
        )


class DeleteEmailView(APIView):
    def post(self, request):
        try:
            email_address = request.GET.get('email_add')
            campaign_id = request.GET.get('campaign_id')

            if not email_address or not campaign_id:
                return Response({"error": "email_add and campaign_id are required"}, status=400)

            email = Email.objects.get(email_address=email_address, campaign_id=campaign_id)
            email.delete()

            return Response({"message": "Email deleted successfully"}, status=200)
        except Email.DoesNotExist:
            return Response({"error": "Email not found"}, status=404)
        except Exception as e:
            return Response({"error": str(e)}, status=500)


class UpdateEmailView(APIView):
    def post(self, request):
        try:
            email_address = request.GET.get('email_add')
            campaign_id = request.GET.get('campaign_id')
            new_name = request.data.get('name', '')

            if not email_address or not campaign_id:
                return Response({"error": "email_add and campaign_id are required"}, status=400)

            email = Email.objects.get(email_address=email_address, campaign_id=campaign_id)
            email.name = new_name
            email.save()

            serializer = EmailSerializer(email)
            return Response(serializer.data, status=200)
        except Email.DoesNotExist:
            return Response({"error": "Email not found"}, status=404)
        except Exception as e:
            return Response({"error": str(e)}, status=500)


class CampaignListView(APIView):
    @extend_schema(
        responses={200: CampaignSerializer(many=True)},
        description="List all existing campaigns.",
    )
    def get(self, request):
        try:
            campaigns = Campaign.objects.all().order_by("-created_at")
            serializer = CampaignSerializer(campaigns, many=True)
            return Response(serializer.data, status=200)
        except Exception as e:
            return Response({"error": str(e)}, status=500)


class EmailTemplateCreateView(APIView):
    @extend_schema(
        request=EmailTemplateSerializer,
        responses={201: EmailTemplateSerializer},
        description="Create a new email template.",
    )
    def post(self, request):
        serializer = EmailTemplateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


class EmailTemplateListView(APIView):
    @extend_schema(
        responses={200: EmailTemplateSerializer(many=True)},
        description="Get all available email templates from the database.",
    )
    def get(self, request):
        try:
            templates = EmailTemplate.objects.all().order_by('-created_at')
            serializer = EmailTemplateSerializer(templates, many=True)
            return Response(serializer.data, status=200)
        except Exception as e:
            return Response({"error": str(e)}, status=500)


class EmailTemplatePreviewView(APIView):
    @extend_schema(
        parameters=[
            OpenApiParameter(
                "template_id",
                type=int,
                location="query",
                required=True,
                description="ID of the template to preview.",
            )
        ],
        responses={200: OpenApiResponse(description="Email template HTML content.")},
    )
    def get(self, request):
        template_id = request.query_params.get("template_id")
        if not template_id:
            return Response({"error": "Template ID is required"}, status=400)

        try:
            template = EmailTemplate.objects.get(template_id=template_id)
            
            # Prepare a sample context for rendering
            context = {
                "name": "John Doe",
                "message": "This is a sample message for the template preview."
            }

            # Render the HTML content from the database
            template_string = Template(template.html_content)
            html_content = template_string.render(Context(context))
            
            return Response({
                "template_name": template.template_name,
                "subject": template.subject,
                "html_content": html_content
            }, status=200)
        except EmailTemplate.DoesNotExist:
            return Response({"error": "Template not found"}, status=404)
        except Exception as e:
            return Response({"error": f"An error occurred: {str(e)}"}, status=500)

