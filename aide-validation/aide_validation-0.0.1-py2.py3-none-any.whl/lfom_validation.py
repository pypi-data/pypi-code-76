"""Helper functions for validating LFOM.
Created on September 18, 2020

@author: jcs528@cornell.edu
"""

from aguaclara.core.units import u
import aguaclara.core.physchem as pc
import aguaclara.core.constants as con


def flow_lfom_vert(height, d_ori, h_ori, n_oris):
    """Returns the flow through the LFOM as a function of height

    Args:
        height: height of water in the LFOM (u.m)

        d_ori: diameter of each orifice (u.m)

        h_ori: height of each row of the LFOM (list)

        n_oris: number of orifices at each row of the LFOM (list of lists)

    Returns:
        flow: flow rate through the LFOM (u.L / u.s)
    """
    flow = pc.flow_orifice_vert(d_ori, height - h_ori, con.VC_ORIFICE_RATIO) * n_oris
    return (sum(flow)).to(u.L / u.s)


def check_flow_lfom_vert(
    diameter, ori_heights, ori_numbers, cutoff, q_input, report_writer
):
    """Evaluates the flow

    Args:
        diameter: diameter of each orifice (u.m)

        ori_heights: height of each row of the LFOM (list)

        ori_numbers: number of orifices at each row of the LFOM (list of lists)

        cutoff: allowable tolerance between design and expected flow as a percent

        q_input: design flow rate (u.L / u.s)

        report_writer: ReportWriter object to record validation results

    Returns:
        flow: flow rate through the LFOM (u.L / u.s)
    """
    try:
        q_calc = flow_lfom_vert(
            ori_heights[-1] + 0.5 * diameter, diameter, ori_heights, ori_numbers
        )
        assert cutoff > (q_calc - q_input) / q_input
        assert -cutoff < (q_calc - q_input) / q_input
        report_writer.write_message(
            "The expected flow rate, {!s}, was very close "
            "to the one calculated by this validation "
            "code, {!s}.\n".format(q_input, q_calc)
        )
    except AssertionError:
        report_writer.write_message(
            "INVALID: The expected flow rate, {!s}, is "
            "different from the one calculated by this "
            "validation code, {!s}.\n".format(q_input, q_calc)
        )
        report_writer.set_result("Invalid: Check Validation Report")
