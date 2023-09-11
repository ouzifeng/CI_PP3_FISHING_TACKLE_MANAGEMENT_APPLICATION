import smtplib
import json
from email.mime.text import MIMEText


def send_email(recipient_email, subject, out_of_stock_items):
    with open('creds.json', 'r') as file:
        creds = json.load(file)
        smtp_creds = creds['aws_smtp']
        smtp_server = smtp_creds['server']
        smtp_port = smtp_creds['port']
        smtp_username = smtp_creds['username']
        smtp_password = smtp_creds['password']

    html_content = """
    <html>
    <head>
        <style>
            table {
                border-collapse: collapse;
                width: 100%;
            }
            th, td {
                border: 1px solid #dddddd;
                text-align: left;
                padding: 8px;
            }
            th {
                background-color: #f2f2f2;
            }
        </style>
    </head>
    <body>
        <h2>Out of Stock Products</h2>
        <table>
            <tr>
                <th>SKU</th>
                <th>Product Name</th>
                <th>Cost Price</th>
                <th>RRP</th>
                <th>Stock</th>
            </tr>
    """
    for item in out_of_stock_items:
        sku = item.get('SKU', '-')
        product_name = item.get('Product Name', '-')
        cost_price = item.get('Cost Price', '-')
        rrp = item.get('RRP', '-')
        stock = item.get('Stock', '-')
        html_content += (
            f"<tr><td>{sku}</td><td>{product_name}</td><td>{cost_price}</td>"
            f"<td>{rrp}</td><td>{stock}</td></tr>"
        )

    html_content += """
    </table>
    </body>
    </html>
    """

    msg = MIMEText(html_content, 'html')
    msg['Subject'] = subject
    msg['From'] = 'orders@tackletarts.uk'
    msg['To'] = recipient_email

    with smtplib.SMTP(smtp_server, smtp_port) as smtp_connection:
        smtp_connection.starttls()
        smtp_connection.login(smtp_username, smtp_password)
        smtp_connection.sendmail(msg['From'], [msg['To']], msg.as_string())
