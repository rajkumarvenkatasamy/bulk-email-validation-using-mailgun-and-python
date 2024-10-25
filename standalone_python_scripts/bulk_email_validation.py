import io
import os
import requests
import json
import logging
import zipfile

from config import API_KEY, LIST_NAME, FILE_PATH, COMMAND, MAILGUN_API_URL

# Enable logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(funcName)s - %(message)s",
)


def create_bulk_validation_job(list_name, file_path):
    """
    This function creates a bulk validation job using the Mailgun API.

    :param list_name: The name of the mailing list for validation.
    :param file_path: The path to the CSV file containing emails to validate.
    :return: Response object containing the job details.
    """
    url = f"{MAILGUN_API_URL}/{list_name}"

    try:
        # Send a POST request with the file to Mailgun's API
        with open(file_path, "rb") as file_data:
            response = requests.post(
                url, auth=("api", API_KEY), files={"file": file_data}
            )

        # Check if the request was successful
        if response.status_code == 202:
            logging.info(f"Bulk validation job created successfully for {list_name}")
        else:
            logging.error(
                f"Error creating validation job: {response.status_code} {response.text}"
            )

        return response.json()

    except Exception as e:
        logging.error(f"An error occurred while creating bulk validation job: {str(e)}")
        return None


def get_bulk_validation_status(list_name):
    """
    This function checks the status of a bulk validation job and downloads the validation results.

    :param list_name: The name of the mailing list for which the status is being checked.
    :return: Validation results or None in case of failure.
    """
    url = f"{MAILGUN_API_URL}/{list_name}"

    try:
        # Send a GET request to Mailgun's API to fetch the job status
        response = requests.get(url, auth=("api", API_KEY))

        # Check if the request was successful
        if response.status_code == 200:
            logging.info(f"Successfully retrieved validation status for {list_name}")

            # Parse the JSON response
            result = response.json()

            # Fetch the download URL for JSON results
            download_url = result.get("download_url", {}).get("json")
            if download_url:
                # Fetch and return the validation results
                return download_validation_results(download_url)
            else:
                logging.info("Download URL not available.")
                return None

        else:
            logging.error(
                f"Error fetching job status: {response.status_code} {response.text}"
            )
            return None

    except Exception as e:
        logging.error(
            f"An error occurred while fetching bulk validation status: {str(e)}"
        )
        return None


def download_validation_results(download_url):
    """
    This function downloads and processes the bulk validation results from the provided URL.

    :param download_url: The URL to download the validation results in JSON format.
    :return: Parsed results or None in case of failure.
    """
    try:
        response = requests.get(download_url)

        # Check if the request was successful
        if response.status_code == 200:
            logging.info("Successfully downloaded validation results.")

            with zipfile.ZipFile(io.BytesIO(response.content)) as zip_ref:
                validation_results_path = os.path.join(
                    os.getcwd(), "validation_results"
                )
                zip_ref.extractall(path=validation_results_path)

            with zipfile.ZipFile(io.BytesIO(response.content)) as zip_ref:
                for file in zip_ref.namelist():
                    if file.endswith(".json"):
                        with zip_ref.open(file) as json_file:
                            validation_results = json.load(json_file)

            # Process the results (handle invalid emails, etc.)
            process_validation_results(validation_results)

            return validation_results

        else:
            logging.error(
                f"Error downloading results: {response.status_code} {response.text}"
            )
            return None

    except Exception as e:
        logging.error(
            f"An error occurred while downloading validation results: {str(e)}"
        )
        return None


def process_validation_results(results):
    """
    This function processes the validation results and handles invalid and risky emails.

    :param results: The JSON object containing the validation results.
    """
    try:
        count_of_deliverable_addresses: int = 0
        emails_tobe_verified = set()

        # Extract the results summary
        logging.info(f"Total email addresses validated: {len(results)}")

        for result in results:
            # Access data within each dictionary
            deliverable = (
                result["result"] == "deliverable"
            )  # Check if result is deliverable
            undeliverable = result["result"] != "deliverable"
            risk = result["risk"]

            # Count the number of deliverable addresses
            if deliverable:
                count_of_deliverable_addresses += 1

            # Count the number of undeliverable addresses and add them to the list for verification
            if undeliverable:
                emails_tobe_verified.add(result["address"])

            # Count the number of risky addresses and add them to the list for verification
            if risk != "low":
                emails_tobe_verified.add(result["address"])

        # Log the results summary
        logging.info(f"Found {count_of_deliverable_addresses} deliverable emails")

        if len(emails_tobe_verified) > 0:
            logging.warning(
                "Found some emails that need to be verified because of its risky or undeliverable state."
            )
            logging.warning(
                "Total emails to be verified: {}".format(len(emails_tobe_verified))
            )
            logging.warning(f"Emails to be verified: {', '.join(emails_tobe_verified)}")

    except Exception as e:
        logging.error(
            f"An error occurred while processing validation results: {str(e)}"
        )


if __name__ == "__main__":

    if COMMAND == "submit_job":
        create_bulk_validation_job(LIST_NAME, FILE_PATH)
    elif COMMAND == "get_job_status":
        get_bulk_validation_status(LIST_NAME)
    else:
        logging.error("Invalid command. Please use 'submit_job' or 'get_job_status'.")
