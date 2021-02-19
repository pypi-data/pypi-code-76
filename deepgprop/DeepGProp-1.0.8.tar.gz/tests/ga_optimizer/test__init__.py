"""Test the :mod:`dgp.ga_optimizer.__init__` module."""
import unittest

from dgp import ga_optimizer
from dgp.utils import read_proben1_partition


class TestGeneticAlgorithm(unittest.TestCase):
    """Test the genetic_algorithm."""

    def test_genetic_algorithm(self):
        """Run the genetic algorithm a few times and check if it works."""
        first_weights, best_weights = ga_optimizer.genetic_algorithm(
            self.dataset,
            5,
            10,
            (6, 6),
            (1, 3),
            0.5,
            0.2,
            0.75,
            0.3,
            0.3,
            False,
            123112432,
        )
        first_score = ga_optimizer.utils.test_individual(
            first_weights, self.dataset
        )
        best_score = ga_optimizer.utils.test_individual(
            best_weights, self.dataset
        )
        self.assertLess(best_score[0], first_score[0])
        self.assertGreater(best_score[2], first_score[2])

    def setUp(self):
        """Setup the model to run the algorithm."""
        self.dataset = read_proben1_partition("cancer1")


if __name__ == "__main__":
    unittest.main()
