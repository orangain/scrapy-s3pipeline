# Scrapy S3 Pipeline

[![PyPI version](https://badge.fury.io/py/scrapy-s3pipeline.svg)](https://badge.fury.io/py/scrapy-s3pipeline) ![CI](https://github.com/orangain/scrapy-s3pipeline/workflows/CI/badge.svg)

Scrapy pipeline to store items into [Amazon S3](https://aws.amazon.com/s3/) or [Google Cloud Storage (GCS)](https://cloud.google.com/storage) bucket with JSONLines format. Unlike built-in [FeedExporter](https://docs.scrapy.org/en/latest/topics/feed-exports.html#s3), the pipeline has the following features:

* The pipeline upload items to S3/GCS by chunk while crawler is running.
* Support GZip compression.

The pipeline aims to run crawler and scraper in different processes, e.g. run crawler process with Scrapy in AWS Fargate and run scraper process with lxml in AWS Lambda.

## Requirements

* Python 3.6+ (Tested in 3.9)
* Scrapy 1.1+ (Tested in 2.4)
* boto3 or google-cloud-storage

## Install

**For S3 users:**

```shell-session
$ pip3 install scrapy-s3pipeline[s3]
```

**For GCS users:**

```shell-session
$ pip3 install scrapy-s3pipeline[gcs]
```

## Getting started

1. Install Scrapy S3 Pipeline with pip.

    ```shell-session
    $ pip3 install scrapy-s3pipeline[s3]
    ```

    or

    ```shell-session
    $ pip3 install scrapy-s3pipeline[gcs]
    ```

2.  Add `'s3pipeline.S3Pipeline'` to `ITEM_PIPELINES` setting in your Scrapy project.

    ```py
    ITEM_PIPELINES = {
        's3pipeline.S3Pipeline': 100,  # Add this line.
    }
    ```

3. Add `S3PIPELINE_URL` setting. You need to change `my-bucket` to your bucket name.

    ```py
    # For S3 users
    S3PIPELINE_URL = 's3://my-bucket/{name}/{time}/items.{chunk:07d}.jl.gz'

    # For GCS users
    S3PIPELINE_URL = 'gs://my-bucket/{name}/{time}/items.{chunk:07d}.jl.gz'
    GCS_PROJECT_ID = 'my-project' # Change to your project id
    ```

4. Setup AWS/GCP credentials.

    **For S3 users:**

    Setup AWS credentials via `aws configure` command or [environment variables](https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-envvars.html). Alternatively, use Scrapy's settings [AWS_ACCESS_KEY_ID](https://docs.scrapy.org/en/latest/topics/settings.html#aws-access-key-id) and [AWS_SECRET_ACCESS_KEY](https://docs.scrapy.org/en/latest/topics/settings.html#aws-secret-access-key).

    **For GCS users:**

    Setup GCP credentials via `gcloud auth application-default login` command or environment variable [GOOGLE_APPLICATION_CREDENTIALS](https://cloud.google.com/docs/authentication/getting-started). Alternatively, you can set json string of service account's key file to `GOOGLE_APPLICATION_CREDENTIALS_JSON` settings.

5. Run your spider. You will see items in your bucket after 100 items are crawled or the spider is closed.

## Settings

### S3PIPELINE_URL (Required)

S3/GCS Bucket URL to store items.

e.g.:

* S3: `s3://my-bucket/{name}/{time}/items.{chunk:07d}.jl.gz`
* GCS: `gs://my-bucket/{name}/{time}/items.{chunk:07d}.jl.gz`

The following replacement fields are supported in `S3PIPELINE_URL`.

* `{chunk}` - gets replaced by a start index of items in current chunk, e.g. '0', '100', '200',....
* `{time}` - gets replaced by a timestamp when the spider is started.

You can also use other spider fields, e.g. `{name}`. You can use [format string syntax](https://docs.python.org/3/library/string.html#formatstrings) here, e.g. `{chunk:07d}`.

### S3PIPELINE_MAX_CHUNK_SIZE (Optional)

Default: `100`

Max count of items in a single chunk.

### S3PIPELINE_MAX_WAIT_UPLOAD_TIME (Optional)

Default: `30.0`

When no new item is processed in more than `S3PIPELINE_MAX_WAIT_UPLOAD_TIME` seconds, it will be forced to upload a chunk.

### S3PIPELINE_GZIP (Optional)

Default: `True` if `S3PIPELINE_URL` ends with `.gz`; otherwise `False`.

If `True`, uploaded files will be compressed with Gzip.

## Page item

For convinience, Scrapy S3 Pipeline provides `s3pipeline.Page` item class to store entire HTTP body. It has `url`, `body` and `crawled_at` fields.

This make it easy to store entire HTTP body and run scraper in other process. It's friendly to server-less architecture which run scraper in AWS Lambda.

Example usage of Page:

```py
from datetime import datetime, timezone

import scrapy
from s3pipeline import Page

# ...

class YourSpider(scrapy.Spider):

    # ...

    def parse(self, response):
        # You can create Page instance just one line.
        yield Page.from_response(response)

        # Or, you can fill item fields manually.
        item = Page()
        item['url'] = response.url
        item['body'] = response.text
        item['crawled_at'] = datetime.now(timezone.utc).replace(microsecond=0).isoformat()
        yield item
```

Note: Page's body is omitted when printed to logs to improve readbility of logs.

## Development

### Test

```
$ python3 setup.py test
```

### Release

```
$ pip install twine wheel
```

```
$ python3 setup.py bdist_wheel sdist
$ twine upload dist/*
```
