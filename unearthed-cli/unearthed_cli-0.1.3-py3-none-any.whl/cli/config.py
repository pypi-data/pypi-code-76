"""Unearthed Configuration."""
from os import environ

if environ.get("DEBUG") or environ.get("UNEARTHED_DEBUG"):
    LAMBDA_URL = "https://crowdml-dev.unearthed.solutions/"
    TRACKER_BASE_URL = "https://development-q5nzhaa-lbjz5xns2dzm2.au.platformsh.site/u"
else:
    LAMBDA_URL = "https://crowdml.unearthed.solutions/"
    TRACKER_BASE_URL = "https://unearthed.solutions/u"
