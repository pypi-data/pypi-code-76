from .mutation import mutate_param_state
from .random_helpers import set_seed


class TestMutateParamState:

    def demo_state(self):
        return {
            "foo": 10,
            "bar": 100,
        }

    def demo_conf(self):
        return {
            "foo": {
                "type": "number",
                "min": 3,
                "max": 8,
                "step": 1,
            }
        }

    def test_with_simple_config(self):
        out_state = set_seed(1)(mutate_param_state)(self.demo_state(), self.demo_conf())
        assert out_state['foo'] == 9

    def test_moves_by_step(self):
        input_state = self.demo_state()
        out_state = set_seed(1)(mutate_param_state)(input_state, self.demo_conf())
        assert out_state['foo'] == input_state['foo'] - 1
