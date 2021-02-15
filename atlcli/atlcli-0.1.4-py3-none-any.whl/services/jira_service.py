import base64
import requests
import json
from atlassian import Jira
import pprint36 as pprint
import ssl
from prettytable import PrettyTable


class JiraService:

    def __init__(self, url, username, password, skipssl):
        self.skipssl = skipssl
        self.url = url        
        self.username = username
        self.password = password
        self.jiraInstance = Jira(
            url=url,
            username=username,
            password=password,
            verify_ssl=self.skipssl)

    def get_ticket(self, ticket_name):
        """get tickets basic infos"""
        pass

    def close_ticket(self, ticket_name):
        """closes a ticket"""
        pass

    def get_changelog(self, ticket_name):
        """get commits and repos changed linked to ticket"""
        issue_details = self.jiraInstance.issue(ticket_name)
        issue_id = issue_details["id"]
        changes = self.get_changes(issue_id)

    def get_repositories_from_issue(self, issue_id):
        endpoint_url = "{url}/rest/dev-status/1.0/issue/detail".format(
            url=self.url)

        querystring = {
            "issueId": issue_id,
            "applicationType": "stash",
            "dataType": "repository"
        }

        payload = ""

        encodedBytes = base64.b64encode("{username}:{password}"
                                        .format(username=self.username,
                                                password=self.password)
                                        .encode("utf-8"))
        base64_auth = str(encodedBytes, "utf-8")
        headers = {
            'Content-Type': "application/json",
            'Authorization': "Basic {0}".format(base64_auth)
        }

        response = requests.request(
            "GET", endpoint_url, data=payload, headers=headers, params=querystring, verify=self.skipssl)
        result = json.loads(response.text)
        repositories = result["detail"][0]["repositories"]
        return repositories

    def get_project_version_infos(self, project_key, version):
        data = self.jiraInstance.get_project_versions_paginated(
            project_key, limit=50)
        versionData = next(
            filter(lambda x: x["name"] == version, data["values"]), None)

        # Validation
        if versionData is not None:
            if "name" not in versionData:
                versionData["name"] = ""
            if "id" not in versionData:
                versionData["id"] = ""
            if "description" not in versionData:
                versionData["description"] = ""
            if "released" not in versionData:
                versionData["released"] = ""
            if "startDate" not in versionData:
                versionData["startDate"] = ""
            if "releaseDate" not in versionData:
                versionData["releaseDate"] = ""
            
            return versionData
        else:
            return None

    def get_project_version_issues(self, project_key, versionId):
        jql_query = "project = {0} AND fixVersion = {1} AND (type = Story OR type = Improvement ) order by key".format(
            project_key, versionId)

        data = self.jiraInstance.jql(jql_query)["issues"]
        return data

    def get_issues_confluence_markup(self, project_key, versionId):
        issues = self.get_project_version_issues(project_key, versionId)

        content = "|| Ticket JIRA || Projects || Status || Summary || Remarques ||\n"
        rows = ""
        for x in issues:
            repositories = self.get_repositories_from_issue(x["id"])
            concatRepos = ""

            if len(repositories) > 0:
                for r in repositories:
                    concatRepos = concatRepos + r["name"] + ", "

            if concatRepos == "":
                concatRepos = " "
            row = "||{ticket}|{repos}|{status}|{summary}|{remarques}|".format(
                ticket=x["key"], repos=concatRepos, status=x["fields"]["status"]["name"], summary=x["fields"]["summary"].replace("|", "-"), remarques=" ")
            rows = rows + row + "\n"

        content = content + rows
        return content

    # Creates the issues refered to a jira product
    def get_issues_printable(self, versionId):
        issues = self.get_project_version_issues(versionId)
        table = PrettyTable()
        table.field_names = ["Key", "Repositories", "Status"]

        for x in issues:
            repositories = self.get_repositories_from_issue(x["id"])
            concatRepos = ""

            if len(repositories) > 0:
                table.add_row([x["key"], repositories[0]["name"],
                               x["fields"]["status"]["name"]])
            else:
                table.add_row([x["key"], "None",
                               x["fields"]["status"]["name"]])

        output = "----------Issues----------\n{0}".format(table)
        return output
