import mxdevtool.shock as mx_s


class Output:
    def __init__(self, name, shock_scen_args):
        self.name = name
        self.shock_scen_args = shock_scen_args
        
        # self.func = func

    def func(self, shocked_scen_data_d: dict(), calc_kwargs, npv_func):
        return 0.0


class Npv(Output):
    def __init__(self, scen: str, currency=None):
        super().__init__(Npv.__name__.lower(), [scen])


class Delta(Output):
    def __init__(self, up: str=None, down: str=None, h=1.0):
        """ 
        center method : ( s_up - s_down ) / (2h)

        Args:
            up (str, optional): shock name for up. Defaults to None.
            down (str, optional): shock name for down. Defaults to None.
            h (float, optional): interval. Defaults to 1.0.

        Raises:
            Exception: [description]
        """        
        super().__init__(Delta.__name__.lower(), [up, down])

        if up is None and down is None:
            raise Exception('up or down is required')

        self.up = up
        self.down = down
        self.h = h


    def func(self, shocked_scen_data_d: dict(), calc_kwargs, npv_func):
        #if self.up is None: -> 처리?
        #if self.down is None: -> 처리?

        upshock_scen = shocked_scen_data_d[self.up]
        downshock_scen = shocked_scen_data_d[self.down]

        v = npv_func(upshock_scen, calc_kwargs) - npv_func(downshock_scen, calc_kwargs)
        v = v / ( 2 * self.h )

        return v


class Gamma(Output):
    def __init__(self, up, down, h=1.0):
        super().__init__(Gamma.__name__.lower(), [up, down])

        if up is None and down is None:
            raise Exception('up or down is required')

        self.up = up
        self.down = down


class CashFlow(Output):
    def __init__(self, scen: str, currency=None, discount=None):
        super().__init__(Gamma.__name__.lower(), [scen])