class EmailSendError(Exception):
    """Raised when there's an error sending the email."""

    def __init__(self, message="Failed to send email. More info in the logs: /utils/logs/EmailSender.log"):
        self.message = message
        super().__init__(self.message)