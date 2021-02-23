import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors


def select_apers(fovs, colormap=None, color=None, NIRCam_long_wl=True,
                 NIRCam_short_wl=True, NIRCam_coron=True, NIRSpec_MSA=True,
                 NIRSpec_IFU=True, NIRSpec_fixed_slits=True, MIRI_imag=True,
                 MIRI_IFU=True, MIRI_4QPM=True, MIRI_Lyot=True, MIRI_slit=True,
                 NIRISS_WFSS=True, NIRISS_AMI=True):
    """
    Selects the apertures to be plotted and assigns their colors.

    Arguments:
    fovs -- pandas DataFrame containing the geometry of all the FOVs.
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


    Returns:
    fovs -- pandas DataFrame containing the FOVs geometry with an extra column
            indicating the color to be used to plot each aperture, and
            excluding rows corresponding to apertures not to be plotted.
    """

    # Create a new column of zeros to store the color to be used when plotting
    # each individual aperture.
    fovs['plot_color'] = np.zeros(len(fovs))

    # If a color is specified, all the apertures will be plotted in that color.
    if type(color) == np.str:
        color = mcolors.to_hex(color)
    col = color

    ##########################################################################
    # NIRCam.
    if colormap is None:
        colmap = plt.get_cmap('Greens')
    else:
        colmap = plt.get_cmap(colormap)

    if NIRCam_long_wl:
        if color is None:
            col = mcolors.to_hex(colmap(0.75))

        for ap in ['NRCA1_FULL', 'NRCA2_FULL', 'NRCA3_FULL', 'NRCA4_FULL',
                   'NRCB1_FULL', 'NRCB2_FULL', 'NRCB3_FULL', 'NRCB4_FULL']:
            fovs.loc[fovs.Aperture == ap, 'plot_color'] = col

    if NIRCam_short_wl:
        if color is None:
            col = mcolors.to_hex(colmap(0.95))

        for ap in ['NRCA5_FULL', 'NRCB5_FULL']:
            fovs.loc[fovs.Aperture == ap, 'plot_color'] = col

    if NIRCam_coron:
        if color is None:
            col = mcolors.to_hex(colmap(0.5))

        for ap in ['NRCA2_MASK210R', 'NRCA5_MASK335R', 'NRCA5_MASK430R',
                   'NRCA4_MASKSWB', 'NRCA5_MASKLWB']:
            fovs.loc[fovs.Aperture == ap, 'plot_color'] = col

    ##########################################################################
    # NIRSpec.
    if colormap is None:
        colmap = plt.get_cmap('Blues')

    if NIRSpec_MSA:
        if color is None:
            col = mcolors.to_hex(colmap(0.95))

        for ap in ['NRS_FULL_MSA1', 'NRS_FULL_MSA2', 'NRS_FULL_MSA3',
                   'NRS_FULL_MSA4']:
            fovs.loc[fovs.Aperture == ap, 'plot_color'] = col

    if NIRSpec_IFU:
        if color is None:
            col = mcolors.to_hex(colmap(0.75))

        fovs.loc[fovs.Aperture == 'NRS_FULL_IFU_IFU',
                 'plot_color'] = col

    if NIRSpec_fixed_slits:
        if color is None:
            col = mcolors.to_hex(colmap(0.5))

        for ap in ['NRS_S200A1_SLIT', 'NRS_S400A1_SLIT', 'NRS_S200A2_SLIT',
                   'NRS_S1600A1_SLIT', 'NRS_S200B1_SLIT']:
            fovs.loc[fovs.Aperture == ap, 'plot_color'] = col

    ##########################################################################
    # MIRI.
    if colormap is None:
        colmap = plt.get_cmap('Reds')

    if MIRI_4QPM:
        if color is None:
            col = mcolors.to_hex(colmap(0.55))

        for ap in ['MIRIM_MASK1065', 'MIRIM_MASK1140', 'MIRIM_MASK1550']:
            fovs.loc[fovs.Aperture == ap, 'plot_color'] = col

    if MIRI_Lyot:
        if color is None:
            col = mcolors.to_hex(colmap(0.65))

        fovs.loc[fovs.Aperture == 'MIRIM_MASKLYOT', 'plot_color'] = col

    if MIRI_slit:
        if color is None:
            col = mcolors.to_hex(colmap(0.95))

        fovs.loc[fovs.Aperture == 'MIRIM_SLIT', 'plot_color'] = col

    if MIRI_imag:
        if color is None:
            col = mcolors.to_hex(colmap(0.70))

        fovs.loc[fovs.Aperture == 'MIRIM_ILLUM', 'plot_color'] = col

    if MIRI_IFU:
        if color is None:
            col = mcolors.to_hex(colmap(0.85))

        fovs.loc[fovs.Aperture == 'MIRIFU_FULL_SHCH1CNTR_CH4',
                 'plot_color'] = col

    ##########################################################################
    # NIRISS.
    if colormap is None:
        colmap = plt.get_cmap('Purples')

    if NIRISS_WFSS:
        if color is None:
            col = mcolors.to_hex(colmap(0.95))

        fovs.loc[fovs.Aperture == 'NIS_CEN', 'plot_color'] = col

    if NIRISS_AMI:
        if color is None:
            col = mcolors.to_hex(colmap(0.65))

        fovs.loc[fovs.Aperture == 'NIS_AMI1', 'plot_color'] = col

    # Removing apertures not to be plotted.
    fovs = fovs.loc[fovs.plot_color != 0]
    fovs.reset_index(drop=True, inplace=True)

    return fovs
