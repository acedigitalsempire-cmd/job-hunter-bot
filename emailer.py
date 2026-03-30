import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from config import EMAIL_USER, EMAIL_PASS, RECEIVER_EMAIL


def send_email(html_body, job_count=0):
    subject = f"🎯 {job_count} Remote Customer Support Job(s) Found Today"

    msg = MIMEMultipart("alternative")
    msg["Subject"] = subject
    msg["From"] = EMAIL_USER
    msg["To"] = RECEIVER_EMAIL

    part = MIMEText(html_body, "html")
    msg.attach(part)

    try:
        with smtplib.SMTP("smtp-relay.brevo.com", 587) as server:
            server.ehlo()
            server.starttls()
            server.login(os.getenv("SMTP_LOGIN"), EMAIL_PASS)
            server.sendmail(EMAIL_USER, RECEIVER_EMAIL, msg.as_string())
        print(f"[INFO] Email sent successfully to {RECEIVER_EMAIL}")
    except Exception as e:
        print(f"[ERROR] Failed to send email: {e}")
        raise
