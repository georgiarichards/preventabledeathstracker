import csv
import os

import stripe
from dotenv import load_dotenv
from MailSchemas import SendEmailGmail, SenderConfigGmail, UserCred
from MailSenderGmail import MailSenderGmail
from map import PATH_KEY, PRODUCT_DETAILS_MAP
from template import fill_email_template

load_dotenv()

stripe.api_key = os.getenv("STRIPE_SECRET_KEY")
PROCESSED_PAYMENTS_FILE = "src/stripe_handler/data/processed_payments.csv"


class OrdersHandler:
    def __init__(self) -> None:
        self.email_cred = UserCred(email=os.getenv("EMAIL"), password=os.getenv("PASSWORD"))
        self.processed_payments = self.load_processed_payments()

    @staticmethod
    def load_processed_payments() -> set:
        if os.path.exists(PROCESSED_PAYMENTS_FILE):
            with open(PROCESSED_PAYMENTS_FILE, "r", newline='') as file:
                reader = csv.reader(file)
                return set(row[0] for row in reader)
        return set()

    @staticmethod
    def save_processed_payment(payment_id: str) -> None:
        with open(PROCESSED_PAYMENTS_FILE, "a", newline='') as file:
            writer = csv.writer(file)
            writer.writerow([payment_id])

    def handle(self) -> None:
        payment_intents = stripe.PaymentIntent.list()
        _orders = {}
        for payment in payment_intents:
            if payment.id in self.processed_payments:
                print(f"Processing {payment.id} skipped, already processed")
                continue

            if payment.status != "succeeded":
                print(f"Processing {payment.id} skipped, payment.status {payment.status}")
                continue

            elif not payment.invoice:
                print(f"Processing {payment.id} skipped, invoice not created")
                continue

            invoice = stripe.Invoice.retrieve(payment.invoice)
            customer_email = invoice.customer_email
            customer_name = invoice.customer_name
            product = invoice.lines.data[0].description
            if product not in PRODUCT_DETAILS_MAP:
                print(f"Processing {payment.id} {product} not checked")
                continue
            product_path = PRODUCT_DETAILS_MAP[product][PATH_KEY]
            print(f"{customer_email} - {product} - path: {product_path}")

            sender_config = SenderConfigGmail(
                host="smtp.gmail.com",
                port=587,
                email_to=customer_email,
                subject=f"{product} - PREVENTABLE-DEATHS",
                body=fill_email_template(customer_name, product),
                file_paths=[product_path],
            )
            send_email_gmail = SendEmailGmail(config=sender_config, **self.email_cred.dict())
            MailSenderGmail(params=send_email_gmail).send_mail()
            print(f"Message sent {customer_email} - {product} - path: {product_path}")

            # Save processed payment ID
            self.save_processed_payment(payment.id)

    def mocked_test(self, product: str = "Reg 29 Addressee Tracker Database") -> None:
        product_path = PRODUCT_DETAILS_MAP[product][PATH_KEY]
        customer_email = ""  # set test customer email
        customer_name = "Test User"
        sender_config = SenderConfigGmail(
            host="smtp.gmail.com",
            port=587,
            email_to=customer_email,
            subject=f"{product} - PREVENTABLE-DEATHS",
            body=fill_email_template(customer_name, product),
            file_paths=[product_path],
        )
        send_email_gmail = SendEmailGmail(config=sender_config, **self.email_cred.dict())
        MailSenderGmail(params=send_email_gmail).send_mail()
        print(f"Message sent {customer_email} - {product} - path: {product_path}")


if __name__ == "__main__":
    handler = OrdersHandler()
    handler.handle()
    # products = ["Reg 28 Database - Completed responses only",
    #             "Reg 28 Database - Pending responses only",
    #             "Reg 28 Database - Overdue responses"]
    # for product in products:
    #     handler.mocked_test(product)
