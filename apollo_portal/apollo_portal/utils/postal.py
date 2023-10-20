"""Custom mail handler for authenticating with Postal server."""

import os
import smtplib
from django.conf import settings
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


def send_mail(email):
    """Dispatch mail with SMTP.

    This is only used for sending emails with specific headers (to satisfy the
    fussy Postal server).
    """
    if (
        os.environ.get('DJANGO_SETTINGS_MODULE')
        == 'apollo_portal.settings.test'
        and not settings.TEST_PRODUCTION_MAIL_SERVER
    ):
        # Revert to django's default mail handler
        return email.send()

    try:
        # Create connection
        server = smtplib.SMTP(settings.EMAIL_HOST, settings.EMAIL_PORT)
        server.ehlo()
        server.login(settings.EMAIL_HOST_USER, settings.EMAIL_HOST_PASSWORD)

        # Build multipart email content
        m = MIMEMultipart('alternative')
        m.set_charset('utf8')
        m['To'] = email.to[0]
        m['From'] = email.from_email
        m['Subject'] = email.subject
        if email.reply_to:
            m['reply-to'] = email.reply_to[0]

        text = MIMEText(email.body, 'plain')
        m.attach(text)

        for content in email.alternatives:
            m.attach(MIMEText(
                content[0],                       # content
                content[1].replace('text/', ''),  # type
            ))
        # Print smtp username and password:
        print("SMTP username: ", settings.EMAIL_HOST_USER)
        print("SMTP password: ", settings.EMAIL_HOST_PASSWORD)
        print("Message SMTP content:\n", m.as_string())
        server.send_message(m)

    finally:
        server.quit()
