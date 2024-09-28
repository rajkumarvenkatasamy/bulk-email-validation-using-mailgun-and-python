import logging

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import requests

from .serializers import (
    BulkEmailValidationJobSubmissionSerializer,
    BulkEmailValidationJobStatusSerializer,
)
from .config import MAILGUN_API_KEY, MAILGUN_API_URL


if MAILGUN_API_KEY:
    API_KEY = MAILGUN_API_KEY


class BulkEmailValidationJobSubmissionView(APIView):
    serializer_class = BulkEmailValidationJobSubmissionSerializer

    def post(self, request, format=None):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        mailing_list_file = serializer.validated_data["mailing_list_file"]
        list_name = serializer.validated_data["mailing_list_name"]

        try:
            response = create_bulk_validation_job(list_name, mailing_list_file)
            # Check if the request was successful
            if response.status_code == 202:
                return Response(
                    {
                        "message": f"Bulk validation job created successfully for {list_name}"
                    },
                    status=status.HTTP_202_ACCEPTED,
                )
            else:
                return Response(
                    {f"Error creating validation job: {response.text}"},
                    status=response.status_code,
                )
        except Exception as e:
            return Response(
                {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


def create_bulk_validation_job(list_name, mailing_list_file):
    """
    This function creates a bulk validation job using the Mailgun API.

    :param list_name: The name of the mailing list for validation.
    :param file_path: The path to the CSV file containing emails to validate.
    :return: Response object containing the job details.
    """
    url = f"{MAILGUN_API_URL}/{list_name}"

    try:
        # Sending a POST request with the file to Mailgun's API
        response = requests.post(
            url, auth=("api", API_KEY), files={"file": mailing_list_file}
        )

        return response

    except Exception as e:
        logging.error(f"An error occurred while creating bulk validation job: {str(e)}")
        return None


class GetBulkEmailValidationJobStatusView(APIView):
    serializer_class = BulkEmailValidationJobStatusSerializer

    def get(self, request, format=None):
        serializer = self.serializer_class(data=request.query_params)
        serializer.is_valid(raise_exception=True)

        mailing_list_name = serializer.validated_data["mailing_list_name"]

        try:
            url = f"{MAILGUN_API_URL}/{mailing_list_name}"

            # Sending a GET request to Mailgun's API to fetch the job status
            response = requests.get(url, auth=("api", API_KEY))

            result = response.json()

            return Response(result, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(
                {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
