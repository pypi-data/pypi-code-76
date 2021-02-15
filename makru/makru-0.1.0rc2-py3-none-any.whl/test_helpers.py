import os
import pytest
from . import helpers
from io import StringIO


class TestChooseFile:
    def test_can_return_path_if_file_exists(self, tmpdir):
        the_file_path = self.write_sample(tmpdir, "test.test")

        result = helpers.choose_file([self.build_path_template(tmpdir)], "test.test")
        assert result
        assert the_file_path == result

    def test_can_return_none_if_file_does_not_exist(self, tmpdir):
        result = helpers.choose_file([self.build_path_template(tmpdir)], "test")
        assert not result

    def test_can_return_correct_path_if_file_exists_when_have_multi_templates(
        self, tmpdir
    ):
        the_file_path = self.write_sample(tmpdir, "test.test")

        result = helpers.choose_file(
            ["./?", self.build_path_template(tmpdir)], "test.test"
        )
        assert result
        assert the_file_path == result

    @staticmethod
    def build_path_template(path):
        return os.path.join(path, "?")

    @staticmethod
    def write_sample(path, filename):
        fpath = os.path.join(path, filename)
        with open(fpath, "w+") as f:
            f.write("sample")
        return fpath


class TextRecorder(object):
    def __init__(self):
        self.buffer = StringIO()

    def record(self, x):
        self.buffer.write(x)

    @property
    def text(self):
        return self.buffer.getvalue()


class TestCheckBinary:
    def test_can_find_echo(self):
        """
        This test depends on the fact that most system have a binary "echo"
        """
        assert helpers.check_binary("echo")


class TestShell:
    def test_can_run_command(self):
        """
        This test depends on a fact that most system have a binary "echo"
        """
        if not helpers.check_binary("echo"):
            pytest.skip("could not found binary echo for this test")
        recorder = TextRecorder()

        helpers.shell(["echo", "test"], printf=recorder.record)

        lines = list(filter(lambda x: x != "", recorder.text.split(os.linesep)))
        assert len(lines) == 2
        assert lines[0].startswith("$")
        assert "echo test" in lines[0]
        assert lines[1] == "test"


class TestVersionHelpers:
    def test_compare_version_smoke_test(self):
        assert helpers.compare_version("0.1.1-alpha.2", "0.1.0-beta.10") > 0

    def test_match_version_smoke_test(self):
        assert helpers.match_version("0.1.2-alpha.2", ">0.1.0") == True
        assert helpers.match_version("0.2.1-pre.2+build.3", "<0.1.10") == False

    def test_is_semver_can_detect_non_semver_string_smoke_test(self):
        assert helpers.is_semver("20201210") == False

    def test_is_semver_can_detect_semver_smoke_test(self):
        assert helpers.is_semver("2.0.0-beta.2+build.4") == True

    def test_is_prerelease_smoke_test(self):
        assert helpers.is_prerelease("2.0.0") == False
        assert helpers.is_prerelease("2.0.0-beta.0") == True

    def test_pick_latest_release_can_pick_latest_release(self):
        DATA = [
            "0.2.0",
            "0.1.0-beta.6",
            "0.1.0-beta.10",
            "0.1.0",
            "0.2.0-alpha.4+build1",
            "0.3.0",
        ]
        assert helpers.pick_latest_release(DATA) == "0.3.0"

    def test_pick_max_version_can_pick_max_version(self):
        DATA = [
            "0.1.0-alpha.4",
            "0.1.0-beta.1",
            "0.1.0-beta.1+build.1",
            "0.2.0",
            "0.3.0-alpha.1",
            "0.3.0-alpha.2+build.1",
            "0.3.0-alpha.2+build.2",
        ]
        assert helpers.pick_max_version(DATA) == "0.3.0-alpha.2+build.2"
