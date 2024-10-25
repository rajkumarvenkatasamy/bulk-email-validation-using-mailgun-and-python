import os

# Retrieve the API key from the environment variable
API_KEY = os.getenv("MAILGUN_API_KEY")

# Mailgun API base URL
MAILGUN_API_URL = "https://api.mailgun.net/v4/address/validate/bulk"

LIST_NAME = "bulk_mailing_list_validation_1"
FILE_PATH = "mailing_list.csv"
COMMAND = "get_job_status"  # Possible values are "submit_job" and "get_job_status"
