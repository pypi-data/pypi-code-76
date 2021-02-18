import unittest
from tjauto import github_util

class TestGitHub(unittest.TestCase):
    def test_get_from_html_url(self):
        repo_name = github_util.get_repo_name("https://github.com/jtong/tjauto")
        self.assertEqual(repo_name, "tjauto")

    def test_get_from_https_clone_url(self):
        repo_name = github_util.get_repo_name("https://github.com/jtong/tjauto.git")
        self.assertEqual(repo_name, "tjauto")

    def test_get_from_ssh_clone_url(self):
        repo_name = github_util.get_repo_name("git@github.com:jtong/tjauto.git")
        self.assertEqual(repo_name, "tjauto")
