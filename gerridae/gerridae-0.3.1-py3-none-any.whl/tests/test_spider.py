"""
test the integer field
"""
import asyncio

from gerridae import Item, Spider, TextField, RegexField
from gerridae.log import get_logger

logger = get_logger(__name__)


class TestBaseField:
    def test_spider(self):
        class TestItem(Item):
            command = TextField(css_select="#pip-command")

        class TestSpider(Spider):
            start_urls = "https://pypi.org/project/gerridae/"

            async def parse(self, resp):
                text = await resp.text(encoding='utf-8')
                result = TestItem.get_item(html=text)
                return result

        results = asyncio.run(TestSpider.start())
        assert "pip install gerridae" == results[0].command

    def test_spider_with_many(self):
        class TestItem(Item):
            command = TextField(css_select="#pip-command", many=True)

        class TestSpider(Spider):
            start_urls = "https://pypi.org/project/gerridae/"

            async def parse(self, resp):
                text = await resp.text(encoding='utf-8')
                result = TestItem.get_item(html=text)
                return result

        results = asyncio.run(TestSpider.start())
        assert ["pip install gerridae"] == results[0].command

    def test_spider_with_multi_urls(self):
        class TestItem(Item):
            command = TextField(css_select="#pip-command", many=True)

        class TestSpider(Spider):
            start_urls = ["https://pypi.org/project/gerridae/", "https://pypi.org/project/gerridae/"]

            async def parse(self, resp):
                text = await resp.text(encoding='utf-8')
                result = TestItem.get_item(html=text)
                setattr(result, 'base_url', resp.url)
                return result

        results = asyncio.run(TestSpider.start())
        assert ["pip install gerridae"] == results[0].command
        assert ["pip install gerridae"] == results[1].command
        assert "https://pypi.org/project/gerridae/" == results[0].base_url

    def test_spider_regex_field(self):
        class TestItem(Item):
            content = RegexField(pattern=r'<div id="content">(.*?)</div>')

        class TestSpider(Spider):
            start_urls = 'https://www.230book.com/book/5483/2065394.html'

            async def parse(self, resp):
                text = await resp.text(encoding='gbk')
                result = TestItem.get_item(html=text)
                return result

        results = asyncio.run(TestSpider.start())
        assert len(results) == 1
        assert len(results[0].content) > 0
