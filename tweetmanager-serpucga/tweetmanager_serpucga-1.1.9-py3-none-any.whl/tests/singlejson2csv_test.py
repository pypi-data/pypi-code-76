#!/usr/bin/env python3

import unittest
import os
import csv
import time
from unittest import mock

import main
from lib import filesystem


class SingleJson2CsvTestCase(unittest.TestCase):

    def setUp(self):
        self.this_file = os.path.realpath(__file__)
        self.this_dir = os.path.dirname(self.this_file)
        self.input_dir = os.path.join(self.this_dir, "input")
        self.output_dir = os.path.join(self.this_dir, "output")
        self.project_dir = os.path.dirname(self.this_dir)

        self.json_file = os.path.join(self.input_dir, "single_tweet.json")
        self.json_file2 = os.path.join(self.input_dir, "single_tweet2.json")
        self.csv_file2 =\
            os.path.join(self.input_dir, "single_tweet2.csv")
        self.include_filter =\
            os.path.join(self.input_dir, "default_include_filter.txt")
        self.exclude_filter =\
            os.path.join(self.input_dir, "default_exclude_filter.txt")
        self.corrupt_json =\
            os.path.join(self.input_dir, "corrupt_json_file.json")
        main.silent = True

    def test_singlejson2csv_singleFileIncludeFilterUpv_OK(self):
        """
        Check that a single JSON file is converted correctly to CSV when
        operating in UPV-compatible mode and with the default UPV filter. That
        is: remove dollar terminations, flatten 1 time the arrays and apply the
        default include filter
        """

        # UPV mode
        main.array_compression = True
        main.compression_depth = 1
        main.remove_dollars = True
        regex_include_filter = filesystem.load_filter(self.include_filter)

        converted_file =\
            main.singlejson2csv_mode(self.json_file2, self.this_dir,
                                     include_filter=regex_include_filter)
        with open(converted_file) as open_converted_file:
            with open(self.csv_file2) as open_csv_file2:
                csv_doc1 = csv.reader(open_converted_file)
                csv_doc2 = csv.reader(open_csv_file2)
                csv_doc1_lines = []
                csv_doc2_lines = []

                for row in csv_doc1:
                    csv_doc1_lines.append(str(row))
                for row in csv_doc2:
                    csv_doc2_lines.append(str(row))

                self.assertEqual(csv_doc1_lines, csv_doc2_lines)
        os.remove(converted_file)

    def test_singlejson2csv_singleFileAlreadyConvertedAnswerNo_exits(self):
        """
        Check that trying to convert a JSON file to CSV when the resulting CSV
        file already exists prompts a message to confirm overwrite Y/N, and
        answering "n" makes the program exit with a 1
        """

        csv_file =\
            main.singlejson2csv_mode(self.json_file, self.this_dir)

        with self.assertRaises(SystemExit) as context_manager:
            with mock.patch('main.input', side_effect=['n']):
                main.singlejson2csv_mode(self.json_file, self.this_dir)

        if os.path.isfile(csv_file):
            os.remove(csv_file)

        self.assertEqual(context_manager.exception.code, 1)

    def test_singlejson2csv_singleFileAlreadyConvertedAnswerYesOverwr_OK(self):
        """
        Check that trying to convert a JSON file to CSV when the resulting CSV
        file already exists prompts a message to confirm overwrite Y/N, and
        answering "y" makes the program overwrite the file. Check that the file
        was overwritten (modification date less than 1 second)
        """

        csv_file =\
            main.singlejson2csv_mode(self.json_file, self.this_dir)

        with mock.patch('main.input', side_effect=['y']):
            csv_file =\
                main.singlejson2csv_mode(self.json_file, self.this_dir)

        now_date = time.time()
        csv_file_date = os.path.getmtime(csv_file)

        self.assertTrue((now_date - csv_file_date) < 1)
        if os.path.isfile(csv_file):
            os.remove(csv_file)

    def test_singlejson2csv_notJsonFile_fails(self):
        """
        Check that trying to apply the JSON to CSV conversion to a not JSON
        file fails in an orderly manner
        """

        with self.assertRaises(SystemExit) as context_manager:
            main.singlejson2csv_mode(self.include_filter, self.this_dir)

        self.assertEqual(context_manager.exception.code, 1)

    def test_singlejson2csv_corruptJsonFile_fails(self):
        """
        Check that trying to apply the JSON to CSV conversion to a file corrupt
        JSON file (with .json extension but that doesn't correctly follow the
        JSON structure) fails in an orderly manner
        """

        with self.assertRaises(SystemExit) as context_manager:
            main.singlejson2csv_mode(self.corrupt_json, self.this_dir)

        self.assertEqual(context_manager.exception.code, 1)

    def test_singlejson2csv_singleFileConvertedKeepFiles_OK(self):
        """
        Check that a single file can be converted correctly and that the
        intermediate files are stored where they belong if keep flag is up
        """

        main.keep_files = True

        csv_file = main.singlejson2csv_mode(self.json_file, self.this_dir)
        flat_file_path = os.path.join(self.this_dir, "single_tweet_flat.json")

        self.assertEqual(os.path.basename(csv_file), "single_tweet.csv")
        self.assertTrue(os.path.isfile(flat_file_path))

        os.remove(csv_file)
        os.remove(os.path.join(self.this_dir, "single_tweet_flat.json"))

        main.keep_files = False

    def test_singlejson2csv_keepFilesDoesNotOverwrite_OK(self):
        """
        Check that when a file is converted to CSV and the keep files flag is
        up, the stored flat file does not overwrite the previous one. Instead,
        the converter adds a number as an ending and keeps both files
        """

        main.keep_files = True

        main.singlejson2csv_mode(self.json_file, self.this_dir)

        with mock.patch('main.input', side_effect=['y']):
            csv_file = main.singlejson2csv_mode(self.json_file, self.this_dir)

        first_file = os.path.join(self.this_dir, "single_tweet_flat.json")
        second_file = os.path.join(self.this_dir, "single_tweet_flat_1.json")

        self.assertTrue(os.path.isfile(first_file))
        self.assertTrue(os.path.isfile(second_file))

        os.remove(first_file)
        os.remove(second_file)
        os.remove(csv_file)

        main.keep_files = False


unittest.main()
