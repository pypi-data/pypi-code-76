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

import appier

class ObjectAPI(object):

    def create_object(
        self,
        bucket,
        name,
        data,
        content_type = None,
        acl = None,
        sha256 = None
    ):
        url = self.bucket_url % bucket + "%s" % appier.legacy.quote(name)
        headers = dict()
        if acl: headers["X-Amz-Acl"] = acl
        contents = self.put(
            url,
            data = data,
            headers = headers,
            sign = True,
            content_type = content_type,
            sha256 = sha256 or self._content_sha256(data = data)
        )
        return contents

    def build_url_object(self, bucket, name):
        return self.bucket_url % bucket + "%s" % name

    def create_file_object(
        self,
        bucket,
        name,
        path,
        content_type = None,
        acl = None,
        sha256 = None
    ):
        return self.create_object(
            bucket,
            name,
            data = appier.file_g(path),
            content_type = content_type,
            acl = acl,
            sha256 = sha256 or self._content_sha256(appier.file_g(path))
        )
