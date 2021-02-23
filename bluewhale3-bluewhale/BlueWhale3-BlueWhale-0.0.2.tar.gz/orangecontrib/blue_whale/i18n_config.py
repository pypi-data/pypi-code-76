import i18n
import os

localedir = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'locale')
if localedir not in i18n.load_path:
    i18n.load_path.append(localedir)
i18n.set('skip_locale_root_data', True)
i18n.set('locale', 'zh')
i18n.set('fallback', 'en')