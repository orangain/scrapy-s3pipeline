from unittest import TestCase

from scrapy.settings import BaseSettings

from s3pipeline import S3Pipeline


class TestPipelines(TestCase):
    def setUp(self):
        self.settings = BaseSettings({
            'S3PIPELINE_URL': 's3://my-bucket/{name}/{time}/items.{chunk:07d}.jl.gz',
        })

    def test_settings(self):
        pipeline = S3Pipeline(self.settings, None)
        self.assertEqual(pipeline.bucket_name, 'my-bucket')
        self.assertEqual(pipeline.object_key_template, '{name}/{time}/items.{chunk:07d}.jl.gz')
        self.assertEqual(pipeline.max_chunk_size, 100)
        self.assertTrue(pipeline.use_gzip)
