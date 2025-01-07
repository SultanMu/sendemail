import openpyxl
from django.core.mail import send_mail
from django.http import JsonResponse
from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader

def send_emails(request):
    # Path to your Excel file
    excel_file_path = "sample_dataset.xlsx"
    
    # Load the Excel file
    wb = openpyxl.load_workbook(excel_file_path)
    sheet = wb.active
    
    # Iterate through the rows in the file
    for row in sheet.iter_rows(min_row=2):  # Assuming headers in the first row
        recipient_email = row[0].value
        subject = row[1].value
        message = row[2].value
        
        # Send the email
        send_mail(
            subject=subject,
            message=message,
            from_email='info@autosad.ai',
            recipient_list=[recipient_email],
        )
    
    return JsonResponse({"message": "Emails sent successfully!"})

def home(request):
    template = loader.get_template('autosad-email-template-new.html')
    return HttpResponse(template.render())

def intro(request):
    return HttpResponse("Welcome to this django app.")
