import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from ..core.config import settings


class EmailService:
    @staticmethod
    async def send_verification_email(email: str, token: str):
        # Add these to your Settings class
        sender_email = settings.EMAIL_FROM  # Add to config
        sender_password = settings.EMAIL_PASSWORD  # Add to config

        verification_link = f"http://localhost:3000/auth/verify-email?token={token}"

        message = MIMEMultipart()
        message["From"] = sender_email
        message["To"] = email
        message["Subject"] = "Verify your Email"

        html = f"""
        <h2>Welcome!</h2>
        <p>Click the link below to verify your email:</p>
        <a href="{verification_link}">{verification_link}</a>
        """

        message.attach(MIMEText(html, "html"))

        try:
            with smtplib.SMTP("smtp.gmail.com", 587) as server:
                server.starttls()
                server.login(sender_email, sender_password)
                server.send_message(message)
        except Exception as e:
            raise Exception(f"Error sending email: {str(e)}")
