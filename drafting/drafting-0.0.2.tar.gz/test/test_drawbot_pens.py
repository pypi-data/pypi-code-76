from drafting.pens.draftingpen import DraftingPen
import unittest
from drafting.geometry import Rect, Point
from drafting.pens.drawbotpen import DrawBotPen, DrawBotPens
from drafting.color import hsl

import drawBot as db


class TestDrawbotPens(unittest.TestCase):
    def test_test(self):
        db.newDrawing()
        db.newPage(300, 300)

        r = Rect(0, 0, 100, 100)
        ((ß:=DraftingPen())
            .define(r=r, c=75)
            .gs("$r↗ ↘|$c|$r↓ ↙|$c|$r↖")
            .align(Rect(300, 300))
            .scale(2)
            .f(hsl(0.8, a=0.1))
            .s(hsl(0.9))
            .sw(5)
            .cast(DrawBotPen)
            ._draw())

        db.saveImage("db_render.png")
        db.endDrawing()


if __name__ == "__main__":
    unittest.main()