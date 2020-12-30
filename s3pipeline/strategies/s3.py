import boto3
from botocore.exceptions import ClientError

from . import UploadError

class S3Strategy:
    def __init__(self, settings):
        self.client = boto3.client(
            's3',
            region_name=settings['AWS_REGION_NAME'], use_ssl=settings['AWS_USE_SSL'],
            verify=settings['AWS_VERIFY'], endpoint_url=settings['AWS_ENDPOINT_URL'],
            aws_access_key_id=settings['AWS_ACCESS_KEY_ID'],
            aws_secret_access_key=settings['AWS_SECRET_ACCESS_KEY'])

    def upload_fileobj(self, f, bucket_name, object_key):
        try:
            self.client.upload_fileobj(f, bucket_name, object_key)
        except ClientError as ex:
            raise UploadError(ex)

