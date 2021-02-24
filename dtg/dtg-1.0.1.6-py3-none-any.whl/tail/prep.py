from dtg.tail.estimate.hill import HillEstimator
from dtg.tail.estimate.moment import MomentEstimator
from dtg.tail.estimate.pickands import PickandEstimator
from dtg.tail.estimate.ratio import RatioEstimator
from dtg.tail.mse import boot_estimate


def basic_tail(data):
    alp = boot_estimate(HillEstimator, data, 1 / 2, 2 / 3, 100, speed=False)[0]
    print("hill", 1 / alp)

    alp = boot_estimate(RatioEstimator, data, 1 / 2, 2 / 3, 100, speed=False)[0]
    print("ratio", 1 / alp)

    alp = boot_estimate(MomentEstimator, data, 1 / 2, 2 / 3, 100, speed=False)[0]
    print("moment", 1 / alp)

    alp = boot_estimate(PickandEstimator, data, 1 / 2, 2 / 3, 100, speed=False)[0]
    print("pickands", 1 / alp)
