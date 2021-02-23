import unittest
from lilies import highlight
from lilies.objects.lilyblock import LilyBlock
from lilies.objects.lilystring import LilyString
from lilies.style import parse_style, Style


class TestHighlight(unittest.TestCase):
    def setUp(self):
        self.hello_world_flat = "Hello, world!"
        self.hello_world_block = LilyBlock("Hello, \nworld!")
        self.l_locations = [2, 3, 10]
        self.highlighted_style = parse_style("yellow")

    def test_highlights_flat_string(self):
        highlighted = highlight(self.hello_world_flat, "l")
        for i in range(len(highlighted)):
            char_style = highlighted.style_at(i)
            if i in self.l_locations:
                self.assertEqual(char_style, self.highlighted_style)
            else:
                self.assertEqual(char_style, Style())

    def test_highlighting_flat_string_returns_lilystring(self):
        highlighted = highlight(self.hello_world_flat, "l")
        self.assertEqual(type(highlighted), LilyString)

    def test_highlights_block(self):
        highlighted = highlight(self.hello_world_block, "l")
        char_counter = 0
        for row in highlighted:
            for i in range(len(row)):
                char_style = row.style_at(i)
                if char_counter in self.l_locations:
                    self.assertEqual(char_style, self.highlighted_style)
                else:
                    self.assertEqual(char_style, Style())
                char_counter += 1

    def test_highlighting_block_returns_block(self):
        highlighted = highlight(self.hello_world_block, "l")
        self.assertEqual(type(highlighted), LilyBlock)

    def test_highlighting_one_char(self):
        locations = self.l_locations[:1]
        highlighted = highlight(self.hello_world_flat, "l", num=1)
        for i in range(len(highlighted)):
            char_style = highlighted.style_at(i)
            if i in locations:
                self.assertEqual(char_style, self.highlighted_style)
            else:
                self.assertEqual(char_style, Style())

    def test_highlighting_two_chars(self):
        locations = self.l_locations[:2]
        highlighted = highlight(self.hello_world_flat, "l", num=2)
        for i in range(len(highlighted)):
            char_style = highlighted.style_at(i)
            if i in locations:
                self.assertEqual(char_style, self.highlighted_style)
            else:
                self.assertEqual(char_style, Style())
