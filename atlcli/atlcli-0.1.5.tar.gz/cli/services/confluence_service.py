import re
import sys,os
import ssl
import pprint36 as pprint
from datetime import datetime
from atlassian import Confluence
from .jira_service import JiraService
from .bitbucket_service import BitbucketService


class ConfluenceService:

    releasenote_template = ""
    product_changelog_template = ""
    component_changelog_template = ""

    def __init__(self, confluence_url, jira_url, bibucket_url, username, password, skipssl):

        self.skipssl = skipssl
        self.jira_service = JiraService(
            url=jira_url,
            username=username,
            password=password,
            skipssl=self.skipssl)

        self.bitbucket_service = BitbucketService(
            url=bibucket_url,
            username=username,
            password=password,
            skipssl=self.skipssl)

        self.confluence = Confluence(
            url=confluence_url,
            username=username,
            password=password,
            verify_ssl=self.skipssl
        )

        self.load_product_changelog_template()
        self.load_component_changelog_template()

    def generate_releasenote(self, project_key, version, template_file):        
        self.load_releasenote_template(template_file)

        versionData = self.jira_service.get_project_version_infos(
            project_key, version)

        if versionData is not None:
            tasks = self.jira_service.get_issues_confluence_markup(
                project_key, versionData["id"])

            releasenote = self.releasenote_template.replace(
                "%fixversion%", versionData["id"])
            releasenote = releasenote.replace("%project-key%", project_key)
            releasenote = releasenote.replace("%validate_task%", tasks)

            return releasenote
        else:
            return None

    def push_releasenote(self, spacekey, version, parent_page_id, releasenote):
        current_date = datetime.today().strftime("%Y-%m-%d")
        semantic_version = ""

        m = re.search(
            "(([0-9]+)\.([0-9]+)\.([0-9]+)(?:-([0-9A-Za-z-]+(?:\.[0-9A-Za-z-]+)*))?(?:\+[0-9A-Za-z-]+)?)", version)

        if m:
            semantic_version = m.group(1)

        title = "{0} - {1}".format(semantic_version, current_date)

        self.push_to_confluence(parent_page_id, title, releasenote)

    def push_changelog(self, name, space_key, version, parent_page_id, isComponent=False):
        changelog_content = None
        current_date = datetime.today().strftime("%Y-%m-%d")

        semantic_version = ""

        m = re.search(
            "(([0-9]+)\.([0-9]+)\.([0-9]+)(?:-([0-9A-Za-z-]+(?:\.[0-9A-Za-z-]+)*))?(?:\+[0-9A-Za-z-]+)?)", version)

        if m:
            semantic_version = m.group(1)

        page_title = "{0} - {1} - {2}".format(name,
                                              semantic_version,
                                              current_date)

        if isComponent:
            changelog_content = self.generate_component_changelog()
            print("creates component changelog")
        else:
            changelog_content = self.generate_product_changelog()
            print("creates product changelog")

        if changelog_content:
            print("")
        else:            
            sys.exit("ERROR: An Issue occured while trying to generate the changelog")

        self.push_to_confluence(parent_page_id, page_title, changelog_content)

    def generate_component_changelog(self, component_name, product_name, version):
        release = self.bitbucket_service.get_release(
            product_name, component_name, version)

        changelog_content = self.component_changelog_template.replace(
            "%component_version%", version)
        changelog_content = changelog_content.replace("%jira_tasks%", version)

        return changelog_content

    def generate_product_changelog(self):
        changelog_content = ""
        return changelog_content

    def push_to_confluence(self, parent_page_id, title, content):
        converted_content = self.confluence.convert_wiki_to_storage(
            content)["value"]
        try:

            self.confluence.update_or_create(
                parent_page_id, title, converted_content, representation='storage')

            print("Page \"{0}\" is pushed to confluence".format(title))
        except HTTPError:
            print()
            sys.exit("ERROR: You may not have the permission to edit or access this page.")

    def load_releasenote_template(self, file_path):
        try:
            file = open(file_path,
                        encoding='utf-8', mode="r")
            self.releasenote_template = file.read()

        except IOError:
            print("Warning: Releasenote template file is missing.")

    def load_product_changelog_template(self):
        try:
            file = open("templates/product-changelog-template.gdlf",
                        encoding='utf-8', mode="r")
            self.product_changelog_template = file.read()

        except IOError:
            print("Warning: Product changelog template file is missing.")

    def load_component_changelog_template(self):
        try:
            file = open("templates/component-changelog-template.gdlf",
                        encoding='utf-8', mode="r")
            self.component_changelog_template = file.read()

        except IOError:
            print("Warning: Component changelog template file is missing.")
