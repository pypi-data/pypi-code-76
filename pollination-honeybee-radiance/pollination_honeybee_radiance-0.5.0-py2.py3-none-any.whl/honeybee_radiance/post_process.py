from dataclasses import dataclass
from pollination_dsl.function import Function, command, Inputs, Outputs


@dataclass
class ConvertToBinary(Function):
    """Convert a Radiance matrix to a new matrix with 0-1 values."""

    # inputs
    input_mtx = Inputs.file(
        description='Input Radiance matrix in ASCII format',
        path='input.mtx'
    )

    @command
    def convert_to_zero_one(self):
        return 'honeybee-radiance post-process convert-to-binary input.mtx ' \
            '--output binary.mtx'

    # outputs
    output_mtx = Outputs.file(
        description='Newly created binary matrix.', path='binary.mtx'
    )


@dataclass
class SumRow(Function):
    """Postprocess a Radiance matrix and add all the numbers in each row.

    This function is useful for translating Radiance results to outputs like radiation
    to total radiation. Input matrix must be in ASCII format. The header in the input
    file will be ignored.
    """

    # inputs
    input_mtx = Inputs.file(
        description='Input Radiance matrix in ASCII format',
        path='input.mtx'
    )

    @command
    def sum_mtx_row(self):
        return 'honeybee-radiance post-process sum-row input.mtx --output sum.mtx'

    # outputs
    output_mtx = Outputs.file(description='Newly created sum matrix.', path='sum.mtx')
