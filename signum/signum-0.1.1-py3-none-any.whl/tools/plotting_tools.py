from matplotlib.ticker import FuncFormatter

from signum.tools.scale_manager import ScaleManager


def adjust_axis_scale(ax, which: str, unit=None, label=None):
    if which not in ['x', 'y']:
        raise ValueError(f"'which' must be 'x' or 'y' (got '{which}')")

    if not unit and not label:
        return

    unit_rescaled = ''

    if unit:
        order = ScaleManager.adjust_scale(getattr(ax, f'get_{which}lim')())
        unit_rescaled, order = ScaleManager.rescale_unit(unit, order)
        unit_rescaled = f' [{unit_rescaled}]'
        scale = ScaleManager.scaling_factor_from_order(order)

        tick_formatter = FuncFormatter(lambda x, pos: f"{scale * x:g}")
        getattr(ax, f'{which}axis').set_major_formatter(tick_formatter)

    getattr(ax, f'set_{which}label')(f"{label or ''}{unit_rescaled}")


def adjust_plot_scale(ax, x_unit=None, x_label=None, y_unit=None, y_label=None):
    adjust_axis_scale(ax, 'x', x_unit, x_label)
    adjust_axis_scale(ax, 'y', y_unit, y_label)

