from __future__ import absolute_import

import logging
import os

import fire

from ddc.task_black import start_black
from ddc.task_build_docker_image import start_build_docker_image
from ddc.task_lint import start_lint
from ddc.task_meta import start_meta
from ddc.info import (
    print_about_version,
    check_pip_version,
    upgrade_pip_version_to_latest,
)
from ddc.task_test import start_test
from ddc.utils import query_yes_no, run_if_time_has_passed


def print_and_exit(exit_code, out):
    sout = out.strip()
    if len(sout) > 0:
        print(sout)  # noqa
    if exit_code == 0:
        print("👌 Looks good!")  # noqa
    else:
        print("⛔️ We have error")  # noqa
    exit(exit_code)


class Cli(object):
    """
    Devision Developers Cli Lib.
    👉 Press 'q' for exit
    """

    def __init__(self) -> None:
        super().__init__()
        self.cwd = os.getcwd()

    def meta(self, workdir=None):
        """
        Start Meta App in dev mode
        :param workdir: str. By default is current dir
        :return:
        """
        if not workdir:
            workdir = self.cwd
        logging.info("Starter Meta. Work dir: " + workdir)
        start_meta(self.cwd)

    def lint(self, lang="py", workdir=None):
        """
        Start lint of current directory. Run in a directory that needs linting
        :param workdir: str. By default is current dir
        :param lang: str Can be: [ py | php ]
        :return:
        """
        if not workdir:
            workdir = self.cwd
        logging.info("Start linter. Work dir: " + workdir)
        exit_code, out = start_lint(workdir, lang)
        print_and_exit(exit_code, out)

    def black(self, lang="py", workdir=None):
        """
        The uncompromising code formatter. Run in a directory that needs formatting
        :param workdir: str. By default is current dir
        :param lang: str Can be: [ py ]
        :return:
        """
        if not workdir:
            workdir = self.cwd
        logging.info("Start black. Work dir: " + workdir)
        exit_code, out = start_black(workdir, lang)
        print_and_exit(exit_code, out)

    def build_docker_image(self, workdir=None):
        """
        Build docker image
        :param workdir: str. By default is current dir
        :return:
        """
        if not workdir:
            workdir = self.cwd
        logging.info("Start build docker image. Work dir: " + workdir)
        exit_code, out, image_tag = start_build_docker_image(workdir)
        if not exit_code:
            print("Image tag: " + str(image_tag))  # noqa
        print_and_exit(exit_code, out)

    def test(self, lang="py", workdir=None, save_test_results=False):
        """
        Test file MUST be in directory /tests in workdir
        If tests are not found, they are considered to have failed.
        :param workdir: str. By default is current dir
        :param lang: str Can be: [ py ]
        :param save_test_results: bool Save results in junit format to directory "test-results"
        :return:
        """
        if not workdir:
            workdir = self.cwd
        logging.info("Start tests. Work dir: " + workdir)
        exit_code, out = start_test(workdir, lang, save_test_results)
        print_and_exit(exit_code, out)

    def version(self):
        """Show the ddc version information"""
        print_about_version()

    def upgrade(self):
        """Upgrade cli lib"""
        upgrade_pip_version_to_latest()


def try_check_version():
    if not check_pip_version():
        print("⚡️ You use not latest version of ddc")  # noqa
        if query_yes_no("Do you want update lib?"):
            upgrade_pip_version_to_latest()


def main():
    run_if_time_has_passed("pip_version", 60, try_check_version)
    fire.Fire(Cli, name="ddc")


if __name__ == "__main__":
    main()
