# -*- coding: utf-8 -*-
#
# Copyright (C) 2021 CESNET.
#
# CESNET-OpenID-Remote is free software; you can redistribute it and/or
# modify it under the terms of the MIT License; see LICENSE file for more
# details.

"""Pytest configuration.

See https://pytest-invenio.readthedocs.io/ for documentation on which test
fixtures are available.
"""
import os
import shutil
import tempfile

import pytest
from flask import Flask
from flask_oauthlib.client import OAuth as FlaskOAuth, OAuthResponse
from invenio_accounts import InvenioAccounts
from invenio_db import InvenioDB, db
from invenio_oauthclient import InvenioOAuthClient, InvenioOAuthClientREST
from invenio_oauthclient.views.client import rest_blueprint
from sqlalchemy_utils import database_exists, create_database, drop_database

from cesnet_openid_remote import CesnetOpenIdRemote, CESNETOpenIDRemote
from cesnet_openid_remote.constants import OPENIDC_GROUPS_SCOPE


@pytest.fixture
def base_app(request):
    """Flask application fixture without OAuthClient initialized."""
    # allow HTTP for keycloak tests, and create the KEYCLOAK_REMOTE_APP
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

    instance_path = tempfile.mkdtemp()
    base_app = Flask('testapp')
    base_app.config.update(
        TESTING=True,
        WTF_CSRF_ENABLED=False,
        LOGIN_DISABLED=False,
        CACHE_TYPE='simple',
        OAUTHCLIENT_REST_REMOTE_APPS=dict(
            cesnet=CesnetOpenIdRemote().remote_app(),
        ),
        CESNET_OPENIDC_CONFIG=dict(
            base_url='https://localhost/tests',
            consumer_key='TEST_OIDC_KEY',
            consumer_secret='TEST_OIDC_SECRET',
            scope=f'openid email profile {OPENIDC_GROUPS_SCOPE} isCesnetEligibleLastSeen'
        ),
        OAUTHCLIENT_STATE_EXPIRES=300,
        # use local memory mailbox
        EMAIL_BACKEND='flask_email.backends.locmem.Mail',
        SQLALCHEMY_DATABASE_URI=os.getenv('SQLALCHEMY_DATABASE_URI',
                                          'sqlite://'),
        SERVER_NAME='localhost',
        DEBUG=False,
        SECRET_KEY='TEST',
        SECURITY_DEPRECATED_PASSWORD_SCHEMES=[],
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
        SECURITY_PASSWORD_HASH='plaintext',
        SECURITY_PASSWORD_SCHEMES=['plaintext'],
        APP_ALLOWED_HOSTS=['localhost'],
        USERPROFILES_EXTEND_SECURITY_FORMS=True,
    )
    InvenioDB(base_app)
    InvenioAccounts(base_app)

    with base_app.app_context():
        if str(db.engine.url) != 'sqlite://' and \
            not database_exists(str(db.engine.url)):
            create_database(str(db.engine.url))
        db.create_all()

    def teardown():
        with base_app.app_context():
            db.session.close()
            if str(db.engine.url) != 'sqlite://':
                drop_database(str(db.engine.url))
            shutil.rmtree(instance_path)
            db.engine.dispose()

    request.addfinalizer(teardown)

    base_app.test_request_context().push()
    return base_app


@pytest.fixture
def app(base_app):
    """Flask application fixture."""
    FlaskOAuth(base_app)
    InvenioOAuthClient(base_app)
    InvenioOAuthClientREST(base_app)
    CESNETOpenIDRemote(base_app)

    # Register blueprint
    base_app.register_blueprint(rest_blueprint)
    return base_app


@pytest.fixture
def models_fixture(base_app):
    """Flask app with example data used to test models."""
    with base_app.app_context():
        datastore = base_app.extensions['security'].datastore
        datastore.create_user(
            email='test1@oarepo.org',
            password='tester',
            active=True
        )
        datastore.create_user(
            email='test2@oarepo.org',
            password='tester',
            active=True
        )
        datastore.create_user(
            email='test3@oarepo.org',
            password='tester',
            active=True
        )
        datastore.create_user(
            email='john.doe@example.oarepo.org',
            password='tester',
            active=True
        )
        datastore.commit()


@pytest.fixture()
def example_cesnet(request):
    """CESNET example data."""
    file_path = os.path.join(os.path.dirname(__file__),
                             'data/cesnet_openid_response.json')
    with open(file_path) as response_file:
        json_data = response_file.read()

    from jwt import encode
    token = encode(dict(name="John Doe"), key="1234")

    return OAuthResponse(
        resp=None,
        content=json_data,
        content_type='application/json'
    ), dict(
        access_token=token,
        token_type='bearer',
        expires_in=1199,
        refresh_token='test_refresh_token'
    ), dict(
        user=dict(
            email='john.doe@oarepo.org',
            profile=dict(username='abcd1234@einfra.cesnet.cz', full_name='John Doe'),
        ),
        external_id='abcd1234@einfra.cesnet.cz',
        external_method='CESNET eduID Login',
        active=True
    )
