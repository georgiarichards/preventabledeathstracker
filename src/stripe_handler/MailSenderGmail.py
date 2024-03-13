import logging
import os
import smtplib
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from MailSchemas import SendEmailGmail


class MailSenderGmail:
    def __init__(self, params: SendEmailGmail) -> None:
        self.email = params.email
        self.password = params.password
        self.config = params.config
        self.msg = MIMEMultipart("alternative")
        self.smtp = smtplib.SMTP(host=self.config.host, port=self.config.port)
        self.logger = logging.getLogger()

    def send_mail(self) -> None:
        """
        Sending email
        """
        self._create_message()
        self._attach_files()
        self.smtp.starttls()
        self.smtp.login(self.email, self.password)
        self.smtp.sendmail(self.email, self.config.email_to, self.msg.as_string())
        self.smtp.quit()
        print("Message sended")

    def _create_message(self) -> None:
        """
        Creating messages
        """
        print("Creating message")
        self.msg["From"] = self.email
        self.msg["To"] = self.config.email_to
        self.msg["Subject"] = self.config.subject
        text_part = MIMEText(self.config.body, "html")
        self.msg.attach(text_part)
        print("Message created")

    def _attach_files(self) -> None:
        """
        Attaching files to email
        """
        if file_paths := self.config.file_paths:
            print("Attaching files")
            for file in file_paths:
                if not os.path.isfile(file):
                    raise FileNotFoundError(f"The file '{file}' does not exist.")
                with open(file, "rb") as f:
                    data = f.read()
                    attach_part = MIMEBase("application", "octet-stream")
                    attach_part.set_payload(data)
                    encoders.encode_base64(attach_part)

                attach_part.add_header("Content-Disposition", f"attachment; filename= {os.path.basename(file)}")
                self.msg.attach(attach_part)
            print("Files successfully attached")
