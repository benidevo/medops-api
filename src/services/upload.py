import os

import boto3
from botocore.exceptions import NoCredentialsError

from utils.utils import replace_space


class FileUpload:
    AWS_ACCESS_KEY = os.environ.get("AWS_ACCESS_KEY")
    AWS_SECRET_KEY = os.environ.get("AWS_SECRET_KEY")
    AWS_BUCKET_NAME = os.environ.get("AWS_BUCKET_NAME")

    @classmethod
    def get_s3_client(cls):
        s3_client = boto3.client(
            "s3",
            aws_access_key_id=cls.AWS_ACCESS_KEY,
            aws_secret_access_key=cls.AWS_SECRET_KEY,
        )
        return s3_client

    @classmethod
    def execute(cls, file, file_name=None):
        s3 = cls.get_s3_client()
        file_name = replace_space(file_name)
        try:
            s3.upload_file(file, cls.AWS_BUCKET_NAME, file_name)
            file_url = f"https://{cls.AWS_BUCKET_NAME}.s3.amazonaws.com/{file_name}"
            return {
                "message": "Upload Successful",
                "status": True,
                "status_code": 200,
                "payload": {"file_url": file_url},
            }
        except FileNotFoundError:
            return {
                "message": "The file was not found",
                "status": False,
                "status_code": 404,
            }
        except NoCredentialsError:
            return {
                "message": "Credentials not available",
                "status": False,
                "status_code": 500,
            }
