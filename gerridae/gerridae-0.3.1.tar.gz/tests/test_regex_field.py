"""
test the integer field
"""
import asyncio

from gerridae import Item, RegexField, Spider
from gerridae.log import get_logger

logger = get_logger(__name__)


class TestRegexField(object):
    def test_regex_filed(self):
        class TestItem(Item):
            command = RegexField(pattern='id="pip-command">(.*?)</span>', many=False)

        class TestSpider(Spider):
            start_urls = "https://pypi.org/project/gerridae/"

            async def parse(self, resp):
                text = await resp.text(encoding='utf-8')
                result = TestItem.get_item(html=text)
                return result

        results = asyncio.run(TestSpider.start())
        print(results)
        assert "pip install gerridae" == results[0].command

    def test_regex_field_with_many(self):
        class TestItem(Item):
            command = RegexField(pattern='id="pip-command">(.*?)</span>', many=True)

        class TestSpider(Spider):
            start_urls = 'https://pypi.org/project/gerridae/'

            async def parse(self, resp):
                text = await resp.text(encoding='utf-8')
                result = TestItem.get_item(html=text)
                return result

        results = asyncio.run(TestSpider.start())
        assert ['pip install gerridae'] == results[0].command
