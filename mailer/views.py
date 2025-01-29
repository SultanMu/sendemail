import openpyxl
from openpyxl.utils.exceptions import InvalidFileException
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
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiResponse, OpenApiExample
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
            500: OpenApiResponse(
                description="Server error",
                examples={
                    "application/json": {
                        "error": "Error message"
                    }
                }
            ),
        },
        description="List all existing campaigns.",
        examples=[
            OpenApiExample(
                "Example Response",
                value=[
                    {
                        "id": 1,
                        "name": "Holiday Sales Campaign",
                        "created_at": "2025-01-01T12:00:00Z",
                        "updated_at": "2025-01-02T08:00:00Z"
                    },
                    {
                        "id": 2,
                        "name": "Summer Discounts Campaign",
                        "created_at": "2025-01-10T14:00:00Z",
                        "updated_at": "2025-01-12T10:30:00Z"
                    }
                ]
            )
        ]
    )
    def get(self, request):
        try:
            campaigns = Campaign.objects.all().order_by("-created_at")
            serializer = CampaignSerializer(campaigns, many=True)
            return Response(serializer.data, status=200)
        except Exception as e:
            return Response({"error": str(e)}, status=500)
        

class CampaignCreateView(APIView):
    @extend_schema(
        request=CampaignSerializer,
        responses={
            201: CampaignSerializer,
            400: OpenApiResponse(
                description="Validation error details",
                examples={
                    "application/json": {
                        "error": "Validation error details"
                    }
                }
            ),
            500: OpenApiResponse(
                description="Server err",
                examples={
                    "application/json": {
                        "error": "Error message"
                    }
                }
            ),
        },
        description="Create a new campaign by providing the required details.",
        examples=[
            OpenApiExample(
                "Example Request",
                value={
                    "campaign_name": "Black Friday Campaign"
                },
                request_only=True,
            ),
            OpenApiExample(
                "Example Response",
                value={
                    "campaign_id": 1,
                    "campaign_name": "AutoSAD Marketing Campaign",
                    "created_at": "2025-01-27T10:00:00Z",
                    "updated_at": "2025-01-27T10:00:00Z",
                },
                response_only=True,
            ),
        ]
    )
    def post(self, request):
        try:
            serializer = CampaignSerializer(data=request.data)
            if serializer.is_valid():
                # Check if campaign with the same name already exists
                if Campaign.objects.filter(campaign_name=serializer.validated_data['campaign_name']).exists():
                    return Response({"error": "A campaign with this name already exists."}, status=400)
                
                serializer.save()
                return Response(serializer.data, status=201)
            
            return Response(serializer.errors, status=400)
        
        except Exception as e:
            return Response({"error": str(e)}, status=500)


# class CampaignUpdateView(APIView):
#     @extend_schema(
#         parameters=[
#             OpenApiParameter(
#                 name="campaign_id",
#                 type=OpenApiTypes.INT,
#                 location=OpenApiParameter.PATH,
#                 description="Campaign ID",
#             ),
#         ],
#         request=CampaignSerializer,
#         responses={
#             200: CampaignSerializer,
#             500: {"error": "Error message"}
#         },
#         description="Update an existing campaign.",
#     )
#     def put(self, request):
#         try:
#             campaign_id = request.data.get('campaign_id')
#             campaign = Campaign.objects.get(id=campaign_id)
#             serializer = CampaignSerializer(campaign, data=request.data)
#             if serializer.is_valid():
#                 serializer.save()
#                 return Response(serializer.data)
#             return Response(serializer.errors, status=400)
#         except Campaign.DoesNotExist:
#             return Response({"error": "Campaign not found"}, status=404)
#         except Exception as e:
#             return Response({"error": str(e)}, status=500)


# class CampaignDeleteView(APIView):
#     @extend_schema(
#         parameters=[
#             OpenApiParameter(
#                 name="campaign_id",
#                 type=OpenApiTypes.INT,
#                 location=OpenApiParameter.PATH,
#                 description="Campaign ID",
#             ),
#         ],
#         responses={
#             204: None,
#             500: {"error": "Error message"}
#         },
#         description="Delete an existing campaign.",
#     )
#     def delete(self, request):
#         try:
#             campaign_id = request.data.get('campaign_id')
#             campaign = Campaign.objects.get(id=campaign_id)
#             campaign.delete()
#             return Response(status=204)
#         except Campaign.DoesNotExist:
#             return Response({"error": "Campaign not found"}, status=404)
#         except Exception as e:
#             return Response({"error": str(e)}, status=500)
        

