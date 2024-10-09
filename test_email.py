import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
import os

def test_send_email():
    email_sender = "vivekbeginning@gmail.com"
    email_password = "rihz qcsn gnwb wckx"
#    email_password = os.getenv("EMAIL_PASSWORD")
    email_recipient = "vivekbeginning@gmail.com"  # Change this to a real recipient email
    invoice_file_path = "/Users/v/PycharmProjects/invoice_generator/invoice_16.pdf"  # Change this to a real file path

    msg = MIMEMultipart()
    msg['From'] = email_sender
    msg['To'] = email_recipient
    msg['Subject'] = "Test Email"

    body = "Dear Client,\n\nPlease find attached your invoice.\n\nThank you for your business!"
    msg.attach(MIMEText(body, 'plain'))

    with open(invoice_file_path, "rb") as attachment:
        part = MIMEApplication(attachment.read(), Name=os.path.basename(invoice_file_path))
        part['Content-Disposition'] = f'attachment; filename="{os.path.basename(invoice_file_path)}"'
        msg.attach(part)

    try:
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            server.login(email_sender, email_password)
            server.send_message(msg)
            print("Test email sent successfully!")

    except Exception as e:
        print(f"Failed to send test email: {e}")



# Call the function to test email sending
test_send_email()
