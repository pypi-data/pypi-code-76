#!/usr/bin/env python
# -*- coding: utf-8 -*-
import unittest
import os
from lilies import columnify, wilt


class TestBordered(unittest.TestCase):
    def setUp(self):
        self.console_width = 30
        self.columns_10_entries_vertical = os.linesep.join(
            [
                "01abcde   05abcde   09abcde",
                "02abcde   06abcde   10abcde",
                "03abcde   07abcde",
                "04abcde   08abcde",
            ]
        )
        self.columns_10_entries_horizontal = os.linesep.join(
            [
                "01abcde   02abcde   03abcde",
                "04abcde   05abcde   06abcde",
                "07abcde   08abcde   09abcde",
                "10abcde",
            ]
        )
        self.one_column_long_entries = os.linesep.join(
            [
                "abcdefghijklmnopqrstuvwxyz0123",
                "0" * 25 + " " * 5,
                "9" * 28 + " " * 2,
            ]
        )
        self.one_entry = "abcd"
        self.empty = ""

    def test_columnify_works_with_10_entries_vertical(self):
        expected = self.columns_10_entries_vertical

        entries = expected.split()
        actual = wilt(columnify(entries, width=self.console_width))
        self.assertEqual(expected, actual)

    def test_columnify_works_with_10_entries_horizontal(self):
        expected = self.columns_10_entries_horizontal

        entries = expected.split()
        actual = wilt(
            columnify(entries, width=self.console_width, horizontal=True)
        )
        self.assertEqual(expected, actual)

    def test_columnify_works_with_long_entries(self):
        expected = self.one_column_long_entries

        entries = expected.split()
        actual = wilt(columnify(entries, width=self.console_width, sort=False))
        self.assertEqual(expected, actual)

    def test_columnify_works_with_one_entry(self):
        expected = self.one_entry

        entries = expected.split()
        actual = wilt(columnify(entries, width=self.console_width))
        self.assertEqual(expected, actual)

    def test_columnify_works_with_empty_list(self):
        expected = self.empty

        entries = expected.split()
        actual = wilt(columnify(entries, width=self.console_width))
        self.assertEqual(expected, actual)
