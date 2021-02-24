"""Test module for cyclotron"""

from compphys import cyclotron


class TestCyclotron:

    def test_solve(self):
        alpha = 1 / 10
        t_final = 20 / alpha
        res = cyclotron.solve(t_final=t_final, t_interval=0.1, much_less_than=alpha)
        assert isinstance(res, cyclotron.Result)
