from typing import List

from django.conf import settings

from link_all.dataclasses import LinkAllModel


link_all_models_default = [
    LinkAllModel(app_label='cms', model_name='Page'),
    LinkAllModel(app_label='filer', model_name='File', url_method='url', is_show_url_in_select=False),
]


LINK_ALL_MODELS: List[LinkAllModel] = getattr(settings, 'LINK_ALL_MODELS_ADDITIONAL', []) + link_all_models_default
LINK_ALL_ENABLE_BUTTON_PLUGIN: bool = getattr(settings, 'LINK_ALL_ENABLE_BUTTON_PLUGIN', False)
LINK_ALL_PLUGINS: List[str] = getattr(settings, 'LINK_ALL_PLUGINS', ['link_all.LinkButtonPluginModel'])
