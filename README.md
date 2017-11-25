# scrapy-s3pipeline

Scrapy pipeline to store items into S3 bucket with JSONLines format. Unlike FeedExporter, the pipeline has the following features:

* The pipeline stores items by chunk.
* Support GZip compression.

## Requirements

* Python 3.4+

## Install

```
$ pip3 install scrapy-s3pipeline
```

## Settings

```
ITEM_PIPELINES = {
    's3pipeline.S3Pipeline': 100,  # Add this line.
}
```

### S3PIPELINE_URL (Required)

Example value: `s3://my-bucket/{name}/items.{chunk:07d}.jl.gz`

It is recommended to use `.gz` suffix if `S3PIPELINE_GZIP` is `True`.

### S3PIPELINE_MAX_CHUNK_SIZE (Optional)

Default: `500`

Max count of items in a single chunk.

### S3PIPELINE_GZIP (Optional)

Default: `True`

If `True`, compress uploaded file with Gzip.
