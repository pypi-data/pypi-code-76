#
# Copyright (c) 2020-2021 Pinecone Systems Inc. All right reserved.
#

from pinecone.api_base import BaseAPI

__all__ = ["HubAPI"]


class HubAPI(BaseAPI):
    """API calls to the hub"""

    def get_login(self):
        """Returns the docker command for logging into the Hub."""
        return self.post("/login")

    def create_repository(self, repository_name):
        return self.post("/repositories",  json={"repository_name": repository_name})

    def delete_repository(self, repository_name):
        return self.delete("/repositories/{}".format(repository_name))

    def list_repository_tags(self, repository_name):
        """List repository tags"""
        return self.get("/repositories/{}/tags".format(repository_name))

    def list_repositories(self):
        """Show all the repositories for the user."""
        return self.get("/repositories")

