import smtplib
from email.message import EmailMessage
import ssl
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# Normal email sending:
def send_mail(email_sender, email_password, email_receiver, subject, body):
    em = EmailMessage()
    em['From'] = email_sender
    em['To'] = email_receiver
    em['Subject'] = subject
    em.set_content(body)

    # Add SSL (layer of security)
    context = ssl.create_default_context()

    # Log in and send the email
    with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
        smtp.login(email_sender, email_password)
        smtp.sendmail(email_sender, email_receiver, em.as_string())

# Email sending with embedded HTML:
def send_alt_mail(email_sender, email_password, email_receiver, subject, text, html):
    port = 587
    smtp_server = "live.smtp.mailtrap.io"
    login = email_sender
    password = email_password
    sender_email = email_sender
    receiver_email = email_receiver
    message = MIMEMultipart("alternative")
    message["Subject"] = subject
    message["From"] = sender_email
    message["To"] = receiver_email
    text = text
    html = html
    part1 = MIMEText(text, "plain")
    part2 = MIMEText(html, "html")
    message.attach(part1)
    message.attach(part2)

    context = ssl.create_default_context()

    with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
        smtp.login(sender_email, password)
        smtp.sendmail(sender_email, receiver_email, message.as_string())