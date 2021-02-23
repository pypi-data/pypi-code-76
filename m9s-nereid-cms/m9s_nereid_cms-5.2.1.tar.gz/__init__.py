# The COPYRIGHT file at the top level of this repository contains
# the full copyright notices and license terms.

from trytond.pool import Pool
from . import cms

__all__ = ['register']


def register():
    Pool.register(
        cms.MenuItem,
        cms.BannerCategory,
        cms.Banner,
        cms.ArticleCategory,
        cms.Article,
        cms.ArticleAttribute,
        cms.NereidStaticFile,
        cms.Website,
        cms.ArticleCategoryRelation,
        module='nereid_cms', type_='model')
