"""A client library for accessing CodeGrade

SPDX-License-Identifier: AGPL-3.0-only OR BSD-3-Clause-Clear
"""
from .client import AuthenticatedClient, Client

__all__ = ("login", "AuthenticatedClient", "Client", "login_from_cli")

login = AuthenticatedClient.get
login_from_cli = AuthenticatedClient.get_from_cli
