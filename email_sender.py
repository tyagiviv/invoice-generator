import smtplib
import os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
import configparser


def send_invoice(email_recipient, invoice_file_path):
    config = configparser.ConfigParser()
    config.read('config.ini')

    email_sender = config['email']['sender']
    email_password = config['email']['password']

    if not email_password:
        print("Error: EMAIL_PASSWORD is not set.")
        return

    if not email_password:
        print("Error: EMAIL_PASSWORD is not set.")
        return

    print(f"Sending email to: {email_recipient} with invoice: {invoice_file_path}")

    # Create the email message
    msg = MIMEMultipart()
    msg['From'] = email_sender
    msg['To'] = email_recipient
    msg['Subject'] = f"Your Invoice_{invoice_file_path.split('_')[-1].split('.')[0]}"  # Extract the invoice number

    # Email body
    body = "Dear Client,\n\nPlease find attached your invoice.\n\nThank you for your business!"
    msg.attach(MIMEText(body, 'plain'))

    # Attach the invoice PDF
    try:
        with open(invoice_file_path, "rb") as attachment:
            part = MIMEApplication(attachment.read(), Name=invoice_file_path)
            part['Content-Disposition'] = f'attachment; filename="{os.path.basename(invoice_file_path)}"'
            msg.attach(part)
    except FileNotFoundError:
        print(f"Error: The file {invoice_file_path} does not exist.")
        return

    # Send the email
    try:
        with smtplib.SMTP('smtp.gmail.com', 587) as server:  # Use SMTP server
            server.starttls()
            server.login(email_sender, email_password)
            server.send_message(msg)
            print("Email sent successfully!")
    except smtplib.SMTPAuthenticationError:
        print("Error: Failed to authenticate with the email server. Check your email and password.")
    except smtplib.SMTPException as e:
        print(f"SMTP Error: {e}")
    except Exception as e:
        print(f"Failed to send email: {e}")
