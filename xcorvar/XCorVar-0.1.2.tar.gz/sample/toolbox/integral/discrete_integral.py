# coding: utf-8

class DiscInt:

    #public:

        def __init__ (self, curve, step):
            self.step = step
            self.curve = curve
            self.start = curve [0]
            self.end = curve [-1]

        def __call__  (self):
            return self.step * (0.5 * (self.start.y + self.end.y) + sum ([pt.y for pt in self.curve [1:-1]]))
