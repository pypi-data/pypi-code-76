# Copyright (c) 2020 SMHI, Swedish Meteorological and Hydrological Institute 
# License: MIT License (see LICENSE.txt or http://opensource.org/licenses/mit).
"""
Created on 2020-12-16 15:26

@author: johannes

"""
from sharkvalidator import App


if __name__ == '__main__':

    app = App()

    app.read(
        'C:/Temp/DV/validator_test/Hallands kustkontroll kvartal 2_2020.xlsx',
        reader='phyche_xlsx',
        delivery_name='hal_phyche',
    )

    # app.read(
    #     'C:/Temp/DV/validator_test/2020-11-25 1345-2020-LANDSKOD 77-FARTYGSKOD 10',
    #     reader='phyche_lims',
    #     delivery_name='lims',
    # )

    # app.read(
    #     'C:/Temp/DV/validator_test/PP_DEEP_Phytoplankton_data_2019_2020-05-07.xlsx',
    #     reader='phytop_xlsx',
    #     delivery_name='deep_phyto',
    # )

    # app.validate('hal_phyche', 'lims', 'deep_phyto')
    app.validate('hal_phyche', disapproved_only=True)
    # app.validate('him', disapproved_only=True)

    app.write(writer='log')
