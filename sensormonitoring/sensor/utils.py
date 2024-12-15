# from django.core.mail import send_mail
# from django.conf import settings

# def send_notification_email(subject, message, recipient_list):
#     try:
#         send_mail(
#             subject,
#             message,
#             settings.EMAIL_HOST_USER,
#             recipient_list,
#             fail_silently=False,
#         )
#     except Exception as e:
#         print(f"Error sending email: {e}")

# sensor/utils.py

# from django.core.mail import send_mail
# from django.conf import settings

# def send_notification_email(subject, message, recipients):
#     """
#     Sends an email to a list of recipients.
#     """
#     send_mail(
#         subject=subject,
#         message=message,
#         from_email=settings.EMAIL_HOST_USER,
#         recipient_list=recipients,
#         fail_silently=False,
#     )


# utils.py
from django.core.mail import send_mail
from django.conf import settings

def send_simple_message(subject, body, to_email):
    """
    Send an email using Gmail's SMTP server configured in Django settings.
    Args:
        subject (str): Subject of the email
        body (str): Body content of the email
        to_email (str): Recipient email address
    Returns:
        str: Success or failure message
    """
    from_email = settings.EMAIL_HOST_USER  # Your configured Gmail address

    try:
        send_mail(
            subject=subject,
            message=body,
            from_email=from_email,
            recipient_list=[to_email],
            fail_silently=False,  # Set to True to suppress exceptions
        )
        return "Email sent successfully!"
    except Exception as e:
        return f"Failed to send email: {str(e)}"
