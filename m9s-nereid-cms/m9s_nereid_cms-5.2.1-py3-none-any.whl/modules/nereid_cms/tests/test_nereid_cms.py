# The COPYRIGHT file at the top level of this repository contains
# the full copyright notices and license terms.
import unittest
import io
import time
import os
import sys

from io import BytesIO
from lxml import objectify

import trytond.tests.test_tryton
from trytond.tests.test_tryton import DB_NAME, with_transaction
from trytond.config import config
from trytond.pool import Pool
from trytond.transaction import Transaction

from nereid.testing import NereidModuleTestCase
from nereid import render_template

from trytond.modules.nereid.tests.test_common import (create_website,
    create_static_file)


def create_article_category(title='Test Category', unique_name='test_category'):
    """
    Create an article category
    """
    pool = Pool()
    ArticleCategory = pool.get('nereid.cms.article.category')

    article_category, = ArticleCategory.create([{
                'title': title,
                'unique_name': unique_name,
                }])
    return article_category


def create_article(title='Test Article', uri='test-article',
        content='Test Content', sequence=10, categories=[], state='draft',
        attributes=[]):
    """
    Create an article
    """
    pool = Pool()
    Article = pool.get('nereid.cms.article')

    if not categories:
        categories = [create_article_category().id]

    data = {'title': title,
            'uri': uri,
            'content': content,
            'sequence': sequence,
            'categories': [('add', categories)],
            'state': state,
            }
    if attributes:
        data['attributes'] = [('create', attributes)]

    article, = Article.create([data])

    return article


def create_banner_category(name='Test Banner Category'):
    """
    Create a banner category
    """
    pool = Pool()
    BannerCategory = pool.get('nereid.cms.banner.category')

    banner_categories = BannerCategory.search([('name', '=', name)])
    if banner_categories:
        return banner_categories[0]

    banner_category, = BannerCategory.create([{
                'name': name,
                }])
    return banner_category


def create_banner(name='Test Banner', type='custom_code',
        custom_code='Custom Banner Code', file=None, category=None,
        state='draft'):
    """
    Create a banner
    """
    pool = Pool()
    Banner = pool.get('nereid.cms.banner')

    data = {'name': name,
            'category': category,
            'type': type,
            'custom_code': custom_code,
            'state': state,
            }
    if custom_code:
        data['custom_code'] = custom_code
    if file:
        data['file'] = file
    banner, = Banner.create([data])

    return banner


