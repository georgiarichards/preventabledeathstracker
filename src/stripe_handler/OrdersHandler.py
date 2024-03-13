import os
from datetime import datetime, timedelta

from dotenv import load_dotenv
import stripe

from MailSenderGmail import MailSenderGmail
from map import PATH_MAP
from MailSchemas import SenderConfigGmail, SendEmailGmail, UserCred

load_dotenv()

stripe.api_key = os.getenv("STRIPE_SECRET_KEY")


class OrdersHandler:
    def __init__(self) -> None:
        self.email_cred = UserCred(email=os.getenv("EMAIL"), password=os.getenv("PASSWORD"))

    def handle(self) -> None:
        start_time = int((datetime.now() - timedelta(minutes=60)).timestamp())
        end_time = int(datetime.now().timestamp())
        payment_intents = stripe.PaymentIntent.list(created={"gte": start_time, "lte": end_time})
        _orders = {}
        for payment in payment_intents:
            if payment.status != "succeeded":
                continue
            invoice = stripe.Invoice.retrieve(payment.invoice)
            customer_email = invoice.customer_email
            product = invoice.lines.data[0].description
            print(f"{customer_email} - {product} - path: {PATH_MAP[product]}")

            sender_config = SenderConfigGmail(
                host="smtp.gmail.com",
                port=587,
                email_to=customer_email,
                subject=f"{product} - PREVENTABLE-DEATHS",
                body=f"Hello, this is a test stripe email! {product}",  #TODO: change body to HTML
                file_paths=[PATH_MAP[product]],
            )
            send_email_gmail = SendEmailGmail(config=sender_config, **self.email_cred.dict())
            MailSenderGmail(params=send_email_gmail).send_mail()


if __name__ == '__main__':
    handler = OrdersHandler()
    handler.handle()
