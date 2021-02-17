from .run import run


class TestRun:

    def demo_state(self):
        return {
            "foo": 10,
            "bar": 360,
        }

    def demo_conf(self):
        return {
            "foo": {
                "type": "number",
                "min": 3,
                "max": 8,
                "step": 8,
            }
        }

    def demo_model(self):
        def model(params, data):
            return sum(data) * params['foo']
        return model

    def demo_loss_function(self):
        def loss_function(output, params):
            return abs(params['bar'] - output)
        return loss_function

    def demo_data(self):
        return [1, 2, 3, 3]

    def demo_best_params(self):
        return {
            "foo": 40,
            "bar": 360,
        }

    def test_simple_run(self):
        best_parameters, iterations, loss_values = run(
            self.demo_state(),
            self.demo_conf(),
            self.demo_model(),
            self.demo_loss_function(),
            self.demo_data(),
            max_iterations=100,
        )
        assert 100 > iterations > 10
        assert best_parameters == self.demo_best_params()

    def test_limited_by_max_iterations(self):
        best_parameters, iterations, loss_values = run(
            self.demo_state(),
            self.demo_conf(),
            self.demo_model(),
            self.demo_loss_function(),
            self.demo_data(),
            max_iterations=10,
        )
        assert best_parameters != self.demo_best_params()
        assert iterations == 10
