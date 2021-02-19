# pip install git+https://github.com/typemytype/drawbot

import drawBot as db

from drafting.geometry import Rect, Point
from drafting.color import Color, Gradient, hsl, rgb
from drafting.pens.draftingpens import DraftingPen, DraftingPens


def db_fill(color):
    if color:
        if isinstance(color, Gradient):
            db_gradient(color)
        elif isinstance(color, Color):
            db.fill(color.r, color.g, color.b, color.a)
    else:
        db.fill(None)

def db_stroke(weight=1, color=None, dash=None):
    db.strokeWidth(weight)
    if dash:
        db.lineDash(dash)
    if color:
        if isinstance(color, Gradient):
            pass # possible?
        elif isinstance(color, Color):
            db.stroke(color.r, color.g, color.b, color.a)
    else:
        db.stroke(None)

def db_shadow(clip=None, radius=10, alpha=0.3, color=Color.from_rgb(0,0,0,1)):
    if clip:
        bp = db.BezierPath()
        bp.rect(*clip)
        db.clipPath(bp)
    #elif self.rect:
    #    cp = DATPen(fill=None).rect(self.rect).xor(self.dat)
    #    bp = db.BezierPath()
    #    cp.replay(bp)
    #    db.clipPath(bp)
    db.shadow((0, 0), radius*3, list(color.with_alpha(alpha)))
    
def db_gradient(gradient):
    stops = gradient.stops
    db.linearGradient(stops[0][1], stops[1][1], [list(s[0]) for s in stops], [0, 1])


class DrawBotPen(DraftingPen):
    def bezierPath(self):
        bp = db.BezierPath()
        self.replay(bp)
        return bp

    def _draw(self):
        for dp in list(self.all_pens()):
            with db.savedState():
                db.fill(None)
                db.stroke(None)
                db.strokeWidth(0)
                for attr, value in dp.allStyledAttrs().items():
                    if attr == "fill":
                        db_fill(value)
                    elif attr == "stroke":
                        db_stroke(value.get("weight", 1), value.get("color"), None)
                    db.drawPath(dp.cast(DrawBotPen).bezierPath())
        return self
    
    def draw(self, rect=None, filters=[]):
        if rect and len(filters) > 0:
            im = db.ImageObject()
            with im:
                db.size(*rect.wh())
                self._draw()
            for filter_name, filter_kwargs in filters:
                getattr(im, filter_name)(**filter_kwargs)
            x, y = im.offset()
            db.image(im, (x, y))
        else:
            self._draw()
        return self

class DrawBotPens(DrawBotPen, DraftingPens):
    pass