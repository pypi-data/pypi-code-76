#!/usr/bin/env python
import os
import unittest
from pathlib import Path
from typing import List

from ltpylib import strings


class TestStrings(unittest.TestCase):

  def test_to_snake_case(self):
    test_file = Path(os.path.dirname(os.path.realpath(__file__))).joinpath("test_to_snake_case.properties")
    with open(test_file, "r") as tf:
      lines: List[str] = tf.read().strip().splitlines()

    assert len(lines) > 0

    for line in lines:
      if not line:
        continue

      expected, val = line.split("=", 1)
      assert strings.to_snake_case(val) == expected


if __name__ == '__main__':
  unittest.main()
