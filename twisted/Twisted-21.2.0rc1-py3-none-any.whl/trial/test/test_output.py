# Copyright (c) Twisted Matrix Laboratories.
# See LICENSE for details.

"""
Tests for the output generated by trial.
"""


import os
from io import StringIO

from twisted.scripts import trial
from twisted.trial import runner
from twisted.trial.test import packages


_noModuleError = "No module named 'frotz'"


def runTrial(*args):
    from twisted.trial import reporter

    config = trial.Options()
    config.parseOptions(args)
    output = StringIO()
    myRunner = runner.TrialRunner(
        reporter.VerboseTextReporter,
        stream=output,
        workingDirectory=config["temp-directory"],
    )
    suite = trial._getSuite(config)
    myRunner.run(suite)
    return output.getvalue()


class ImportErrorsTests(packages.SysPathManglingTest):
    """Actually run trial as if on the command line and check that the output
    is what we expect.
    """

    def debug(self):
        pass

    parent = "_testImportErrors"

    def runTrial(self, *args):
        return runTrial("--temp-directory", self.mktemp(), *args)

    def _print(self, stuff):
        print(stuff)
        return stuff

    def assertIn(self, container, containee, *args, **kwargs):
        # redefined to be useful in callbacks
        super().assertIn(containee, container, *args, **kwargs)
        return container

    def assertNotIn(self, container, containee, *args, **kwargs):
        # redefined to be useful in callbacks
        super().assertNotIn(containee, container, *args, **kwargs)
        return container

    def test_trialRun(self):
        self.runTrial()

    def test_nonexistentModule(self):
        d = self.runTrial("twisted.doesntexist")
        self.assertIn(d, "[ERROR]")
        self.assertIn(d, "twisted.doesntexist")
        return d

    def test_nonexistentPackage(self):
        d = self.runTrial("doesntexist")
        self.assertIn(d, "doesntexist")
        self.assertIn(d, "ModuleNotFound")
        self.assertIn(d, "[ERROR]")
        return d

    def test_nonexistentPackageWithModule(self):
        d = self.runTrial("doesntexist.barney")
        self.assertIn(d, "doesntexist.barney")
        self.assertIn(d, "ObjectNotFound")
        self.assertIn(d, "[ERROR]")
        return d

    def test_badpackage(self):
        d = self.runTrial("badpackage")
        self.assertIn(d, "[ERROR]")
        self.assertIn(d, "badpackage")
        self.assertNotIn(d, "IOError")
        return d

    def test_moduleInBadpackage(self):
        d = self.runTrial("badpackage.test_module")
        self.assertIn(d, "[ERROR]")
        self.assertIn(d, "badpackage.test_module")
        self.assertNotIn(d, "IOError")
        return d

    def test_badmodule(self):
        d = self.runTrial("package.test_bad_module")
        self.assertIn(d, "[ERROR]")
        self.assertIn(d, "package.test_bad_module")
        self.assertNotIn(d, "IOError")
        self.assertNotIn(d, "<module ")
        return d

    def test_badimport(self):
        d = self.runTrial("package.test_import_module")
        self.assertIn(d, "[ERROR]")
        self.assertIn(d, "package.test_import_module")
        self.assertNotIn(d, "IOError")
        self.assertNotIn(d, "<module ")
        return d

    def test_recurseImport(self):
        d = self.runTrial("package")
        self.assertIn(d, "[ERROR]")
        self.assertIn(d, "test_bad_module")
        self.assertIn(d, "test_import_module")
        self.assertNotIn(d, "<module ")
        self.assertNotIn(d, "IOError")
        return d

    def test_recurseImportErrors(self):
        d = self.runTrial("package2")
        self.assertIn(d, "[ERROR]")
        self.assertIn(d, "package2")
        self.assertIn(d, "test_module")
        self.assertIn(d, _noModuleError)
        self.assertNotIn(d, "<module ")
        self.assertNotIn(d, "IOError")
        return d

    def test_nonRecurseImportErrors(self):
        d = self.runTrial("-N", "package2")
        self.assertIn(d, "[ERROR]")
        self.assertIn(d, _noModuleError)
        self.assertNotIn(d, "<module ")
        return d

    def test_regularRun(self):
        d = self.runTrial("package.test_module")
        self.assertNotIn(d, "[ERROR]")
        self.assertNotIn(d, "IOError")
        self.assertIn(d, "OK")
        self.assertIn(d, "PASSED (successes=1)")
        return d

    def test_filename(self):
        self.mangleSysPath(self.oldPath)
        d = self.runTrial(os.path.join(self.parent, "package", "test_module.py"))
        self.assertNotIn(d, "[ERROR]")
        self.assertNotIn(d, "IOError")
        self.assertIn(d, "OK")
        self.assertIn(d, "PASSED (successes=1)")
        return d

    def test_dosFile(self):
        ## XXX -- not really an output test, more of a script test
        self.mangleSysPath(self.oldPath)
        d = self.runTrial(os.path.join(self.parent, "package", "test_dos_module.py"))
        self.assertNotIn(d, "[ERROR]")
        self.assertNotIn(d, "IOError")
        self.assertIn(d, "OK")
        self.assertIn(d, "PASSED (successes=1)")
        return d
