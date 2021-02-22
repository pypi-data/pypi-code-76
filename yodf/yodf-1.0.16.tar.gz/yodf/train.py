import numpy as np


class GradientDescentOptimizer:
    # Minimize supports only the operations listed below
    # if Tensor passed to it is not a literal
    MINIMZE_SUPPORTED_OPERATIONS = {
        'reduce_mean',
        'reduce_sum',
    }

    def __init__(self, learning_rate):
        self.learning_rate = learning_rate
        self.cost = None

    def minimize(self, cost):
        if len(cost.shape) == 0 or cost.operation in GradientDescentOptimizer.MINIMZE_SUPPORTED_OPERATIONS:
            self.cost = cost
        else:
            error = f"Neither Tensor value is a literal nor is the operation " + \
                f"one from {GradientDescentOptimizer.SUPPORTED_OPERATIONS_MINIMZE}."
            raise ValueError(error)
        return self

    # Variable (basically a Tensor) can either be a literal
    # or 2 dimensional numpy array. This function handles
    # latter type of variables
    def __execute_variable_matrix(self, v, feed_dict=None):
        from .core import get_session
        s = get_session()

        gradient = np.zeros(v.shape)
        for i in range(v.shape[0]):
            for j in range(v.shape[1]):
                v.gradient.fill(0)
                v.gradient[i][j] = 1
                s.run(self.cost, feed_dict)
                gradient[i][j] = self.cost.gradient
        return gradient

    def execute(self, feed_dict=None):
        from .core import get_session
        s = get_session()

        vars = s.get_variables(self.cost)
        gradients = []
        for i in range(len(vars)):
            vars[i].set_gradient(1)
            for j in range(len(vars)):
                if i != j:
                    vars[j].set_gradient(0)
            if len(vars[i].shape) > 0:
                gradients.append(
                    self.__execute_variable_matrix(vars[i], feed_dict))
            else:
                s.run(self.cost, feed_dict)
                gradients.append(self.cost.gradient)

        # Restoring gradients of variables to 1
        for i in range(len(vars)):
            vars[i].set_gradient(1)

        # Need to update all variables only after all the gradients have been computed.
        # Updating a variable immediately after its gradient is computed would result
        # in subsqeunt gradients being wrongly computed
        for i in range(len(gradients)):
            vars[i].value = vars[i].value-self.learning_rate*gradients[i]
