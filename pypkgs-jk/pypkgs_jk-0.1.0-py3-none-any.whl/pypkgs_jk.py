import altair as alt

def write_test_altair(chart_name, chart):
    """
    Writes a skeleton test from an altair chart.

    Parameters
    ----------
    chart_name : str
      Name of the altair chart.
    chart : alt.vegalite.v4.api.Chart
      An altair chart that you wish to create skeleton test for.

    Returns
    -------
    str
      str that contains assert statements to test the altair chart.

    Examples
    --------
    >>> from pypkgs_jk import pypkgs_jk
    >>> import altair as alt
    >>> from vega_datasets import data
    >>> cars = data.cars()
    >>> fuel_efficiency = alt.Chart(cars).mark_area().encode(x='Year', y='mean(Miles_per_Gallon)').properties(title="Fuel efficiency over time")
    >>> pypkgs_jk.write_test_altair("fuel_efficiency", fuel_efficiency)
    "\n            assert fuel_efficiency is not None, 'Your answer does not exist. Have you passed in the correct variable?'\n            assert type(fuel_efficiency) == type(alt.Chart()), 'Your answer is not an altair Chart object. Check to make sure that you have assigned an alt.Chart object to fuel_efficiency.'\n            assert fuel_efficiency['mark'] == area, 'Make sure you are using the area mark type.\n            "
    """
    if type(chart) == alt.vegalite.v4.api.Chart:
        test_string = f"""
            assert {chart_name} is not None, 'Your answer does not exist. Have you passed in the correct variable?'
            assert type({chart_name}) == type(alt.Chart()), 'Your answer is not an altair Chart object. Check to make sure that you have assigned an alt.Chart object to {chart_name}.'
            assert {chart_name}['mark'] == {chart.mark}, 'Make sure you are using the {chart.mark} mark type.
            """
        return test_string