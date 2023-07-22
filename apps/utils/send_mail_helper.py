from sendgrid.helpers.mail import Mail
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from apps.accounts.models import User
from django.conf import settings
from sendgrid import SendGridAPIClient


class SendMail:
    @staticmethod
    def send_mail(email):
        user = User.objects.get(email__iexact=email)
        uid = urlsafe_base64_encode(force_bytes(user.id))
        verify_link = f"http://127.0.0.1:8000/accounts/verify-account/{uid}/"
        try:
            message = Mail(
                from_email=settings.EMAIL_HOST_USER,
                to_emails=email,
                subject="Verify account",
                html_content=f"We receive a request to signup in drf-blog, cick this link to verify your account --> {verify_link}",
            )
            sg = SendGridAPIClient(api_key=settings.SENDGRID_API_KEY)
            sg.send(message)
        except Exception as e:
            raise e
