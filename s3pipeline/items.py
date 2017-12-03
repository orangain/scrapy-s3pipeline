from datetime import datetime, timezone

import scrapy


class Page(scrapy.Item):
    """
    General scrapy item to store entire HTTP body
    """

    url = scrapy.Field()
    body = scrapy.Field()
    crawled_at = scrapy.Field()

    def __repr__(self):
        """
        Omit body to shorten logs.
        """

        p = self.__class__(self)  # Duplicate Page instance
        if len(p['body']) > 203:
            p['body'] = p['body'][:100] + '...' + p['body'][-100:]

        return super(Page, p).__repr__()  # Return representation of duplicated page

    @classmethod
    def from_response(cls, response):
        item = cls()
        item['url'] = response.url
        item['body'] = response.text
        item['crawled_at'] = datetime.now(timezone.utc).replace(microsecond=0).isoformat()
        return item
