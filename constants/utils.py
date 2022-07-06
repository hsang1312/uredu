from rest_framework import status as _status_
from django.conf import settings
from constants import res_mess

def ResponseSuccess(message, status):
    response = {
        'code': 'success',
        'status': status,
        'message': message,
    }
    return response

def ResponseError(message, status=_status_.HTTP_400_BAD_REQUEST):
    response = {
        'code': 'error',
        'status': status,
        'message': message,
    }
    return response

from email.message import EmailMessage
import smtplib

def send_mail(email_receiver, email_subject, email_body):
    em = EmailMessage()
    em['From'] = settings.EMAIL_USERNAME
    em['To'] = email_receiver
    em['Subject'] = email_subject
    em.set_content(email_body)

    with smtplib.SMTP_SSL(settings.EMAIL_HOST, settings.EMAIL_PORT, context=settings.EMAIL_CONTEXT) as smtp:
        smtp.login(settings.EMAIL_USERNAME, settings.EMAIL_PASSWORD)
        smtp.sendmail(settings.EMAIL_USERNAME, email_receiver, em.as_string())


def password_validate(value):
    password_length_required = 9
    special_characters = "[~\!@#\$%\^&\*\(\)_\+{}\":;'\[\]]"
    errors = list()
    if any(' ' in value for char in value):
        errors.append(res_mess.ErrorsPasswordContainSpaceValid)
    
    if len(value) < password_length_required:
        errors.append(res_mess.ErrorsPasswordLengthRequired)
        
    if not any(char.isupper() for char in value):
        errors.append(res_mess.ErrorsPasswordUppercaseRequired)
        
    if not any(char.islower() for char in value):
        errors.append(res_mess.ErrorsPasswordLowercaseRequired)
        
    if not any(char.isdigit() for char in value):
        errors.append(res_mess.ErrorsPasswordDigitsRequired)
                    
    if not any(char in special_characters for char in value):
        errors.append(res_mess.ErrorsPasswordSpecialCharRequired)
        
    if errors:
        return errors
    
    return value