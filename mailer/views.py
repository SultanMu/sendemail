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
from .models import Email
from .serializers import EmailSerializer


class XLSReaderView(APIView):
    parser_classes = [MultiPartParser]

    @extend_schema(
        request={
            'multipart/form-data': {
                'type': "object",
                'properties': {
                    'file': {'type': 'string', 'format': 'binary', 'description': 'XLS file to upload'}
                }
            }
        },
        parameters={
            OpenApiParameter("Campaign-ID", type=int, location="query", required=True)
        },
        responses={
            201: {"message": "Emails saved successfully!"}, 
            400: {"error": "Error message"}
        },
        description="Upload an XLS file to save email data into the database. The file should contain 'name' and 'email_address' columns.",
    )
    
    def post(self, request):
        file = request.FILES.get('file')
        if not file:
            return Response({"error": "No file uploaded"}, status=400)
        
        # Validate file type
        if not file.name.endswith(('.xls', '.xlsx')):
            return Response({"error": "Unsupported file format. Please upload an Excel file."}, status=400)

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
                    Email.objects.get_or_create(  # make sure it only checks unique emails not names
                        email_address=recipient_email,
                        name=name
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



class EmailsSentView(APIView):
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
        pass
        
        # write funtion to output list of emails that are saved in the database.
        
        # learn drf_spectacular/django rest framework to create 
    
        
        
class ListEmailsView(APIView):
    @extend_schema(
        responses={
            200: {
                "type": "object",
                "properties": {
                    "message": {"type": "string"},
                    "data": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {
                                "name": {"type": "string"},
                                "email_address": {"type": "string"}
                            }
                        }
                    },
                    "count": {"type": "integer"}
                }
            },
            500: {"error": "Error message"}
        },
        description="Retrieve all emails stored in the database.",
    )
    def get(self, request):
        try:
            emails = Email.objects.all()
            email_list = []
            
            for email in emails:
                email_list.append({
                    'name': email.name,
                    'email_address': email.email_address
                    # Add any other fields you want to include
                })
            
            return Response({
                "message": "Emails retrieved successfully",
                "data": email_list,
                "count": len(email_list)
            }, status=200)
            
        except Exception as e:
            return Response({
                "error": f"Failed to retrieve emails: {str(e)}"
            }, status=500)