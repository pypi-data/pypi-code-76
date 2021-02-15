# coding: utf-8

"""
    IBM Watson Machine Learning REST API

    ## Authorization  ### IBM Watson Machine Learning Credentials (ML Credentials)  The IBM Watson Machine Learning Credentials are available for the Bluemix user for each bound application or requested service key. You will find them in the VCAP information as well you can access them using Cloud Foundry API.  Here is the example of the ML Credentials:  ```json {   \"url\": \"https://ibm-watson-ml.mybluemix.net\",   \"username\": \"c1ef4b80-2ee2-458e-ab92-e9ca97ec657d\",   \"password\": \"edb699da-8595-406e-bae0-74a834fa4d34\",    \"access_key\": \"0uUQPsbQozcci4uwRI7xo0jQnSNOM9YSk....\" } ```  - `url` - the base WML API url - `username` / `password` - the service credentials required to generate the token - `access_key` - the access key used by previous version of the service API (ignored)  The `username` / `password` pair are used to access the Token Endpoint (using HTTP Basic Auth) and obtain the service token (see below). Example:  `curl --basic --user c1ef4b80-2ee2-458e-ab92-e9ca97ec657d:edb699da-8595-406e-bae0-74a834fa4d34 https://ibm-watson-ml.mybluemix.net/v3/identity/token`  ### IBM Watson Machine Learning Token (ML Token)  The IBM Watson Machine Learning REST API is authorized with ML token obtained from the Token Endpoint. The ML token is used as a baerer token send in `authorization` header.  Use WML service credentials (username, password) to gather the token from:   `/v3/identity/token` (see example above).  The token is self-describing JWT (JSON Web Tokens) protected by digital signature for authentication. It holds information required for a service tenant identification. Each ML micro-service is able to verify the token with the public key without request to the token endpoint and firing a database query. The ML service token (ML token) contains the expiration time what simplifies implementation of the access revocation.  ## Spark Instance  The IBM Watson ML co-operates with the Spark as a Service to make calculation and deploy pipeline models. Each API method that requires the Spark service instance accepts a custom header: `X-Spark-Service-Instance` where the Spark instance data like credentials, kernel ID and version can be specified. The header value is a base64 encoded string with the JSON data in the following format:    ```   {     \"credentials\": {       \"tenant_id\": \"sf2c-xxxxx-05b1d10fb12b\",       \"cluster_master_url\": \"https://spark.stage1.bluemix.net\",       \"tenant_id_full\": \"xxxxx-a94d-4f20-bf2c-xxxxxx-xxxx-4c65-a156-05b1d10fb12b\",       \"tenant_secret\": \"xxxx-86fd-40cd-xxx-969aafaeb505\",       \"instance_id\": \"xxx-a94d-xxx-bf2c-xxxx\",       \"plan\": \"ibm.SparkService.PayGoPersonal\"     },     \"version\": \"2.0\",     \"kernelId\": \"xxx-a94d-xxx-bf2c-xxxx\"   }   ```  The fields are: - `credentials` - from the VCAP information of the Spark service instance - `version` - requested Spark version (possible values: 2.0) - `kernelId` (optional) - the Spark kernel ID is only required by actions that operates on running Spark kernel.   This field is redundant when creating any kind of deployment.

    OpenAPI spec version: 2.0.0
    
    Generated by: https://github.com/swagger-api/swagger-codegen.git

    Licensed under the Apache License, Version 2.0 (the "License");
    you may not use this file except in compliance with the License.
    You may obtain a copy of the License at

        http://www.apache.org/licenses/LICENSE-2.0

    Unless required by applicable law or agreed to in writing, software
    distributed under the License is distributed on an "AS IS" BASIS,
    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
    See the License for the specific language governing permissions and
    limitations under the License.
"""

from __future__ import absolute_import

import sys
import io
import json
import ssl
import certifi
import logging
import re
import os

# python 2 and python 3 compatibility library
from six import iteritems

from .configuration import Configuration

try:
    import urllib3
except ImportError:
    raise ImportError('Swagger python client requires urllib3.')

try:
    # for python3
    from urllib.parse import urlencode
except ImportError:
    # for python2
    from urllib import urlencode


logger = logging.getLogger(__name__)


class RESTResponse(io.IOBase):

    def __init__(self, resp):
        self.urllib3_response = resp
        self.status = resp.status
        self.reason = resp.reason
        self.data = resp.data

    def getheaders(self):
        """
        Returns a dictionary of the response headers.
        """
        return self.urllib3_response.getheaders()

    def getheader(self, name, default=None):
        """
        Returns a given response header.
        """
        return self.urllib3_response.getheader(name, default)


