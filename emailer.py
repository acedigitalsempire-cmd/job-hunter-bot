import os
import resend

RECEIVER_EMAIL = os.getenv("RECEIVER_EMAIL", "jobhauntgithub@gmail.com")
EMAIL_FROM = "Job Hunter Bot <onboarding@resend.dev>"

resend.api_key = os.getenv("RESEND_API_KEY")


def send_email(html_body, job_count=0):
    subject = f"🎯 {job_count} Remote Customer Support Job(s) Found Today"

    try:
        params = {
            "from": EMAIL_FROM,
            "to": [RECEIVER_EMAIL],
            "subject": subject,
            "html": html_body,
        }
        email = resend.Emails.send(params)
        print(f"[INFO] Email sent successfully. ID: {email['id']}")
    except Exception as e:
        print(f"[ERROR] Failed to send email: {e}")
        raise
