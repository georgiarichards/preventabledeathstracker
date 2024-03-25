import os
from datetime import datetime, timedelta

import stripe
from dotenv import load_dotenv
from MailSchemas import SendEmailGmail, SenderConfigGmail, UserCred
from MailSenderGmail import MailSenderGmail
from map import PATH_KEY, PRODUCT_DETAILS_MAP
from template import fill_email_template

load_dotenv()

stripe.api_key = os.getenv("STRIPE_SECRET_KEY")


class OrdersHandler:
    def __init__(self) -> None:
        self.email_cred = UserCred(email=os.getenv("EMAIL"), password=os.getenv("PASSWORD"))

    def handle(self) -> None:
        start_time = int((datetime.now() - timedelta(minutes=60)).timestamp())
        end_time = int(datetime.now().timestamp())
        payment_intents = stripe.PaymentIntent.list()
        # Doesn't work for some reason  created={"gte": start_time, "lte": end_time})
        _orders = {}
        for payment in payment_intents:
            if not (start_time <= payment.created <= end_time):
                continue
            if payment.status != "succeeded" or not payment.invoice:
                continue
            print(payment)
            invoice = stripe.Invoice.retrieve(payment.invoice)
            customer_email = invoice.customer_email
            customer_name = invoice.customer_name
            product = invoice.lines.data[0].description
            if product not in PRODUCT_DETAILS_MAP:
                continue
            product_path = PRODUCT_DETAILS_MAP[product]["path"]
            print(f"{customer_email} - {product} - path: {product_path}")

            sender_config = SenderConfigGmail(
                host="smtp.gmail.com",
                port=587,
                email_to=customer_email,
                subject=f"{product} - PREVENTABLE-DEATHS",
                body=fill_email_template(customer_name, product),
                file_paths=[PRODUCT_DETAILS_MAP[product][PATH_KEY]],
            )
            send_email_gmail = SendEmailGmail(config=sender_config, **self.email_cred.dict())
            MailSenderGmail(params=send_email_gmail).send_mail()


if __name__ == "__main__":
    handler = OrdersHandler()
    handler.handle()
