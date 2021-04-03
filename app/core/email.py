from email.message import EmailMessage

import aiosmtplib
from pydantic import EmailStr

from app.core import config


async def send_email_verify_otp(email: EmailStr, otp: int):
    if not config.TESTING:
        message = EmailMessage()
        message["From"] = config.MAIL_SENDER
        message["To"] = email
        message["Subject"] = "Verify email"
        message.set_content("Your OTP is " + str(otp))

        await aiosmtplib.send(
            message,
            sender=config.MAIL_SENDER,
            recipients=[email],
            hostname=config.MAIL_SERVER,
            port=config.MAIL_PORT,
            username=config.MAIL_USERNAME,
            password=config.MAIL_PASSWORD,
            use_tls=config.MAIL_USE_TLS,
        )
