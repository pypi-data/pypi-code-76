from aws_cdk import core
from aws_static_website.website_stack import WebsiteStack
from aws_cdk_test_synth.test_synth import TestSynth

class TestWebsiteStack(TestSynth):
    def __init__(self, *args, **kwargs):
        TestSynth.__init__(self, 'tests/website_stack.yaml', *args, **kwargs)

    def synth(self, app):
        WebsiteStack(app, 
            id="test",
            bucket_name="bucket.domain.name",
            website_params={
                "index_document": "index.html",
                "error_document": "index.html"
            },
            hosted_params={
                "zone_name": "domain.name"
            }
        )

    def synth_with_zone_id(self, app):
        WebsiteStack(app, 
            id="test",
            bucket_name="bucket.domain.name",
            website_params={
                "index_document": "index.html",
                "error_document": "index.html"
            },
            hosted_params={
                "zone_name": "domain.name",
                "zone_id": "Z2FDTNDATAQYW2"
            }
        )

    def synth_without_hosted_zone(self, app):
        WebsiteStack(app, 
            id="test",
            bucket_name="bucket.domain.name",
            website_params={
                "index_document": "index.html",
                "error_document": "index.html"
            }
        )

    def test_synth_with_zone_id(self):
        self.load_template('tests/website_stack_with_zone_id.yaml')
        self.synthesizes('synth_with_zone_id')

    def test_synth_without_hosted_zone(self):
        self.load_template('tests/website_stack_without_hosted_zone.yaml')
        self.synthesizes('synth_without_hosted_zone')

if __name__ == '__main__':
    unittest.main()
