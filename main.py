from g_rpc import Server
import os
import logging
from utils import EmailSender
from dotenv import load_dotenv
import time

load_dotenv()

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

if __name__ == "__main__":
    
    logger = logging.getLogger("MAIN")

    email_sender = EmailSender(os.environ.get("SENDER_EMAIL"),
                               os.environ.get("PASSWORD"),
                               os.environ.get("SERVER_HOST"),
                               os.environ.get("SERVER_PORT"))
    
    logger.info("initalized EmailSender")
    
    server = Server("EMAIL_SENDER", host = os.environ.get("RABBITMQ_HOST"))
    server.connect()
    server.add_method('order_completed', email_sender.order_completed)
    logger.info("Order_completed method done")
    server.start()
