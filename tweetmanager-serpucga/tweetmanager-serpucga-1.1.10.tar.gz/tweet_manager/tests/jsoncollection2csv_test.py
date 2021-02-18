#!/usr/bin/env python3

import unittest
import os
import shutil

import main
from lib import filesystem


class JsonCollection2CsvTestCase(unittest.TestCase):

    def setUp(self):
        self.this_file = os.path.realpath(__file__)
        self.this_dir = os.path.dirname(self.this_file)
        self.input_dir = os.path.join(self.this_dir, "input")
        self.project_dir = os.path.dirname(self.this_dir)
        self.output_dir = os.path.join(self.project_dir, "output")

        self.ten_tweets = os.path.join(self.input_dir, "ten_tweets.json")
        self.two_tweets = os.path.join(self.input_dir, "two_tweets.json")
        self.split_ten_tweets = os.path.join(self.input_dir, "ten_tweets")

    def test_jsoncollection2csv_noKeep_OK(self):
        """
        Check that the test makes the full conversion cycle from a collection
        of JSON files to a collection of CSVs correctly. This doesn't keep
        intermediate files, so it is just the CSV collection that needs to be
        cleaned at the end.
        """

        output_dir =\
            filesystem.create_collection_dir(self.ten_tweets, self.this_dir,
                                             "jsoncollection2csv", True)
        csv_ten_tweets =\
            main.jsoncollection2csv_mode(self.ten_tweets, output_dir)
        i = 0
        for year_dir in os.listdir(csv_ten_tweets):
            year_dir_path = os.path.join(csv_ten_tweets, year_dir)

            for month_dir in os.listdir(year_dir_path):
                month_dir_path = os.path.join(year_dir_path, month_dir)

                for day_dir in os.listdir(month_dir_path):
                    day_dir_path = os.path.join(month_dir_path, day_dir)

                    for json_file in os.listdir(day_dir_path):

                        self.assertRegex(day_dir, r'\d{2}')
                        self.assertRegex(month_dir, r'\d{2}')
                        self.assertRegex(year_dir, r'\d{4}')
                        self.assertRegex(json_file, r'.*.csv')
                        i += 1

        self.assertTrue(i == 10)
        shutil.rmtree(output_dir)

    def test_jsoncollection2csv_keepFiles_OK(self):
        """
        Full conversion cycle from a collection of JSON files to one of CSV
        files, keeping the intermediate results. Check that the 3 collections
        exist (split, flat and csv) and then clean that files. CARE: This will
        fail if the user creates a "ten_tweets" collection in the split or flat
        output folders
        """

        main.keep_files = True
        output_dir =\
            filesystem.create_collection_dir(self.ten_tweets, self.this_dir,
                                             "jsoncollection2csv", True)
        main.jsoncollection2csv_mode(self.ten_tweets, output_dir)

        self.assertTrue("ten_tweets" in os.listdir(self.this_dir))
        self.assertTrue("Split" in os.listdir(output_dir))
        self.assertTrue("Flat" in os.listdir(output_dir))
        self.assertTrue("CSV" in os.listdir(output_dir))

        shutil.rmtree(output_dir)

        main.keep_files = False


unittest.main()
