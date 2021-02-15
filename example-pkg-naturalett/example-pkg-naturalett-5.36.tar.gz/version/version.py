#!/usr/bin/env python
import os, re, logging
from os.path import dirname

_LOG = logging.getLogger(__name__)

my_dir = dirname(__file__)

class VersionPattern:
    """
    Version pattern class
    """

    def __init__(self):
        self.path = os.path.join(*[my_dir, "__init__.py"])
        self.patterns_parser = self._patterns_parser()

    def git_version(self):
        """
        Return a tag of the latest version and its commit hash.
        :return: A latest_tag and latest_tag_commit
        """
        try:
            import git

            try:
                repo = git.Repo(os.path.join(*[my_dir, "../.git"]))
            except git.NoSuchPathError:
                _LOG.warning('.git directory not found: Cannot compute the git version')
                return ''
            except git.InvalidGitRepositoryError:
                _LOG.warning('Invalid .git directory not found: Cannot compute the git version')
                return ''
        except ImportError:
            _LOG.warning('gitpython not found: Cannot compute the git version.')
            return ''
        if repo:
            if os.getenv('TEST_PYPI_PUBLISH'):
                latest_tag_commit = repo.head.commit
                latest_tag = ""
            else:
                tags = sorted(repo.tags, key=lambda t: t.commit.committed_datetime)
                latest_tag = tags[-1]
                latest_tag_commit = latest_tag.commit
            return latest_tag, latest_tag_commit

        return 'no_git_version'

    def replace(self, pattern: str, new_version: str):
        """
        Update the versions matching this pattern.
        This method reads the underlying file, replaces each occurrence of the
        matched pattern, then writes the updated file.
        :param new_version: The new version number as a string
        """

        with open(self.path, "r") as f:
            old_content = f.read()

        new_content = re.sub(pattern, r'\1 = "{0}"'.format(new_version), old_content, flags=re.MULTILINE)

        _LOG.debug(
            f"Writing new version number: path={self.path!r} version={new_version!r}"
        )

        with open(self.path, mode="w") as f:
            f.write(new_content)

    def _patterns_parser(self):
        """
        Return the versions matching this pattern.
        Because a pattern can match in multiple places, this method returns a
        set of matches.
        """
        latest_tag, latest_tag_commit = self.git_version()
        patterns_parser = [
            {'pattern': r'^(__version__) = .*$', 'new_version': latest_tag},
            {'pattern': r'^(__sha__) = .*$', 'new_version': latest_tag_commit}
        ]

        return patterns_parser

    def write_version(self):
        """
        Write the Semver version + git hash to file.
        """
        for parser in self.patterns_parser:
            self.replace(parser['pattern'], parser['new_version'])
            _LOG.debug(
                f"Writing new version number: path={self.path!r} version={parser['new_version']!r}"
            )

        return True

def do_setup() -> None:
    version = VersionPattern()
    version.write_version()

if __name__ == "__main__":
    do_setup()