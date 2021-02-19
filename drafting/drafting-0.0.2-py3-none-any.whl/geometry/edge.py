from enum import Enum


class Edge(Enum):
    MaxY = 1
    MaxX = 2
    MinY = 3
    MinX = 4
    CenterY = 5
    CenterX = 6


def txt_to_edge(txt):
    if isinstance(txt, str):
        txt = txt.lower()
        if txt in ["maxy", "mxy", "n"]:
            return Edge.MaxY
        elif txt in ["maxx", "mxx", "e"]:
            return Edge.MaxX
        elif txt in ["miny", "mny", "s"]:
            return Edge.MinY
        elif txt in ["minx", "mnx", "w"]:
            return Edge.MinX
        elif txt in ["centery", "cy", "midy", "mdy"]:
            return Edge.CenterY
        elif txt in ["centerx", "cx", "midx", "mdx"]:
            return Edge.CenterX
        else:
            return None
    else:
        return txt