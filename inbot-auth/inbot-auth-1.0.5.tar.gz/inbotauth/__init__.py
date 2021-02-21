import uuid
import logging
from flask import Flask, redirect, request, render_template, url_for, session
from flask.helpers import get_env, get_debug_flag
from flask_session import Session
from flask_sqlalchemy import SQLAlchemy

from inbotauth.config import BaseConfig
from inbotauth.azure import (load_cache, save_cache, build_msal_app,
                             build_auth_url, get_token_from_cache,
                             query_user_info, get_user)

LOGGER = logging.getLogger(__name__)


class FlaskOIDC(Flask):
    def _before_request(self):
        # ToDo: Need to refactor and divide this method in functions.
        # Whitelisted Endpoints i.e., health checks and status url
        LOGGER.info(f"Request Path: {request.path}")
        LOGGER.info(f"Request Endpoint: {request.endpoint}")
        LOGGER.info(f"Whitelisted Endpoint: {BaseConfig.WHITELISTED_ENDPOINTS}")

        if request.path.strip("/") in BaseConfig.WHITELISTED_ENDPOINTS.split(",") or \
                request.endpoint in BaseConfig.WHITELISTED_ENDPOINTS.split(","):
            return

        # If accepting token in the request headers
        token = None
        if 'Authorization' in request.headers and request.headers['Authorization'].startswith('Bearer '):
            token = request.headers['Authorization'].split(None, 1)[1].strip()
        elif 'access_token' in request.form:
            token = request.form['access_token']
        elif 'access_token' in request.args:
            token = request.args['access_token']
        else:
            token = get_token_from_cache(self.config['SCOPE'])
        if not token:
            return redirect(url_for('login'))

    def __init__(self, *args, **kwargs):
        super(FlaskOIDC, self).__init__(*args, **kwargs)

        # Setup Session Database
        _sql_db = SQLAlchemy(self)
        self.config["SESSION_SQLALCHEMY"] = _sql_db

        # Setup Session Store, that will hold the session information
        # in database. OIDC by default keep the sessions in memory
        _session = Session(self)
        _session.app.session_interface.db.create_all()

        # Register the before request function that will make sure each
        # request is authenticated before processing
        self.before_request(self._before_request)

        self.jinja_env.globals.update(_build_auth_url=build_auth_url)  # Used in template

        @self.route('/login')  # catch_all
        def login():
            return render_template("login.html")

        @self.route('/mslogin')  # catch_all
        def mslogin():
            session["state"] = str(uuid.uuid4())
            # Technically we could use empty list [] as scopes to do just sign in,
            # here we choose to also collect end user consent upfront
            auth_url = build_auth_url(scopes=self.config['SCOPE'], state=session["state"])
            return redirect(auth_url)

        @self.route('/oidc_callback')  # catch_all
        def authorized():
            if request.args.get('state') != session.get("state"):
                return redirect(url_for('index'))  # No-OP. Goes back to Index page
            if "error" in request.args:  # Authentication/Authorization failure
                return render_template("auth_error.html", result=request.args)
            if request.args.get('code'):
                cache = load_cache()
                result = build_msal_app(cache=cache).acquire_token_by_authorization_code(
                    request.args['code'],
                    scopes=self.config['SCOPE'],  # Misspelled scope would cause an HTTP 400 error here
                    redirect_uri=url_for("authorized", _external=True))
                if "error" in result:
                    return render_template("auth_error.html", result=result)
                user_info = result.get("id_token_claims")
                if not user_info:
                    LOGGER.info("failed to get user info for state {}, code {}".format(
                        request.args.get('state'), request.args.get('code')))
                    return render_template("auth_error.html", result=result)
                user_info = query_user_info(cache.find("AccessToken")[0])
                # the user is authenticated only if successfully adding the user
                user = self.config['PUT_USER_METHOD'](self, user_info)
                if not user:
                    return render_template("auth_error.html", result=request.args)
                save_cache(cache)
                session["auth_user"] = user
                session['login_type'] = 'microsoft'
            return redirect(url_for('index'))

        @self.route('/logout')  # catch_all
        def logout():
            session.clear()  # Wipe out user and its token cache from session
            return redirect(  # Also logout from your tenant's web session
                self.config['AUTHORITY'] + "/oauth2/v2.0/logout" + "?post_logout_redirect_uri=" \
                + url_for("index", _external=True))

    def make_config(self, instance_relative=False):
        """
        Overriding the default `make_config` function in order to support
        Flask OIDC package and all of their settings.
        """
        root_path = self.root_path
        if instance_relative:
            root_path = self.instance_path
        defaults = dict(self.default_config)
        defaults['ENV'] = get_env()
        defaults['DEBUG'] = get_debug_flag()

        # Append all the configurations from the base config class.
        for key, value in BaseConfig.__dict__.items():
            if not key.startswith('__'):
                defaults[key] = value
        return self.config_class(root_path, defaults)
