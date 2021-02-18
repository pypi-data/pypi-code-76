#!/usr/bin/env python3

import unittest
import os
import shutil
from unittest import mock

import main
from lib import filesystem


class SplitTestCase(unittest.TestCase):

    def setUp(self):
        """
        Set up some variables
        """

        self.this_file = os.path.realpath(__file__)
        self.this_dir = os.path.dirname(self.this_file)  # Test dir
        self.input_dir = os.path.join(self.this_dir, "input")
        self.json_collection = os.path.join(self.input_dir,
                                            "ChicagoGeoTime_Brexit.json")
        self.ten_tweets_file = os.path.join(self.input_dir, "ten_tweets.json")
        self.two_tweets_file = os.path.join(self.input_dir, "two_tweets.json")
        self.single_tweet_file = os.path.join(self.input_dir,
                                              "single_tweet.json")
        self.not_json_file = os.path.join(self.input_dir, "text_file.txt")
        self.bad_json_file = os.path.join(self.input_dir,
                                          "corrupt_json_file.json")
        self.not_tweet_collection = os.path.join(self.input_dir,
                                                 "not_tweet_collection.json")
        main.silent = True

    def test_splitMode_jsonCollection_OK(self):
        """
        Test that the activation of split mode works fine with a more or
        less large JSON file. Then remove the resulting collection dir.
        """

        # print("\nExecuting test_splitMode_jsonCollection_OK")
        split_col = main.split_mode(self.json_collection, self.this_dir)
        shutil.rmtree(split_col)
        # print("Contents of the test dir: " + str(os.listdir(self.this_dir)))

    def test_splitMode_tenTweetsCol_OK(self):
        """
        Test that the splitting of a mini-collection of ten tweets works
        fine and results in a new dir with ten splitted JSONs.
        """

        # print("\nExecuting test_splitMode_tenTweetsCol_OK")
        split_col = main.split_mode(self.ten_tweets_file, self.this_dir)
        self.assertEqual(len(os.listdir(split_col)), 10)
        shutil.rmtree(split_col)
        # print("Contents of the test dir: " + str(os.listdir(self.this_dir)))

    def test_splitMode_singleTweet_OK(self):
        """
        Even though the split method was thought for more or less large
        collections, it should work well as well with a single tweet
        (which simply copies the tweet)
        """

        # print("\nExecuting test_splitMode_singleTweet_OK")
        single_tweet = main.split_mode(self.single_tweet_file, self.this_dir)
        self.assertEqual(len(os.listdir(single_tweet)), 1)
        self.assertEqual(os.listdir(single_tweet)[0], "0.json")
        shutil.rmtree(single_tweet)
        # print("Contents of the test dir: " + str(os.listdir(self.this_dir)))

    def test_splitMode_inputNotJson_fails(self):
        """
        If the input is something else (not a .json file) the program
        should abort and throw error
        """

        # print("\nExecuting test_splitMode_inputNotJson_fails")
        with self.assertRaises(SystemExit) as context_manager:
            output_dir =\
                filesystem.create_collection_dir(self.not_json_file,
                                                 self.this_dir, "split", True)
            main.split_mode(self.not_json_file, output_dir)
        self.assertEqual(context_manager.exception.code, 1)
        # print("Contents of the test dir: " + str(os.listdir(self.this_dir)))

    def test_splitMode_inputCorruptJson_fails(self):
        """
        If the input is a bad JSON (in this case we only check that the
        number of braces is good), the program should fail appropriately and no
        collection dir should be created
        """

        # print("\nExecuting test_splitMode_inputCorruptJson_fails")
        with self.assertRaises(SystemExit) as context_manager:
            main.split_mode(self.bad_json_file, self.this_dir)
        self.assertEqual(context_manager.exception.code, 1)
        self.assertFalse(os.path.isdir(os.path.join(self.this_dir, "Split")))
        # print("Contents of the test dir: " + str(os.listdir(self.this_dir)))

    def test_splitMode_collectionAlreadyExistsOverwrite_OK(self):
        """
        Try to split a collection twice: the first time it should create
        the output dir normally, and the second one it will find the
        previous dir. Mock up a 'y' response to the overwrite prompt and
        remove the new directory.
        Care!! If a dir for that collection previously existed this
        could fail
        """

        # print(
        # "\nExecuting test_splitMode_collectionAlreadyExistsOverwrite_OK")
        with mock.patch('main.input', side_effect=['y']):

            split_col = main.split_mode(self.two_tweets_file, self.this_dir)
            split_col = main.split_mode(self.two_tweets_file, self.this_dir)

        if 'split_col' in locals():
            shutil.rmtree(split_col)
        # print("Contents of the test dir: " + str(os.listdir(self.this_dir)))

    def test_splitMode_collectionAlreadyExistsAbort_OK(self):
        """
        Try to split a collection twice: the first time it creates a new
        collection and the second one it answers "n" to the overwriting
        question. Program should abort and exit with code 1
        """

        # print("\nExecuting test_splitMode_collectionAlreadyExistsAbort_OK")
        with self.assertRaises(SystemExit) as context_manager:
            with mock.patch('main.input', side_effect=['n']):
                splt_col = main.split_mode(self.two_tweets_file, self.this_dir)
                splt_col = main.split_mode(self.two_tweets_file, self.this_dir)

        if 'splt_col' in locals():
            shutil.rmtree(splt_col)

        self.assertEqual(context_manager.exception.code, 1)
        # print("Contents of the test dir: " + str(os.listdir(self.this_dir)))

    def test_splitMode_notTweetJsonCollection_OK(self):
        """
        Splitter should be good for any type of JSON files, not just
        tweet objects. This test checks that everything is alright with
        other data not taken from Twitter, and when split creates a
        collection with JSON files named with numbers
        """

        # print("\nExecuting test_splitMode_notTweetJsonCollection_OK")
        split_col =\
            main.split_mode(self.not_tweet_collection, self.this_dir)
        for filename in os.listdir(split_col):
            self.assertRegex(filename, r'\d+\.json$')
        shutil.rmtree(split_col)
        # print("Contents of the test dir: " + str(os.listdir(self.this_dir)))


unittest.main()
