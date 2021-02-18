#!/usr/bin/env python3

import unittest
import os
import json

from lib import json2csv as jsontoolkit


class AlgorithmsTestCase(unittest.TestCase):
    """Tests for the implemented algorithms"""

    def setUp(self):
        """
        Set up some variables
        """

        self.this_file = os.path.realpath(__file__)
        self.this_dir = os.path.dirname(self.this_file)
        self.input_dir = os.path.join(self.this_dir, "input")
        self.two_tweets_file =\
            os.path.join(self.input_dir, "two_tweets.json")
        self.single_tweet_file =\
            os.path.join(self.input_dir, "single_tweet.json")
        self.single_tweet_file_flat =\
            os.path.join(self.input_dir, "single_tweet_flat.json")

    def test_identifySplitPoints_simpleCase_OK(self):
        """
        A simple case to check that the JSON delimiter identifier works
        as expected
        """

        test_string = '    { "{{{{}": {yey}              } {"}}}}"}'
        brace_delimiters_position = ([4, 36], [34, 43])

        self.assertEqual(
            jsontoolkit.identify_split_points(test_string),
            brace_delimiters_position)

    def test_identifySplitPoints_realCase_OK(self):
        """
        A bit more complex (but still simple case) with a collection
        file containing two JSONs, in this case two real tweet objects
        """

        with open(self.two_tweets_file) as json_file:
            json_text = json_file.read()

        brace_delimiters_position = ([0, 5770], [5768, 8755])
        self.assertEqual(jsontoolkit.identify_split_points(json_text),
                         brace_delimiters_position)

    def test_flatten_simpleCase_OK(self):
        """
        Use a simple manually written JSON object to check that the
        flattening algorithm works as expected
        """

        flat_result = {}

        json_object = {"name": "Ulf", "age": "24", "offense": {"damage":
                       "25", "attack_speed": "1.50", "range": "1"}, "weapons":
                       ["spear", "battleaxe", "morningstar", {"name": "Hourki",
                        "type": "trident"}]}

        expected_flat_object = {"name": "Ulf", "age": "24",
                                "offense.damage": "25",
                                "offense.attack_speed": "1.50",
                                "offense.range": "1", "weapons[0]": "spear",
                                "weapons[1]": "battleaxe",
                                "weapons[2]": "morningstar",
                                "weapons[3].name": "Hourki",
                                "weapons[3].type": "trident"}

        jsontoolkit.flatten("", json_object, flat_result)
        self.assertEqual(flat_result, expected_flat_object)

    def test_flatten_realCase_OK(self):
        """
        A bit more complex example using a long tweet object. Result is
        compared to a flattened file that has been checked for
        correctness
        """

        result_after_flattening = {}

        with open(self.single_tweet_file) as tweet_file:
            json_file = json.load(tweet_file)

        jsontoolkit.flatten("", json_file, result_after_flattening)

        with open(self.single_tweet_file_flat) as tweet_file_flat:
            json_file_flat = json.load(tweet_file_flat)

        self.assertEqual(result_after_flattening, json_file_flat)

    def test_json2csv_simpleCase_OK(self):
        """
        Use a simple manually written JSON flat object to check that the
        to-CSV conversion algorithm works correctly
        """

        flat_object_input = {"name": "Ulf", "age": "24",
                             "offense.damage": "25",
                             "offense.attack_speed": "1.50",
                             "offense.range": "1", "weapons[0]": "spear",
                             "weapons[1]": "battleaxe",
                             "weapons[2]": "morningstar",
                             "weapons[3].name": "Hourki",
                             "weapons[3].type": "trident"}

        expected_csv =\
            'name,age,offense.damage,offense.attack_speed,offense.range,' +\
            'weapons[0],weapons[1],weapons[2],weapons[3].name,' +\
            'weapons[3].type\n"Ulf","24","25","1.50","1","spear",' +\
            '"battleaxe","morningstar","Hourki","trident"'

        result_csv = jsontoolkit.json2csv(flat_object_input,
                                          array_compression=False,
                                          compression_depth=0,
                                          remove_dollars=False,)
        self.assertEqual(result_csv, expected_csv)

    def test_json2csv_simpleCase_sorted_coordinates_OK(self):
        """
        Use a simple manually written JSON flat object with nested ordered
        coordinates to check that the CSV conversion algorithm doesn't mess
        everything up
        """

        flat_object_input = {"type": "Military base",
                             "coordinates[0][3][0]": "17.91",
                             "coordinates[0][1][1]": "88",
                             "coordinates[0][0][0]": "51.2",
                             "coordinates[0][1][0]": "12.12",
                             "coordinates[0][2][1]": "111.1",
                             "coordinates[0][3][1]": "17.89",
                             "coordinates[0][0][1]": "2.3",
                             "coordinates[0][2][0]": "8321.1",
                             "name": "Area 51",
                             }

        expected_csv =\
            'type,name,coordinates\n"Military base","Area 51",' +\
            '"[[[""51.2"", ""2.3""], [""12.12"", ""88""], ' +\
            '[""8321.1"", ""111.1""], [""17.91"", ""17.89""]]]"'

        result_csv = jsontoolkit.json2csv(flat_object_input,
                                          array_compression=True,
                                          compression_depth=10,
                                          remove_dollars=False,)
        self.assertEqual(result_csv, expected_csv)

    def test_json2csv_realCase_OK(self):
        """
        Use a sample (but real) flattened tweet and convert it to CSV
        format. Then compare the results with a CSV sample file that
        matches the tweet and which has previously checked for
        correctness
        """

        pass


unittest.main()
