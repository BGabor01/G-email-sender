def format_order_email(email_data):

    html = """
    <html>
        <body>
            <h2>Order Completed!</h2>
            <p>Dear {customer_name},</p>
            <p>Thank you for your order. Here are your order details:</p>
            <ul>
    """
    for product in email_data["ordered_products"]:
        html += f"<li>{product['name']} (Quantity: {product['quantity']}): ${product['price']} each</li>"
    html += f"""
            </ul>
            <p>Total Price: ${email_data['total_price']}</p>
            <p>Thank you for shopping with us!</p>
        </body>
    </html>
    """.format(customer_name=email_data['customer_name'])

    return html


def format_reg_email():
    html = """<html>
    <head>
        <title>Thank You</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                padding: 20px;
                background-color: #f7f7f7;
            }
            .container {
                background-color: #ffffff;
                padding: 20px;
                border-radius: 8px;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h2>Thank You for Your Registration!</h2>
            <p>We're glad to have you with us. If you have any questions, feel free to reach out!</p>
        </div>
    </body>
    </html>"""

    return html
