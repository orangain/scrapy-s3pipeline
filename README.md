# Scrapy S3 Pipeline

Scrapy pipeline to store items into S3 bucket with JSONLines format. Unlike FeedExporter, the pipeline has the following features:

* The pipeline upload items to S3 by chunk while crawler is running.
* Support GZip compression.

The pipeline aims to run crawler and scraper in different processes, e.g. run crawler process with Scrapy in AWS Fargate and run scraper process with lxml in AWS Lambda.

## Requirements

* Python 3.4+ (Tested in 3.6)
* Scrapy 1.1+ (Tested in 1.4)
* boto3

## Install

```shell-session
$ pip3 install scrapy-s3pipeline
```

## Getting started

1. Install Scrapy S3 Pipeline with pip.

    ```shell-session
    $ pip3 install scrapy-s3pipeline
    ```

2.  Add `'s3pipeline.S3Pipeline'` to `ITEM_PIPELINES` setting in your Scrapy project.

    ```py
    ITEM_PIPELINES = {
        's3pipeline.S3Pipeline': 100,  # Add this line.
    }
    ```

3. Add `S3PIPELINE_URL` setting. You need to change `my-bucket` to your bucket name.

    ```py
    S3PIPELINE_URL = 's3://my-bucket/{name}/{time}/items.{chunk:07d}.jl.gz'
    ```

4. Run your spider. You will see items in your bucket after 100 items are crawled or the spider is closed.

## Settings

### S3PIPELINE_URL (Required)

S3 Bucket URL to store items.

e.g.: `s3://my-bucket/{name}/{time}/items.{chunk:07d}.jl.gz`

The following replacement fields are supported in `S3PIPELINE_URL`.

* `{chunk}` - gets replaced by a start index of items in current chunk, e.g. '0', '100', '200',....
* `{time}` - gets replaced by a timestamp when the spider is started.

You can also use other spider fields, e.g. `{name}`. You can use [format string syntax](https://docs.python.org/3/library/string.html#formatstrings) here, e.g. `{chunk:07d}`.

### S3PIPELINE_MAX_CHUNK_SIZE (Optional)

Default: `100`

Max count of items in a single chunk.

### S3PIPELINE_GZIP (Optional)

Default: `True` if `S3PIPELINE_URL` ends with `.gz`; otherwise `False`.

If `True`, compress uploaded file with Gzip.

## Page item

For convinience, Scrapy S3 Pipeline provides `s3pipeline.Page` item class to store entire HTTP body. It has `url`, `body` and `crawled_at` fields.

This make it easy to store entire HTTP body and run scraper in other process. It's friendly to server-less architecture which run scraper in AWS Lambda.

Example usage of Page:

```py
from datetime import datetime

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
        item['crawled_at'] = datetime.now()
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
$ python3 setup.py bdist_wheel sdist
$ twine upload dist/*
```
