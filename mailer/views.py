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
        responses={
            201: {"message": "Emails saved successfully!"}, 
            400: {"error": "Error message"}
        },
        description="Upload an XLS file to save email data into the database. The file should contain 'email_address', 'subject', and 'message' columns.",
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
                    Email.objects.create(
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
        
        
        
        html_content = render_to_string('autosad-temp-email.html')

        # Iterate through the emails and send them
        for email in emails:
            try:
                
                html_content = render_to_string('autosad-temp-email.html') # context not added because there are not context variables in the html template
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




# def send_emails(request):
#     # Path to your Excel file
#     excel_file_path = "sample_dataset.xlsx"
    
#     # Load the Excel file
#     wb = openpyxl.load_workbook(excel_file_path)
#     sheet = wb.active
    
#     # Iterate through the rows in the file
#     for row in sheet.iter_rows(min_row=2):  # Assuming headers in the first row
#         recipient_email = row[0].value
#         subject = row[1].value
#         message = row[2].value
        
#         # Send the email
#         send_mail(
#             subject=subject,
#             message=message,
#             from_email='info@autosad.ai',
#             recipient_list=[recipient_email],
#         )
    
#     return JsonResponse({"message": "Emails sent successfully!"})

# def home(request):
#     template = loader.get_template('autosad-email-template-new.html')
#     return HttpResponse(template.render())

# def intro(request):
#     return HttpResponse("Welcome to this django app.")
