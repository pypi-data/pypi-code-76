from ..Core.Core import core


class FunctionConstructor:
    # Значение активационных функций
    value: core.ndarray = None
    x: core.ndarray = None

    def get_values(self):
        return self.value


class SigmoidActFunction(FunctionConstructor):
    ''' Сигмоида '''

    def act_func(self, x: core.ndarray):
        y = 1 / (1 + core.exp(-x))
        self.value = y
        self.x = x
        return self.value

    def act_func_der(self, x: core.ndarray = None):
        # Проверяем если пришла не та же координата,
        # то считаем значение функции заново
        if (x is None or (x == self.x).all()):
            y = self.value
        else:
            y = self.act_func(x)
            self.value = y

        return y * (1 - y)


functions = {
    'sigmoid': SigmoidActFunction
}


def get_act(func_type: str):
    return functions[func_type]()
