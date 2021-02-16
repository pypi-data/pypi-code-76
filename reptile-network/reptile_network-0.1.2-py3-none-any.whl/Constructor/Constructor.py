from ..Layer.Layer import Layer, EmptyLayer
from json import loads, dumps
from ..constants import VERSION
from ..helpers import check_version


class Constructor:
    # Тип функции активации
    act_func_type: str = None

    # Входной слой
    input_layer: Layer = None

    # Выходной слой
    output_layer: Layer = None

    # Слои нейронки
    layers: list = None

    # Количество слоёв
    count_layers: int = 0

    def __init__(self, act_func_type='sigmoid'):
        self.act_func_type = act_func_type
        self.layers = []

    def __repr__(self):
        line = f'Input layer\n{repr(self.input_layer)}\n'
        
        for index, layer in enumerate(self.layers):
            line += f'Layer #{index}\n{repr(layer)}\n'

        return line

    def input(self, size: int):
        if len(self.layers):
            raise Exception('Unexpacted behaviour. Network does already have hidden layers.')

        self.input_layer = EmptyLayer(size)
        return self
        
    def layer(self, size: int, *args, **kwargs):
        layers = self.layers
        prev_layer = None

        if not self.input_layer:
            raise Exception('No input layer')

        if not len(self.layers):
            prev_layer = self.input_layer
        else:
            prev_layer = layers[-1]

        layer = Layer(
            size,
            *args,
            **({
                'prev_layer': prev_layer,
                'act_func_type': self.act_func_type,
                **kwargs,
            })
        )
        
        layers.append(layer)
        self.output_layer = layer
        self.count_layers += 1
        return self

    def reset(self):
        for layer in self.layers:
            layer.reset()

    def dumps(self, file_path: str = None):
        if not self.layer:
            raise Exception('No input layer')

        if len(self.layers) < 2:
            raise Exception('No enough layers present')

        layers_snapshot = [
            {
                'type': 'input_layer',
                'snapshot': self.input_layer.save()
            }
        ]

        for layer in self.layers:
            layers_snapshot.append({
                'type': 'layer',
                'snapshot': layer.save()
            })

        json = dumps({
            'version': VERSION,
            'params': {
                'act_func_type': self.act_func_type
            },
            'layers': layers_snapshot
        })

        if file_path:
            with open(file_path, 'w+') as file:
                file.write(json)
        else:
            return json

    def loads(self, json: str = None, file_path: str = None):
        cur_json = json

        if file_path:
            with open(file_path, 'r') as file:
                cur_json = file.read()
       
        if not cur_json:
            raise Exception('No json present')

        snapshot = loads(cur_json)
        
        version = snapshot['version']
        if not check_version(version):
            raise Exception('Invalid snapshot version')

        params = snapshot['params']
        self.act_func_type = params['act_func_type']

        for layer in snapshot['layers']:
            if layer['type'] == 'input_layer':
                self.input(**layer['snapshot'])
            elif layer['type'] == 'layer':
                self.layer(**{
                    'act_func_type': self.act_func_type,
                    **layer['snapshot']
                })
