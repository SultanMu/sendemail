import openpyxl
from openpyxl.utils.exceptions import InvalidFileException
from django.core.mail import send_mail

# from django.http import JsonResponse
from django.shortcuts import render
from django.db import transaction

# from django.http import HttpResponse
# from django.template import loader
from django.core.mail import send_mail, send_mass_mail
from django.template.loader import render_to_string
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
from .models import Email, Campaign
from .serializers import EmailSerializer, CampaignSerializer
from django.conf import settings
from .models import EmailTemplate
from .serializers import EmailTemplateSerializer, EmailTemplateCreateSerializer, TemplatePreviewSerializer, CampaignDetailSerializer, EmailTemplateUpdateSerializer
from django.db import models

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
            200: CampaignDetailSerializer(many=True),
            500: OpenApiResponse(
                description="Server error",
                examples={"application/json": {"error": "Error message"}},
            ),
        },
        description="List all existing campaigns with template information.",
        examples=[
            OpenApiExample(
                "Example Response",
                value=[
                    {
                        "campaign_id": 1,
                        "campaign_name": "Holiday Sales Campaign",
                        "created_at": "2025-01-01T12:00:00Z",
                        "updated_at": "2025-01-02T08:00:00Z",
                        "custom_template": None,
                        "custom_template_id": None,
                        "custom_subject": "",
                        "custom_message": "",
                        "use_custom_template": False,
                    },
                    {
                        "campaign_id": 2,
                        "campaign_name": "Summer Discounts Campaign",
                        "created_at": "2025-01-10T14:00:00Z",
                        "updated_at": "2025-01-12T10:30:00Z",
                        "custom_template": {
                            "template_id": 1,
                            "name": "Welcome Template",
                            "description": "Welcome email template",
                            "subject": "Welcome!",
                            "html_content": "<html>...</html>",
                            "css_styles": "",
                            "is_active": True,
                            "is_default": False,
                            "created_at": "2025-01-01T00:00:00Z",
                            "updated_at": "2025-01-01T00:00:00Z",
                            "template_variables": [],
                            "variables_count": 0,
                        },
                        "custom_template_id": 1,
                        "custom_subject": "Welcome to Summer Discounts!",
                        "custom_message": "Enjoy our summer discounts!",
                        "use_custom_template": True,
                    },
                ],
            )
        ],
    )
    def get(self, request):
        try:
            campaigns = Campaign.objects.all().order_by("-created_at")
            serializer = CampaignDetailSerializer(campaigns, many=True)
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
                examples={"application/json": {"error": "Validation error details"}},
            ),
            500: OpenApiResponse(
                description="Server err",
                examples={"application/json": {"error": "Error message"}},
            ),
        },
        description="Create a new campaign by providing the required details.",
        examples=[
            OpenApiExample(
                "Example Request",
                value={"campaign_name": "Black Friday Campaign"},
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
        ],
    )
    def post(self, request):
        try:
            serializer = CampaignSerializer(data=request.data)
            if serializer.is_valid():
                # Check if campaign with the same name already exists
                if Campaign.objects.filter(
                    campaign_name=serializer.validated_data["campaign_name"]
                ).exists():
                    return Response(
                        {"error": "A campaign with this name already exists."},
                        status=400,
                    )

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
            "multipart/form-data": {
                "type": "object",
                "properties": {
                    "file": {
                        "type": "string",
                        "format": "binary",
                        "description": "Excel file containing email data.",
                    }
                },
            }
        },
        parameters=[
            OpenApiParameter(
                "campaign_id",
                type=int,
                location="query",
                required=True,
                description="ID of the campaign to associate the emails with.",
            )
        ],
        responses={
            201: OpenApiResponse(
                description="Emails saved successfully!",
                examples={
                    "application/json": {"message": "Emails saved successfully!"}
                },
            ),
            400: OpenApiResponse(
                description="Error in file format, missing data, or invalid campaign ID.",
                examples={"application/json": {"error": "Error message"}},
            ),
            400: OpenApiResponse(
                description="Email already exists in database.",
                examples={"application/json": {"error": "Error message"}},
            ),
            500: OpenApiResponse(
                description="Server-side error.",
                examples={"application/json": {"error": "Error message"}},
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
                value={"message": "Emails saved successfully!"},
                response_only=True,
            ),
        ],
    )
    def post(self, request):
        file = request.FILES.get("file")
        campaign_id = request.query_params.get("campaign_id")

        # Step 1: Validate campaign ID
        if not campaign_id:
            return Response(
                {"error": "Campaign ID is required as a query parameter."}, status=400
            )

        try:
            campaign_id = int(campaign_id)
            campaign = Campaign.objects.get(campaign_id=campaign_id)
        except ValueError:
            return Response({"error": "Campaign ID must be an integer."}, status=400)
        except Campaign.DoesNotExist:
            return Response(
                {"error": "Invalid Campaign ID. Campaign not found."}, status=400
            )

        # Step 2: Validate file upload
        if not file:
            return Response(
                {"error": "No file uploaded. Please provide an Excel file."}, status=400
            )

        if not file.name.endswith((".xls", ".xlsx", ".csv")):
            return Response(
                {"error": "Unsupported file format. Please upload an Excel file."},
                status=400,
            )

        # Use openpyxl to read the Excel file
        try:
            # Step 3: Process the Excel file
            wb = openpyxl.load_workbook(file)
            sheet = wb.active

            emails_to_save = []
            invalid_rows = []
            duplicate_email = []

            # using a HashSet to query once (O(1)) instead of multiple queries (O(n)) in the loop.
            # changable in the future
            existing_emails = set(
                Email.objects.filter(campaign_id=campaign).values_list(
                    "email_address", flat=True
                )
            )

            for row_number, row in enumerate(
                sheet.iter_rows(min_row=2), start=2
            ):  # Start from the second row
                name = row[0].value
                recipient_email = row[1].value

                # Row validation
                if not recipient_email or "@" not in recipient_email:
                    invalid_rows.append(
                        {
                            "row": row_number,
                            "error": "Invalid or missing email address.",
                        }
                    )
                    continue

                # Skip if email already exists
                if recipient_email in existing_emails:
                    duplicate_email.append(recipient_email)
                    continue  # skips the email if its already there :)

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

            if len(duplicate_email) != 0:
                return Response(
                    {
                        "message": f"Emails saved successfully, but some emails already exists in database under campaign ID {campaign_id}",
                        "duplicate email count": len(duplicate_email),
                        "duplicate emails": duplicate_email,
                    },
                    status=201,
                )

            return Response({"message": "Emails saved successfully!"}, status=201)

        except InvalidFileException:
            return Response(
                {"error": "Invalid Excel file. Please upload a valid Excel file."},
                status=400,
            )

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
                "email_template",
                type=int,
                location="query",
                required=True,
                description="Enter 1 for AutoSAD template or 2 for XCV AI template or 3 for AutoSAD.V2 or 4 for AutoSAD.V3 template",
                enum=["AutoSAD v1", "AutoSAD v2", "AutoSAD v3", "XCV AI"],
            ),
        ],
        request={
            "application/json": {
                "type": "object",
                "properties": {
                    "message": {
                        "type": "string",
                        "description": "Custom message to send in the email (optional). If not provided, the default message will be used.",
                    }
                },
                "example": {
                    "message": "Thank you for applying to the AUTOSAD Get Certified program. We're thrilled to have you on board and look forward to helping you gain the knowledge and credentials to excel in the AUTOSAD ecosystem. To finalize your enrollment and start your certification journey, simply click the link below to complete your registration process.",
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
                        "custom_message_used": "Thank you for applying to the AUTOSAD Get Certified program. We're thrilled to have you on board and look forward to helping you gain the knowledge and credentials to excel in the AUTOSAD ecosystem. To finalize your enrollment and start your certification journey, simply click the link below to complete your registration process.",
                    }
                },
            ),
            400: OpenApiResponse(
                description="Invalid or missing campaign ID.",
                examples={
                    "application/json": {"error": "Invalid or missing campaign ID."}
                },
            ),
            404: OpenApiResponse(
                description="No emails found for the given campaign.",
                examples={
                    "application/json": {
                        "error": "No emails found for the given campaign."
                    }
                },
            ),
            500: OpenApiResponse(
                description="Internal server error.",
                examples={"application/json": {"error": "Internal server error."}},
            ),
        },
        description="Send emails to all recipients associated with a specific campaign. Optionally provide a custom message.\n (Make sure the email list is uploaded for specific campaign ID before sending emails)",
    )
    def post(self, request):
        # Get campaign ID from query parameters
        campaign_id = request.query_params.get("campaign_id")
        email_template = request.query_params.get("email_template")

        if not campaign_id:
            return Response({"error": "Campaign ID is required."}, status=400)

        if not email_template:
            return Response({"error": "Email Template is required."}, status=400)

        try:
            campaign = Campaign.objects.get(campaign_id=campaign_id)
        except Campaign.DoesNotExist:
            return Response({"error": "Campaign not found."}, status=404)

        emails = Email.objects.filter(campaign_id=campaign)

        if not emails.exists():
            return Response(
                {"error": "No emails found for the given campaign."}, status=404
            )

        # Get the custom message from the request, or use the default
        custom_message = request.data.get("message")

        if not custom_message:
            custom_message = "Thank you for applying to the AUTOSAD Get Certified program. We're thrilled to have you on board and look forward to helping you gain the knowledge and credentials to excel in the AUTOSAD ecosystem. To finalize your enrollment and start your certification journey, simply click the link below to complete your registration process."
        success_count = 0
        failure_count = 0

        try:
            if email_template == "1":
                from_email = "autosad-temp-email.html"
                subject = "Welcome to AUTOSAD Get Certified"
            elif email_template == "2":
                from_email = "XCV_AI.html"
                subject = "Welcome onboard to XCV AI"
            elif email_template == "3":
                from_email = "autosad-temp-email2.html"
                subject = "Welcome to AUTOSAD Get Certified"
            elif email_template == "4":
                from_email = "autosad-email-temp-3.html"
                subject = "Welcome to AUTOSAD"

        except:
            return Response({"error": "Error. Template not found."}, status=400)

        for email in emails:
            try:
                context = {
                    "name": email.name,
                    "message": custom_message,
                }

                html_content = render_to_string(from_email, context)

                send_mail(
                    subject=subject,
                    message="",
                    from_email="info@autosad.ai",
                    recipient_list=[email.email_address],
                    html_message=html_content,
                )
                success_count += 1

            except Exception as e:
                failure_count += 1
                print(f"Failed to send email to {email.email_address}: {str(e)}")

        # for later purpose.

        # context = {'name': email.name, 'message': custom_message}
        # html_content = render_to_string(from_email, context)
        # email_msg = email.EmailMessage(
        #     subject,
        #     html_content,
        #     'info@autosad.ai',
        #     [email.email_address],
        #     connection=connection,  # Reuse connection here
        # )
        # email_msg.content_subtype = 'html'
        # email_msg.send()

        return Response(
            {
                "message": "Emails sent successfully!",
                "details": {
                    "sent": success_count,
                    "failed": failure_count,
                },
                "custom_message_used": custom_message,
            },
            status=200 if failure_count == 0 else 207,
        )  # 207: Multi-Status for partial success


