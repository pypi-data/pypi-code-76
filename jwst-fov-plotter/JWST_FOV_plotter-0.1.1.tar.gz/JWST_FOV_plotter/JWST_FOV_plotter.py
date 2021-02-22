import matplotlib.pyplot as plt
from fovs_loader import fovs_loader
from FOV_transform import FOVs_to_radec
from apertures_selecter import select_apers
from auxiliar_functions import plot_single_FOV, reg_file_line


def plot_JWST_FOVs(ra, dec, fovs=None, ax=None, ref_instrument='NIRCam', rot=0,
                   instr_to_plot=['NIRCam', 'NIRSpec', 'MIRI', 'NIRISS'],
                   colormap=None, color=None, NIRCam_long_wl=True,
                   NIRCam_short_wl=True, NIRCam_coron=True, NIRSpec_MSA=True,
                   NIRSpec_IFU=True, NIRSpec_fixed_slits=True, MIRI_imag=True,
                   MIRI_IFU=True, MIRI_4QPM=True, MIRI_Lyot=True,
                   MIRI_slit=True, NIRISS_WFSS=True, NIRISS_AMI=True,
                   **kwargs):
    """
    Plots the JWST FOVs of any combination of pointings, instruments and
    apertures. It takes one of the four JWST instruments as reference for the
    central coordinates and rotation angle of the pointing.

    Arguments:
    ra -- central RA of the pointing in degrees.
    dec -- central Dec of the pointing in degrees.

    Optional arguments:
    fovs -- name of a .csv or .fits file containing the geometry of all the
            FOVs in the V2V3 reference system, including at least the following
            columns:
            [Instrument', 'Aperture', 'V2_Ref', 'V3_Ref', 'V3_IdlYAngle',
            'V2_1', 'V2_2', 'V2_3', 'V2_4', 'V3_1', 'V3_2', 'V3_3', 'V3_4]
.           If None, the SIAF table from
        https://jwst-docs.stsci.edu/jwst-observatory-hardware/jwst-field-of-view
            is used. Default: None.
    ax -- matplotlib axes to plot the FOVs. If None, it gets the current
          axis from matplotlib. Default: None.
    ref_instrument -- instrument taken as reference for the pointing.
                      Possible values: 'NIRCam', 'NIRSpec', 'MIRI', 'NIRISS'
                      Default: 'NIRCam'.
    rot -- counterclockwise rotation APA angle in degrees, as measured in the
           ideal coordinate system of the reference instrument. Default: 0.
    instr_to_plot -- list with the instruments whose FOV will be plotted.
                     Not including any of the instruments will automatically
                     turn off all its apertures.
                     Default: ['NIRCam', 'NIRSpec', 'MIRI', 'NIRISS'].
    colormap -- matplotlib colormap to plot the different apertures of each
                instrument. If None, each instrument will use a different
                default colormap: 'Blues' for NIRSpec, 'Greens' for NIRCam,
                'Reds' for MIRI and 'Purples' for NIRISS. Default: None.
    color -- matplotlib color to plot all the apertures of all the instruments.
             Overwrittes the information given in the colormap argument.
             If None, it plots the different apertures with different colors
             according to the assigned colormaps. Default: None.
    NIRCam_long_wl -- if True, it plots the FOV of the NIRCam long wavelength
                      detectors. Default: True.
    NIRCam_short_wl -- if True, it plots the FOV of the NIRCam short wavelength
                       detectors. Default: True.
    NIRCam_coron -- if True, it plots the FOV of the NIRCam coronagraph masks.
                    Default:True.
    NIRSpec_MSA -- if True, it plots the NIRSpec MSA FOV. Default: True.
    NIRSpec_IFU -- if True, it plots the NIRSpec IFU FOV. Default: True.
    NIRSpec_fixed_slits -- if True, it plots the NIRSpec fixed slits.
                           Default: True.
    MIRI_imag -- if True, it plots the MIRI imaging FOV. Default: True.
    MIRI_IFU -- if True, it plots the MIRI IFU FOV. Default: True.
    MIRI_4QPM -- if True, it plots the MIRI FOV of the 4QPM coronagraphs.
                 Default: True.
    MIRI_Lyot -- if True, it plots the MIRI FOV of the Lyot coronagraph.
                 Default: True.
    MIRI_slit -- if True, it plots the MIRI slit of the LRS. Default: True.
    NIRISS_WFSS -- if True, it plots the NIRISS WFSS FOV (same as for imaging).
                   Default: True
    NIRISS_AMI -- if True, it plots the NIRISS AMI FOV. Default: True.
    **kwargs -- any other optional matplotlib plotting argument.

    Returns:
    radec_fovs -- pandas DataFrame with the geometry of the JWST FOVs in
                  RA-Dec for the requested pointing and rotation angle.
    """

    # Reading axes.
    ax = ax or plt.gca()

    # Loading SIAF information with the geometry of the fields in the V2V3
    # coordinate system.
    fovs = fovs_loader(fovs)

    # Pointing, rotating and transforming the new FOVs geometry to ICRS.
    radec_fovs = FOVs_to_radec(ra, dec, rot, fovs, ref_instrument)

    # Selecting apertures to be plotted and setting their colors.
    apers = select_apers(radec_fovs, colormap=colormap, color=color,
                         NIRCam_long_wl=NIRCam_long_wl,
                         NIRCam_short_wl=NIRCam_short_wl,
                         NIRCam_coron=NIRCam_coron, NIRSpec_MSA=NIRSpec_MSA,
                         NIRSpec_IFU=NIRSpec_IFU,
                         NIRSpec_fixed_slits=NIRSpec_fixed_slits,
                         MIRI_imag=MIRI_imag, MIRI_IFU=MIRI_IFU,
                         MIRI_4QPM=MIRI_4QPM, MIRI_Lyot=MIRI_Lyot,
                         MIRI_slit=MIRI_slit, NIRISS_WFSS=NIRISS_WFSS,
                         NIRISS_AMI=NIRISS_AMI)

    # Removing all apertures of instruments not to be represented.
    apers = apers.loc[apers.Instrument.isin(instr_to_plot)]
    apers.reset_index(drop=True, inplace=True)

    # FOVs plotting.
    for i in range(len(apers)):
        col = apers.iloc[i].plot_color
        plot_single_FOV(apers.iloc[i], ax=ax, color=col, **kwargs)

    return apers


