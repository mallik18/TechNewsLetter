import sendgrid
from sendgrid.helpers.mail import *

from dotenv import load_dotenv
import os


from main import tech_news

load_dotenv()


if __name__ == "__main__":
    try:
        sg = sendgrid.SendGridAPIClient(api_key=os.environ.get('SENDGRID_API_KEY'))
        from_email = Email(os.getenv("SENDER_EMAIL"))
        to_email = To(os.getenv("RECEIVER_EMAIL"))
        subject = "Tech News Letter"
        content = Content("text/plain", tech_news())
        mail = Mail(from_email, to_email, subject, content)
        response = sg.client.mail.send.post(request_body=mail.get())
        print(response.status_code)
        print(response.body)
        print(response.headers)
    except Exception as e:
        print(e)