import numpy as np


def rotation_2d(matrix_2d, theta, rot_point=[0, 0]):
    """
    Performs a clockwise 2d rotation of a 2xN matrix. This translates into a
    counterclockwise rotation on the projected sky in RA-Dec or V2V3.

    Arguments:
    matrix_2d -- 2xN matrix to be rotated.
    theta -- rotation angle in degrees.

    Optional arguments:
    rot_point -- [x, y] point about which the rotation is going to be
                 performed. Default: [0, 0] (coordinates origin).

    Returns:
    roted_2d -- rotated 2xN matrix.
    """

    theta = np.radians(theta)

    # Rotation matrix.
    R = np.array(((np.cos(theta), np.sin(theta), 0),
                  (-np.sin(theta),  np.cos(theta), 0),
                  (0, 0, 1)))
    T = np.array(((1, 0, rot_point[0]),
                  (0, 1, rot_point[1]),
                  (0, 0, 1)))
    T_ = np.array(((1, 0, -rot_point[0]),
                   (0, 1, -rot_point[1]),
                   (0, 0, 1)))

    P = np.array((matrix_2d[0], matrix_2d[1], np.ones(np.shape(matrix_2d)[1])))

    roted = T @ R @ T_ @ P
    roted_2d = np.array((roted[0], roted[1]))

    return roted_2d


def fix_reference_pointing(fovs, instrument):
    """
    Gives the reference V2V3 coordinates of the instrument used as reference
    for the pointing coordinates, as well as the relative angle of its ideal
    coordinate system.

    Arguments:
    fovs -- pandas DataFrame containing the geometry of all the FOVs in
            the V2V3 reference system.
    instrument -- instrument used as reference for the pointing.
                  Possible values: 'NIRCam', 'NIRSpec', 'MIRI', 'NIRISS'

    Returns:
    ref_v2, ref_v3 -- reference coordinates of the instrument in V2V3 (arcsec).
    idl_ang -- instrument ideal system angle in degrees (counterclockwise angle
               of the Y axis of the instrument ideal coordinate system relative
               to V3).
    """

    # This dictionary defines the label of the row in fovs associated with
    # the global FOV of each instrument, whose V2V3 reference coordinates
    # correspond with the instrument pointing coordinates.
    ref_ape_key = {'NIRCam': 'NRCALL_FULL*', 'NIRSpec': 'NRS_FULL_MSA*',
                   'MIRI': 'MIRIM_FULL*', 'NIRISS': 'NIS_CEN'}

    # WARNING: The MIRI V3_IdlYAngle does not seem right in the original SIAF
    # file. It was replaced by 4.83 deg (according to the MIRI APA-V3PA
    # transformation implemented in the APT).

    # Getting reference values.
    ref_row = fovs.loc[fovs.Aperture == ref_ape_key[instrument]]
    ref_v2 = ref_row.V2_Ref.values[0]
    ref_v3 = ref_row.V3_Ref.values[0]
    idl_ang = ref_row.V3_IdlYAngle.values[0]

    return ref_v2, ref_v3, idl_ang


def FOVs_to_radec(ra, dec, rot, fovs, ref_instrument):
    """
    Transforms the FOVs V2V3 coordinates to the corresponding ICRS coordinates
    for the specified pointing. It performs the pointing, rotation and
    coordinate transformation.

    Arguments:
    ra -- central RA of the pointing in degrees.
    dec -- central Dec of the pointing in degrees.
    rot -- counterclockwise rotation APA angle in degrees, as measured in the
           ideal coordinate system of the reference instrument.
    fovs -- pandas DataFrame containing the geometry of all the FOVs in the
            V2V3 reference system.
    ref_instrument -- instrument taken as reference for the pointing.
                      Possible values: 'NIRCam', 'NIRSpec', 'MIRI', 'NIRISS'

    Returns:
    radec_fovs -- pandas DataFrame with the geometry of the JWST FOVs in
                  RA-Dec for the requested pointing and rotation angle.

    """

    # Getting reference V2V3 coordinates of the specified reference instrument
    # used for the pointing. These reference coordinates correspond to the
    # center of each instrument global FOV (except for MIRI, for which they
    # correspond to the center of the imaging aperture).
    v2_ref, v3_ref, idl_ang = fix_reference_pointing(fovs, ref_instrument)

    # Angular difference between the ideal coordinate system of the instrument
    # used as reference and V2V3.
    rot -= idl_ang

    # Rotation in V2V3 coordinates.
    for vertex in ['Ref', '1', '2', '3', '4']:
        vertices = np.array((fovs['V2_%s' % vertex], fovs['V3_%s' % vertex]))
        rot_vert = rotation_2d(vertices, rot, rot_point=[v2_ref, v3_ref])
        fovs['V2_%s' % vertex] = rot_vert[0]
        fovs['V3_%s' % vertex] = rot_vert[1]

    # Linking RA-Dec to V2V3 and redefining FOVs in terms of sky coordinates.
    # V2V3 coordinates are given in arcsec. Hence the conversion factor.
    radec_fovs = fovs.copy()

    # RA columns.
    for col in ['V2_Ref', 'V2_1', 'V2_2', 'V2_3', 'V2_4']:
        radec_fovs[col] = ((fovs[col].values - v2_ref)
                           / np.cos(np.radians(dec)) / 3600 + ra)

    # Dec columns.
    for col in ['V3_Ref', 'V3_1', 'V3_2', 'V3_3', 'V3_4']:
        radec_fovs[col] = (fovs[col].values - v3_ref) / 3600 + dec

    # Updating column names of the output FOVs geometry in RA-Dec.
    new_colnames = ['Instrument', 'Aperture', 'RA_Ref', 'DEC_Ref',
                    'V3_IdlYAngle', 'RA_1', 'RA_2', 'RA_3', 'RA_4', 'DEC_1',
                    'DEC_2', 'DEC_3', 'DEC_4']
    radec_fovs.columns = new_colnames

    return radec_fovs
