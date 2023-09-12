import smtplib
import ssl
import json
import logging
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from .exceptions import EmailSendError
from .helpers import format_order_email, format_reg_email



logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
                    datefmt='%Y-%m-%d %H:%M',
                    handlers=[
                        logging.FileHandler("./utils/logs/EmailSender.log", 'a', 'utf-8'),
                        logging.StreamHandler()
                    ])

logger = logging.getLogger("Email-Sender")


class EmailSender:
    """
    A utility class to send emails using an SMTP SSL connection.

    """

    def __init__(self, sender_email : str, password : str, server_host : str, server_port : int):
        """
        Initialize an EmailSender instance and establish an SMTP SSL connection.

        Parameters
        ----------
        sender_email : str
            Email address used to send emails.

        password : str
            Password for the sender_email.

        server_host : str
            Hostname of the SMTP server.

        server_port : int
            Port number for the SMTP server.
        """

        logger.info("Starting SMTP connection...")
        self.sender_email = sender_email
        self.password = password
        self.server = smtplib.SMTP_SSL(server_host, server_port)
        self._login()
        logger.info("SMTP connection established.")

    def _login(self):
        """
        Authenticate and log in to the SMTP server using the provided email and password.
        
        Raises
        ------
        ConnectionError
            If login to SMTP server fails.
        """

        try:
            self.server.login(self.sender_email, self.password)
            logger.info("Logged in successfully.")
        except (smtplib.SMTPException, ssl.SSLError) as e:
            logger.error(f"Error during SMTP login: {e}")
            raise ConnectionError("Failed to login to the SMTP server. More info in the logs: /utils/logs/EmailSender.log")


    def order_completed(self, order_data:json) -> str:
        """
        Send an email detailing a completed order.
        
        Parameters
        ----------
        order_data : str
            JSON string containing order details.

        Returns
        -------
        str
            A message confirming email sent status.

        Raises
        ------
        EmailSendError
            If sending the email fails.
        """
        
        email_data = json.loads(order_data)

        msg = MIMEMultipart('alternative')
        msg['Subject'] = 'Your Order Details'
        msg['From'] = self.sender_email
        msg['To'] = email_data["customer_email"]

        formatted_message = format_order_email(email_data)

        msg.attach(MIMEText(formatted_message, 'html'))

        try:
            self.server.send_message(msg)
            logger.info("Email sent!")
            return "Email sent!"
        except smtplib.SMTPException as e:
            logger.error(f"Error: {e}")
            raise EmailSendError()
        
    def registration_email(self, user_email : bytes) -> str:
        """
        Send a registration confirmation email.
        
        Parameters
        ----------
        user_email : bytes
            Byte encoded string containing the user's email address.

        Returns
        -------
        str
            A message confirming email sent status.

        Raises
        ------
        EmailSendError
            If sending the email fails.
        """

        msg = MIMEMultipart('alternative')
        msg['Subject'] = 'Registration'
        msg['From'] = self.sender_email
        msg['To'] = user_email.decode()

        formatted_message = format_reg_email()

        msg.attach(MIMEText(formatted_message, 'html'))

        try:
            self.server.send_message(msg)
            logger.info("Email sent!")
            return "Email sent!"
        except smtplib.SMTPException as e:
            logger.error(f"Error: {e}")
            raise EmailSendError()



