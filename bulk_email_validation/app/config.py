import os

MAILGUN_API_KEY = os.getenv("MAILGUN_API_KEY")
MAILGUN_API_URL = "https://api.mailgun.net/v4/address/validate/bulk"
