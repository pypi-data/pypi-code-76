"""CLI utilities"""

import os
import click
from matatika.exceptions import NoDefaultContextSetError, VariableNotSetError
from matatika.context import MatatikaContext
from matatika.library import MatatikaClient


def create_table(*cols, separator="\t", max_cell_size=64):
    """Creates a string table for an arbitrary amount of columns"""

    for col in cols:

        # cast all elements in col to str
        for i, element in enumerate(col):
            col[i] = str(element)

        # find the largest cell, then constrain and update largest cell if necessary
        largest_cell = max(col, key=len)

        if len(largest_cell) > max_cell_size:
            truncated_val = largest_cell[:max_cell_size - 1] + "\u2026"
            col[col.index(largest_cell)] = truncated_val
            largest_cell = truncated_val

        # right-pad all column cells to thd size of the largest cell
        for i, cell in enumerate(col):
            if len(cell) > max_cell_size:
                cell = cell[:max_cell_size - 1] + "\u2026"
            col[i] = cell.ljust(len(largest_cell))

    rows = []

    # construct each row
    for i, _ in enumerate(cols[0]):
        rows.append(separator.join([col[i] for col in cols]))

    return "\n".join(rows)


class Resolver():
    """Resolves values from from click commands and the context file"""

    def __init__(self, ctx):

        self.ctx = ctx

    def auth_token(self) -> str:
        """Returns a value for auth_token"""

        return self._resolve('auth_token')

    def endpoint_url(self) -> str:
        """Returns a value for endpoint_url"""

        return self._resolve('endpoint_url')

    def workspace_id(self) -> str:
        """Returns a value for workspace_id"""

        return self._resolve('workspace_id')

    def client(self,
               auth_token=auth_token,
               endpoint_url=endpoint_url,
               workspace_id=workspace_id) -> MatatikaClient:
        """Returns a MatatikaClient object populated with resolved values"""

        variables = [auth_token, endpoint_url, workspace_id]

        if self.ctx.obj['trace']:

            names = ["VARIABLE NAME",
                     "AUTH TOKEN",
                     "ENDPOINT URL",
                     "WORKSPACE ID"]
            values = ["VALUE"]
            sources = ["SOURCE"]

            for var in variables:
                values.append(var(self)[0] if var else None)
                sources.append(var(self)[1] if var else "N/A")

            table = create_table(names, values, sources)

            click.echo("Creating a client with the following variables...\n")
            click.echo(table + "\n")

        auth_token_value, endpoint_url_value, workspace_id_value = [
            var(self)[0] if var else None for var in variables]

        return MatatikaClient(auth_token_value, endpoint_url_value, workspace_id_value)

    def _resolve(self, var: str) -> tuple:
        """
        Resolves the value for a given variable from click commands,
         environment and the context file
        """

        click_var = self.ctx.obj.get(var)

        if click_var:
            return click_var, 'command'

        env_var = os.getenv(var.upper())

        if env_var:
            return env_var, 'env'

        context_var = None
        try:
            _default_context_name, default_context_vars = MatatikaContext().get_default_context()
            context_var = default_context_vars.get(var)

        except NoDefaultContextSetError:
            pass

        if context_var:
            return context_var, 'context'

        raise VariableNotSetError(var)
