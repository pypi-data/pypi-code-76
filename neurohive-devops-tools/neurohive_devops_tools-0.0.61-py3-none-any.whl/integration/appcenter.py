import logging
import sys
import os
from typing import List

import requests
from requests.exceptions import RequestException
from tenacity import retry, stop_after_attempt, wait_exponential

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()


class AppCenterWrapperException(Exception):
    pass


class AppCenter:
    def __init__(self, owner: str) -> None:
        self.token = os.environ['APPCENTER_API_TOKEN']
        self.owner = owner
        self.headers = {
            'Content-Type': 'application/json',
            'X-API-Token': self.token
        }
        self.base_url = 'https://api.appcenter.ms'

    def get_new_idids(self, app_name: str, distr_grp_name: str) -> list():
        url = f'{self.base_url}/v0.1/apps/{self.owner}/{app_name}/distribution_groups/{distr_grp_name}/devices'
        try:
            req = requests.get(url, headers=self.headers)
        except RequestException as e:
            logging.error(e)
            sys.exit(1)
        if req.status_code == 200:
            to_provision = [d for d in req.json() if d.get('status') != 'provisioned']
            return to_provision
        else:
            logging.error(req.text)

    @retry(stop=stop_after_attempt(3), wait=wait_exponential(1, 3, 9))
    def get_apps(self):
        url = f'{self.base_url}/v0.1/apps'
        req = requests.get(url, headers=self.headers)
        if req.status_code != 200:
            logger.error(req.text)
            raise AppCenterWrapperException("Cant get apps")
        return req.json()

    def cleanup_old_builds(self, app_name, leave_num=30):
        logging.info(f"delete {app_name} builds")
        builds = self._get_builds_for_app(app_name)
        builds = sorted(builds, key=lambda x: x["id"])[0:-leave_num]
        if builds:
            for build in builds:
                self._delete_release_by_id(app_name, build)

    def get_download_link(self, app_name, build_ver):
        builds = self._get_builds_for_app(app_name)
        filtered = list(filter(lambda x: x['version'] == build_ver or x['short_version'] == build_ver, builds))
        if not filtered:
            raise AppCenterWrapperException("Cant find build for version")
        release_info = self._get_release_info(app_name, filtered[0]['id'])
        return release_info['download_url']

    def get_distr_members_by_grp(self, grp_name):
        uri = f'{self.base_url}/v0.1/orgs/{self.owner}/distribution_groups/{grp_name}/members'
        req = requests.get(uri, headers=self.headers)
        if req.status_code != 200:
            logger.error(req.text)
            raise AppCenterWrapperException(f'Error getting members of group: {grp_name}')
        return req.json()

    def add_users_to_distr_grp(self, grp_name, users: List[str]):
        uri = f'{self.base_url}/v0.1/orgs/{self.owner}/distribution_groups/{grp_name}/members'
        data = {
            'user_emails': users
        }
        req = requests.post(uri, headers=self.headers, json=data)
        if req.status_code != 200:
            logger.error(req.text)
            raise AppCenterWrapperException(f'Error getting members of group: {grp_name}')
        return req.json()

    @retry(stop=stop_after_attempt(3), wait=wait_exponential(1, 3, 9))
    def _get_release_info(self, app_name, release_id):
        uri = f'{self.base_url}/v0.1/apps/{self.owner}/{app_name}/releases/{release_id}'
        req = requests.get(uri, headers=self.headers)
        if req.status_code != 200:
            logger.error(req.text)
            raise AppCenterWrapperException('Error getting release info')
        return req.json()

    def _get_builds_for_app(self, app_name):
        url = f'{self.base_url}/v0.1/apps/{self.owner}/{app_name}/releases'
        req = requests.get(url, headers=self.headers)
        if req.status_code != 200:
            logger.error(req.text)
            raise AppCenterWrapperException('Error getting builds for app')
        return req.json()

    def _delete_release_by_id(self, app_name, build):
        logging.info(f'delete id:{build["id"]}, ver:{build["short_version"]}')
        url = f'{self.base_url}/v0.1/apps/{self.owner}/{app_name}/releases/{build["id"]}'
        req = requests.delete(url, headers=self.headers)
        if req.status_code != 200:
            raise AppCenterWrapperException("Error delete build")

    def _get_appid(self, app_name):
        apps = self.get_apps()
        app = list(filter(lambda x: x['display_name'] == app_name, apps))
        if not app:
            raise AppCenterWrapperException("Cant get app id")
        return app[0]['name']
