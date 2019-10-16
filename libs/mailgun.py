import os
from requests import Response, post
from typing import List


class MailgunException(Exception):
    def __init__(self, error_message: str):
        self.message = error_message


class Mailgun:

    FROM_TITLE = "Princing Service"
    FROM_EMAIL = "do_not_reply@sandboxba3b3baa57404ec29a67394aca9538ed.mailgun.org"
    
    @classmethod
    def send_mail(cls, email: List[str], subject: str, text: str, html: str) -> Response:
        api_key = os.environ.get('MAILGUN_API_KEY', None)
        domain = os.environ.get('MAILGUN_DOMAIN', None)
        
        if api_key is None:
            raise MailgunException("Failed to load Mailgun API key")
        if domain is None:
            raise MailgunException("Failed to load Mailgun Domain")

        response = post(f"{domain}/messages",
                        auth=("api", api_key),
                        data={"from": f"{cls.FROM_TITLE} <{cls.FROM_EMAIL}>",
                              "to": email,
                              "subject": subject,
                              "text": text,
                              "html": html})

        if response.status_code != 200:
            raise MailgunException('An error occured while sending e-mail')
        return response
