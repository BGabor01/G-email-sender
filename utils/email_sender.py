import smtplib
import ssl
import json
import logging
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from .helpers import format_order_email, format_reg_email
from .exceptions import EmailSendError


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
    A class to send emails using an SMTP SSL connection.
    """

    def __init__(self, sender_email, password, server_host, server_port):
        """
        Initialize the EmailSender with SMTP configurations.
        
        :param sender_email: Email address used to send emails.
        :param password: Password for the sender_email.
        :param server_host: SMTP server host.
        :param server_port: SMTP server port.
        """
        logger.info("Starting SMTP connection...")
        self.sender_email = sender_email
        self.password = password
        self.server = smtplib.SMTP_SSL(server_host, server_port)
        self._login()
        logger.info("SMTP connection established.")

    def _login(self):
        """
        Log in to the SMTP server.
        """
        try:
            self.server.login(self.sender_email, self.password)
            logger.info("Logged in successfully.")
        except (smtplib.SMTPException, ssl.SSLError) as e:
            logger.error(f"Error during SMTP login: {e}")
            raise ConnectionError("Failed to login to the SMTP server. More info in the logs: /utils/logs/EmailSender.log")


    def order_completed(self, order_data):
        
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
        
    def registration_email(self, user_data):

        json.loads(user_data)

        msg = MIMEMultipart('alternative')
        msg['Subject'] = 'Registration'
        msg['From'] = self.sender_email
        msg['To'] = user_data["email"]

        formatted_message = format_reg_email()

        msg.attach(MIMEText(formatted_message, 'html'))

        try:
            self.server.send_message(msg)
            logger.info("Email sent!")
            return "Email sent!"
        except smtplib.SMTPException as e:
            logger.error(f"Error: {e}")
            raise EmailSendError()



