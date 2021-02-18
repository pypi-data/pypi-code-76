import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = "cv-d4n^*5*$58w474b15pnoqm^fo*10^nv1gg&7q(uaw14o&4p"
DEBUG = True

ALLOWED_HOSTS = []

INSTALLED_APPS = [
    "django.contrib.staticfiles",
    "django_yarnpkg",
    "dj_cleavejs.apps.DjCleaveJSConfig",
    "dj_cleavejs_example.apps.DjCleaveJSExampleConfig",
]

YARN_INSTALLED_APPS = [
    "cleave.js",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.middleware.common.CommonMiddleware",
]

ROOT_URLCONF = "dj_cleavejs_example.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
            ],
        },
    },
]

WSGI_APPLICATION = "dj_cleavejs_example.wsgi.application"

STATIC_URL = "/static/"
STATIC_ROOT = os.path.join(BASE_DIR, "static")
STATICFILES_FINDERS = [
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
    "django_yarnpkg.finders.NodeModulesFinder",
]

NODE_MODULES_ROOT = os.path.join(BASE_DIR, "node_modules")

CLEAVE_JS = "cleave.js/dist/cleave.min.js"