class RESTClientObject(object):

    def __init__(self, pools_size=4):
        # urllib3.PoolManager will pass all kw parameters to connectionpool
        # https://github.com/shazow/urllib3/blob/f9409436f83aeb79fbaf090181cd81b784f1b8ce/urllib3/poolmanager.py#L75
        # https://github.com/shazow/urllib3/blob/f9409436f83aeb79fbaf090181cd81b784f1b8ce/urllib3/connectionpool.py#L680
        # ca_certs vs cert_file vs key_file
        # http://stackoverflow.com/a/23957365/2985775

        # cert_reqs
        if Configuration().verify_ssl:
            cert_reqs = ssl.CERT_REQUIRED
        else:
            cert_reqs = ssl.CERT_NONE

        # skip ssl validation for private - ICP environment
        if 'DEPLOYMENT_PLATFORM' in os.environ and os.environ['DEPLOYMENT_PLATFORM'] == 'private':
            cert_reqs = ssl.CERT_NONE

        # ca_certs
        if Configuration().ssl_ca_cert:
            ca_certs = Configuration().ssl_ca_cert
        else:
            # if not set certificate file, use Mozilla's root certificates.
            ca_certs = certifi.where()

        # cert_file
        cert_file = Configuration().cert_file

        # key file
        key_file = Configuration().key_file

        # https pool manager
        self.pool_manager = urllib3.PoolManager(
            num_pools=pools_size,
            cert_reqs=cert_reqs,
            ca_certs=ca_certs,
            cert_file=cert_file,
            key_file=key_file
        )

    def request(self, method, url, query_params=None, headers=None,
                body=None, post_params=None):
        """
        :param method: http request method
        :param url: http request url
        :param query_params: query parameters in the url
        :param headers: http request headers
        :param body: request json body, for `application/json`
        :param post_params: request post parameters,
                            `application/x-www-form-urlencode`
                            and `multipart/form-data`
        """
        method = method.upper()
        assert method in ['GET', 'HEAD', 'DELETE', 'POST', 'PUT', 'PATCH', 'OPTIONS']

        if post_params and body:
            raise ValueError(
                "body parameter cannot be used with post_params parameter."
            )

        post_params = post_params or {}
        headers = headers or {}

        if 'Content-Type' not in headers:
            headers['Content-Type'] = 'application/json'

        try:
            # For `POST`, `PUT`, `PATCH`, `OPTIONS`, `DELETE`
            if method in ['POST', 'PUT', 'PATCH', 'OPTIONS', 'DELETE']:
                if query_params:
                    url += '?' + urlencode(query_params)
                if re.search('json', headers['Content-Type'], re.IGNORECASE):
                    request_body = None
                    if body or isinstance(body, dict):
                        request_body = json.dumps(body)
                    r = self.pool_manager.request(method, url,
                                                  body=request_body,
                                                  headers=headers)
                if headers['Content-Type'] == 'application/x-www-form-urlencoded':
                    r = self.pool_manager.request(method, url,
                                                  fields=post_params,
                                                  encode_multipart=False,
                                                  headers=headers)
                if headers['Content-Type'] == 'multipart/form-data':
                    # must del headers['Content-Type'], or the correct Content-Type
                    # which generated by urllib3 will be overwritten.
                    del headers['Content-Type']
                    r = self.pool_manager.request(method, url,
                                                  fields=post_params,
                                                  encode_multipart=True,
                                                  headers=headers)
            # For `GET`, `HEAD`
            else:
                r = self.pool_manager.request(method, url,
                                              fields=query_params,
                                              headers=headers)
        except urllib3.exceptions.SSLError as e:
            msg = "{0}\n{1}".format(type(e).__name__, str(e))
            raise ApiException(status=0, reason=msg)

        r = RESTResponse(r)

        # In the python 3, the response.data is bytes.
        # we need to decode it to string.
        if sys.version_info > (3,):
            r.data = r.data.decode('utf8')

        # log response body
        logger.debug("response body: %s" % r.data)

        if r.status not in range(200, 206):
            raise ApiException(http_resp=r)

        return r

    def GET(self, url, headers=None, query_params=None):
        return self.request("GET", url,
                            headers=headers,
                            query_params=query_params)

    def HEAD(self, url, headers=None, query_params=None):
        return self.request("HEAD", url,
                            headers=headers,
                            query_params=query_params)

    def OPTIONS(self, url, headers=None, query_params=None, post_params=None, body=None):
        return self.request("OPTIONS", url,
                            headers=headers,
                            query_params=query_params,
                            post_params=post_params,
                            body=body)

    def DELETE(self, url, headers=None, query_params=None, body=None):
        return self.request("DELETE", url,
                            headers=headers,
                            query_params=query_params,
                            body=body)

    def POST(self, url, headers=None, query_params=None, post_params=None, body=None):
        return self.request("POST", url,
                            headers=headers,
                            query_params=query_params,
                            post_params=post_params,
                            body=body)

    def PUT(self, url, headers=None, query_params=None, post_params=None, body=None):
        return self.request("PUT", url,
                            headers=headers,
                            query_params=query_params,
                            post_params=post_params,
                            body=body)

    def PATCH(self, url, headers=None, query_params=None, post_params=None, body=None):
        return self.request("PATCH", url,
                            headers=headers,
                            query_params=query_params,
                            post_params=post_params,
                            body=body)


class ApiException(Exception):

    def __init__(self, status=None, reason=None, http_resp=None):
        if http_resp:
            self.status = http_resp.status
            self.reason = http_resp.reason
            self.body = http_resp.data
            self.headers = http_resp.getheaders()
        else:
            self.status = status
            self.reason = reason
            self.body = None
            self.headers = None

    def __str__(self):
        """
        Custom error messages for exception
        """
        error_message = "({0})\n"\
                        "Reason: {1}\n".format(self.status, self.reason)
        if self.headers:
            error_message += "HTTP response headers: {0}\n".format(self.headers)

        if self.body:
            error_message += "HTTP response body: {0}\n".format(self.body)

        return error_message
