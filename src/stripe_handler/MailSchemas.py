from typing import Optional, List

from pydantic import BaseModel


class UserCred(BaseModel):
    """
    User email credentials model.
    Attributes:
        email: Email address of the user.
        password: Password for the email account.
    """
    email: str
    password: str


class BaseEmailCred(BaseModel):
    """
    Base email configuration model.

    Attributes:

        host: Email host. For example, "smtp.gmail.com"
        port: The port to use for the email service. For example, 587 for Gmail's SMTP.
    """

    host: str
    port: int


class BaseSenderConfig(BaseModel):
    """
    Base sender configuration model.

    Attributes:

        email_to: Recipient's email address.
        subject: The subject of the email. Default: "Subject".
        file_paths: List of file paths to be attached to the email.
        body: The body text of the email.
    """

    email_to: str
    subject: str = "Subject"
    file_paths: Optional[List[str]]
    body: str


class SenderConfigGmail(BaseEmailCred, BaseSenderConfig):
    """
    Sender configuration for Gmail.
    """
    pass


class SendEmailGmail(UserCred):
    """
    Gmail specific sender email parameters.
    Attributes:
        config: Configuration parameters for sending email through Gmail.
    """
    config: SenderConfigGmail
