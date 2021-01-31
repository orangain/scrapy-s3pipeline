from unittest import TestCase

from scrapy.exporters import JsonLinesItemExporter, JsonItemExporter
from scrapy.settings import BaseSettings, default_settings

from s3pipeline import S3Pipeline
from s3pipeline.strategies.s3 import S3Strategy
from s3pipeline.strategies.gcs import GCSStrategy

class TestPipelineSettings(TestCase):

    def test_s3(self):
        settings = BaseSettings({
            'S3PIPELINE_URL': 's3://my-bucket/{name}/{time}/items.{chunk:07d}.jl.gz',
            'FEED_EXPORTERS_BASE': default_settings.FEED_EXPORTERS_BASE,
        })

        pipeline = S3Pipeline(settings, None)
        self.assertEqual(pipeline.bucket_name, 'my-bucket')
        self.assertEqual(pipeline.object_key_template, '{name}/{time}/items.{chunk:07d}.jl.gz')
        self.assertEqual(pipeline.max_chunk_size, 100)
        self.assertTrue(pipeline.use_gzip)
        self.assertEqual(pipeline.max_wait_upload_time, 30)
        self.assertIsInstance(pipeline.strategy, S3Strategy)
        self.assertEqual(pipeline.exporter_cls, JsonLinesItemExporter)


    def test_gcs(self):
        settings = BaseSettings({
            'S3PIPELINE_URL': 'gs://my-bucket/{name}/{time}/items.{chunk:07d}.jl',
            'FEED_EXPORTERS_BASE': default_settings.FEED_EXPORTERS_BASE,
        })

        pipeline = S3Pipeline(settings, None)
        self.assertEqual(pipeline.bucket_name, 'my-bucket')
        self.assertEqual(pipeline.object_key_template, '{name}/{time}/items.{chunk:07d}.jl')
        self.assertEqual(pipeline.max_chunk_size, 100)
        self.assertFalse(pipeline.use_gzip)
        self.assertEqual(pipeline.max_wait_upload_time, 30)
        self.assertIsInstance(pipeline.strategy, GCSStrategy)
        self.assertEqual(pipeline.exporter_cls, JsonLinesItemExporter)

    def test_json(self):
        settings = BaseSettings({
            'S3PIPELINE_URL': 's3://my-bucket/{name}/{time}/items.{chunk:07d}.json',
            'FEED_EXPORTERS_BASE': default_settings.FEED_EXPORTERS_BASE,
        })

        pipeline = S3Pipeline(settings, None)
        self.assertFalse(pipeline.use_gzip)
        self.assertEqual(pipeline.exporter_cls, JsonItemExporter)

    def test_json_gz(self):
        settings = BaseSettings({
            'S3PIPELINE_URL': 's3://my-bucket/{name}/{time}/items.{chunk:07d}.json.gz',
            'FEED_EXPORTERS_BASE': default_settings.FEED_EXPORTERS_BASE,
        })

        pipeline = S3Pipeline(settings, None)
        self.assertTrue(pipeline.use_gzip)
        self.assertEqual(pipeline.exporter_cls, JsonItemExporter)

    def test_force_gzip(self):

        settings = BaseSettings({
            'S3PIPELINE_URL': 's3://my-bucket/{name}/{time}/items.{chunk:07d}.jl',
            'S3PIPELINE_GZIP': True,
            'FEED_EXPORTERS_BASE': default_settings.FEED_EXPORTERS_BASE,
        })

        pipeline = S3Pipeline(settings, None)
        self.assertTrue(pipeline.use_gzip)

    def test_force_no_gzip(self):

        settings = BaseSettings({
            'S3PIPELINE_URL': 's3://my-bucket/{name}/{time}/items.{chunk:07d}.jl.gz',
            'S3PIPELINE_GZIP': False,
            'FEED_EXPORTERS_BASE': default_settings.FEED_EXPORTERS_BASE,
        })

        pipeline = S3Pipeline(settings, None)
        self.assertFalse(pipeline.use_gzip)

    def test_max_chunk_size(self):

        settings = BaseSettings({
            'S3PIPELINE_URL': 's3://my-bucket/{name}/{time}/items.{chunk:07d}.jl.gz',
            'S3PIPELINE_MAX_CHUNK_SIZE': 1000,
            'FEED_EXPORTERS_BASE': default_settings.FEED_EXPORTERS_BASE,
        })

        pipeline = S3Pipeline(settings, None)
        self.assertEqual(pipeline.max_chunk_size, 1000)

    def test_max_wait_upload_time(self):

        settings = BaseSettings({
            'S3PIPELINE_URL': 's3://my-bucket/{name}/{time}/items.{chunk:07d}.jl.gz',
            'S3PIPELINE_MAX_WAIT_UPLOAD_TIME': 300,
            'FEED_EXPORTERS_BASE': default_settings.FEED_EXPORTERS_BASE,
        })

        pipeline = S3Pipeline(settings, None)
        self.assertEqual(pipeline.max_wait_upload_time, 300)
