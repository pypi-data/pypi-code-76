#!/usr/bin/env python3

import unittest
import os
import shutil

import main


class Flat2CsvTestCase(unittest.TestCase):

    def setUp(self):
        """Set up some variables and files"""

        self.this_file = os.path.realpath(__file__)
        self.this_dir = os.path.dirname(self.this_file)
        self.input_dir = os.path.join(self.this_dir, "input")

        self.json_file = os.path.join(self.input_dir, "single_tweet.json")
        self.json_flat_file =\
            os.path.join(self.input_dir, "single_tweet_flat.json")
        self.not_json_file = os.path.join(self.input_dir, "text_file.txt")
        self.bad_json_file =\
            os.path.join(self.input_dir, "corrupt_json_file.json")
        self.json_collection = os.path.join(self.input_dir, "ten_tweets")
        self.not_tweet_json_file =\
            os.path.join(self.input_dir, "not_tweet_file.json")
        self.not_tweet_json_flat_file =\
            os.path.join(self.input_dir, "not_tweet_file_flat.json")
        self.not_tweet_json_collection =\
            os.path.join(self.input_dir, "not_tweet_collection")
        self.not_json_dir = os.path.join(self.input_dir, "not_json_dir")
        self.flat_json_collection =\
            os.path.join(self.input_dir, "ten_tweets_flat")
        self.not_fully_flat_collection =\
            os.path.join(self.input_dir, "ten_tweets_flat_one_no_flat")

        main.silent = True

    def test_flat2csv_singleFlatJsonFile_OK(self):
        """
        Given a single flat JSON file as input, the CSV converter
        function should perform as expected and generate a single CSV
        file. Check that file exists.
        """

        csv_file =\
            main.flat2csv_mode(self.json_flat_file, self.this_dir)
        self.assertTrue(os.path.isfile(csv_file))

        os.remove(csv_file)

    def test_flat2csv_singleNotJsonFile_fail(self):
        """
        Given a single non JSON file, the program should make a neat
        fail for not being capable of performing the conversion
        """

        with self.assertRaises(SystemExit) as context_manager:
            main.flat2csv_mode(self.not_json_file, self.this_dir)
        self.assertEqual(context_manager.exception.code, 1)

    def test_flat2csv_singleNotFlatJsonFile_fail(self):
        """
        Given a single JSON file which has not been flattened, the
        program should fail
        NOTE: This could be changed to another way of managing the
        exception in a future
        """

        with self.assertRaises(SystemExit) as context_manager:
            main.flat2csv_mode(self.json_file, self.this_dir)
        self.assertEqual(context_manager.exception.code, 1)

    def test_flat2csv_flatJsonCollection_OK(self):
        """
        Given a collection of flat JSON files, the CSV converter
        function should perform as expected and generate a collection
        of CSV files
        """

        csv_collection =\
            main.flat2csv_mode(self.flat_json_collection, self.this_dir)

        for year_dir in os.listdir(csv_collection):
            year_col = os.path.join(csv_collection, year_dir)

            for month_dir in os.listdir(year_col):
                month_col = os.path.join(year_col, month_dir)

                for day_dir in os.listdir(month_col):
                    day_col = os.path.join(month_col, day_dir)

                    for csv_file in os.listdir(day_col):
                        csv_file_path = os.path.join(day_col, csv_file)

                        self.assertRegex(year_dir, r'\d{4}')
                        self.assertRegex(month_dir, r'\d{2}')
                        self.assertRegex(day_dir, r'\d{2}')
                        self.assertTrue(os.path.isfile(csv_file_path))
                        self.assertEqual(len(os.listdir(day_col)), 10)
                        self.assertRegex(csv_file, r'\d+\.csv$')

        shutil.rmtree(csv_collection)

    def test_flat2csv_notJsonCollection_fail(self):
        """
        Given the path of a directory containing not JSON files, the
        program should exit in an orderly way
        """

        with self.assertRaises(SystemExit) as context_manager:
            main.flat2csv_mode(self.not_json_dir, self.this_dir)
        self.assertEqual(context_manager.exception.code, 1)

    def test_flat2csv_notFlatJsonCollection_fail(self):
        """
        Given a collection of JSON files where at least one of them has
        not been previously flattened, the program should fail
        NOTE: might be changed for another kind of managing
        """

        with self.assertRaises(SystemExit) as context_manager:
            main.flat2csv_mode(self.not_fully_flat_collection, self.this_dir)
        self.assertEqual(context_manager.exception.code, 1)


unittest.main()
