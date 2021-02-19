# -*- coding: utf-8 -*-
"""Slack class for Gaia."""
import logging

import requests
from slack_sdk import WebClient


class SCIM:
    """SCIM class."""

    def __init__(self, slack, token):
        """Initialize a SCIM instance."""
        self.base_url = "https://api.slack.com/scim/v1"
        self.headers = {
            "Accept": "application/json",
            "Authorization": f"Bearer {token}",
        }
        self.session = requests.Session()
        self.session.headers.update(self.headers)
        self.slack = slack

    def get_groups(self):
        """Return a list of all Slack IDP groups."""
        url = f"{self.base_url}/Groups"
        count = 1000
        params = {
            "count": count,
            "startIndex": 0,
        }
        groups = []
        while True:
            response = self.session.get(url, params=params).json()
            results = response["Resources"]
            if results:
                groups.extend(results)
            if len(results) < count:
                break
            params["startIndex"] += count
        return groups

    def get_users(self):
        """Return a list of all Slack IDP users."""
        url = f"{self.base_url}/Users"
        count = 1000
        params = {
            "count": count,
            "startIndex": 0,
        }
        users = []
        while True:
            response = self.session.get(url, params=params).json()
            results = response["Resources"]
            if results:
                users.extend(results)
            if len(results) < count:
                break
            params["startIndex"] += count
        return users


class Slack:
    """Slack class."""

    def __init__(self, token):
        """Initialize a Slack instance."""
        self.client = WebClient(token=token)
        self.token = token

    def get_usergroups(self):
        """Return a list of all Slack usergroups."""
        response = self.client.usergroups_list(
            include_count=True,
            include_disabled=True,
        )
        if response.get("ok"):
            return response.get("usergroups")
        return []

    def get_users(self):
        """Return a list of all Slack users."""
        response = self.client.users_list(limit=1000)
        if not response.get("ok"):
            logging.error("Failed to list Slack users.")
            return []
        users = response.get("members")
        next_cursor = response["response_metadata"].get("next_cursor")
        while next_cursor:
            response = self.client.users_list(cursor=next_cursor, limit=1000)
            if not response.get("ok"):
                logging.error("Failed to list Slack users.")
                return []
            users.extend(response.get("members"))
            next_cursor = response["response_metadata"].get("next_cursor")
        return users

    def scim(self, token=None):
        """Return a SCIM instance."""
        if not token:
            token = self.token
        return SCIM(self, token)
