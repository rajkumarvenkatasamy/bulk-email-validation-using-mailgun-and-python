import os

# Set the environment variable "MAILGUN_API_KEY" with your API key
API_KEY = os.getenv("MAILGUN_API_KEY")

# Mailgun API base URL
MAILGUN_API_URL = "https://api.mailgun.net/v4/address/validate/bulk"

LIST_NAME = "bulk_mailing_list_validation_1"
FILE_PATH = "mailing_list.csv"
COMMAND = "submit_job"  # possible values are "submit_job" and "get_job_status"
