#!/usr/bin/python
# -*- coding: utf-8 -*-

# Hive Amazon S3 API
# Copyright (c) 2008-2020 Hive Solutions Lda.
#
# This file is part of Hive Amazon S3 API.
#
# Hive Amazon S3 API is free software: you can redistribute it and/or modify
# it under the terms of the Apache License as published by the Apache
# Foundation, either version 2.0 of the License, or (at your option) any
# later version.
#
# Hive Amazon S3 API is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# Apache License for more details.
#
# You should have received a copy of the Apache License along with
# Hive Amazon S3 API. If not, see <http://www.apache.org/licenses/>.

__author__ = "João Magalhães <joamag@hive.pt>"
""" The author(s) of the module """

__version__ = "1.0.0"
""" The version of the module """

__revision__ = "$LastChangedRevision$"
""" The revision number of the module """

__date__ = "$LastChangedDate$"
""" The last change date of the module """

__copyright__ = "Copyright (c) 2008-2020 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "Apache License, Version 2.0"
""" The license for the module """

import hmac
import hashlib
import datetime

import appier

from . import bucket
from . import object

BASE_URL = "https://s3.amazonaws.com/"
""" The default base URL to be used when no other
base URL value is provided to the constructor """

REGION = "us-east-1"
""" The default region to be used when no region value
is provided, ensure compatibility """

class API(
    appier.API,
    bucket.BucketAPI,
    object.ObjectAPI
):

    def __init__(self, *args, **kwargs):
        appier.API.__init__(self, *args, **kwargs)
        self.base_url = appier.conf("S3_BASE_URL", BASE_URL)
        self.access_key = appier.conf("S3_ACCESS_KEY", None)
        self.secret = appier.conf("S3_SECRET", None)
        self.region = appier.conf("S3_REGION", None)
        self.base_url = kwargs.get("base_url", self.base_url)
        self.access_key = kwargs.get("access_key", self.access_key)
        self.secret = kwargs.get("secret", self.secret)
        self.region = kwargs.get("region", self.region)
        if self.region: self.base_url = self.base_url.replace(
            "https://s3", "https://s3." + self.region
        )
        self.bucket_url = self.base_url.replace("https://", "https://%s.")

    def build(
        self,
        method,
        url,
        data = None,
        data_j = None,
        data_m = None,
        headers = None,
        params = None,
        mime = None,
        kwargs = None
    ):
        sign = kwargs.pop("sign", False)
        content_type = kwargs.pop("content_type", None)
        content_sha256 = kwargs.pop("sha256", None)
        if sign and self.access_key and self.secret:
            headers["X-Amz-Content-Sha256"] = content_sha256 or\
                self._content_sha256(data = data)
            headers["Content-Type"] = content_type or self._content_type()
            headers["Host"] = self._host(url)
            headers["X-Amz-Date"] = self._date()
            headers["Authorization"] = self._signature(
                method,
                url,
                headers = headers
            )

    def _content_sha256(self, data = None):
        data = data or b""
        if appier.legacy.is_bytes(data): data = iter((len(data), data))
        next(data)
        sha256 = hashlib.sha256()
        for chunk in data: sha256.update(chunk)
        return sha256.hexdigest()

    def _content_type(self, data = None):
        return "text/plain"

    def _host(self, url):
        return appier.legacy.urlparse(url).hostname

    def _date(self):
        date = datetime.datetime.utcnow()
        return date.strftime("%Y%m%dT%H%M%SZ")

    def _signature(self, method, url, data = None, headers = None, region = None, service = "s3"):
        region = region or self.region

        date = headers["X-Amz-Date"]
        content_sha256 = headers["X-Amz-Content-Sha256"]

        day_s = date[:8]

        url_parse = appier.legacy.urlparse(url)
        path = url_parse.path or "/"
        query = url_parse.query

        headers_l = []
        headers_n = []

        for key in sorted(appier.legacy.keys(headers)):
            value = headers[key]
            key = key.lower()
            value = value.strip()
            headers_l.append("%s:%s" % (key, value))
            headers_n.append(key)

        headers_s = "\n".join(headers_l)
        headers_n = ";".join(headers_n)

        canonical_request = "%s\n%s\n%s\n%s\n\n%s\n%s" % (
            method,
            path,
            query,
            headers_s,
            headers_n,
            content_sha256
        )
        canonical_request = appier.legacy.bytes(canonical_request, force = True)
        canonical_request_sha256 = hashlib.sha256(canonical_request)
        canonical_request_sha256 = canonical_request_sha256.hexdigest()

        scope = "%s/%s/s3/aws4_request" % (day_s, region)
        credential = "%s/%s" % (self.access_key, scope)

        base = "AWS4-HMAC-SHA256\n%s\n%s\n%s" % (
            date,
            scope,
            canonical_request_sha256
        )
        base = appier.legacy.bytes(base, force = True)

        secret = self._secret(day_s, region = region, service = service)
        signature = hmac.new(secret, base, hashlib.sha256).hexdigest()

        return "AWS4-HMAC-SHA256 Credential=%s,SignedHeaders=%s,Signature=%s" % (
            credential, headers_n, signature
        )

    def _secret(self, day_s, region = None, service = "s3"):
        region = region or self.region

        secret = appier.legacy.bytes("AWS4" + self.secret, force = True)
        values = (day_s, region, service, "aws4_request")

        for value in values:
            value = appier.legacy.bytes(value, force = True)
            secret = hmac.new(secret, value, hashlib.sha256).digest()

        return secret