def create_ds9_region(out, ra, dec, fovs=None, ref_instrument='NIRCam', rot=0,
                      instr_to_plot=['NIRCam', 'NIRSpec', 'MIRI', 'NIRISS'],
                      colormap=None, color=None, NIRCam_long_wl=True,
                      NIRCam_short_wl=True, NIRCam_coron=True,
                      NIRSpec_MSA=True,
                      NIRSpec_IFU=True, NIRSpec_fixed_slits=True,
                      MIRI_imag=True, MIRI_IFU=True,
                      MIRI_4QPM=True, MIRI_Lyot=True, MIRI_slit=True,
                      NIRISS_WFSS=True, NIRISS_AMI=True, extra_params=''):
    """
    Creates a DS9 region file with the contours of JWST FOVs for any
    combination of pointings, instruments and apertures. It takes one of the
    four JWST instruments as reference for the central coordinates and rotation
    angle of the pointing.

    Arguments:
    out -- name of the output DS9 region file to be created.
    ra -- central RA of the pointing in degrees.
    dec -- central Dec of the pointing in degrees.

    Optional arguments:
    fovs -- name of a .csv or .fits file containing the geometry of all the
            FOVs in the V2V3 reference system, including at least the following
            columns:
            [Instrument', 'Aperture', 'V2_Ref', 'V3_Ref', 'V3_IdlYAngle',
            'V2_1', 'V2_2', 'V2_3', 'V2_4', 'V3_1', 'V3_2', 'V3_3', 'V3_4]
.           If None, the SIAF table from
        https://jwst-docs.stsci.edu/jwst-observatory-hardware/jwst-field-of-view
            is used. Default: None.
    ref_instrument -- instrument taken as reference for the pointing.
                      Possible values: 'NIRCam', 'NIRSpec', 'MIRI', 'NIRISS'
                      Default: 'NIRCam'.
    rot -- counterclockwise rotation APA angle in degrees, as measured in the
           ideal coordinate system of the reference instrument. Default: 0.
    instr_to_plot -- list with the instruments whose FOV will be plotted.
                     Not including any of the instruments will automatically
                     turn off all its apertures.
                     Default: ['NIRCam', 'NIRSpec', 'MIRI', 'NIRISS'].
    colormap -- matplotlib colormap to plot the different apertures of each
                instrument. If None, each instrument will use a different
                default colormap: 'Blues' for NIRSpec, 'Greens' for NIRCam,
                'Reds' for MIRI and 'Purples' for NIRISS. Default: None.
    color -- matplotlib color to plot all the apertures of all the instruments.
             Overwrittes the information given in the colormap argument.
             If None, it plots the different apertures with different colors
             according to the assigned colormaps. Default: None.
    NIRCam_long_wl -- if True, it plots the FOV of the NIRCam long wavelength
                      detectors. Default: True.
    NIRCam_short_wl -- if True, it plots the FOV of the NIRCam short wavelength
                       detectors. Default: True.
    NIRCam_coron -- if True, it plots the FOV of the NIRCam coronagraph masks.
                    Default:True.
    NIRSpec_MSA -- if True, it plots the NIRSpec MSA FOV. Default: True.
    NIRSpec_IFU -- if True, it plots the NIRSpec IFU FOV. Default: True.
    NIRSpec_fixed_slits -- if True, it plots the NIRSpec fixed slits.
                           Default: True.
    MIRI_imag -- if True, it plots the MIRI imaging FOV. Default: True.
    MIRI_IFU -- if True, it plots the MIRI IFU FOV. Default: True.
    MIRI_4QPM -- if True, it plots the MIRI FOV of the 4QPM coronagraphs.
                 Default: True.
    MIRI_Lyot -- if True, it plots the MIRI FOV of the Lyot coronagraph.
                 Default: True.
    MIRI_slit -- if True, it plots the MIRI slit of the LRS. Default: True.
    NIRISS_WFSS -- if True, it plots the NIRISS WFSS FOV (same as for imaging).
                   Default: True
    NIRISS_AMI -- if True, it plots the NIRISS AMI FOV. Default: True.
    extra_params -- str including any additional text to be included at the end
                    of each line in the region file, for extra DS9 region
                    parameters. Default: ''.

    """

    # Loading SIAF information with the geometry of the fields in the V2V3
    # coordinate system.
    fovs = fovs_loader(fovs)

    # Pointing, rotating and transforming new FOVs geometry to RA-Dec.
    radec_fovs = FOVs_to_radec(ra, dec, rot, fovs, ref_instrument)

    # Selecting apertures to be plotted.
    apers = select_apers(radec_fovs, colormap=colormap, color=color,
                         NIRCam_long_wl=NIRCam_long_wl,
                         NIRCam_short_wl=NIRCam_short_wl,
                         NIRCam_coron=NIRCam_coron, NIRSpec_MSA=NIRSpec_MSA,
                         NIRSpec_IFU=NIRSpec_IFU,
                         NIRSpec_fixed_slits=NIRSpec_fixed_slits,
                         MIRI_imag=MIRI_imag, MIRI_IFU=MIRI_IFU,
                         MIRI_4QPM=MIRI_4QPM, MIRI_Lyot=MIRI_Lyot,
                         MIRI_slit=MIRI_slit, NIRISS_WFSS=NIRISS_WFSS,
                         NIRISS_AMI=NIRISS_AMI)

    # Removing all apertures of instruments not to be represented.
    apers = apers.loc[apers.Instrument.isin(instr_to_plot)]
    apers.reset_index(drop=True, inplace=True)

    new_file = open(out, 'w')
    new_file.write('# DS9 region file.\nicrs\n')
    for i in range(len(apers)):
        new_file.write(reg_file_line(apers.iloc[i], extra_params=extra_params))
    new_file.close()

    return apers
