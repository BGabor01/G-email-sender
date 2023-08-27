from g_rpc import Server
from rpc_commands import send_reg_email


if __name__ == "__main__":
    server = Server("EMAIL_SENDER")
    server.connect()
    server.add_method('registration_email', send_reg_email)
    server.start()
