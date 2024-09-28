from rest_framework import serializers


class BulkEmailValidationJobSubmissionSerializer(serializers.Serializer):
    mailing_list_file = serializers.FileField()
    mailing_list_name = serializers.CharField()


class BulkEmailValidationJobStatusSerializer(serializers.Serializer):
    mailing_list_name = serializers.CharField()
