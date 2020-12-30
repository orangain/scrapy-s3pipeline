import json

from google.cloud import storage
from google.cloud.exceptions import GoogleCloudError
from google.oauth2 import service_account

from s3pipeline.strategies.error import UploadError

class GCSStrategy:
    def __init__(self, settings):
        kwargs = {}
        kwargs['project'] = settings['GCS_PROJECT_ID']

        if settings['GOOGLE_APPLICATION_CREDENTIALS_JSON']:
            credentials_info = json.loads(settings['GOOGLE_APPLICATION_CREDENTIALS_JSON'])
            credentials = service_account.Credentials.from_service_account_info(
                credentials_info
            )
            kwargs['credentials'] = credentials

        self.client = storage.Client(**kwargs)

    def upload_fileobj(self, f, bucket_name, object_key):
        try:
            bucket = self.client.bucket(bucket_name)
            blob = bucket.blob(object_key)
            blob.upload_from_file(f)
        except GoogleCloudError as ex:
            raise UploadError(ex)
