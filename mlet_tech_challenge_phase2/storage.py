import boto3


def get_client():
    client = boto3.resource("s3")
    return client


def create_bucket(client, name):
    client.create_bucket(Bucket=name)
