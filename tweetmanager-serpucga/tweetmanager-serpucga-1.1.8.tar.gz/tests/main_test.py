#!/usr/bin/env python3

import unittest
import os

import main
from lib import filesystem


class MainTestCase(unittest.TestCase):
    """Tests for the main execution script"""

    def setUp(self):
        """
        Set up some variables
        """

        self.this_file = os.path.realpath(__file__)
        self.this_dir = os.path.dirname(self.this_file)
        self.input_dir = os.path.join(self.this_dir, "input")

        # Run the tests silently to avoid filling screen with text
        main.silent = True

    def test_changeOutputDir_toRealDir_OK(self):
        """Test that change_output_dir returns the new dir"""

        output_dir = filesystem.change_output_dir(self.this_dir, False, True)
        self.assertEqual(output_dir, self.this_dir)

    def test_changeOutputDir_toFile_fails(self):
        """
        Test that change_output_dir makes sys.exit(2) when someone
        passes a file instead of a dir
        """
        with self.assertRaises(SystemExit) as context_manager:
            filesystem.change_output_dir(self.this_file, False, True)
        self.assertEqual(context_manager.exception.code, 2)

    def test_changeOutputDir_toJunk_fails(self):
        """
        Test that change_output_dir makes sys.exit(2) when someone
        passes random things
        """
        with self.assertRaises(SystemExit) as context_manager:
            filesystem.change_output_dir("waza wasa", False, True)
        self.assertEqual(context_manager.exception.code, 2)

    def test_changeExecutionMode_toFlatten_OK(self):
        """
        Test that change_execution_mode to some of the existent
        execution modes works well
        """

        self.assertEqual(main.change_execution_mode("flatten"), "flatten")

    def test_changeExecutionMode_toRamen_fails(self):
        """
        Test that change_execution_mode to something else fails
        """

        with self.assertRaises(SystemExit) as context_manager:
            main.change_execution_mode("Ramen")
        self.assertEqual(context_manager.exception.code, 2)


unittest.main()
