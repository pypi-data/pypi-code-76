import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = "cv-d4n^*5*$58w474b15pnoqm^fo*10^nv1gg&7q(uaw14o&4p"
DEBUG = True

ALLOWED_HOSTS = []

INSTALLED_APPS = [
    "django.contrib.staticfiles",
    "django_yarnpkg",
    "dj_iconify.apps.DjIconifyConfig",
    "dj_iconify_server.apps.DjIconifyServerConfig",
]

YARN_INSTALLED_APPS = [
    "@iconify/json",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.middleware.common.CommonMiddleware",
]

ROOT_URLCONF = "dj_iconify_server.urls"

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

WSGI_APPLICATION = "dj_iconify_server.wsgi.application"

STATIC_URL = "/static/"

NODE_MODULES_ROOT = os.path.join(BASE_DIR, "node_modules")

ICONIFY_JSON_ROOT = os.path.join(NODE_MODULES_ROOT, "@iconify", "json")
