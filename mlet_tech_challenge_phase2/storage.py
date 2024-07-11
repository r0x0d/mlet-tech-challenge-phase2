import boto3
from botocore.exceptions import ClientError


class S3Storage:
    def __init__(self) -> None:
        self._client = boto3.client("s3")

    def create_bucket(self, name: str) -> None:
        """Create a bucket with a given name"""
        self._client.create_bucket(Bucket=name)

    def upload_file(
        self,
        bucket: str,
        file_name: str,
        object_name: str,
    ) -> None:
        """Upload a local file to the s3 bucket"""
        try:
            self._client.upload_file(file_name, bucket, object_name)
        except ClientError as e:
            print(e)
