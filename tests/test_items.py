from unittest import TestCase
from datetime import datetime, timezone

from scrapy.http.response.html import HtmlResponse

from s3pipeline import Page

EXAMPLE_HTML = '<DOCTYPE! html>\n<html>\n<head>\n</head>\n<body>' + \
    ('long ' * 100) + '</body>\n</html'


class TestItems(TestCase):
    def test_repr(self):
        item = Page()
        item['url'] = 'http://example.com'
        item['body'] = EXAMPLE_HTML
        item['crawled_at'] = datetime.now(timezone.utc).replace(microsecond=0).isoformat()

        self.assertTrue(len(repr(item)) < len(item['body']), 'repr(item) is ommited')

    def test_from_response(self):
        response = HtmlResponse(
            url='http://example.com',
            body=EXAMPLE_HTML.encode('ascii'),
        )

        item = Page.from_response(response)

        self.assertEqual(item['url'], 'http://example.com')
        self.assertEqual(item['body'], EXAMPLE_HTML)
        self.assertIsInstance(item['crawled_at'], str)
