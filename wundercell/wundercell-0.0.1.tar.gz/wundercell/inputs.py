from typing import List
from IPython.display import HTML, display
from ipywidgets import Output, Layout, HBox, Dropdown, Button, interactive
import IPython.display


def select_box(options: List[str], default_value: str = None, position: str = None):
    '''
    Decorator that appends a select box to the UI.

    Usage:
    @select_box(options, default_value, position)
    def tester(selected_option):
        return dataframe[selected_option]
    '''
    out = Output()
    dropdown = Dropdown(options=options, value=default_value)
    
    def inner(fcn):
        def wrapper(*args, **kwargs):
            result = fcn(dropdown.value)
            out.clear_output()
            with out:
                display(result)
            return HBox([dropdown, out]) if position == "left" else HBox([out, dropdown])

        dropdown.observe(wrapper, names='value')

        return wrapper

    return inner
