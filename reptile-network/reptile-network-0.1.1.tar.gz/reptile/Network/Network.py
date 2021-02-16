from ..Core.Core import core
from ..Constructor.Constructor import Constructor


class Network(Constructor):
    def feed(self, data):
        if self.count_layers < 2:
            raise Exception('No enough layers present')
        
        input_data = core.array(data)
        return self.input_layer.feed(input_data)

    def fit(
        self,
        data,
        labels,
        batch_size: int = 1,
        learning_const: float = 0.1,
        epochs: int = 1,
        console = True,
        print_error = False
    ):
        set_length = len(labels)
        data_arr = core.array(data)
        labels_arr = core.array(labels)

        for epoch_index in core.arange(epochs):
            if (console):
                print(f'Epoch #{epoch_index + 1}')

            for input_data, labels_data in self.get_random_batches(data_arr, labels_arr, set_length, batch_size):
                net_output = self.feed(input_data)
                net_error = net_output - labels_data

                if print_error:
                    cost_func_value = core.sum((net_error**2), axis=1)
                    average_cost_func_value = core.mean(cost_func_value)
                    print(average_cost_func_value)

                self.output_layer.fit(net_error, learning_const)

    # Генератор рандомных батчей из обучающей выборки
    def get_random_batches(self, dataset: core.ndarray, labels: core.ndarray, set_lenght: int, batch_size: int):
        count_batches = set_lenght // batch_size
        indicies = core.arange(set_lenght)
        core.random.shuffle(indicies)
        batched_indicies = core.array_split(indicies, count_batches)

        for batch_indicies in batched_indicies:
            batched_dataset = dataset[batch_indicies]
            batched_labels = labels[batch_indicies]
            yield batched_dataset, batched_labels
