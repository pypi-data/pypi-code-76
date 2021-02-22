from dataclasses import dataclass
from pollination_dsl.function import Inputs, Outputs, Function, command


@dataclass
class ModelToOsm(Function):
    """Translate a Model JSON file into an OpenStudio Model and corresponding IDF."""

    model = Inputs.file(
        description='Honeybee model in JSON format.', path='model.json',
        extensions=['hbjson', 'json']
    )

    sim_par = Inputs.file(
        description='SimulationParameter JSON that describes the settings for the '
        'simulation.', path='sim-par.json', extensions=['json']
    )

    @command
    def model_to_osm(self):
        return 'honeybee-energy translate model-to-osm model.json ' \
            '--sim-par-json sim-par.json --folder output ' \
            '--log-file output/output_paths.json'

    osm = Outputs.file(
        description='The OpenStudio model file.', path='output/run/in.osm'
    )

    idf = Outputs.file(
        description='The IDF file.', path='output/run/in.idf'
    )
