import openpyxl
from django.core.mail import send_mail
# from django.http import JsonResponse
from django.shortcuts import render
from django.db import transaction
# from django.http import HttpResponse
# from django.template import loader
from django.core.mail import send_mail
from django.template.loader import render_to_string
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser
from drf_spectacular.utils import extend_schema, OpenApiParameter
from drf_spectacular.types import OpenApiTypes
from .models import Email, Campaign
from .serializers import EmailSerializer, CampaignSerializer


# 1) view for listing existing campaigns - list it with id, name
# 2) view for adding new campaigns - user will provide campaign name and model will be created
# 3) view for editing existing campaigns - user will provide campaign name and model will be updated - later (optional)
# 4) view for deleting existing campaigns - user will provide campaign name and model will be deleted - later (optional)

# 5) view for uploading emails from XLS file - user will provide campaign id and XLS file and model will be created
# 6) view for listing emails - will list all emails in the database
# 7) view for sending emails - user will provide campaign id and model will send emails to all emails in the database with that campaign id
# 

class CampaignListView(APIView):
    @extend_schema(
        responses={
            200: CampaignSerializer(many=True),
            500: {"error": "Error message"}
        },
        description="List all existing campaigns.",
    )
    def get(self, request):
        try:
            campaigns = Campaign.objects.all()
            serializer = CampaignSerializer(campaigns, many=True)
            return Response(serializer.data)
        except Exception as e:
            return Response({"error": str(e)}, status=500)
        

class CampaignCreateView(APIView):
    @extend_schema(
        request=CampaignSerializer,
        responses={
            201: CampaignSerializer,
            500: {"error": "Error message"}
        },
        description="Create a new campaign.",
    )
    def post(self, request):
        try:
            serializer = CampaignSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=201)
            return Response(serializer.errors, status=400)
        except Exception as e:
            return Response({"error": str(e)}, status=500)


class CampaignUpdateView(APIView):
    @extend_schema(
        parameters=[
            OpenApiParameter(
                name="campaign_id",
                type=OpenApiTypes.INT,
                location=OpenApiParameter.PATH,
                description="Campaign ID",
            ),
        ],
        request=CampaignSerializer,
        responses={
            200: CampaignSerializer,
            500: {"error": "Error message"}
        },
        description="Update an existing campaign.",
    )
    def put(self, request):
        try:
            campaign_id = request.data.get('campaign_id')
            campaign = Campaign.objects.get(id=campaign_id)
            serializer = CampaignSerializer(campaign, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=400)
        except Campaign.DoesNotExist:
            return Response({"error": "Campaign not found"}, status=404)
        except Exception as e:
            return Response({"error": str(e)}, status=500)


class CampaignDeleteView(APIView):
    @extend_schema(
        parameters=[
            OpenApiParameter(
                name="campaign_id",
                type=OpenApiTypes.INT,
                location=OpenApiParameter.PATH,
                description="Campaign ID",
            ),
        ],
        responses={
            204: None,
            500: {"error": "Error message"}
        },
        description="Delete an existing campaign.",
    )
    def delete(self, request):
        try:
            campaign_id = request.data.get('campaign_id')
            campaign = Campaign.objects.get(id=campaign_id)
            campaign.delete()
            return Response(status=204)
        except Campaign.DoesNotExist:
            return Response({"error": "Campaign not found"}, status=404)
        except Exception as e:
            return Response({"error": str(e)}, status=500)
        

class XLSReaderView(APIView):
    parser_classes = [MultiPartParser]

    @extend_schema(
        parameters=[
            OpenApiParameter(
                name="campaign_id",
                type=OpenApiTypes.INT,
                location=OpenApiParameter.PATH,
                description="Campaign ID",
                required=True,
            ),
        ],
        request={
            'multipart/form-data': {
                'type': "object",
                'properties': {
                    'file': {'type': 'string', 'format': 'binary', 'description': 'XLS file to upload'}
                }
            }
        },
        responses={
            201: {"message": "Emails saved successfully!"}, 
            400: {"error": "Error message"}
        },
        description="Upload an XLS file to save email data into the database. The file should contain 'name' and 'email_address' columns.",
    )
    
    def post(self, request):
        file = request.FILES.get('file')
        campaign_id = request.query_params.get('campaign_id')

        if not file:
            return Response({"error": "No file uploaded"}, status=400)
        
        if not campaign_id:
            return Response({"error": "Campaign ID is required"}, status=400)
        
        # Validate file type
        if not file.name.endswith(('.xls', '.xlsx')):
            return Response({"error": "Unsupported file format. Please upload an Excel file."}, status=400)

        try:
            campaign = Campaign.objects.get(id=campaign_id)
        except Campaign.DoesNotExist:
            return Response({"error": "Invalid campaign ID"}, status=400)
        
        # Use openpyxl to read the Excel file
        try:
            wb = openpyxl.load_workbook(file)
            sheet = wb.active

            with transaction.atomic():
                # Iterate through the rows and insert emails into the database
                for row in sheet.iter_rows(min_row=2):  # Skipping header row
                    name = row[0].value
                    recipient_email = row[1].value
                    # message = row[2].value

                    # Validate row data
                    if not recipient_email:
                        raise ValueError(f"Invalid row data: {row}")
                    
                    # Save to the database
                    Email.objects.get_or_create(
                        email_address=recipient_email,
                        name=name
                        # subject=subject,
                        # message=message
                    )

            return Response({"message": "Emails saved successfully!"}, status=201)
        
        except ValueError as ve:
            return Response({"error": str(ve)}, status=400)

        except Exception as e:
            return Response({"error": str(e)}, status=500)


class SendEmailsView(APIView):
    @extend_schema(
        request=None,
        responses={
            200: {"message": "Emails sent successfully!", "details": "Number of emails sent and failed"},
            500: {"error": "Error message"}
        },
        description="Send emails to all recipients stored in the database.",
    )
    def post(self, request):
        emails = Email.objects.all()  # Fetch all emails from the database
        success_count = 0
        failure_count = 0
        
        MESSAGE = "Thank you for applying to the AUTOSAD Get Certified program. We’re excited to have you on board and look forward to helping you gain the knowledge and credentials to excel in the AUTOSAD ecosystem. To finalize your enrollment and start your certification journey, simply click the link below to complete your registration process."

        # Iterate through the emails and send them
        for email in emails:
            try:
                context = {
                    'name': email.name,
                    'message': MESSAGE,
                }
                html_content = render_to_string('autosad-temp-email.html', context) # context not added because there are not context variables in the html template
                send_mail(
                    subject='Sample Subject for now',
                    message='',
                    from_email='info@autosad.ai',
                    recipient_list=[email.email_address],
                    html_message=html_content
                )
                success_count += 1
            except Exception as e:
                failure_count += 1
                print(f"Failed to send email to {email.email_address}: {str(e)}")

        return Response({
            "message": "Emails sent successfully!",
            "details": {
                "sent": success_count,
                "failed": failure_count,
            }
        }, status=200 if failure_count == 0 else 500)


class ListEmailView(APIView):
    @extend_schema(
        responses={
            200: EmailSerializer(many=True),
            500: {"error": "Error message"}
        },
        description="List all emails stored in the database.",
    )
    def get(self, request):
        try:
            emails = Email.objects.all()
            serializer = EmailSerializer(emails, many=True)
            return Response(serializer.data)
        except Exception as e:
            return Response({"error": str(e)}, status=500)


# def home(request):
#     template = loader.get_template('autosad-email-template-new.html')
#     return HttpResponse(template.render())

# def intro(request):
#     return HttpResponse("Welcome to this django app.")
