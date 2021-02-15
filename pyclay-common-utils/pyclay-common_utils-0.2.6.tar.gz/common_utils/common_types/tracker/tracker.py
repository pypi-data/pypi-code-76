class MinMaxTracker:
    def __init__(self):
        self.val_min = None
        self.val_max = None

    def process(self, val):
        if self.val_min is None or val < self.val_min:
            self.val_min = val
        if self.val_max is None or val > self.val_max:
            self.val_max = val

    def get_result(self):
        return self.val_min, self.val_max

class Point2DMinMaxTracker:
    def __init__(self):
        self.x = MinMaxTracker()
        self.y = MinMaxTracker()

    def process(self, point: list):
        self.x.process(point[0])
        self.y.process(point[1])

    def get_result(self):
        xmin, xmax = self.x.get_result()
        ymin, ymax = self.y.get_result()
        return [xmin, ymin, xmax, ymax]

class Point3DMinMaxTracker:
    def __init__(self):
        self.x = MinMaxTracker()
        self.y = MinMaxTracker()
        self.z = MinMaxTracker()

    def process(self, point: list):
        self.x.process(point[0])
        self.y.process(point[1])
        self.z.process(point[2])

    def get_result(self):
        xmin, xmax = self.x.get_result()
        ymin, ymax = self.y.get_result()
        zmin, zmax = self.z.get_result()
        return [xmin, ymin, zmin, xmax, ymax, zmax]