class ListEmailView(APIView):
    @extend_schema(
        parameters=[
            OpenApiParameter(
                "campaign_id",
                type=int,
                location="query",
                required=True,
                description="ID of the campaign to list emails for.",
            )
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
                            "added_at": "2025-01-01T12:00:00Z",
                        },
                        {
                            "email_address": "jane.smith@example.com",
                            "name": "Jane Smith",
                            "campaign_id": 2,
                            "added_at": "2025-01-10T14:00:00Z",
                        },
                    ]
                },
            ),
            400: OpenApiResponse(
                description="Invalid or missing campaign ID.",
                examples={
                    "application/json": {"error": "Invalid or missing campaign ID."}
                },
            ),
            404: OpenApiResponse(
                description="No emails found for the given campaign.",
                examples={
                    "application/json": {
                        "error": "No emails found for the given campaign."
                    }
                },
            ),
            500: OpenApiResponse(
                description="Internal server error.",
                examples={"application/json": {"error": "Internal server error."}},
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
                return Response(
                    {"error": "No emails found for the given campaign."}, status=404
                )

            serializer = EmailSerializer(emails, many=True)
            return Response(serializer.data, status=200)
        except Exception as e:
            return Response({"error": str(e)}, status=500)


class UpdateCampaignView(APIView):
    @extend_schema(
        parameters=[
            OpenApiParameter(
                "campaign_id",
                type=int,
                location="query",
                required=True,
                description="ID of the campaign to update.",
            ),
            OpenApiParameter(
                "campaign_name",
                type=str,
                location="query",
                required=True,
                description="New Campaign Name",
            ),
        ],
        responses={
            200: OpenApiResponse(
                description="Campaign name updated successfully.",
                examples={
                    "application/json": {
                        "campaign_id": 1,
                        "campaign_name": "Updated Campaign Name",
                        "created_at": "2025-01-27T10:00:00Z",
                        "updated_at": "2025-01-27T12:00:00Z",
                    }
                },
            ),
            400: OpenApiResponse(
                description="Invalid request or missing campaign ID.",
                examples={
                    "application/json": {"error": "Invalid or missing campaign ID."}
                },
            ),
            404: OpenApiResponse(
                description="Campaign not found.",
                examples={"application/json": {"error": "Campaign not found."}},
            ),
            500: OpenApiResponse(
                description="Internal server error.",
                examples={"application/json": {"error": "Internal server error."}},
            ),
        },
        description="Update the name of a specific campaign in the database.",
    )
    def post(self, request):
        campaign_id = request.query_params.get("campaign_id")
        updated_campaign_name = request.query_params.get("campaign_name")

        if not campaign_id or not updated_campaign_name:
            return Response(
                {"error": "Campaign ID and new campaign name are required."}, status=400
            )

        try:
            campaign = Campaign.objects.get(campaign_id=campaign_id)
        except Campaign.DoesNotExist:
            return Response({"error": "Campaign not found."}, status=404)

        try:
            campaign.campaign_name = updated_campaign_name
            campaign.save()

            return Response(
                {
                    "campaign_id": campaign.campaign_id,
                    "campaign_name": campaign.campaign_name,
                    "created_at": campaign.created_at,
                    "updated_at": campaign.updated_at,
                },
                status=200,
            )
        except Exception as e:
            return Response({"error": str(e)}, status=500)


class DeleteCampaignView(APIView):
    @extend_schema(
        parameters=[
            OpenApiParameter(
                "campaign_id",
                type=int,
                location="query",
                required=False,
                description="ID of the campaign to delete.",
            )
        ],
        responses={
            200: OpenApiResponse(
                description="Campaign deleted successfully.",
                examples={
                    "application/json": {
                        "message": "Campaign and associated emails deleted successfully.",
                        "campaign_id": 1,
                    }
                },
            ),
            400: OpenApiResponse(
                description="Invalid request or missing campaign ID.",
                examples={
                    "application/json": {"error": "Invalid or missing campaign ID."}
                },
            ),
            404: OpenApiResponse(
                description="Campaign not found.",
                examples={"application/json": {"error": "Campaign not found."}},
            ),
            500: OpenApiResponse(
                description="Internal server error.",
                examples={"application/json": {"error": "Internal server error."}},
            ),
        },
        description="Delete a specific campaign and all its associated emails from the database.",
    )
    def post(self, request):
        campaign_id = request.query_params.get("campaign_id")

        if not campaign_id:
            return Response({"error": "Campaign ID is required."}, status=400)

        try:
            campaign = Campaign.objects.get(campaign_id=campaign_id)
        except Campaign.DoesNotExist:
            return Response({"error": "Campaign not found."}, status=404)

        try:
            campaign = Campaign.objects.get(campaign_id=campaign_id)
        except Campaign.DoesNotExist:
            return Response({"error": "Campaign not found."}, status=404)

        try:
            campaign.delete()

            return Response(
                {
                    "message": "Campaign and associated emails deleted successfully.",
                    "campaign_id": campaign_id,
                },
                status=200,
            )

        except Exception as e:
            return Response({"error": str(e)}, status=500)


class DeleteEmailView(APIView):
    @extend_schema(
        parameters=[
            OpenApiParameter(
                "email_add",
                type=str,
                location="query",
                required=False,
                description="Email address from the database to delete.",
            ),
            OpenApiParameter(
                "campaign_id",
                type=int,
                location="query",
                required=True,
                description="Campaign ID of the campagain to delete.",
            ),
        ],
        responses={
            200: OpenApiResponse(
                description="Email address deleted successfully.",
                examples={
                    "application/json": {
                        "Message": "Campaign and associated emails deleted successfully.",
                        "Email Address": "sample@mail.com",
                        "Campaign ID": "1",
                    }
                },
            ),
            400: OpenApiResponse(
                description="Invalid request or missing email address.",
            ),
            404: OpenApiResponse(
                description="Email address not found.",
                examples={
                    "application/json": {"error": "Email Database empty or not found."}
                },
            ),
            500: OpenApiResponse(
                description="Internal server error.",
                examples={"application/json": {"error": "Internal server error."}},
            ),
        },
        description="Delete an email address and all its associated ID, campaign_id and other data.",
    )
    def post(self, request):
        email_add = request.query_params.get("email_add")
        campaign_id = request.query_params.get("campaign_id")

        if not email_add:
            return Response({"error": "Email address is required."}, status=400)

        if not campaign_id:
            return Response({"error": "Campaign ID is required."}, status=400)

        # try:
        #     email = Email.objects.get(email_address=email_add)
        # except Email.DoesNotExist:
        #     return Response({"error": "Email Database empty or not found."}, status=404)

        # try:
        #     campaign_id = Email.objects.get(campaign_id=campaign_id)
        # except Email.DoesNotExist:
        #     return Response(
        #         {"error": "Campaign ID not found."},
        #         status=404
        #     )

        try:
            email = Email.objects.get(email_address=email_add, campaign_id=campaign_id)
        except Email.DoesNotExist:
            return Response(
                {
                    "error": f"Email: [{email_add}] with campaign ID: {campaign_id} not found."
                },
                status=404,
            )

        try:
            email.delete()
            return Response(
                {
                    "Message": "Campaign and associated emails deleted successfully.",
                    "Email Address": email_add,
                    "Campaign ID": campaign_id,
                },
                status=200,
            )
        except Exception as e:
            return Response({"error": str(e)}, status=500)


class UpdateEmailView(APIView):
    @extend_schema(
        parameters=[
            OpenApiParameter(
                "campaign_id",
                type=int,
                location="query",
                required=True,
                description="ID of the campaign to update.",
            ),
            OpenApiParameter(
                "email_id",
                type=str,
                location="query",
                required=True,
                description="ID of email to update.",
            ),
            OpenApiParameter(
                "email_add",
                type=str,
                location="query",
                required=True,
                description="New email address to update",
            ),
        ],
        responses={
            200: OpenApiResponse(
                description="Email address updated successfully.",
                examples={
                    "application/json": {
                        "campaign_id": 1,
                        "email_id": "6",
                        "New email address": "new_mail@mail.com",
                        "updated_at": "2025-01-27T12:00:00Z",
                    }
                },
            ),
            400: OpenApiResponse(
                description="Invalid request or missing parameters.",
                examples={
                    "application/json": {
                        "error": "Campaign ID and email ID are required."
                    }
                },
            ),
            404: OpenApiResponse(
                description="Email not found.",
                examples={"application/json": {"error": "Email not found."}},
            ),
            500: OpenApiResponse(
                description="Internal server error.",
                examples={"application/json": {"error": "Internal server error."}},
            ),
        },
        description="Update the email address for a specific campaign in the database.",
    )
    def post(self, request):
        campaign_id = request.query_params.get("campaign_id")
        email_id = request.query_params.get("email_id")
        email_add = request.query_params.get("email_add")

        if not campaign_id or not email_id:
            return Response(
                {"error": "Campaign ID and email address are required."}, status=400
            )

        if not email_add:
            return Response({"error": "Email address is required."}, status=400)

        try:
            email = Email.objects.get(campaign_id=campaign_id, email_id=email_id)
        except Email.DoesNotExist:
            return Response(
                {
                    "error": f"Email with ID [{email_id}] not found in Campaign [{campaign_id}]."
                },
                status=404,
            )

        try:
            email.email_add = email_add
            email.save()  # saves the email from the ORM

            return Response(
                {
                    "campaign_id": 1,
                    "email_id": "6",
                    "New email address": "new_mail@mail.com",
                    "updated_at": "2025-01-27T12:00:00Z",
                },
                status=200,
            )
        except Exception as e:
            return Response({"error": str(e)}, status=500)


# ==================== TEMPLATE MANAGEMENT VIEWS ====================

class TemplateListView(APIView):
    @extend_schema(
        parameters=[
            OpenApiParameter(
                "active_only",
                type=bool,
                location="query",
                required=False,
                description="Filter to show only active templates",
            ),
            OpenApiParameter(
                "search",
                type=str,
                location="query",
                required=False,
                description="Search templates by name or description",
            ),
        ],
        responses={
            200: EmailTemplateSerializer(many=True),
            500: OpenApiResponse(
                description="Server error",
                examples={"application/json": {"error": "Error message"}},
            ),
        },
        description="List all available email templates with optional filtering.",
    )
    def get(self, request):
        try:
            templates = EmailTemplate.objects.all()
            
            # Filter by active status
            active_only = request.query_params.get("active_only", "false").lower() == "true"
            if active_only:
                templates = templates.filter(is_active=True)
            
            # Search functionality
            search = request.query_params.get("search", "")
            if search:
                templates = templates.filter(
                    models.Q(name__icontains=search) | 
                    models.Q(description__icontains=search)
                )
            
            serializer = EmailTemplateSerializer(templates, many=True)
            return Response(serializer.data, status=200)
        except Exception as e:
            return Response({"error": str(e)}, status=500)


class TemplateCreateView(APIView):
    @extend_schema(
        request=EmailTemplateCreateSerializer,
        responses={
            201: EmailTemplateSerializer,
            400: OpenApiResponse(
                description="Validation error",
                examples={"application/json": {"error": "Validation error details"}},
            ),
            500: OpenApiResponse(
                description="Server error",
                examples={"application/json": {"error": "Error message"}},
            ),
        },
        description="Create a new email template with optional variables.",
    )
    def post(self, request):
        try:
            serializer = EmailTemplateCreateSerializer(data=request.data)
            if serializer.is_valid():
                # Check if template with the same name already exists
                if EmailTemplate.objects.filter(name=serializer.validated_data["name"]).exists():
                    return Response(
                        {"error": "A template with this name already exists."},
                        status=400,
                    )
                
                template = serializer.save()
                response_serializer = EmailTemplateSerializer(template)
                return Response(response_serializer.data, status=201)
            
            return Response(serializer.errors, status=400)
        except Exception as e:
            return Response({"error": str(e)}, status=500)


class TemplateDetailView(APIView):
    @extend_schema(
        parameters=[
            OpenApiParameter(
                "template_id",
                type=int,
                location="path",
                required=True,
                description="Template ID",
            ),
        ],
        responses={
            200: EmailTemplateSerializer,
            404: OpenApiResponse(
                description="Template not found",
                examples={"application/json": {"error": "Template not found"}},
            ),
            500: OpenApiResponse(
                description="Server error",
                examples={"application/json": {"error": "Error message"}},
            ),
        },
        description="Get detailed information about a specific template.",
    )
    def get(self, request, template_id):
        try:
            template = EmailTemplate.objects.get(template_id=template_id)
            serializer = EmailTemplateSerializer(template)
            return Response(serializer.data, status=200)
        except EmailTemplate.DoesNotExist:
            return Response({"error": "Template not found."}, status=404)
        except Exception as e:
            return Response({"error": str(e)}, status=500)


class TemplateUpdateView(APIView):
    @extend_schema(
        parameters=[
            OpenApiParameter(
                "template_id",
                type=int,
                location="path",
                required=True,
                description="Template ID",
            ),
        ],
        request=EmailTemplateUpdateSerializer,
        responses={
            200: EmailTemplateSerializer,
            400: OpenApiResponse(
                description="Validation error",
                examples={"application/json": {"error": "Validation error details"}},
            ),
            404: OpenApiResponse(
                description="Template not found",
                examples={"application/json": {"error": "Template not found"}},
            ),
            500: OpenApiResponse(
                description="Server error",
                examples={"application/json": {"error": "Error message"}},
            ),
        },
        description="Update an existing email template.",
    )
    def put(self, request, template_id):
        try:
            template = EmailTemplate.objects.get(template_id=template_id)
            serializer = EmailTemplateUpdateSerializer(template, data=request.data)
            if serializer.is_valid():
                updated_template = serializer.save()
                response_serializer = EmailTemplateSerializer(updated_template)
                return Response(response_serializer.data, status=200)
            return Response(serializer.errors, status=400)
        except EmailTemplate.DoesNotExist:
            return Response({"error": "Template not found."}, status=404)
        except Exception as e:
            return Response({"error": str(e)}, status=500)


class TemplateDeleteView(APIView):
    @extend_schema(
        parameters=[
            OpenApiParameter(
                "template_id",
                type=int,
                location="path",
                required=True,
                description="Template ID",
            ),
        ],
        responses={
            204: None,
            404: OpenApiResponse(
                description="Template not found",
                examples={"application/json": {"error": "Template not found"}},
            ),
            500: OpenApiResponse(
                description="Server error",
                examples={"application/json": {"error": "Error message"}},
            ),
        },
        description="Delete an email template.",
    )
    def delete(self, request, template_id):
        try:
            template = EmailTemplate.objects.get(template_id=template_id)
            template.delete()
            return Response(status=204)
        except EmailTemplate.DoesNotExist:
            return Response({"error": "Template not found."}, status=404)
        except Exception as e:
            return Response({"error": str(e)}, status=500)


class TemplatePreviewView(APIView):
    @extend_schema(
        request=TemplatePreviewSerializer,
        responses={
            200: OpenApiResponse(
                description="Template preview with rendered HTML",
                examples={
                    "application/json": {
                        "template_id": 1,
                        "subject": "Welcome to our platform",
                        "html_content": "<html>...</html>",
                        "variables_used": ["name", "company"]
                    }
                },
            ),
            400: OpenApiResponse(
                description="Validation error",
                examples={"application/json": {"error": "Validation error details"}},
            ),
            404: OpenApiResponse(
                description="Template not found",
                examples={"application/json": {"error": "Template not found"}},
            ),
        },
        description="Preview a template with sample data.",
    )
    def post(self, request):
        try:
            serializer = TemplatePreviewSerializer(data=request.data)
            if serializer.is_valid():
                template_id = serializer.validated_data["template_id"]
                sample_data = serializer.validated_data.get("sample_data", {})
                
                template = EmailTemplate.objects.get(template_id=template_id)
                
                # Render template with sample data
                from django.template import Template, Context
                template_obj = Template(template.html_content)
                context = Context(sample_data)
                rendered_html = template_obj.render(context)
                
                return Response({
                    "template_id": template_id,
                    "subject": template.subject,
                    "html_content": rendered_html,
                    "variables_used": list(sample_data.keys())
                }, status=200)
            
            return Response(serializer.errors, status=400)
        except EmailTemplate.DoesNotExist:
            return Response({"error": "Template not found."}, status=404)
        except Exception as e:
            return Response({"error": str(e)}, status=500)


class CampaignTemplateUpdateView(APIView):
    @extend_schema(
        parameters=[
            OpenApiParameter(
                "campaign_id",
                type=int,
                location="query",
                required=True,
                description="Campaign ID",
            ),
        ],
        request=CampaignDetailSerializer,
        responses={
            200: CampaignDetailSerializer,
            400: OpenApiResponse(
                description="Validation error",
                examples={"application/json": {"error": "Validation error details"}},
            ),
            404: OpenApiResponse(
                description="Campaign not found",
                examples={"application/json": {"error": "Campaign not found"}},
            ),
        },
        description="Update campaign template and custom message settings.",
    )
    def post(self, request):
        campaign_id = request.query_params.get("campaign_id")
        
        if not campaign_id:
            return Response({"error": "Campaign ID is required."}, status=400)
        
        try:
            campaign = Campaign.objects.get(campaign_id=campaign_id)
            serializer = CampaignDetailSerializer(campaign, data=request.data, partial=True)
            
            if serializer.is_valid():
                updated_campaign = serializer.save()
                response_serializer = CampaignDetailSerializer(updated_campaign)
                return Response(response_serializer.data, status=200)
            
            return Response(serializer.errors, status=400)
        except Campaign.DoesNotExist:
            return Response({"error": "Campaign not found."}, status=404)
        except Exception as e:
            return Response({"error": str(e)}, status=500)


# Enhanced SendEmailsView with custom template support
class EnhancedSendEmailsView(APIView):
    @extend_schema(
        parameters=[
            OpenApiParameter(
                "campaign_id",
                type=int,
                location="query",
                required=True,
                description="ID of the campaign to send emails for.",
            ),
        ],
        request={
            "application/json": {
                "type": "object",
                "properties": {
                    "message": {
                        "type": "string",
                        "description": "Custom message to send in the email (optional).",
                    },
                    "subject": {
                        "type": "string", 
                        "description": "Custom subject line (optional).",
                    },
                    "use_custom_template": {
                        "type": "boolean",
                        "description": "Whether to use campaign's custom template (default: false).",
                    }
                },
            }
        },
        responses={
            200: OpenApiResponse(
                description="Emails processed successfully.",
                examples={
                    "application/json": {
                        "message": "Emails sent successfully!",
                        "details": {"sent": 10, "failed": 2},
                        "template_used": "Custom Template Name",
                        "custom_message_used": "Custom message content",
                    }
                },
            ),
            400: OpenApiResponse(
                description="Invalid or missing campaign ID.",
                examples={"application/json": {"error": "Invalid or missing campaign ID."}},
            ),
            404: OpenApiResponse(
                description="No emails found for the given campaign.",
                examples={"application/json": {"error": "No emails found for the given campaign."}},
            ),
        },
        description="Send emails using custom templates and messages.",
    )
    def post(self, request):
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
        
        # Get custom settings from request
        custom_message = request.data.get("message", campaign.custom_message)
        custom_subject = request.data.get("subject", campaign.custom_subject)
        use_custom_template = request.data.get("use_custom_template", campaign.use_custom_template)
        
        # Determine which template to use
        if use_custom_template and campaign.custom_template:
            template = campaign.custom_template
            template_name = template.name
            subject = custom_subject or template.subject
        else:
            # Fall back to default templates (existing logic)
            email_template = request.query_params.get("email_template", "1")
            if email_template == "1":
                template_name = "autosad-temp-email.html"
                subject = custom_subject or "Welcome to AUTOSAD Get Certified"
            elif email_template == "2":
                template_name = "XCV_AI.html"
                subject = custom_subject or "Welcome onboard to XCV AI"
            elif email_template == "3":
                template_name = "autosad-temp-email2.html"
                subject = custom_subject or "Welcome to AUTOSAD Get Certified"
            elif email_template == "4":
                template_name = "autosad-email-temp-3.html"
                subject = custom_subject or "Welcome to AUTOSAD"
            else:
                return Response({"error": "Invalid template selection."}, status=400)
        
        success_count = 0
        failure_count = 0
        
        for email in emails:
            try:
                context = {
                    "name": email.name,
                    "message": custom_message or "Thank you for applying to the AUTOSAD Get Certified program...",
                }
                
                # Use custom template if available
                if use_custom_template and campaign.custom_template:
                    html_content = render_to_string_from_template(campaign.custom_template, context)
                else:
                    html_content = render_to_string(template_name, context)
                
                send_mail(
                    subject=subject,
                    message="",
                    from_email="info@autosad.ai",
                    recipient_list=[email.email_address],
                    html_message=html_content,
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
            },
            "template_used": template_name if not use_custom_template else (campaign.custom_template.name if campaign.custom_template else "Custom Template"),
            "custom_message_used": custom_message,
        }, status=200 if failure_count == 0 else 207)


def render_to_string_from_template(template_obj, context):
    """Helper function to render custom template with context"""
    from django.template import Template, Context
    template = Template(template_obj.html_content)
    return template.render(Context(context))
