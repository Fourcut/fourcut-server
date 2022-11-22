import os

import boto3
from botocore.client import BaseClient
from dotenv import load_dotenv

load_dotenv()

AWS_ACCESS_KEY_ID = os.environ.get("AWS_ACCESS_KEY_ID")
AWS_SECRET_KEY = os.environ.get("AWS_SECRET_KEY")


def s3_auth() -> BaseClient:
    s3 = boto3.client(
        service_name="s3",
        region_name="ap-northeast-2",
        aws_access_key_id=AWS_ACCESS_KEY_ID,
        aws_secret_access_key=AWS_SECRET_KEY,
    )

    return s3
