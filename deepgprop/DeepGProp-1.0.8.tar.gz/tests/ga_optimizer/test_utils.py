"""Test the :mod:`dgp.ga_optimizer.utils` module."""
import unittest

from unittest import mock

from dgp.ga_optimizer.utils import (
    apply_crossover,
    apply_mutation,
    evaluate_population,
)


class TestUtils(unittest.TestCase):
    """Test the util functions."""

    def test_evaluate_population(self):
        """Test the population evaluator."""
        mock_fitness = 1
        mock_evaulate_fn = lambda x: mock_fitness
        mock_ind_1 = mock.Mock()
        mock_ind_2 = mock.Mock()
        mock_population = [mock_ind_1, mock_ind_2]

        evaluate_population(mock_population, mock_evaulate_fn)

        self.assertEqual(mock_ind_1.fitness.values, mock_fitness)
        self.assertEqual(mock_ind_2.fitness.values, mock_fitness)

    def test_apply_crossover(self):
        """Test the crossover applyer."""
        mock_ind_1 = mock.Mock()
        mock_ind_1.fitness.values = (1.0,)
        mock_ind_1.can_mate.return_value = True
        mock_ind_2 = mock.Mock()
        mock_ind_2.fitness.values = (1.0,)
        mock_ind_3 = mock.Mock()
        mock_ind_3.fitness.values = (1.0,)
        mock_crossover_fn = mock.Mock()
        mock_crossover_fn.return_value = ((2, 4), 2)

        crossed_individuals = apply_crossover(
            [mock_ind_1, mock_ind_2, mock_ind_3], 1.0, mock_crossover_fn
        )

        # There is going to be only 1 crossover
        self.assertEqual(crossed_individuals, 1)

        mock_crossover_fn.assert_called_with(mock_ind_1, mock_ind_2)

        # Ensure individuals 1 and 2 has no fitness defined
        with self.assertRaises(AttributeError):
            mock_ind_1.fitness.values

        with self.assertRaises(AttributeError):
            mock_ind_2.fitness.values

        # As it was not used, will not have the fitness deleted
        self.assertEqual(mock_ind_3.fitness.values, (1.0,))

    @mock.patch("dgp.ga_optimizer.utils.random")
    def test_apply_mutation(self, mock_random):
        """Test the mutation applyer."""
        mock_ind_1 = mock.Mock(constant_hidden_layers=False)
        mock_ind_1.fitness.values = (1.0,)
        mock_ind_2 = mock.Mock(constant_hidden_layers=False)
        mock_ind_2.fitness.values = (1.0,)
        mock_ind_3 = mock.Mock(constant_hidden_layers=True)
        mock_ind_3.fitness.values = (1.0,)
        mock_toolbox = mock.Mock()
        mock_mut_neurons_prob = 0.5
        mock_mut_layers_prob = 0.5

        # Only first individual's neurons and layers will be muted
        mock_random.random.side_effect = (
            0.8,  # First individual
            0.8,  # First individual
            0.1,  # Second individual
            0.1,  # Second individual
        )

        muted_individuals = apply_mutation(
            [mock_ind_1, mock_ind_2, mock_ind_3],
            mock_toolbox,
            mock_mut_neurons_prob,
            mock_mut_layers_prob,
        )

        # All three muted their weights and bias
        self.assertEqual(mock_toolbox.mutate_bias.call_count, 3)
        self.assertEqual(mock_toolbox.mutate_weights.call_count, 3)

        # Only the second individual muted the neurons and layers, as:
        # random < prob
        #    0.1 < 0.5
        mock_toolbox.mutate_neuron.assert_called_with(mock_ind_2)
        mock_toolbox.mutate_layer.assert_called_with(mock_ind_2)