class XLSReaderView(APIView):
    parser_classes = [MultiPartParser]

    @extend_schema(
        request={
            'multipart/form-data': {
                'type': "object",
                'properties': {
                    'file': {'type': 'string', 'format': 'binary', 'description': "Excel file containing email data."}
                }
            }
        },
        parameters=[
            OpenApiParameter("campaign_id", type=int, location="query", required=True, description="ID of the campaign to associate the emails with.")
        ],
        responses={
            201: OpenApiResponse(
                    description="Emails saved successfully!",
                    examples={
                        "application/json": {
                            "message": "Emails saved successfully!"
                        }
                    }
                ),
            400: OpenApiResponse(
                    description="Error in file format, missing data, or invalid campaign ID.",
                    examples={
                        "application/json": {
                            "error": "Error message"
                        }
                    }
                ),
            500: OpenApiResponse(
                    description="Server-side error.",
                    examples={
                        "application/json": {
                            "error": "Error message"
                        }
                    }
                ),
        },
        description=(
            "Upload an Excel file to save email data into the database. "
            "The file should contain 'name' and 'email_address' columns. "
            "Provide a valid campaign ID as a query parameter to associate the emails with a campaign."
        ),
        examples=[
            OpenApiExample(
                "Example Request",
                value={
                    "file": "(binary file data here)",
                },
                request_only=True,
            ),
            OpenApiExample(
                "Example Response",
                value={
                    "message": "Emails saved successfully!"
                },
                response_only=True,
            ),
        ],
    )
    def post(self, request):
        file = request.FILES.get('file')
        campaign_id = request.query_params.get('campaign_id')

        # Step 1: Validate campaign ID
        if not campaign_id:
            return Response({"error": "Campaign ID is required as a query parameter."}, status=400)

        try:
            campaign_id = int(campaign_id)
            campaign = Campaign.objects.get(campaign_id=campaign_id)
        except ValueError:
            return Response({"error": "Campaign ID must be an integer."}, status=400)
        except Campaign.DoesNotExist:
            return Response({"error": "Invalid Campaign ID. Campaign not found."}, status=400)

        # Step 2: Validate file upload
        if not file:
            return Response({"error": "No file uploaded. Please provide an Excel file."}, status=400)

        if not file.name.endswith((".xls", ".xlsx", ".csv")):
            return Response({"error": "Unsupported file format. Please upload an Excel file."}, status=400)

        
        # Use openpyxl to read the Excel file
        try:
            # Step 3: Process the Excel file
            wb = openpyxl.load_workbook(file)
            sheet = wb.active

            emails_to_save = []
            invalid_rows = []

            for row_number, row in enumerate(sheet.iter_rows(min_row=2), start=2):  # Start from the second row
                name = row[0].value
                recipient_email = row[1].value

                # Row validation
                if not recipient_email or "@" not in recipient_email:
                    invalid_rows.append({"row": row_number, "error": "Invalid or missing email address."})
                    continue

                # Prepare the data for bulk create
                emails_to_save.append(
                    Email(
                        campaign_id=campaign,
                        name=name,
                        email_address=recipient_email,
                    )
                )

            # Step 4: Save emails to the database
            with transaction.atomic():
                Email.objects.bulk_create(emails_to_save)
                
            if invalid_rows:
                return Response(
                    {
                        "message": f"Emails saved successfully, but some rows were invalid.",
                        "invalid_rows": invalid_rows,
                    },
                    status=201,
                )

            return Response({"message": "Emails saved successfully!"}, status=201)
        
        except InvalidFileException:
            return Response({"error": "Invalid Excel file. Please upload a valid Excel file."}, status=400)

        except Exception as e:
            return Response({"error": str(e)}, status=500)


