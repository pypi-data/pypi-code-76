from pyqalx import Bot

from qalx_orcaflex.bots.sim.functions import (
    process_orcaflex,
    preprocess_orcaflex,
    begin_orcaflex,
    initialise_orcaflex_bot,
    post_process_orcaflex,
)


class SimBot(Bot):
    """Simulation bot

    This bot will take the source, options and settings provided in data_models.OrcaFlexJob and will run the simulation
    and perform all the requested post-processing.

    Four step functions are pre-defined in `bots.sim.fuctions`:
        initialisation_function
        begin_function
        preprocess_function
        process_function

    """

    def __init__(self, bot_name):
        super(SimBot, self).__init__(bot_name)

        self.process_function = process_orcaflex
        self.preprocess_function = preprocess_orcaflex
        self.begin_function = begin_orcaflex
        self.initialisation_function = initialise_orcaflex_bot
        self.postprocess_function = post_process_orcaflex
