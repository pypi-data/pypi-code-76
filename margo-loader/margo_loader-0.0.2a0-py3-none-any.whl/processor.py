"""Process a notebook with margo preamble"""
from margo_parser.api import (
    MargoBlock,
    MargoMarkdownCellPreambleBlock,
    MargoPythonCellPreambleBlock,
    MargoStatementTypes,
)
import json
import re
import sys
import types


def remove_magics(source: str) -> str:
    """Remove magics from source for execution outside of Jupyter"""

    ret = ""
    for line in source.splitlines():
        if line.strip().startswith("%"):
            continue
        ret += line + "\n"
    return ret


def get_views(cell_preamble: MargoBlock):
    """Get the submodules this cell belongs to"""
    ret = []
    for statement in cell_preamble.statements:
        if statement.type != MargoStatementTypes.DECLARATION:
            continue
        if statement.name != "submodule":
            continue
        ret = ret + statement.value

    return ret


def preamble_contains_ignore_cell(cell_preamble: MargoBlock):
    """Determine if a cell contains ignore-cell margo directive"""

    for statement in cell_preamble.statements:
        if (
            statement.type == MargoStatementTypes.DIRECTIVE
            and statement.name == "ignore-cell"
        ):
            return True
    return False


class Processor:
    def __init__(self, module, name):
        self.module = module
        self.name = name

    def process_cells(self, cells):
        """Parse preambles and execute code cells of a notebook accordingly
        Currently supports:
        # :: ignore-cell :: to skip this cell
        # :: submodule: 'submodule_name' :: to create a virtual submodule in
        which this cell's code will be executed and can later be imported with
        from notebook.submodule_name import stuff_you_defined

        If first cell is markdown, it will be used as the module's docstring
        """
        idx = -1
        for cell in cells:
            idx += 1
            # If the first cell is a markdown cell, use it
            # as the module docstring
            if idx == 0 and cell.cell_type == "markdown":
                self.module.__doc__ = cell.source

            # cell_preamble = get_preamble_block(cell.source, cell_type=cell.cell_type)
            if cell.cell_type == "markdown":
                cell_preamble = MargoMarkdownCellPreambleBlock(cell.source)
            else:
                cell_preamble = MargoPythonCellPreambleBlock(cell.source)
            cell_source = remove_magics(cell.source)

            # ignore-cell support
            if preamble_contains_ignore_cell(cell_preamble):
                continue

            # view: module.view_name support ::
            views = get_views(cell_preamble)
            for view in views:
                full_view_name = self.name + "." + view

                if full_view_name in sys.modules:
                    mod = sys.modules[full_view_name]

                else:
                    mod = types.ModuleType(full_view_name)
                    sys.modules[full_view_name] = mod
                # Execute the code code within the given view name
                exec(cell_source, mod.__dict__)
                # TODO - This version does not do it, but I should
                # probably execute every cell in a view. Cells
                # without a view specified should run in a default
                # view, and then that view should be assigned to the main
                # module at the end
                self.module.__dict__[view] = mod

            if cell.cell_type == "code":
                exec(cell_source, self.module.__dict__)
