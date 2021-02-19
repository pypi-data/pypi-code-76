from typing import Callable, Optional

from drafting.sh import sh
from drafting.geometry import Geometrical, Rect
from drafting.pens.draftingpen import DraftingPen


class DraftingPens(DraftingPen):
    def __init__(self, pens=None):
        self.pens = []
        super().__init__()

        self.single_pen_class = DraftingPen
        self._in_progress_pen = None

        self.subs = {
            "□": "ctx.bounds()",
            "■": "_dps.bounds()"
        }

        if pens:
            for p in pens:
                self.append(p)
    
    def tree(self, out=None, depth=0) -> str:
        """Hierarchical string representation"""
        if out is None:
            out = []
        out.append(" |"*depth + " " + str(self))
        for pen in self.pens:
            if hasattr(pen, "pens"):
                pen.tree(out=out, depth=depth+1)
            else:
                out.append(" |"*(depth+1) + " " + str(pen))
        return "\n".join(out)
    
    def __repr__(self):
        return f"<{type(self).__name__}:{len(self.pens)}>"
    
    def __len__(self):
        return len(self.pens)
    
    def __getitem__(self, index):
        return self.pens[index]
        
    def __setitem__(self, index, pen):
        self.pens[index] = pen
    
    def __iadd__(self, item):
        return self.append(item)
    
    def __add__(self, item):
        return self.append(item)
    
    def append(self, pen):
        if isinstance(pen, Geometrical):
            return self.pens.append(self.single_pen_class(pen))
        elif isinstance(pen, DraftingPen):
            self.pens.append(pen)
        else:
            try:
                for p in pen:
                    if p:
                        self.pens.append(p)
            except TypeError:
                self.pens.append(pen)
        return self
    
    def insert(self, index, pen):
        if pen:
            self.pens.insert(index, pen)
        return self
    
    def extend(self, pens):
        if hasattr(pens, "pens"):
            self.append(pens)
        else:
            for p in pens:
                if p:
                    if hasattr(p, "value"):
                        self.append(p)
                    else:
                        self.extend(p)
        return self
    
    def reversePens(self):
        """Reverse the order of the pens; useful for overlapping glyphs from the left-to-right rather than right-to-left (as is common in OpenType applications)"""
        self.pens = list(reversed(self.pens))
        return self
    
    # Sizing
    
    def ambit(self, th=False, tv=False):
        """Get the calculated rect boundary of the DraftingPens;
        `th` means `(t)rue (h)orizontal`;
        `ty` means `(t)rue (v)ertical`;
        passing either ignores a non-bounds-derived frame
        in either dimension"""
        if self._frame and (th == False and tv == False):
            return self._frame
        else:
            try:
                union = self.pens[0].ambit(th=th, tv=tv)
                for p in self.pens[1:]:
                    union = union.union(p.ambit(th=th, tv=tv))
                return union
            except Exception as e:
                return Rect(0,0,0,0)
    
    def bounds(self):
        """Calculated bounds of a DATPens"""
        return self.ambit(th=1, tv=1)
    
    def gs(self, s, fn=None, tag=None):
        return self.append(
            self.single_pen_class().gs(sh(s, ctx=self, dps=type(self)()), tag=tag, fn=fn))
    
    def gss(self, s):
        dps = type(self)()
        xs = sh(s, ctx=self, dps=dps)
        return self.extend(dps.pens)
    
    # RecordingPen contract

    def moveTo(self, p0):
        self._in_progress_pen = self.single_pen_class()
        self._in_progress_pen.moveTo(p0)
        return self
    
    def lineTo(self, p1):
        self._in_progress_pen.lineTo(p1)
        return self
    
    def qCurveTo(self, *points):
        self._in_progress_pen.qCurveTo(*points)
        return self
    
    def curveTo(self, *points):
        self._in_progress_pen.curveTo(*points)
        return self
    
    def closePath(self):
        self._in_progress_pen.closePath()
        self.append(self._in_progress_pen)
        self._in_progress_pen = None
        return self
    
    def endPath(self):
        self._in_progress_pen.endPath()
        self.append(self._in_progress_pen)
        self._in_progress_pen = None
        return self
    
    def replay(self, pen):
        self.pen().replay(pen)
    
    # Drawing
    
    def pen(self):
        """A flat representation of this set as a single pen"""
        dp = self.single_pen_class()
        fps = self.collapse()
        for p in fps.pens:
            dp.record(p)
        if len(fps.pens) > 0:
            for k, attrs in fps.pens[0].attrs.items():
                dp.attr(tag=k, **attrs)
        dp.frame(self.frame())
        return dp
    
    def collapse(self, levels=100, onself=False):
        """AKA `flatten` in some programming contexts, though
        `flatten` is a totally different function here that flattens
        outlines; this function flattens nested collections into
        one-dimensional collections"""
        pens = []
        for idx, p in enumerate(self.pens):
            if hasattr(p, "pens") and levels > 0:
                pens.extend(p.collapse(levels=levels-1).pens)
            else:
                pens.append(p)
        dps = type(self)(pens)
        if onself:
            self.pens = dps.pens
            return self
        else:
            return dps
        
    def copy(self, with_data=False):
        """Get a completely new copy of this whole set of pens,
        usually done so you can duplicate and further modify a
        DATPens without mutating the original"""
        dps = type(self)()
        for p in self.pens:
            dps.append(p.copy(with_data=with_data))
        return dps
    
    def remove_blanks(self):
        """Remove blank pens"""
        nonblank_pens = []
        for pen in self.pens:
            if hasattr(pen, "pens"):
                pen.remove_blanks()
                nonblank_pens.append(pen)
            elif len(pen.value) > 0:
                nonblank_pens.append(pen)
            #rb = pen.remove_blanks()
            #print("RB RES", rb, bool(rb))
            #if not rb:
            #    nonblank_pens.append(pen)
        self.pens = nonblank_pens
        return self
    
    def remove_overlap(self):
        for p in self.pens:
            p.removeOverlap()
        return self
    
    removeOverlap = remove_overlap
    
    def transform(self, transform, transformFrame=True):
        for p in self.pens:
            p.transform(transform, transformFrame=transformFrame)
        if transformFrame and self._frame:
            self._frame = self._frame.transform(transform)
        return self
    
    def attr(self, key="default", field=None, **kwargs):
        if field: # getting, not setting, kind of weird to return the first value?
            if len(self.pens) > 0:
                return self.pens[0].attr(key=key, field=field)
            else:
                return None
        for p in self.pens:
            p.attr(key, **kwargs)
        return self
    
    def lattr(self, tag, fn: Callable[[DraftingPen], Optional[DraftingPen]]):
        for p in self.pens:
            p.lattr(tag, fn)
        return self
    
    def round_to(self, rounding):
        """Round all values for all pens in this set to nearest multiple of rounding value (rather than places, as in `round`)"""
        for p in self.pens:
            p.round_to(rounding)
        return self