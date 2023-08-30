import smtplib, ssl
import json
import logging


logger = logging.getLogger("Email-Sender")


class EmailSender:

    def __init__(self, sender_email, password, server_host, server_port):
        logger.info("Starting SMTP connection...")
        self.sender_email = sender_email
        self.password = password
        self.server = smtplib.SMTP(server_host, server_port, timeout=10)
        self._login()
        logger.info("SMTP connection established.")

    def _login(self):
        try:
            self.server.starttls(context=ssl.create_default_context())
            self.server.login(self.sender_email, self.password)
            logger.info("Logged in successfully.")
        except (smtplib.SMTPException, ssl.SSLError) as e:
            logger.error(f"Error during SMTP login: {e}")
            raise


    def order_completed(self, order_data):
        order_data = json.loads(order_data)
        print(order_data)
        reciever_email = "balogh.j.gabor@gmail.com"
        try:
            self.server.sendmail(self.sender_email, reciever_email, str(order_data["ordered_products"]))
        except smtplib.SMTPException:
            raise Exception("Somethign went wrong")

        return "Email send succesfully!"

