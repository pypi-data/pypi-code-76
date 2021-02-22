from pollination_dsl.alias import OutputAlias
from queenbee.io.common import IOAliasHandler


"""Daylight factor recipe output.

The results are separated by line and the numbers cannot be more than 100.
"""
parse_daylight_factor_results = [
    OutputAlias.any(
        name='daylight_factor',
        description='Daylight factor values.',
        platform=['grasshopper'],
        handler=[
            IOAliasHandler(
                language='python',
                module='pollination_handlers.outputs.daylight',
                function='read_df_from_folder'
            )
        ]
    )
]


"""Annual daylight recipe output.

Sort the .ill result files output by an annual daylight simulation.
"""
sort_annual_daylight_results = [
    OutputAlias.any(
        name='annual_daylight',
        description='Annual daylight result files.',
        platform=['grasshopper'],
        handler=[
            IOAliasHandler(
                language='python',
                module='pollination_handlers.outputs.daylight',
                function='sort_ill_from_folder'
            )
        ]
    )
]
