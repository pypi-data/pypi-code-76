from ..Core.Core import core
from ..ActFunctions.ActFunctions import get_act


class EmptyLayer:
    # Количество нейронов
    size: int = None

    # Входные значения
    input_values: core.ndarray = None

    # Выходные значения
    output_values: core.ndarray = None

    # Ссылка на следующий слой
    next_layer = None

    # Ссылка на предыдущий слой
    prev_layer = None

    def __init__(self, size: int):
        self.size = size

    def __repr__(self):
        return \
            f'Size: {self.size}\n\
            \rInput values: \n{core.shape(self.input_values)}\n\
            \rOutput values: \n{core.shape(self.output_values)}\n'

    def tie_next_layer(self, next_layer):
        self.next_layer = next_layer

    def feed(self, data: core.ndarray):
        self.input_values = data
        next_layer = self.next_layer
        if not next_layer:
            self.output_values = data
            return data
        else:
            return next_layer.feed(data)
    
    def fit(self, *args, **kwargs):
        prev_layer = self.prev_layer
        if not prev_layer:
            return
        prev_layer.fit(*args, **kwargs)

    def save(self):
        return {
            'size': self.size
        }


class Layer(EmptyLayer):
    # Матрица весов
    weight_matrix: core.ndarray = None

    # Столбец баесов
    biases: core.ndarray = None

    # Тип активационной функции
    act_func_type: str = None

    # Функция активации
    act_func = None

    # Производная функции активации
    act_func_der = None

    # Геттер текущих значений нейронов
    get_values = None

    def __init__(
        self,
        size: int,
        act_func_type: str,
        *args,
        prev_layer = None,
        weight_matrix: core.ndarray = None,
        biases: core.ndarray = None,
        **kwargs
    ):
        super().__init__(size, *args, **kwargs)

        self.prev_layer = prev_layer
        prev_layer.tie_next_layer(self)

        Act = get_act(act_func_type)
        self.act_func_type = act_func_type
        self.act_func = Act.act_func
        self.act_func_der = Act.act_func_der
        self.get_values = Act.get_values

        if not (weight_matrix is None and biases is None):
            # Заполняем матрицы готовыми данными
            self.weight_matrix = core.array(weight_matrix)
            self.biases = core.array(biases)
        else:
            # Инициализируем рандомные матрицы весов и баесов
            self.reset()

    def __repr__(self):
        line = super().__repr__()

        if self.weight_matrix is not None:
            line += f'\rWeight matrix: \n{core.shape(self.weight_matrix)}\n'
        
        if self.biases is not None:
            line += f'\rBiases: \n{core.shape(self.biases)}\n'

        return line

    def reset(self):
        # Инициализируем рандомные матрицы весов и баесов
        self.weight_matrix = core.random.randn(self.prev_layer.size, self.size)
        self.biases = core.random.randn(self.size)

    def feed(self, data: core.ndarray):
        summ = core.dot(data, self.weight_matrix) + self.biases
        self.output_values = self.act_func(summ)
        return super().feed(self.output_values)

    def fit(self, cost_der: core.ndarray, learning_const: float):
        delta = cost_der * self.act_func_der()
        
        previous_layer_values = None
        prev_layer = self.prev_layer
        if not isinstance(prev_layer, EmptyLayer):
            previous_layer_values = prev_layer.get_values()
        else:
            previous_layer_values = prev_layer.input_values

        weight_grad = core.dot(previous_layer_values.T, delta)
        biases_grad = core.sum(delta, axis=0)

        prev_layer_const_der = core.dot(delta, self.weight_matrix.T)

        self.weight_matrix -= learning_const * weight_grad
        self.biases -= learning_const * biases_grad

        super().fit(prev_layer_const_der, learning_const)

    def save(self):
        return {
            **super().save(),
            'act_func_type': self.act_func_type,
            'weight_matrix': self.weight_matrix.tolist(),
            'biases': self.biases.tolist()
        }
