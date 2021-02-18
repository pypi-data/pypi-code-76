from aguaclara.core.units import u
from aguaclara.core import physchem as pc
from aguaclara.core import constants as con
import numpy as np


def check_inlet_manifold(diam, pi_flow_manifold, vel_diffuser, q_input, report_writer):
    """Check that the inlet manifold's design flow rate is less than the one
    calculated according to the model's geometry.

    Args:
        diam: diameter of the manifold (u.m)

        pi_flow_mainfold: ratio of flow from the first port of the manifold
        to the last port. See
        https://aguaclara.github.io/Textbook/Hydraulics/Hydraulics_Intro.html#equation-pi-q-ports

        vel_diffuser: velocity through the diffuser (u.m / u.s)

        q_input: design flow rate (u.L / u.s)

        report_writer: ReportWriter object to record validation results

    Returns:
        none
    """
    try:
        q_calc = (
            np.pi
            * (
                vel_diffuser
                * np.sqrt(2 * (1 - pi_flow_manifold ** 2) / (pi_flow_manifold ** 2 + 1))
            )
            * diam ** 2
        ) / 4
        q_calc = q_calc.to(u.L / u.s)

        assert q_calc > q_input

        report_writer.write_message(
            "The inlet manifold design flow rate, {!s}, is less than "
            "the one calculated by this validation "
            "code, {!s}.\n".format(q_input, q_calc)
        )
    except AssertionError:
        report_writer.write_message(
            "INVALID: The inlet manifold design flow rate, {!s}, is "
            "greater than the one calculated by this "
            "validation code, {!s}.\n".format(q_input, q_calc)
        )
        report_writer.set_result("Invalid: Check Validation Report")


def check_plate_settlers(
    vel_capture,
    n_plate,
    l_plate,
    w_plate,
    space_plate,
    angle_plate,
    plate_thickness,
    q_input,
    report_writer,
):
    """Check that the plate settler's design flow rate is less than the one
    calculated according to the model's geometry. For more info see
    https://aguaclara.github.io/Textbook/Sedimentation/Sed_Design.html#plate-settlers

    Args:
        vel_capture: design capture velocity (u.m / u.s)

        n_plate: number of plates

        l_plate: length of one plate (u.m)

        w_plate: width of one plate (u.m)

        space_plate: edge-to-edge spacing between plates (u.m)

        angle_plate: the angle of each plate from horizontal (u.deg)

        plate_thickness: thickness of one plate (u.m)

        q_input: design flow rate (u.L / u.s)

        report_writer: ReportWriter object to record validation results

    Returns:
        none
    """
    try:
        q_calc = vel_capture * (
            n_plate
            * w_plate
            * (l_plate * np.cos(angle_plate) + (space_plate / np.sin(angle_plate)))
        )
        q_calc = q_calc.to(u.L / u.s)

        assert q_calc > q_input

        report_writer.write_message(
            "The plate settlers' design flow rate, {!s}, is less than "
            "the one calculated by this validation "
            "code, {!s}.\n".format(q_input, q_calc)
        )
    except AssertionError:
        report_writer.write_message(
            "INVALID: The plate settlers' design flow rate, {!s}, is "
            "greater than the one calculated by this "
            "validation code, {!s}.\n".format(q_input, q_calc)
        )
        report_writer.set_result("Invalid: Check Validation Report")


def check_sed_tank(length, width, vel_up, q_input, report_writer):
    """Check that the sed tank's design flow rate is less than the one
    calculated according to the model's geometry.

    Args:
        length: length of the tank (u.m)

        width: width of the tank (u.m)

        vel_up: design upflow velocity through the sed tank (u.m / u.s)

        q_input: design flow rate (u.L / u.s)

        report_writer: ReportWriter object to record validation results

    Returns:
        none
    """
    try:
        q_calc = length * width * vel_up
        q_calc = q_calc.to(u.L / u.s)

        assert q_calc > q_input

        report_writer.write_message(
            "The sed tank's design flow rate, {!s}, is less than "
            "the one calculated by this validation "
            "code, {!s}.\n".format(q_input, q_calc)
        )
    except AssertionError:
        report_writer.write_message(
            "INVALID: The sed tank's design flow rate, {!s}, is "
            "greater than the one calculated by this "
            "validation code, {!s}.\n".format(q_input, q_calc)
        )
        report_writer.set_result("Invalid: Check Validation Report")


