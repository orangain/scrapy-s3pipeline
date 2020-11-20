from io import BytesIO
from urllib.parse import urlparse
from datetime import datetime
import gzip
from threading import Timer

import boto3
from botocore.exceptions import ClientError

from scrapy.exporters import JsonLinesItemExporter


class S3Pipeline:
    """
    Scrapy pipeline to store items into S3 bucket with JSONLines format.
    Unlike FeedExporter, the pipeline has the following features:

    * The pipeline stores items by chunk.
    * Support GZip compression.
    """

    def __init__(self, settings, stats):
        self.stats = stats

        url = settings['S3PIPELINE_URL']
        o = urlparse(url)
        self.bucket_name = o.hostname
        self.object_key_template = o.path[1:]  # Remove the first '/'

        self.max_chunk_size = settings.getint('S3PIPELINE_MAX_CHUNK_SIZE', 100)
        self.use_gzip = settings.getbool('S3PIPELINE_GZIP', url.endswith('.gz'))
        self.max_wait_upload_time = settings.getfloat('S3PIPELINE_MAX_WAIT_UPLOAD_TIME', 30.0)
        self.item_exporter_args = settings.get('S3PIPELINE_ITEM_EXPORTER_ARGS', {})

        self.s3 = boto3.client(
            's3',
            region_name=settings['AWS_REGION_NAME'], use_ssl=settings['AWS_USE_SSL'],
            verify=settings['AWS_VERIFY'], endpoint_url=settings['AWS_ENDPOINT_URL'],
            aws_access_key_id=settings['AWS_ACCESS_KEY_ID'],
            aws_secret_access_key=settings['AWS_SECRET_ACCESS_KEY'])
        self.items = []
        self.chunk_number = 0

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler.settings, crawler.stats)

    def process_item(self, item, spider):
        """
        Process single item. Add item to items and then upload to S3 if size of items
        >= max_chunk_size.
        """
        self._timer_cancel()

        self.items.append(item)
        if len(self.items) >= self.max_chunk_size:
            self._upload_chunk()

        self._timer_start()

        return item

    def open_spider(self, spider):
        """
        Callback function when spider is open.
        """
        # Store timestamp to replace {time} in S3PIPELINE_URL
        self.ts = datetime.utcnow().replace(microsecond=0).isoformat().replace(':', '-')
        self._spider = spider
        self._timer = None

    def close_spider(self, spider):
        """
        Callback function when spider is closed.
        """
        # Upload remained items to S3.
        self._upload_chunk()
        self._timer_cancel()

    def _upload_chunk(self):
        """
        Do upload items to S3.
        """
        
        if not self.items:
            return  # Do nothing when items is empty.

        f = self._make_fileobj()

        # Build object key by replacing variables in object key template.
        object_key = self.object_key_template.format(**self._get_uri_params())

        try:
            self.s3.upload_fileobj(f, self.bucket_name, object_key)
        except ClientError:
            self.stats.inc_value('pipeline/s3/fail')
            raise
        else:
            self.stats.inc_value('pipeline/s3/success')
        finally:
            # Prepare for the next chunk
            self.chunk_number += len(self.items)
            self.items = []

    def _get_uri_params(self):
        params = {}
        for key in dir(self._spider):
            params[key] = getattr(self._spider, key)

        params['chunk'] = self.chunk_number
        params['time'] = self.ts
        return params

    def _make_fileobj(self):
        """
        Build file object from items.
        """

        bio = BytesIO()
        f = gzip.GzipFile(mode='wb', fileobj=bio) if self.use_gzip else bio

        # Build file object using ItemExporter
        exporter = JsonLinesItemExporter(f, **self.item_exporter_args)
        exporter.start_exporting()
        for item in self.items:
            exporter.export_item(item)
        exporter.finish_exporting()

        if f is not bio:
            f.close()  # Close the file if GzipFile

        # Seek to the top of file to be read later
        bio.seek(0)

        return bio
    
    def _timer_start(self):
        """
        Start the timer in s3pipeline
        """
        self._timer = Timer(self.max_wait_upload_time, self._upload_chunk)
        self._timer.start()
    
    def _timer_cancel(self):
        """
        Stop the timer in s3pipeline
        """
        if self._timer is not None:
            self._timer.cancel()
