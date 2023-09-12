import os
import logging
from dotenv import load_dotenv

from g_rpc import Server
from utils import EmailSender

load_dotenv()


logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
    datefmt='%Y-%m-%d %H:%M',
    handlers=[
        logging.FileHandler("./utils/logs/MainService.log", 'a', 'utf-8'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger("MainService")


def initialize_email_sender() -> EmailSender:
    """
    Initialize and return an instance of EmailSender.
    
    Returns
    -------
    EmailSender
        An initialized EmailSender object.
        
    Raises
    ------
    KeyError
        If any required environment variables are missing.
    """
    try:
        email_sender = EmailSender(
            os.environ.get("SENDER_EMAIL"),
            os.environ.get("PASSWORD"),
            os.environ.get("SERVER_HOST"),
            os.environ.get("SERVER_PORT")
        )
        logger.info("Initialized EmailSender")
        return email_sender
    except KeyError:
        logger.error("Error initializing EmailSender: Missing environment variables.")
        raise

def initialize_server(email_sender : EmailSender) -> Server:
    """
    Initialize and return a gRPC server with email methods.

    Parameters
    ----------
    email_sender : EmailSender
        An initialized EmailSender object.

    Returns
    -------
    Server
        An initialized gRPC Server object.

    Raises
    ------
    ConnectionError
        If there's a connection problem when initializing the server.
    """

    try:
        server = Server("EMAIL_SENDER", host=os.environ.get("RABBITMQ_HOST"))
        server.connect()
        server.add_method('order_completed', email_sender.order_completed)
        logger.info("Order_completed method added to the server")
        server.add_method('registration', email_sender.registration_email)
        return server
    except ConnectionError:
        logger.error("Error initializing server: Connection Error")
        raise

def main():
    """Main execution function."""
    load_dotenv()

    email_sender = initialize_email_sender()
    server = initialize_server(email_sender)
    
    try:
        server.start()
    except RuntimeError:
        logger.error("Error starting server: Runtime Error")
        raise


if __name__ == "__main__":
    main()