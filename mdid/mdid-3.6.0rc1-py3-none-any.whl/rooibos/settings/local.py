from .base import *  # NOQA

# Make this unique, and don't share it with anybody.
SECRET_KEY = 'e#!poDuIJ}N,".K=H:T/4z5POb;Gl/N6$6a&,(DRAHUF5c",_p'

# Add the hostname of your server, or keep '*' to allow all host names
ALLOWED_HOSTS = ['*']

# Database settings
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'usf_mdid3',
        'USER': 'usf',
        'PASSWORD': 'usf',
        'HOST': '',
        'PORT': '',
        'OPTIONS': {
            'use_unicode': True,
            'charset': 'utf8',
        },
    }
}

RABBITMQ_OPTIONS = {
    'host': 'localhost',
}

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'America/Chicago'

SOLR_URL = 'http://127.0.0.1:8983/solr/mdid'
SOLR_RECORD_INDEXER = None
SOLR_RECORD_PRE_INDEXER = None


# Theme colors for use in CSS
PRIMARY_COLOR = "rgb(152, 189, 198)"
SECONDARY_COLOR = "rgb(118, 147, 154)"


handler = LOGGING['handlers']['file']
handler['filename'] = os.path.join(
    '/Users/andreas/temp', os.path.basename(handler['filename']))
