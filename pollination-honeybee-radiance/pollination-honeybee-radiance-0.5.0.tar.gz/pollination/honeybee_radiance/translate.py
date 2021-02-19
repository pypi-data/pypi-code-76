from dataclasses import dataclass
from pollination_dsl.function import Function, command, Inputs, Outputs


@dataclass
class CreateRadianceFolder(Function):
    """Create a Radiance folder from a HBJSON input file."""

    input_model = Inputs.file(
        description='Path to input HBJSON file.',
        path='model.hbjson'
    )

    sensor_grid = Inputs.str(
        description='A pattern to filter grids to be exported to radiance folder. By '
        'default all the grids will be exported.', default='*'
    )

    @command
    def hbjson_to_rad_folder(self):
        return 'honeybee-radiance translate model-to-rad-folder model.hbjson ' \
            '--grid "{{self.sensor_grid}}"'

    model_folder = Outputs.folder(description='Radiance folder.', path='model')

    sensor_grids = Outputs.list(
        description='Sensor grids information.', path='model/grid/_info.json'
    )

    sensor_grids_file = Outputs.file(
        description='Sensor grids information JSON file.', path='model/grid/_info.json'
    )
