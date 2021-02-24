import os
from datetime import datetime
import logging
import argparse
from copy import deepcopy

import requests


class UnityCloudException(Exception):
    pass


class UnityCloud:
    def __init__(self, org_id, project_name):
        self.base_url = 'https://build-api.cloud.unity3d.com/api/v1'
        self.api_key = os.getenv("UNITY_API_KEY")
        if not self.api_key:
            raise UnityCloudException("setup UNITY_API_KEY env var")
        self.auth_headers = {
            'Authorization': 'Basic ' + self.api_key
        }
        self.org_id = org_id
        self.project_name = project_name
        self.project_id = None
        self._set_project_id()
        self.build_targets = None

    def run_build(self, target_name, clean=False):
        self._set_targets()
        target_id = self._get_target_id(target_name)
        url = f'{self.base_url}/orgs/{self.org_id}/projects/{self.project_id}/buildtargets/{target_id}/builds'
        data = {
            "clean": clean
        }
        resp = requests.post(url, headers=self.auth_headers, json=data)
        if resp.status_code != 202:
            logging.error(resp.text)
            raise UnityCloudException("Cant create build")

    def list_projects(self):
        url = f'{self.base_url}/orgs/{self.org_id}/projects'
        req = requests.get(url, headers=self.auth_headers)
        return req.json()

    def upload_ios_credentials(self, bundle_id, cert_stream, prov_stream, cert_secret):
        url = f'{self.base_url}/orgs/{self.org_id}/projects/{self.project_id}/credentials/signing/ios'
        label = f'{datetime.now().strftime("%Y-%m-%d-%s")}-{self.project_name}-{bundle_id}'
        files = {
            'fileCertificate': cert_stream,
            'fileProvisioningProfile': prov_stream,
        }
        data = {
            "label": label,
            "certificatePass": cert_secret,
        }
        resp = requests.post(url, data=data, files=files, headers=self.auth_headers)
        if resp.status_code != 201:
            logging.error(f'{resp.status_code}: {resp.text}')
            raise UnityCloudException("Error create iOS credentials")
        return resp.json()["credentialid"]

    def update_ios_app_creds(self, target_name, creds_id):
        if not self.build_targets:
            self._set_targets()
        buildtargetid = self._get_target_id(target_name)
        print(f"target_name:{target_name}, target_id: {buildtargetid}")
        # PUT /orgs/{orgid}/projects/{projectid}/buildtargets/{buildtargetid}
        url = f'{self.base_url}/orgs/{self.org_id}/projects/{self.project_id}/buildtargets/{buildtargetid}'
        headers = self.auth_headers
        headers.update({
            'Content-Type': 'application/json'
        })
        data = {
            "credentials": {
                "signing": {
                    "credentialid": creds_id
                }
            }
        }
        req = requests.put(url, json=data, headers=headers)
        if req.status_code != 200:
            logging.error(req.json())
            raise UnityCloudException("Error update apps creds")

    def clone_build_target(self, org_target_name, new_target_name, branch):
        org_target = self.find_target_by_name(org_target_name)
        org_target_settings = self._get_build_target_settings(org_target['buildtargetid'])
        new_target_settings = deepcopy(org_target_settings)
        new_target_settings['name'] = new_target_name
        new_target_settings['settings']['scm']['branch'] = branch
        new_target_settings.pop('buildtargetid')
        new_target_settings.pop('lastBuilt')
        new_target_settings.pop('links')
        new_build_target = self._create_build_target(new_target_settings)
        return new_build_target
        # NOTE Definitely unused, to removal
        # self._create_build(new_build_target['buildtargetid'])

    def _create_build_target(self, target_data):
        url = f'{self.base_url}/orgs/{self.org_id}/projects/{self.project_id}/buildtargets'
        resp = requests.post(url=url, json=target_data, headers=self.auth_headers)
        if resp.status_code == 201:
            return resp.json()
        raise UnityCloudException(f'Cant create build target: {resp.text}')

    def find_target_by_name(self, name):
        targets = self._get_all_targets()
        for target in targets:
            if target['name'] == name:
                return target

    def remove_target_with_prefix(self, prefix):
        build_targets = self._get_all_targets()
        to_delete = [target for target in build_targets if target['name'].startswith(prefix)]
        for target in to_delete:
            logging.info(f'Delete: {target["name"]}')
            self._delete_build_target(target['buildtargetid'])

    def _delete_build_target(self, build_target_id):
        url = f'{self.base_url}/orgs/{self.org_id}/projects/{self.project_id}/buildtargets/{build_target_id}'
        resp = requests.delete(url, headers=self.auth_headers)
        if resp.status_code != 204:
            raise UnityCloudException("Cant delete target id")

    def _create_build(self, build_target_id):
        url = f'{self.base_url}/orgs/{self.org_id}/projects/{self.project_id}/buildtargets/{build_target_id}/builds'
        data = {"clean": True}
        resp = requests.post(url, json=data, headers=self.auth_headers)
        if resp.status_code == 202:
            return resp.json()
        raise UnityCloudException('Cant run build')

    def _get_build_target_settings(self, target_id):
        url = f'{self.base_url}/orgs/{self.org_id}/projects/{self.project_id}/buildtargets/{target_id}'
        resp = requests.get(url, headers=self.auth_headers)
        return resp.json()

    def _get_all_targets(self):
        url = f'{self.base_url}/orgs/{self.org_id}/projects/{self.project_id}/buildtargets'
        resp = requests.get(url, headers=self.auth_headers)
        return resp.json()

    def _get_target_id(self, target_name):
        return [bt for bt in self.build_targets if bt['name'] == target_name][0]["buildtargetid"]

    def _set_targets(self):
        url = f'{self.base_url}/orgs/{self.org_id}/projects/{self.project_id}/buildtargets'
        req = requests.get(url, headers=self.auth_headers)
        self.build_targets = req.json()

    def _set_project_id(self):
        projects = self.list_projects()
        self.project_id = [p for p in projects if p['name'] == self.project_name][0]["projectid"]


def run_build():
    parser = argparse.ArgumentParser()
    parser.add_argument('--org-id', required=True)
    parser.add_argument('--project', required=True)
    parser.add_argument('--target', required=True)
    parser.add_argument('--clean', default=False, type=bool)
    args = parser.parse_args()
    uc = UnityCloud(args.org_id, args.project)
    uc.run_build(args.target, clean=args.clean)
