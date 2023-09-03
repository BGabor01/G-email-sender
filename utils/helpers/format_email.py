def format_email(email_data):

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
