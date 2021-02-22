#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `pset1` package."""

import os
from tempfile import TemporaryDirectory
from unittest import TestCase
from environs import Env
from pset1.hash_str import hash_str, get_user_id, get_csci_pepper, get_csci_salt
from pset1.io import atomic_write
from pset1.canvas import get_assignment_id, get_quiz_id, get_course_id, get_excel_user_ids, get_answers, get_questions
from pset1.__main__ import main

env = Env()
env.read_env()


class FakeFileFailure(IOError):
    pass


class HashTests(TestCase):
    """ Testing related to hash string functions"""
    def test_basic(self):
        """test if hash string function works or not"""
        self.assertEqual(hash_str("world!", salt="hello, ").hex()[:6], "68e656")

    def test_csci_salt(self):
        """test csci salt value"""
        self.assertEqual(get_csci_salt().hex()[:6], '3f87b3')

    def test_csci_pepper(self):
        """test csci pepper value"""
        self.assertEqual(get_csci_pepper().hex()[:6], '888e12')

    def test_hash_str_salt_type(self):
        """test salt type only accepts str or byte"""
        try:
            hash_str("world!", salt=1).hex()[:6]
        except:
            self.assertRaises(TypeError)

    def test_hash_str_value_type(self):
        """test for value is only accepted in string or bytes"""
        try:
            hash_str(12, salt='hello, ').hex()[:6]
        except:
            self.assertRaises(TypeError)

    def test_hash_str_both_value_type(self):
        """test if salt and input is not string or byte"""
        try:
            hash_str(12, salt=23).hex()[:6]
        except:
            self.assertRaises(TypeError)

    def test_user_id_value(self):
        """testing get user id function value"""
        self.assertEqual(get_user_id('gorlins'), '70ded892')


class AtomicWriteTests(TestCase):
    def test_atomic_write(self):
        """Ensure file exists after being written successfully"""

        with TemporaryDirectory() as tmp:
            fp = os.path.join(tmp, "asdf.txt")

            with atomic_write(fp, "w") as f:
                assert not os.path.exists(fp)
                tmpfile = f.name
                f.write("asdf")

            assert not os.path.exists(tmpfile)
            assert os.path.exists(fp)

            with open(fp) as f:
                self.assertEqual(f.read(), "asdf")

    def test_atomic_failure(self):
        """Ensure that file does not exist after failure during write"""

        with TemporaryDirectory() as tmp:
            af = os.path.join(tmp, "atomic_failure.txt")

            with self.assertRaises(FakeFileFailure):
                with atomic_write(af, "w") as f:
                    tmpfile = f.name
                    assert os.path.exists(tmpfile)
                    raise FakeFileFailure()

            assert not os.path.exists(tmpfile)
            assert not os.path.exists(af)

    def test_file_exists(self):
        """Ensure an error is raised when a file exists"""

        with TemporaryDirectory() as tmp:
            fe = os.path.join(tmp, "test_file_exists.txt")

            with atomic_write(fe, "w") as f:
                assert not os.path.exists(fe)
                tmpfile = f.name
                f.write("test_file_exists")

            assert not os.path.exists(tmpfile)
            assert os.path.exists(fe)
            try:
                with atomic_write(fe, "w") as new_file:
                    new_file_name = new_file.name
                assert not os.path.exists(new_file_name)
            except:
                self.assertRaises(Exception)

    def test_as_file_arg(self):
        """Ensure right file type is returned with as_file argument"""

        with TemporaryDirectory() as tmp:
            fa = os.path.join(tmp, "abcd.txt")

            try:
                with atomic_write(fa, "w", as_file=True) as f:
                    assert not os.path.exists(fa)
                    self.assertEqual(type(f), "io.TextIOWrapper")

            except:
                with atomic_write(fa, "w", as_file=False) as f:
                    assert not os.path.exists(fa)
                    assert os.path.exists(f)

            finally:
                pass


class CanvasQuizTests(TestCase):
    """tests to validate canvas quiz submission functions"""

    def test_course_id(self):
        """test course id value"""
        self.assertEqual(get_course_id(), 81475)
        self.assertEqual(hash_str(get_course_id(uuid=True), '').hex()[:6], '764e76')

    def test_quiz_id(self):
        """test quiz id value"""
        self.assertEqual(get_quiz_id(), 205389)

    # def test_quiz_id_exception(self) :
    #     """test quiz id exception value"""
        try:
            get_quiz_id("pset3")

        except:
            self.assertRaises(NameError)

    def test_assignment_id(self):
        """test assignment id value"""
        self.assertEqual(get_assignment_id(), 437143)

        try:
            get_assignment_id("pset3")

        except:
            self.assertRaises(NameError)

    def test_excel_data(self):
        """test if excel data is right ordered or not"""
        self.assertEqual(get_excel_user_ids().index[0], '0d733444')
        self.assertEqual(get_excel_user_ids().index[1], '19fd3c63')

    def test_get_question(self):
        """test if questions are supplied or not"""
        self.assertEqual(get_questions()[0].id, 2494554)

    def test_get_answers(self):
        """test if answer out is generated or not"""
        self.assertEqual(get_answers(get_questions())[0]['id'], 2494554)


class MainFileTests(TestCase):
    """tests to validate main file functions"""

    def test_user_id_main(self):
        try:
            main(user_id_func=True, atomic_write_func=False, parquet_func=False, canvas_func=False)
        except:
            self.assertRaises(Exception)

    def test_atomic_write_main(self):
        try:
            main(user_id_func=False, atomic_write_func=True, parquet_func=False, canvas_func=False)
            os.remove("data/hashed.parquet")
        except:
            self.assertRaises(Exception)

    def test_parquet_main(self):
        try:
            main(user_id_func=False, atomic_write_func=False, parquet_func=True, canvas_func=False)
        except:
            self.assertRaises(Exception)

    def test_canvas_main(self):
        try:
            main(user_id_func=False, atomic_write_func=False, parquet_func=False, canvas_func=True)
        except:
            self.assertRaises(Exception)




