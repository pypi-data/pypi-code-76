"""Helper functions for validating LFOM.
Created on January 6, 2021

@author: fchapin@aguaclarareach.org
"""

import math
import aguaclara.core.physchem as pc
import aguaclara.core.constants as con


def check_baffle_spacing(channel_l, baffle_s, report_writer):
    """Evaluates whether 3 < H_e / S < 6 and writes the result to a report.
    (both H_e and S can be given by model geometry)

    Args:
        channel_l: length of channel (u.m)

        baffle_s: space (edge-to-edge) between two baffles (u.m)

        report_writer: ReportWriter object to record validation results

    Returns:
        none
    """
    try:
        assert 3 <= channel_l / baffle_s
        assert channel_l / baffle_s <= 6

        report_writer.write_message(
            "Ratio of channel length, {!s}, "
            "to baffle spacing, {!s} "
            "was within the acceptable range "
            "(between 3 and 6).\n".format(channel_l, baffle_s)
        )
    except AssertionError:
        report_writer.write_message(
            "INVALID: Ratio of channel length, {!s}, "
            "to baffle spacing, {!s} "
            "was not in the acceptable range "
            "(between 3 and 6).\n".format(channel_l, baffle_s)
        )
        report_writer.set_result("Invalid: Check Validation Report")


def check_G_theta(
    q,
    channel_l,
    design_water_height,
    channel_n,
    channel_w,
    hl,
    temp,
    report_writer,
    min_G_theta=30000,
):
    """Evaluates whether G theta > 30000 (no maximum) and writes the result to a report.

    Args:
        q: design flow rate (u.L / u.s)

        channel_l: length of one channel (u.m)

        design_water_height: intended height of water in the flocculator (u.m)

        baffle_s: space (edge-to-edge) between two baffles (u.m)

        channel_n: number of flocculator channels

        channel_w: width of one channel (u.m)

        hl: headloss throught the flocculator (u.m)

        temp: design temperature (u.degC)

        report_writer: ReportWriter object to record validation results

        min_G_theta: minimum allowable G theta. Default: 30000

    Returns:
        none
    """
    try:
        theta = (channel_l * design_water_height * channel_n * channel_w) / q
        G_theta = math.sqrt(
            con.GRAVITY * hl * theta / pc.viscosity_kinematic_water(temp)
        )
        assert G_theta > min_G_theta
        report_writer.write_message(
            "The G Theta, {!s}, was above the minimum "
            "value of {!s}.\n".format(G_theta, min_G_theta)
        )
    except AssertionError:
        report_writer.write_message(
            "INVALID: G Theta, {!s}, was below the minimum "
            "value of {!s}.\n".format(G_theta, min_G_theta)
        )
        report_writer.set_result("Invalid: Check Validation Report")