class NereidCmsTestCase(NereidModuleTestCase):
    'Test Nereid Cms module'
    module = 'nereid_cms'

    def setUp(self):
        self.templates = {
            'home.jinja':
            '''{% for banner in get_banner_category("CAT-A", silent=False).banners %}
            {{ banner.get_html()|safe }}
            {% endfor %}
            ''',
            'article-category.jinja': '{{ articles|length }}',
            'article.jinja': '{{ article.content }}',
            'test-category.jinja':
            '''{% for article in articles %}
            {{ article.uri }}
            {% endfor %}
            ''',
            }

    @with_transaction()
    def test_0010_article_category(self):
        '''
        Successful rendering of an article_category page
        '''
        app = self.get_app()

        create_website()
        category = create_article_category(unique_name='test-categ')
        article1 = create_article(title='Test Article 1', uri='test-article1',
            sequence=10, categories=[category.id], state='published')
        article2 = create_article(title='Test Article 2', uri='test-article2',
            sequence=20, categories=[category.id], state='draft')

        with app.test_client() as c:
            response = c.get('/en/article-category/test-categ/')
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.data.decode('utf-8'), '1')
            self.assertEqual(len(category.published_articles), 1)
            self.assertEqual(len(category.articles), 2)

    @with_transaction()
    def test_0015_get_article_category(self):
        """
        Test for the return values of context processor get_article_category()
        """
        self.templates = {
            'home.jinja':
            '''{% for article in get_article_category("CAT-A", silent=False).articles %}
            {{ article.uri|safe }}
            {{ article.publish_date|safe }}
            {% endfor %}
            ''',
            }

        website = create_website()

        template_unique_name = 'CAT-A'
        category1 = create_article_category(unique_name='CAT-0')
        article1 = create_article(title='Test Article 1', uri='test-article1',
            sequence=10, categories=[category1.id], state='published')

        # RuntimeError for non-existent category, context processor called with
        # silent=False
        app = self.get_app()
        with self.assertRaises(RuntimeError) as a, app.test_client() as c:
            response = c.get('/en/')
        self.assertEqual('Article category %s not found' % template_unique_name,
            str(a.exception))

        # Now provide a category with correct unique_name
        category2 = create_article_category(unique_name='CAT-A')
        article2 = create_article(title='Test Article 2', uri='test-article2',
            sequence=10, categories=[category2.id], state='published')

        app = self.get_app()
        with app.test_client() as c:
            response = c.get('/en/')
            self.assertIn('test-article2', response.data.decode('utf-8'))

    @with_transaction()
    def test_0020_article(self):
        '''
        Successful rendering of an article page
        '''
        pool = Pool()
        Article = pool.get('nereid.cms.article')

        app = self.get_app()

        create_website()
        category = create_article_category(unique_name='test-categ')
        article1 = create_article(title='Test Article 1', uri='test-article1',
            sequence=10, categories=[category.id], state='draft')

        # Publish the article first
        Article.publish([article1])

        with app.test_client() as c:
            response = c.get('/en/article/test-article1')
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.data.decode('utf-8'), 'Test Content')

    @with_transaction()
    def test_0030_sitemapindex(self):
        '''
        Successful index rendering
        '''
        app = self.get_app()

        create_website()
        with app.test_client() as c:
            response = c.get('/en/sitemaps/article-category-index.xml')
            self.assertEqual(response.status_code, 200)
            self.assertTrue(
                '<sitemapindex xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'
                in response.data.decode('utf-8'))

    @with_transaction()
    def test_0040_category_sitemap(self):
        '''
        Successful rendering artical catagory sitemap
        '''
        app = self.get_app()

        create_website()
        with app.test_client() as c:
            response = c.get('/en/sitemaps/article-category-1.xml')
            self.assertEqual(response.status_code, 200)
            self.assertTrue(
                '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'
                in response.data.decode('utf-8'))

    @with_transaction()
    def test_0050_article_attribute(self):
        '''
        Test creating and deleting an Article with attributes
        '''
        pool = Pool()
        Article = pool.get('nereid.cms.article')
        ArticleAttribute = pool.get('nereid.cms.article.attribute')

        create_website()
        category = create_article_category(unique_name='test-categ')
        attributes = [{
                'name': 'website',
                'value': 'abc',
                }]
        article1 = create_article(title='Test Article 1', uri='test-article1',
            sequence=10, categories=[category.id], state='published',
            attributes=attributes)

        # Checks an article is created with attributes
        self.assertTrue(article1.id)
        self.assertEqual(ArticleAttribute.search([], count=True), 1)
        # Checks that if an article is deleted then respective attributes
        # are also deleted.
        Article.delete([article1])
        self.assertEqual(ArticleAttribute.search([], count=True), 0)

    @with_transaction()
    def test_0055_article_content(self):
        """
        Test that the article has been rendered properly.
        """
        create_website()
        category = create_article_category(unique_name='test-categ')
        attributes = [{
                'name': 'website',
                'value': 'abc',
                }]
        article1 = create_article(title='Test Article 1', uri='test-article1',
            sequence=10, categories=[category.id], state='published',
            attributes=attributes)

        # Plain content.
        self.assertEqual(article1.__html__(), article1.content)

        # HTML content.
        article1.content = '<html><body><p>A paragraph.</p></body></html>'
        article1.content_type = 'html'

        self.assertEqual(article1.__html__(), article1.content)

        # Markdown content.
        article1.content = '**This is strong in markdown**'
        article1.content_type = 'markdown'
        article1.save()
        self.assertIn('<strong>This is strong in markdown</strong>',
            article1.__html__())

        article1.content = '`A blockquote`'
        article1.save()
        self.assertIn('<p><code>A blockquote</code></p>',
            article1.__html__())

        # RST content.
        article1.content = '*This is emphasis in rst*'
        article1.content_type = 'rst'
        article1.save()
        self.assertIn('<em>This is emphasis in rst</em>',
            article1.__html__())

    @with_transaction()
    def test_0060_sort_articles_by_sequence_on_article_category_page(self):
        '''
        Sort Articles by sequence on Articles Category Page
        '''
        create_website()
        category = create_article_category(unique_name='test-categ')
        article1 = create_article(title='Test Article 1', uri='test-article1',
            sequence=30, categories=[category.id], state='published')
        article2 = create_article(title='Test Article 2', uri='test-article2',
            sequence=20, categories=[category.id], state='published')

        category.sort_order = 'sequence'
        category.template = 'test-category.jinja'
        category.save()

        app = self.get_app()
        with app.test_client() as c:
            response = c.get('/en/article-category/test-categ/')
            data = response.data.decode('utf-8')
            self.assertTrue(data.find(article1.uri) > data.find(article2.uri))

    @with_transaction()
    def test_0090_article_states(self):
        """
        All articles in published state.

        The articles attribute of the article category returns all the articles
        irrespective of the status. The attribute published_articles must only
        return the active articles.

        This test creates four articles of which two are later archived, and
        the test ensures that there are only two published articles
        """
        create_website()
        category1 = create_article_category(unique_name='test-categ1')
        category2 = create_article_category(unique_name='test-categ2')
        article1 = create_article(title='Test Article 1', uri='test-article1',
            sequence=10, categories=[category1.id], state='archived')
        article2 = create_article(title='Test Article 2', uri='test-article2',
            sequence=20, categories=[category1.id], state='published')
        article3 = create_article(title='Test Article 3', uri='test-article1',
            sequence=30, categories=[category2.id], state='archived')
        article2 = create_article(title='Test Article 2', uri='test-article2',
            sequence=40, categories=[category2.id], state='published')

        self.assertEqual(len(category1.articles), 2)
        self.assertEqual(len(category2.articles), 2)
        self.assertEqual(len(category1.published_articles), 1)
        self.assertEqual(len(category2.published_articles), 1)


    @with_transaction()
    def test_0100__menuitem(self):
        """
        Test creation of menuitem
        """
        pool = Pool()
        MenuItem = pool.get('nereid.cms.menuitem')

        create_website()
        category = create_article_category(unique_name='blog')
        article1 = create_article(title='Hello World', uri='hello-world',
            sequence=10, categories=[category.id], state='published')

        main_view, = MenuItem.create([{
                    'type_': 'view',
                    'title': 'Test Title',
                    }])
        menu1, menu2, menu3 = MenuItem.create([{
                    'type_': 'static',
                    'title': 'Test Title',
                    'link': 'http://www.m9s.biz/',
                    'parent': main_view
                    }, {
                    'type_': 'record',
                    'title': 'About Us',
                    'record': '%s,%s' % (article1.__name__, article1.id),
                    'parent': main_view
                    }, {
                    'type_': 'record',
                    'title': 'Blog',
                    'record': '%s,%s' % (category.__name__, category.id),
                    'parent': main_view
                    }])

        self.assertTrue(menu1)
        self.assertTrue(menu2)
        self.assertTrue(menu3)

        app = self.get_app()

        with app.test_request_context('/'):
            rv = main_view.get_menu_item(max_depth=10)
        for child in rv['children']:
            if child['type_'] == 'record' and child['record'] == category:
                self.assertEqual(len(child['children']), 1)

    @with_transaction()
    def test_0210_banner_states(self):
        """
        All banners in published state.

        The banners attribute of the banner category returns all the banners
        irrespective of the status. The attribute published_banners must only
        return the active banners.

        This test creates four banner of which two are later archived, and the
        test ensures that there are only two published banners
        """
        create_website()
        category1 = create_banner_category(name='CAT-A')
        category2 = create_banner_category(name='CAT-B')
        banner1 = create_banner(name='CAT-A1', category=category1,
            state='archived', custom_code='Custom code A1')
        banner2 = create_banner(name='CAT-A2', category=category1,
            state='published', custom_code='Custom code A2')
        banner3 = create_banner(name='CAT-B1', category=category2,
            state='archived', custom_code='Custom code B1')
        banner4 = create_banner(name='CAT-B2', category=category2,
            state='published', custom_code='Custom code B2')

        self.assertEqual(len(category1.banners), 2)
        self.assertEqual(len(category2.banners), 2)
        self.assertEqual(len(category1.published_banners), 1)
        self.assertEqual(len(category2.published_banners), 1)

    @with_transaction()
    def test_0220_banner_image(self):
        """
        Test the image type banner created using static files
        """
        website = create_website()
        file_memoryview = memoryview(b'test-content')
        static_file = create_static_file(file_memoryview, name='logo.png')

        category1 = create_banner_category(name='CAT-A')
        banner1 = create_banner(name='CAT-A1', category=category1,
            state='published', file=static_file, type='media')

        # get_banner_category() filters on website, so we provide one
        category1.website = website
        category1.save()

        app = self.get_app()
        with app.test_client() as c:
            response = c.get('/en/')
            html = objectify.fromstring(response.data)
            folder_name = static_file.folder.name
            self.assertEqual(html.find('img').get('src'),
                '/en/static-file/%s/logo.png' % folder_name)

    @with_transaction()
    def test_0230_get_banner_category(self):
        """
        Test for the return values of context processor get_banner_category()
        """
        website = create_website()
        file_memoryview = memoryview(b'test-content')
        static_file = create_static_file(file_memoryview, name='logo.png')

        category1 = create_banner_category(name='CAT-A')
        banner1 = create_banner(name='CAT-A1', category=category1,
            state='published', file=static_file, type='media')

        # RuntimeError without website, context processor called with
        # silent=False
        app = self.get_app()
        with self.assertRaises(RuntimeError) as a, app.test_client() as c:
            response = c.get('/en/')
        self.assertEqual('Banner category %s not found' % category1.name,
            str(a.exception))

        # Now provide a website
        category1.website = website
        category1.save()

        app = self.get_app()
        with app.test_client() as c:
            response = c.get('/en/')
            html = objectify.fromstring(response.data)
            folder_name = static_file.folder.name
            self.assertEqual(html.find('img').get('src'),
                '/en/static-file/%s/logo.png' % folder_name)

    @with_transaction()
    def test_0240_banner_custom_code(self):
        """
        Test the banner custom code
        """
        website = create_website()
        category1 = create_banner_category(name='CAT-A')
        custom_code = 'Some very complex custom code A1'
        banner1 = create_banner(name='CAT-A1', category=category1,
            state='published', custom_code=custom_code)

        # get_banner_category() filters on website, so we need to provide one
        category1.website = website
        category1.save()

        app = self.get_app()
        with app.test_client() as c:
            response = c.get('/en/')
            self.assertTrue(custom_code in response.data.decode('utf-8'))

    @with_transaction()
    def test_00250_banner_get_html(self):
        """
        Get HTML for banners with type `custom_code`.
        """
        website = create_website()
        category1 = create_banner_category(name='CAT-A')
        custom_code = 'Some very complex custom code A1'
        banner1 = create_banner(name='CAT-A1', category=category1,
            state='published', custom_code=custom_code)

        rv = banner1.get_html()
        self.assertEqual(rv, banner1.custom_code)


def suite():
    suite = trytond.tests.test_tryton.suite()
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(
            NereidCmsTestCase))
    return suite
