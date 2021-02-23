# ----------------------------------------------------------------------------------------------------
# IBM Confidential
# OCO Source Materials
# 5900-A3Q, 5737-H76
# Copyright IBM Corp. 2021
# The source code for this program is not published or other-wise divested of its trade 
# secrets, irrespective of what has been deposited with the U.S.Copyright Office.
# ----------------------------------------------------------------------------------------------------

# coding=utf-8

import os
import pytest
from ibm_ai_openscale_cli.setup_classes.token_manager import TokenManager
from unittest import TestCase


@pytest.mark.skipif(
    os.getenv('APIKEY') is None, reason='requires APIKEY')
class TokenManagerTests(TestCase):
    def test_get_iam_token(self):
        token_manager = TokenManager(apikey=os.environ['APIKEY'])
        access_token = token_manager.get_token()
        assert access_token is not None

    def test_get_uaa_token(self):
        token_manager = TokenManager(
            apikey=os.environ['APIKEY'], iam_token=False)
        access_token = token_manager.get_token()
        assert access_token is not None
