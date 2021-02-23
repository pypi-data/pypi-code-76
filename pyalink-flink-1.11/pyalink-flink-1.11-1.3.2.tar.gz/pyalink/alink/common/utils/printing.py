import pandas as pd

from .packages import in_ipython


def print_with_title(d, title: str = None):
    if title is not None:
        print(title)
    if in_ipython() and isinstance(d, pd.DataFrame):
        from IPython import display
        display.display(d)
    else:
        print(d)
