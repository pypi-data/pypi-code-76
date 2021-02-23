from .run import run, run_iterator


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
        iteration_state = run(
            self.demo_state(),
            self.demo_conf(),
            self.demo_model(),
            self.demo_loss_function(),
            self.demo_data(),
            max_iterations=100,
            tolerance=0.005,
        )
        assert 100 > iteration_state.iterations > 10
        assert iteration_state.best_parameters == self.demo_best_params()

    def test_limited_by_max_iterations(self):
        iteration_state = run(
            self.demo_state(),
            self.demo_conf(),
            self.demo_model(),
            self.demo_loss_function(),
            self.demo_data(),
            max_iterations=10,
            verbose=True,
        )
        assert iteration_state.best_parameters != self.demo_best_params()
        assert iteration_state.iterations == 10

    def test_running_in_parallel(self):
        iteration_state = run(
            self.demo_state(),
            self.demo_conf(),
            self.demo_model(),
            self.demo_loss_function(),
            self.demo_data(),
            max_iterations=10,
            parallel=True,
            verbose=True,
        )
        assert iteration_state.best_parameters != self.demo_best_params()
        assert iteration_state.iterations == 10


class TestRunParallelIterator:

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
                "max": 80,
                "step": 8,
            }
        }

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
        def demo_model_b(params, data):
            return sum(data) * params['foo']

        model = run_iterator(
            self.demo_state(),
            self.demo_conf(),
            demo_model_b,
            self.demo_loss_function(),
            self.demo_data(),
            max_iterations=100,
            tolerance=0.005,
            verbose=True,
        )
        iterations_state = next(model)
        assert iterations_state.iterations == 1
        assert iterations_state.loss < 99999
