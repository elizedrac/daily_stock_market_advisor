import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os

def send_email(subject, body):
    # check if the email user and password are set
    if not os.environ["EMAIL_USER"] or not os.environ["EMAIL_PASS"]:
        raise RuntimeError("EMAIL_USER and EMAIL_PASS are missing. Set them in your environment or .env.")

    # get the email user and password
    sender = os.environ["EMAIL_USER"]
    password = os.environ["EMAIL_PASS"]
    recipient = os.environ["EMAIL_TO"]

    # check if the recipient is set
    if not recipient:
        raise RuntimeError("EMAIL_TO is missing. Set it in your environment or .env.")

    # create the email message
    msg = MIMEMultipart()
    msg["From"] = sender
    msg["To"] = recipient
    msg["Subject"] = subject

    # attach the body to the email message
    msg.attach(MIMEText(body, "plain"))

    # send the email
    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        # login to the email server
        server.login(sender, password)
        server.send_message(msg)
