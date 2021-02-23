#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import unittest
from lilies import wilt, resize
from lilies.objects.lilyblock import LilyBlock


class TestResize(unittest.TestCase):
    def setUp(self):
        self.strings = [
            "hello",
            "dfDfEEFdfaC",
            "Mister John",
            "mr. jOhn",
            "iSn't it",
            "comma,separated,values",
            "trailing,comma,",
            ",",
        ]
        self.block_str = os.linesep.join(self.strings)
        self.twenty_chars = "12345678901234567890"

    def test_empty_align_fails(self):
        with self.assertRaises(TypeError):
            resize(self.twenty_chars, 20, align="")

    def test_garbage_align_fails(self):
        with self.assertRaises(TypeError):
            resize(self.twenty_chars, 20, align="garbage")

    def test_garbage_x_align_fails(self):
        with self.assertRaises(TypeError):
            resize(self.twenty_chars, align="top garbage")

    def test_garbage_y_align_fails(self):
        with self.assertRaises(TypeError):
            resize(self.twenty_chars, align="garbage left")

    def test_resize_vertically_respects_fill_character(self):
        resized = resize("   ", 5, 3, "center", character="a")
        expected = "\n".join(["aaaaa", "a   a", "aaaaa"])
        self.assertEqual(expected, wilt(resized))

    def test_resize_to_same_size_leaves_unchanged(self):
        resized = resize(self.twenty_chars, 20, add_elipsis=False)
        self.assertEqual(self.twenty_chars, wilt(resized))

    def test_resize_same_width_with_elipsis_leaves_unchanged(self):
        resized = resize(self.twenty_chars, 20, add_elipsis=True)
        self.assertEqual(self.twenty_chars, wilt(resized))

    def test_resize_same_width_centered_leaves_unchanged(self):
        resized = resize(self.twenty_chars, 20, align="center")
        self.assertEqual(self.twenty_chars, wilt(resized))

    def test_resize_smaller_left_no_elipsis_truncates(self):
        expected = self.twenty_chars[:10]
        resized = resize(
            self.twenty_chars, 10, align="left", add_elipsis=False
        )
        self.assertEqual(expected, wilt(resized))

    def test_resize_smaller_left_with_elipsis_truncates(self):
        expected = self.twenty_chars[:8] + ".."
        resized = resize(self.twenty_chars, 10, align="left", add_elipsis=True)
        self.assertEqual(expected, wilt(resized))

    def test_resize_smaller_right_with_elipsis_truncates(self):
        # we basically expect this to be the same. Don't truncate left side.
        expected = self.twenty_chars[:8] + ".."
        resized = resize(
            self.twenty_chars, 10, align="right", add_elipsis=True
        )
        self.assertEqual(expected, wilt(resized))

    def test_resize_smaller_center_with_elipsis_truncates(self):
        # we basically expect this to be the same. Don't truncate left side.
        expected = self.twenty_chars[:8] + ".."
        resized = resize(
            self.twenty_chars, 10, align="center", add_elipsis=True
        )
        self.assertEqual(expected, wilt(resized))

    def test_resize_horiz_larger_left(self):
        expected = self.twenty_chars + " " * 20
        resized = resize(self.twenty_chars, 40, align="left")
        self.assertEqual(expected, wilt(resized))

    def test_resize_horiz_larger_right(self):
        expected = " " * 20 + self.twenty_chars
        resized = resize(self.twenty_chars, 40, align="right")
        self.assertEqual(expected, wilt(resized))

    def test_resize_horiz_larger_center_even(self):
        expected = " " * 10 + self.twenty_chars + " " * 10
        resized = resize(self.twenty_chars, 40, align="center")
        self.assertEqual(expected, wilt(resized))

    def test_resize_horiz_larger_center_odd(self):
        expected = " " * 9 + self.twenty_chars + " " * 10
        resized = resize(self.twenty_chars, 39, align="center")
        self.assertEqual(expected, wilt(resized))

    def test_resize_block_horiz_larger(self):
        control_group = [
            "hello                  ",
            "dfDfEEFdfaC            ",
            "Mister John            ",
            "mr. jOhn               ",
            "iSn't it               ",
            "comma,separated,values ",
            "trailing,comma,        ",
            ",                      ",
        ]
        control = os.linesep.join(control_group)
        block = LilyBlock(self.block_str)
        result = resize(block, width=23)
        self.assertEqual(control, wilt(result))

    def test_resize_block_vert_top_larger(self):
        control_group = [
            "hello                 ",
            "dfDfEEFdfaC           ",
            "Mister John           ",
            "mr. jOhn              ",
            "iSn't it              ",
            "comma,separated,values",
            "trailing,comma,       ",
            ",                     ",
            "                      ",
            "                      ",
            "                      ",
        ]
        control = os.linesep.join(control_group)
        block = LilyBlock(self.block_str)
        result = resize(block, height=11, align="top")
        self.assertEqual(control, wilt(result))

    def test_resize_block_vert_bottom_larger(self):
        control_group = [
            "                      ",
            "                      ",
            "hello                 ",
            "dfDfEEFdfaC           ",
            "Mister John           ",
            "mr. jOhn              ",
            "iSn't it              ",
            "comma,separated,values",
            "trailing,comma,       ",
            ",                     ",
        ]
        control = os.linesep.join(control_group)
        block = LilyBlock(self.block_str)
        result = resize(block, height=10, align="bottom")
        self.assertEqual(control, wilt(result))

    def test_resize_block_vert_center_larger(self):
        control_group = [
            "                      ",
            "                      ",
            "hello                 ",
            "dfDfEEFdfaC           ",
            "Mister John           ",
            "mr. jOhn              ",
            "iSn't it              ",
            "comma,separated,values",
            "trailing,comma,       ",
            ",                     ",
            "                      ",
            "                      ",
            "                      ",
        ]
        control = os.linesep.join(control_group)
        block = LilyBlock(self.block_str)
        result = resize(block, height=13, align="center left")
        self.assertEqual(control, wilt(result))

    def test_resize_block_vert_top_smaller(self):
        control_group = [
            "hello      ",
            "dfDfEEFdfaC",
            "Mister John",
            "mr. jOhn   ",
            "iSn't it   ",
        ]
        control = os.linesep.join(control_group)
        block = LilyBlock(self.block_str)
        result = resize(block, height=5, align="top")
        self.assertEqual(control, wilt(result))

    def test_resize_block_vert_bottom_smaller(self):
        control_group = [
            "dfDfEEFdfaC           ",
            "Mister John           ",
            "mr. jOhn              ",
            "iSn't it              ",
            "comma,separated,values",
            "trailing,comma,       ",
            ",                     ",
        ]
        control = os.linesep.join(control_group)
        block = LilyBlock(self.block_str)
        result = resize(block, height=7, align="bottom")
        self.assertEqual(control, wilt(result))

    def test_resize_block_vert_center_smaller(self):
        control_group = [
            "dfDfEEFdfaC           ",
            "Mister John           ",
            "mr. jOhn              ",
            "iSn't it              ",
            "comma,separated,values",
        ]
        control = os.linesep.join(control_group)
        block = LilyBlock(self.block_str)
        result = resize(block, height=5, align="center left")
        self.assertEqual(control, wilt(result))