class SendEmailsView(APIView):
    @extend_schema(
        parameters=[
            OpenApiParameter("campaign_id", type=int, location="query", required=True, description="ID of the campaign to send emails for.")
        ],
        request={
            'application/json': {
                'type': 'object',
                'properties': {
                    'message': {
                        'type': 'string',
                        'description': "Custom message to send in the email (optional). If not provided, the default message will be used."
                    }
                },
                'example': {
                    'message': "Thank you for applying to our program! We're thrilled to have you on board.",
                },
            }
        },
        responses={
            200: OpenApiResponse(
                description="Emails processed successfully.",
                examples={
                    "application/json": {
                        "message": "Emails processed.",
                        "details": {"sent": 10, "failed": 2},
                        "custom_message_used": "Thank you for applying to the AUTOSAD Get Certified program. We're thrilled to have you on board and look forward to helping you gain the knowledge and credentials to excel in the AUTOSAD ecosystem. To finalize your enrollment and start your certification journey, simply click the link below to complete your registration process."
                    }
                }
            ),
            400: OpenApiResponse(
                description="Invalid or missing campaign ID.",
                examples={
                    "application/json": {
                        "error": "Invalid or missing campaign ID."
                    }
                }
            ),
            404: OpenApiResponse(
                description="No emails found for the given campaign.",
                examples={
                    "application/json": {
                        "error": "No emails found for the given campaign."
                    }
                }
            ),
            500: OpenApiResponse(
                description="Internal server error.",
                examples={
                    "application/json": {
                        "error": "Internal server error."
                    }
                }
            )
        },
        description="Send emails to all recipients associated with a specific campaign. Optionally provide a custom message."
    )
    def post(self, request):
        # Get campaign ID from query parameters
        campaign_id = request.query_params.get("campaign_id")
        
        if not campaign_id:
            return Response({"error": "Campaign ID is required."}, status=400)
        
        try:
            campaign = Campaign.objects.get(campaign_id=campaign_id)
        except Campaign.DoesNotExist:
            return Response({"error": "Campaign not found."}, status=404)
        
        emails = Email.objects.filter(campaign_id=campaign)

        if not emails.exists():
            return Response({"error": "No emails found for the given campaign."}, status=404)
        
        # Get the custom message from the request, or use the default
        custom_message = request.data.get('message')

        if not custom_message:
            custom_message = "Thank you for applying to the AUTOSAD Get Certified program. We're thrilled to have you on board and look forward to helping you gain the knowledge and credentials to excel in the AUTOSAD ecosystem. To finalize your enrollment and start your certification journey, simply click the link below to complete your registration process."
        success_count = 0
        failure_count = 0

        # Iterate through the emails and send them
        for email in emails:
            try:
                context = {
                    'name': email.name,
                    'message': custom_message,
                }
                
                html_content = render_to_string('autosad-temp-email.html', context) # context not added because there are not context variables in the html template
                
                send_mail(
                    subject='Welcome to AUTOSAD Get Certified',
                    message='',
                    from_email='info@autosad.ai',
                    recipient_list=[email.email_address],
                    html_message=html_content
                )
                success_count += 1
            
            except Exception as e:
                failure_count += 1
                # print(f"Failed to send email to {email.email_address}: {str(e)}")

        return Response({
            "message": "Emails sent successfully!",
            "details": {
                "sent": success_count,
                "failed": failure_count,
            },
            "custom_message_used": custom_message,
        }, status=200 if failure_count == 0 else 207) # 207: Multi-Status for partial success


class ListEmailView(APIView):
    @extend_schema(
        parameters=[
            OpenApiParameter("campaign_id", type=int, location="query", required=True, description="ID of the campaign to list emails for.")
        ],
        responses={
            200: OpenApiResponse(
                description="List of emails associated with the given campaign.",
                examples={
                    "application/json": [
                        {
                            "email_address": "john.doe@example.com",
                            "name": "John Doe",
                            "campaign_id": 1,
                            "added_at": "2025-01-01T12:00:00Z"
                        },
                        {
                            "email_address": "jane.smith@example.com",
                            "name": "Jane Smith",
                            "campaign_id": 2,
                            "added_at": "2025-01-10T14:00:00Z"
                        }
                    ]
                }
            ),
            400: OpenApiResponse(
                description="Invalid or missing campaign ID.",
                examples={
                    "application/json": {"error": "Invalid or missing campaign ID."}
                }
            ),
            404: OpenApiResponse(
                description="No emails found for the given campaign.",
                examples={
                    "application/json": {"error": "No emails found for the given campaign."}
                }
            ),
            500: OpenApiResponse(
                description="Internal server error.",
                examples={
                    "application/json": {"error": "Internal server error."}
                }
            ),
        },
        description="List all emails stored in the database for a specific campaign.",
    )
    def get(self, request):
        # Get campaign ID from query parameters
        campaign_id = request.query_params.get("campaign_id")
        
        if not campaign_id:
            return Response({"error": "Campaign ID is required."}, status=400)
        
        try:
            campaign = Campaign.objects.get(campaign_id=campaign_id)
        except Campaign.DoesNotExist:
            return Response({"error": "Campaign not found."}, status=404)
        
        try:
            emails = Email.objects.filter(campaign_id=campaign)
        
            if not emails.exists():
                return Response({"error": "No emails found for the given campaign."}, status=404)
        
            serializer = EmailSerializer(emails, many=True)
            return Response(serializer.data, status=200)
        except Exception as e:
            return Response({"error": str(e)}, status=500)
       

# def home(request):
#     template = loader.get_template('autosad-email-template-new.html')
#     return HttpResponse(template.render())

# def intro(request):
#     return HttpResponse("Welcome to this django app.")
