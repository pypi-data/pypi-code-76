from math import ceil

MIN_XP_PER_MSG: int = 15
MAX_XP_PER_MSG: int = 25


class XPCalculator:
    xp_needed: float
    min_msgs: int
    avg_msgs: int
    max_msgs: int

    def __init__(self, *, desired_level: int = 0, current_xp: int = 0):
        if desired_level <= 0:
            raise ValueError('desired level should be bigger than 0')

        self.desired_level = desired_level
        self.current_xp = current_xp

        self.calculate()

	# f(xp) = (5/6 * level * (2*level*level+27*level+91)) - currentXP
    def calculate(self):
        self.xp_needed = (5 / 6 * self.desired_level * (
                2 * self.desired_level * self.desired_level + 27 * self.desired_level + 91)) - self.current_xp
        self.min_msgs = ceil(self.xp_needed / MAX_XP_PER_MSG)
        self.avg_msgs = ceil(self.xp_needed / ((MIN_XP_PER_MSG + MAX_XP_PER_MSG) / 2))
        self.max_msgs = ceil(self.xp_needed / MIN_XP_PER_MSG)

    def get_xp_needed(self):
        return ceil(self.xp_needed)

    def get_avg_msgs(self):
        return self.avg_msgs

    def get_min_msgs(self):
        return self.min_msgs

    def get_max_msgs(self):
        return self.max_msgs
