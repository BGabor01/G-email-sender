import smtplib
import ssl
import json
import logging
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
        order_data = json.loads(order_data)
        print(order_data)
        try:
            self.server.sendmail(self.sender_email, order_data["reciever_email"], str(order_data["ordered_products"]))
        except smtplib.SMTPException as e:
            logger.error(f"Failed to send the order completion email. {e}")
            raise EmailSendError()

        return "Email send succesfully!"

