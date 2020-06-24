import os
from logging import warning

from dotenv import load_dotenv

load_dotenv()

API_V1_STR = "/api/v1"

"""
a string of origins separated by commas, e.g: "http://localhost, http://localhost:4200,
http://localhost:3000, http://localhost:8080, http://local.dockertoolbox.tiangolo.com"
"""
BACKEND_CORS_ORIGINS = os.getenv("BACKEND_CORS_ORIGINS")

PROJECT_NAME = os.getenv("PROJECT_NAME")
DATABASE_URL = os.getenv("DATABASE_URL")
SECRET_KEY = os.getenv("SECRET_KEY")

# 60 minutes * 24 hours * 8 days = 8 days
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24 * 8

OTP_EXPIRY_MINUTES = 5

# Configs for sending emails
if os.getenv("MAIL_ENABLED") == "True":
    MAIL_ENABLED = True
    MAIL_SERVER = os.getenv("MAIL_SERVER")
    MAIL_PORT = int(os.getenv("MAIL_PORT")) or 465
    MAIL_USERNAME = os.getenv("MAIL_USERNAME")
    MAIL_PASSWORD = os.getenv("MAIL_PASSWORD")
    MAIL_SENDER = os.getenv("MAIL_SENDER")
    if tls := os.getenv("MAIL_USE_TLS"):
        if tls == "True":
            MAIL_USE_TLS = True
        elif tls == "False":
            MAIL_USE_TLS = False
            warning("Setting MAIL_USE_TLS to `False`")
    else:
        MAIL_USE_TLS = True
        warning("Invalid .env value provided for MAIL_USE_TLS. Setting it to `True`")
else:
    warning("Setting MAIL_ENABLED env variable `False`")
    MAIL_ENABLED = False
