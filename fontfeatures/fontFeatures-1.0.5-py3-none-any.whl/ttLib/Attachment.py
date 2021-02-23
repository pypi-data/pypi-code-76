from glyphtools import categorize_glyph


def lookup_type(self):
    if not self.has_context:
        if self.is_cursive:
            return 3
        if self.font and categorize_glyph(self.font,base[0][0])[0] == "mark":
            return 6
        return 4
    return 8
