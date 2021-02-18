"""Unearthed Cognito."""
import json
import logging
import os

import cognitojwt
from botocore.exceptions import ClientError
from cognitojwt import CognitoJWTException
from cognitojwt.exceptions import CognitoJWTException
from pycognito import Cognito

_TOKEN_PATH = os.path.expanduser("~/.unearthed/tokens.json")

logger = logging.getLogger(__name__)


class UnearthedCognito(Cognito):
    """Authentication handler for Unearthed's Cognito instance."""

    def __init__(self):
        """Use the Unearthed Cognito Pool."""
        super().__init__(
            user_pool_id="us-east-2_yCpz99wwX",
            user_pool_region="us-east-2",
            client_id="1urju2o6sedoa8rkao8d6iino6",
        )
        # logger.debug("__init__")
        # self.__load_tokens()

    def __load_tokens(self):
        """Load saved tokens from user profile/home."""
        try:
            with open(_TOKEN_PATH) as json_file:
                # logger.debug(f"loading tokens from {_TOKEN_PATH}")
                saved_tokens = json.load(json_file)
                self.id_token = saved_tokens["IdToken"]
                self.access_token = saved_tokens["AccessToken"]
                self.refresh_token = saved_tokens["RefreshToken"]
                id_token = self.decoded_id_token(skip_expiry_check=True)
                self.username = id_token["email"]
                # logger.debug(f"tokens loaded for {self.username} from {_TOKEN_PATH}")
        except FileNotFoundError as e:
            logger.debug(f"{_TOKEN_PATH} not found")
        except ClientError as e:
            logger.exception(e)
        except (Exception) as e:
            logger.error(f"failed to read {_TOKEN_PATH}")

    def check_token(self):
        """Check tokens and refresh if required."""
        # logger.debug("check_token")
        self.__load_tokens()
        try:
            refreshed = super().check_token()
            if refreshed:
                self.username = self.decoded_id_token()["email"]
                logger.debug(f"token refreshed for {self.username}")
            return refreshed
        except Exception:
            logger.debug("failure refreshing token, forcing logout")
            self.logout()
            return False

    def __decode(self, token, testmode=False):
        return cognitojwt.decode(
            token,
            self.user_pool_region,
            self.user_pool_id,
            app_client_id=self.client_id,
            testmode=testmode,
        )

    def decoded_id_token(self, skip_expiry_check=False):
        """Decode the Id Token."""
        # logger.debug("decoded_id_token")
        if self.id_token is not None:
            return self.__decode(self.id_token, testmode=skip_expiry_check)
        else:
            return "No Id Token"

    def decoded_access_token(self):
        """Decode the Access Token."""
        logger.debug("decoded_access_token")
        return self.__decode(self.access_token)

    def _save(self):
        logger.debug(f"saving token to {_TOKEN_PATH}")
        os.makedirs(os.path.dirname(_TOKEN_PATH), exist_ok=True)
        tokens = {
            "IdToken": self.id_token,
            "RefreshToken": self.refresh_token,
            "AccessToken": self.access_token,
            # TODO remove email in a later release
            "email": self.username,
            "username": self.username,
        }
        with open(_TOKEN_PATH, "w") as json_file:
            json.dump(tokens, json_file, indent=2)

    def authenticate(self, password):
        """Authenticate the username and password."""
        logger.debug("authenticate")
        super().authenticate(password)
        self._save()

    def logout(self):
        """Log out the current session and remove token caches."""
        logger.debug("logout")
        if os.path.exists(_TOKEN_PATH):
            logger.debug(f"removing {_TOKEN_PATH}")
            os.remove(_TOKEN_PATH)

        if self.access_token is not None:
            try:
                super().logout()
            except Exception:
                pass

    def is_logged_in(self):
        """Is the current session logged in."""
        self.check_token()
        return os.path.exists(_TOKEN_PATH)
