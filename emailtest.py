import json
import smtplib
from email.mime.text import MIMEText

# Load credentials from creds.json
with open('creds.json', 'r') as file:
    creds = json.load(file)
    smtp_creds = creds['aws_smtp']

# Connect to the SMTP server using the loaded credentials
smtp_server = smtp_creds['server']
smtp_port = smtp_creds['port']
smtp_username = smtp_creds['username']
smtp_password = smtp_creds['password']

# Create a MIMEText object to represent the email
msg = MIMEText("This is the body of the email.")
msg['Subject'] = "Test Email from AWS SES"
msg['From'] = "orders@tackletarts.uk"  # Replace with your sending email
msg['To'] = "mr.davidoak@gmail.com"  # Replace with the recipient's email

# Send the email
with smtplib.SMTP(smtp_server, smtp_port) as smtp_connection:
    smtp_connection.starttls()
    smtp_connection.login(smtp_username, smtp_password)
    smtp_connection.sendmail(msg['From'], [msg['To']], msg.as_string())

print("Email sent successfully!")
