from aguaclara.core.units import u
import aguaclara.core.physchem as pc
import aguaclara.core.onshape_parser as par
from aguaclara.design.floc import Flocculator
from aide_validation.report_writer import ReportWriter
from aide_validation.floc_validation import check_baffle_spacing, check_G_theta
from aide_validation.lfom_validation import check_flow_lfom_vert
from aide_validation.sed_validation import (
    check_inlet_manifold,
    check_outlet_manifold,
    check_diffuser,
    check_sed_tank,
    check_plate_settlers,
)


class Validator(object):
    """Class to orchestrate validation of an AguaClara plant"""

    def __init__(self):
        self.report_writer = ReportWriter()

    def close_report(self):
        """Closes the report file associated with this Validator

        Args:
            none

        Returns:
            none
        """
        self.report_writer.close()

    def save_pdf(self):
        """Closes the report file associated with this Validator
        then converts it to a PDF.

        Args:
            none

        Returns:
            none
        """
        self.close_report()
        self.report_writer.to_pdf()

    def validate(self, url):
        """Validates the if the AguaClara component or plant model
        at the given URL is correct

        Args:
            url: URL of Onshape model to validate (string)

        Returns:
            result: text which represents validation result (string)
        """
        measurements, _, processes = par.get_parsed_measurements(
            link=url, for_docs=False
        )
        result = "Invalid: No Unit Process Selected by Onshape Documenter"

        if "ET" in processes:
            result = self.validate_lfom(measurements)

        if "Floc" in processes:
            result = self.validate_floc(measurements)

        if "Sed" in processes:
            result = self.validate_sed(measurements)

        self.save_pdf()

        return result

    def validate_lfom(self, measurements):
        """Validates the LFOM model at the given URL is correct

        Args:
            measurements: dictionary of parsed variables

        Returns:
            result: text which represents validation result (string)
        """
        try:
            # Onshape predicates can't handle flow and temp units
            q = measurements["Flow"] / u.s
            d_orifices = measurements["D.LfomOrifices"]
            n_orifices = measurements["N.LfomOrifices"]
            h_orifices = measurements["H.LfomOrifices"]
            # Due to some odd behavior of Pint lists, we need to do this conversion
            h_orifices = [
                measure.to_base_units().magnitude for measure in h_orifices
            ] * u.m

            # Acceptable tolerance
            tol = 0.05
            # TODO: make ReportWriter and measurments attributes of validation
            # orchestrator instead of passing them between functions
            check_flow_lfom_vert(
                d_orifices, h_orifices, n_orifices, tol, q, self.report_writer
            )
        except Exception as e:
            self.report_writer.set_result("Error: {}".format(e))

        return self.report_writer.get_result()

    def validate_floc(self, measurements):
        """Validates the flocculator model at the given URL is correct

        Args:
            measurements: dictionary of parsed variables

        Returns:
            result: text which represents validation result (string)
        """
        try:
            # Onshape predicates can't handle flow and temp units
            q = measurements["Flow"] / u.s
            temp = measurements["TempCelsius"] * u.degC
            channel_n = measurements["N.FlocChannels"]
            baffle_n_per_chan = measurements["N.FlocChannelBaffles"]
            baffle_s = measurements["S.FlocBaffle"]
            channel_w = measurements["W.FlocChannel"]
            channel_l = measurements["L.FlocChannel"]
            channel_h = measurements["H.FlocChannel"]
            design_water_height = channel_h - measurements["FB"]

            # estimate head loss with minor loss equation and coefficient for baffles
            spaces_n = (baffle_n_per_chan + 1) * channel_n
            k_minor = Flocculator().BAFFLE_K * spaces_n
            vel = q / (baffle_s * channel_w)
            hl = pc.headloss_minor_channel(vel, k_minor)

            check_G_theta(
                q,
                channel_l,
                design_water_height,
                channel_n,
                channel_w,
                hl,
                temp,
                self.report_writer,
            )
            check_baffle_spacing(channel_l, baffle_s, self.report_writer)
        except Exception as e:
            self.report_writer.set_result("Error: {}".format(e))

        return self.report_writer.get_result()

    def validate_sed(self, measurements):
        """Validates the sedimentor model at the given URL is correct

        Args:
            measurements: dictionary of parsed variables

        Returns:
            result: text which represents validation result (string)
        """
        try:
            # Onshape predicates can't handle flow, velocity, and temp units
            q = measurements["Flow"] / u.s
            vel_up = measurements["V.SedUp"] / u.s
            vel_capture = measurements["V.SedC"] / u.s
            temp = measurements["TempCelsius"] * u.degC

            # TODO: Create these new variables with Documenter feature
            # Only nominal diameter is included in design specs.
            diam_inlet_manifold = measurements["ID.SedManifold"]
            # Diffuser head loss was also not included in design specs
            max_hl_diffuser = measurements["HL.Diffuser"]

            pi_flow_mainfold = measurements["Pi.QLaunderOrifices"]
            w_tank = measurements["W.Sed"]
            l_tank = measurements["L.Sed"]
            n_plate = measurements["N.SedPlates"]
            l_plate = measurements["L.SedPlate"]
            w_plate = measurements["W.SedPlate"]
            plate_thickness = measurements["T.SedPlate"]
            angle_plate = measurements["AN.SedPlate"]
            space_plate = measurements["S.SedPlate"]
            w_diffuser = measurements["W.SedDiffuserInner"]
            hl_outlet_manifold = measurements["HL.SedLaunderBod"]
            diam_orifice = measurements["D.SedLaunderOrifice"]
            n_orifices = measurements["N.SedLaunderOrifices"]

            vel_diffuser = check_diffuser(
                w_tank, w_diffuser, vel_up, max_hl_diffuser, temp, self.report_writer
            )
            check_inlet_manifold(
                diam_inlet_manifold,
                pi_flow_mainfold,
                vel_diffuser,
                q,
                self.report_writer,
            )
            check_plate_settlers(
                vel_capture,
                n_plate,
                l_plate,
                w_plate,
                space_plate,
                angle_plate,
                plate_thickness,
                q,
                self.report_writer,
            )
            check_sed_tank(l_tank, w_tank, vel_up, q, self.report_writer)
            check_outlet_manifold(
                n_orifices, diam_orifice, hl_outlet_manifold, q, self.report_writer
            )
        except Exception as e:
            self.report_writer.set_result("Error: {}".format(e))

        return self.report_writer.get_result()