def check_diffuser(
    w_sed,
    w_diffuser,
    vel_up,
    max_hl,
    temp,
    report_writer,
    shear_floc_max=0.5 * u.Pa,
    pi_plane_jet=0.0124,
):
    """Check that the diffuser's are designed appropriately by first checking
    the velocity calculated from their geometry is less than the maximum allowed
    due to shear. Then check that the head loss is less than the maximum allowable.

    For more info on shear stress calculation and default values see
    https://aguaclara.github.io/Textbook/Sedimentation/Sed_Design.html#jet-reverser-shear-stress

    Args:
        w_sed: width of the sed tank (u.m)

        w_diffuser: width of a diffuser (u.m)

        vel_up: design upflow velocity through the sed tank (u.m / u.s)

        max_hl: maximum allowable head loss over a diffuser (u.m)

        q_input: design flow rate (u.L / u.s)

        report_writer: ReportWriter object to record validation results

        shear_floc_max: maximum shear allowed without disrupting flocculation.
        Defaults to 0.5 Pascals

        pi_plane_jet: the amount of energy lost in the time that it takes for
        the jet to travel it's width normalized by the total kinetic energy.
        Defaults to 0.0124

    Returns:
        none
    """
    rho = pc.density_water(temp)
    nu = pc.viscosity_kinematic_water(temp)
    vel_diffuser = vel_up * w_sed / w_diffuser

    try:
        vel_max_shear = (
            (shear_floc_max / rho) ** (1 / 2)
            * (vel_up * w_sed / (nu * pi_plane_jet)) ** (1 / 4)
        ).to(u.mm / u.s)
        assert vel_diffuser < vel_max_shear

        report_writer.write_message(
            "The max diffuser velocity based on floc shear, {!s}, "
            "is greater than the one calculated by this validation "
            "code, {!s}.\n".format(vel_max_shear, vel_diffuser)
        )
    except AssertionError:
        report_writer.write_message(
            "INVALID: The max diffuser velocity based on floc shear, {!s}, "
            "is less than the one calculated by this validation "
            "code, {!s}.\n".format(vel_max_shear, vel_diffuser)
        )
        report_writer.set_result("Invalid: Check Validation Report")

    try:
        head_loss = (vel_diffuser ** 2 / (2 * u.g_0)).to(u.cm)
        assert head_loss < max_hl

        report_writer.write_message(
            "The max head loss, {!s}, is greater than "
            "the one calculated by this validation "
            "code, {!s}.\n".format(max_hl, head_loss)
        )
    except AssertionError:
        report_writer.write_message(
            "INVALID: The max head loss, {!s}, "
            "is less than the one calculated by this validation "
            "code, {!s}.\n".format(max_hl, head_loss)
        )
        report_writer.set_result("Invalid: Check Validation Report")

    return vel_diffuser


def check_outlet_manifold(n_orifices, diam_orifice, hl_design, q_input, report_writer):
    """Check that the sed tank's design flow rate is less than the one
    calculated according to the model's geometry.

    Args:
        n_orifices: number of orifices in the manifold (u.m)

        diam_orifice: diameter of a single orifice (u.m)

        hl_design: design head loss through the outlet manifold (u.m)

        q_input: design flow rate (u.L / u.s)

        report_writer: ReportWriter object to record validation results

    Returns:
        none
    """
    try:
        q_calc = (
            pc.flow_orifice(diam_orifice, hl_design, con.VC_ORIFICE_RATIO) * n_orifices
        ).to(u.L / u.s)
        assert q_calc > q_input

        report_writer.write_message(
            "The outlet manifold design flow rate, {!s}, is less than "
            "the one calculated by this validation "
            "code, {!s}.\n".format(q_input, q_calc)
        )
    except AssertionError:
        report_writer.write_message(
            "INVALID: The outlet manifold design flow rate, {!s}, is "
            "greater than the one calculated by this "
            "validation code, {!s}.\n".format(q_input, q_calc)
        )
        report_writer.set_result("Invalid: Check Validation Report")
